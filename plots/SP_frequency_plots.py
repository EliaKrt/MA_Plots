import os
import glob

import numpy as np
from nptdms import TdmsFile
from Plot_Template import *

def calculate_rms(data):

    data = data - np.mean(data)
    return np.sqrt(np.mean(data**2))


def get_frequency_response(
        tdms_file,
        normalize=True):

    tdms = TdmsFile.read(tdms_file)

    group = tdms.groups()[0]

    freqs = []
    amps = []

    for f in range(1, 121):

        p_ch = None
        pos_ch = None

        for ch in group.channels():

            n = ch.name.lower().replace(" ", "")

            if f"[pressure@{f}hz]" in n:
                p_ch = ch

            if f"[position@{f}hz]" in n:
                pos_ch = ch

        if p_ch and pos_ch:

            rms_p = calculate_rms(p_ch.data)
            rms_pos = calculate_rms(pos_ch.data)

            if rms_pos > 1e-4:

                freqs.append(f)
                amps.append(rms_p / rms_pos)

    freqs = np.asarray(freqs)
    amps = np.asarray(amps)

    if normalize:

        amps = amps / amps[0]

    return freqs, amps

def plot_group_frequency_response(
        ax,
        groups,
        show_legend=True,
        normalize=True,
        show_std=True,
        show_3db=True,
        freq_range=None):

    common_freq = np.arange(1,101)

    for label, folders in groups.items():

        curves = []
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

                    f,a = get_frequency_response(
                        file,
                        normalize
                    )

                    interp = np.interp(
                        common_freq,
                        f,
                        a
                    )

                    curves.append(interp)
                    n_used +=1

                except:
                    pass

        if len(curves) == 0:
            continue
        print("SP_Tester-Frequency: "
        f"{label}: "
        f"{n_used}/{n_found} files used")

        curves = np.asarray(curves)

        mean_curve = np.mean(
            curves,
            axis=0
        )

        std_curve = np.std(
            curves,
            axis=0
        )

        line = ax.plot(
            common_freq,
            mean_curve,
            label=label
        )[0]

        color = line.get_color()

        if show_std:

            ax.plot(
                common_freq,
                mean_curve + std_curve,
                "--",
                color=color,
                alpha=0.7
            )

            ax.plot(
                common_freq,
                mean_curve - std_curve,
                "--",
                color=color,
                alpha=0.7
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

    if freq_range:

        ax.set_xlim(*freq_range)
        
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

    ax.grid(True)

    if show_legend:
        ax.legend()