import os
import glob

import numpy as np
import matplotlib.pyplot as plt

from nptdms import TdmsFile

from Plot_Template import *


def calculate_rms(data):

    data = data - np.mean(data)

    return np.sqrt(
        np.mean(data ** 2)
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


def get_measurement_name(
        filepath):

    folder = os.path.basename(
        os.path.dirname(filepath)
    )

    idx = folder.find(
        "AMC"
    )

    if idx >= 0:

        return folder[idx:]

    return folder


def plot_psst_frequency_response_measurements(
        ax,
        folders,
        normalize=True,
        show_3db=True,
        show_legend=True,
        freq_range=None):

    colors = plt.cm.tab20.colors

    color_idx = 0

    n_found = 0
    n_used = 0

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

            n_found += 1

            try:

                freqs, amps = (
                    get_psst_frequency_response(
                        file,
                        normalize
                    )
                )

                label = (
                    get_measurement_name(
                        file
                    )
                )

                ax.plot(
                    freqs,
                    amps,
                    color=colors[
                        color_idx
                        % len(colors)
                    ],
                    linewidth=1.5,
                    label=label
                )

                color_idx += 1
                n_used += 1

            except Exception:

                continue

    print(
        f"Frequency Responses: "
        f"{n_used}/{n_found} files used"
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
            fontsize=8,
            va="bottom"
        )

        ax.text(
            0.01,
            plus3,
            "+3 dB",
            transform=ax.get_yaxis_transform(),
            fontsize=8,
            va="bottom"
        )

    if freq_range is not None:

        ax.set_xlim(
            *freq_range
        )

        autoscale_y(
            ax,
            *freq_range
        )

    else:

        ax.set_xlim(
            0,
            100
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

        ax.legend(
            fontsize=7,
            ncol=2
        )