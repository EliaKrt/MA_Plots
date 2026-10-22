import os
import glob


import numpy as np
import matplotlib.pyplot as plt
from nptdms import TdmsFile
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.colors as mcolors
from Plot_Template import *

def calculate_rms(data):

    detrended_data = (
        data - np.mean(data)
    )

    return np.sqrt(
        np.mean(
            detrended_data ** 2
        )
    )

def get_psst_frequency_response(
        tdms_file,
        normalize=True):

    tdms = TdmsFile.read(tdms_file)

    group = tdms.groups()[0]

    frequencies = []
    amplitudes = []

    channels = group.channels()

    for f in range(1, 101):

        pressure_channel = None
        position_channel = None

        for channel in channels:

            name = channel.name.lower()

            if (
                    "sensorpad" in name
                    and "pressure" in name
                    and f" {f} hz" in name
            ):
                pressure_channel = channel

            if (
                    "position" in name
                    and "feedback" in name
                    and f" {f} hz" in name
            ):
                position_channel = channel

        if (
                pressure_channel is None
                or position_channel is None
        ):
            continue

        rms_pressure = calculate_rms(
            pressure_channel.data
        )

        rms_position = calculate_rms(
            position_channel.data
        )

        if rms_position > 1e-4:

            frequencies.append(
                float(f)
            )

            amplitudes.append(
                rms_pressure
                /
                rms_position
            )

    frequencies = np.asarray(
        frequencies
    )

    amplitudes = np.asarray(
        amplitudes
    )

    if normalize:

        idx_1hz = np.argmin(
            np.abs(
                frequencies - 1
            )
        )

        reference = amplitudes[
            idx_1hz
        ]

        if reference > 0:

            amplitudes = (
                amplitudes
                /
                reference
            )

    return (
        frequencies,
        amplitudes
    )

def is_valid_file(
        filepath,
        exclude_dirs=None,
        valid_sizes=None):

    path_low = filepath.lower()

    if exclude_dirs:

        for excluded in exclude_dirs:

            if excluded.lower() in path_low:
                return False

    if valid_sizes:

        found_size = False

        for size in valid_sizes:

            if size.lower() in path_low:

                found_size = True
                break

        if not found_size:
            return False

    return True

def plot_psst_frequency_response(
        ax,
        groups,
        show_legend=True,
        normalize=True,
        show_std=True,
        show_3db=True,
        freq_range=None,
        exclude_dirs=None,
        valid_sizes=None):

    common_freq = np.arange(
        1,
        101
    )

    colors = plt.rcParams[
        "axes.prop_cycle"
    ].by_key()["color"]

    for idx, (
            group_name,
            folders
    ) in enumerate(
        groups.items()
    ):

        color = colors[
            idx % len(colors)
        ]

        curves = []

        for folder in folders:

            files = glob.glob(
                os.path.join(
                    folder,
                    "**",
                    "FrequencyResponse.tdms"
                ),
                recursive=True
            )

            for file in files:

                if not is_valid_file(
                        file,
                        exclude_dirs,
                        valid_sizes):
                    continue

                try:

                    f, a = (
                        get_psst_frequency_response(
                            file,
                            normalize
                        )
                    )

                    interpolated = np.interp(
                        common_freq,
                        f,
                        a
                    )

                    curves.append(
                        interpolated
                    )

                except Exception:
                     continue

        if len(curves) == 0:
            continue

        curves = np.asarray(
            curves
        )

        mean_curve = np.nanmean(
            curves,
            axis=0
        )

        std_curve = np.nanstd(
            curves,
            axis=0
        )

        ax.plot(
            common_freq,
            mean_curve,
            color=color,
            label=group_name
        )

        if show_std:

            ax.plot(
                common_freq,
                mean_curve
                + std_curve,
                "--",
                color=color,
                alpha=0.6
            )

            ax.plot(
                common_freq,
                mean_curve
                - std_curve,
                "--",
                color=color,
                alpha=0.6
            )

    if show_3db and normalize:

        minus3 = 0.707
        plus3 = 1.414

        ax.axhline(
            minus3,
            color="black",
            linestyle=":"
        )

        ax.axhline(
            plus3,
            color="black",
            linestyle=":"
        )

        ax.text(
            0.01,
            minus3,
            "-3 dB",
            transform=ax.get_yaxis_transform(),
            color="black",
            fontsize=8,
            va="bottom"
        )

        ax.text(
            0.01,
            plus3,
            "+3 dB",
            transform=ax.get_yaxis_transform(),
            color="black",
            fontsize=8,
            va="bottom"
        )

    if freq_range is None:

        ax.set_xlim(
            0,
            100
        )

    else:

        ax.set_xlim(*freq_range)

        autoscale_y(
            ax,
            *freq_range
        )

    ax.set_xlabel(
        "Frequency [Hz]"
    )

    if normalize:

        ax.set_ylabel(
            "Normalized Amplitude"
        )

    else:

        ax.set_ylabel(
            "Amplitude"
        )

    ax.grid(
        True,
        alpha=0.3
    )

    if show_legend:
        ax.legend()