import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from nptdms import TdmsFile
from scipy.stats import ttest_ind
from Plot_Template import *

TRIANGULAR_FILES = [
    "TriangularResponse.tdms",
    "TriangularResponse2.tdms",
    "TriangularResponse3.tdms",
    "TriangularResponse4.tdms",
    "TriangularResponse5.tdms",
]

def normalize_signal(values):

    values = np.asarray(values)

    minimum = np.nanmin(values)
    maximum = np.nanmax(values)

    if maximum == minimum:
        return np.zeros_like(values)

    return (values - minimum) / (maximum - minimum)

def find_channel(group, candidates):

    for candidate in candidates:

        for channel in group.channels():

            if channel.name.lower() == candidate.lower():
                return channel

    for candidate in candidates:

        for channel in group.channels():

            if candidate.lower() in channel.name.lower():
                return channel

    return None

def get_channel_time(channel):

    try:
        return np.asarray(
            channel.time_track(),
            dtype=float
        )
    except:
        pass

    try:

        dt = channel.properties[
            "wf_increment"
        ]

        n = len(channel)

        return np.arange(n) * float(dt)

    except:
        pass

    return np.arange(len(channel))

def interpolate_to_time(
        time_source,
        signal,
        time_target):

    return np.interp(
        time_target,
        time_source,
        signal
    )

def cohens_d(x, y):

    nx = len(x)
    ny = len(y)

    pooled_std = np.sqrt(
        (
            (nx - 1) * np.var(x, ddof=1)
            +
            (ny - 1) * np.var(y, ddof=1)
        )
        /
        (nx + ny - 2)
    )

    return (
        np.mean(x)
        - np.mean(y)
    ) / pooled_std

def load_triangular_response(filepath):

    tdms = TdmsFile.read(filepath)

    position_channel = None
    pressure_channel = None
    force_channel = None

    for group in tdms.groups():

        if position_channel is None:
            position_channel = find_channel(
                group,
                [
                    "Piezo Position",
                    "Position"
                ]
            )

        if pressure_channel is None:
            pressure_channel = find_channel(
                group,
                [
                    "Pressure"
                ]
            )

        if force_channel is None:
            force_channel = find_channel(
                group,
                [
                    "Force"
                ]
            )

    position = np.asarray(
        position_channel[:],
        dtype=float
    )

    pressure = np.asarray(
        pressure_channel[:],
        dtype=float
    )

    force = np.asarray(
        force_channel[:],
        dtype=float
    )

    position_time = get_channel_time(
        position_channel
    )

    pressure_time = get_channel_time(
        pressure_channel
    )

    force_time = get_channel_time(
        force_channel
    )

    position_norm = normalize_signal(position)

    peak_idx = np.argmax(
        position_norm
    )

    time_shift = position_time[peak_idx]

    position_time = (
        position_time
        - time_shift
    )

    pressure_time = (
        pressure_time
        - time_shift
    )

    force_time = (
        force_time
        - time_shift
    )

    pressure = interpolate_to_time(
        pressure_time,
        pressure,
        position_time
    )

    force = interpolate_to_time(
        force_time,
        force,
        position_time
    )

    return {
        "time": position_time,
        "position": normalize_signal(position),
        "pressure": normalize_signal(pressure),
        "force": normalize_signal(force)
    }

def create_common_time_axis(
        measurements):

    start_time = max(
        m["time"][0]
        for m in measurements
    )

    end_time = min(
        m["time"][-1]
        for m in measurements
    )

    dt_values = []

    for m in measurements:

        dt_values.extend(
            np.diff(m["time"])
        )

    dt = np.nanmedian(
        dt_values
    )

    return np.arange(
        start_time,
        end_time,
        dt
    )

def plot_triangular_response(
        ax,
        groups,
        show_legend=True,
        show_values=True,
        show_std=True,
        show_position=True,
        time_range=None,
        statistic_values=True):

    position_plotted = False
    group_delays ={}

    colors = plt.rcParams[
        "axes.prop_cycle"
    ].by_key()["color"]

    for idx, (group_name, folders) in enumerate(
            groups.items()):

        color = colors[
            idx % len(colors)
        ]

        measurements = []
        delays = []
        n_found = 0
        n_used = 0

        for folder in folders:

            for pattern in TRIANGULAR_FILES:

                files = glob.glob(
                    os.path.join(
                        folder,
                        "**",
                        pattern
                    ),
                    recursive=True
                )

                for file in files:
                    n_found += 1

                    try:

                        measurement = (load_triangular_response(file))
                        measurements.append(measurement)
                        n_used += 1
                        position = measurement["position"]
                        pressure = measurement["pressure"]
                        time = measurement["time"]
    
                        position_peak = time[
                            np.argmax(position)
                        ]
    
                        pressure_peak = time[
                            np.argmax(pressure)
                        ]
    
                        delay_ms = (
                            pressure_peak
                            - position_peak
                        ) * 1000
    
                        delays.append(
                            delay_ms
                        )

                    except Exception:

                        continue

        if len(measurements) == 0:
            continue

        common_time = create_common_time_axis(
            measurements
        )

        delays = np.asarray(delays)
        delay_mean = np.mean(delays)
        delay_std = np.std(delays)
        delay_cv = (delay_std / delay_mean * 100)

        group_delays[group_name]= delays

        pressure_signals = []

        for measurement in measurements:

            pressure_interp = np.interp(
                common_time,
                measurement["time"],
                measurement["pressure"]
            )

            pressure_signals.append(
                pressure_interp
            )

        pressure_signals = np.asarray(
            pressure_signals
        )

        mean_curve = np.nanmean(
            pressure_signals,
            axis=0
        )

        std_curve = np.nanstd(
            pressure_signals,
            axis=0
        )

        position_signals = []

        for measurement in measurements:

            position_interp = np.interp(
                common_time,
                measurement["time"],
                measurement["position"]
            )

            position_signals.append(
                position_interp
            )

        position_signals = np.asarray(
            position_signals
        )

        position_mean = np.nanmean(
            position_signals,
            axis=0
        )

        start_idx = np.where(
            position_mean > 0.01
        )[0][0]
        
        time_offset = common_time[
                    start_idx
                ]
        
        plot_time = (common_time - time_offset)

        ax.plot(
            plot_time,
            mean_curve,
            color=color,
            label=group_name
        )

        if show_values:
            print(f"\n{group_name}")

            print(
                f"Delay Mean = "
                f"{delay_mean:.2f} ms"
            )

            print(
                f"Delay STD = "
                f"{delay_std:.2f} ms"
            )

            print(
                f"Delay CV = "
                f"{delay_cv:.2f} %"
            )

            print("SP-Triangular Response: "
                        f"{group_name}: "
                        f"{n_used}/{n_found} files used")
            
        if show_std:

            ax.plot(
                plot_time,
                mean_curve + std_curve,
                "--",
                color=color,
                alpha=0.6
            )

            ax.plot(
                plot_time,
                mean_curve - std_curve,
                "--",
                color=color,
                alpha=0.6
            )

        if (
                show_position and
                not position_plotted
        ):

            ax.plot(
                plot_time,
                position_mean,
                "--",
                color="black",
                linewidth=1.5,
                label="Piezo Position"
            )

            position_plotted = True

    if statistic_values:
        if len(group_delays) > 1:

            reference_name = "Reference"

            if reference_name in group_delays:

                reference_delays = (
                    group_delays[reference_name]
                )

                print(
                    "\n--- SP Triangular Response - Statistical Comparison ---"
                )

                for group_name, delays in group_delays.items():

                    if group_name == reference_name:
                        continue

                    t_stat, p_value = ttest_ind(
                        delays,
                        reference_delays,
                        equal_var=False
                    )

                    d = cohens_d(
                        delays,
                        reference_delays
                    )

                    print(
                        f"\n{group_name} vs "
                        f"{reference_name}"
                    )

                    print(
                        f"p-value = "
                        f"{p_value:.4f}"
                    )

                    print(
                        f"Cohen's d = "
                        f"{d:.3f}"
                    )

    if time_range is not None:

        ax.set_xlim(*time_range)

        autoscale_y(
            ax,
            *time_range
        )

    ax.set_xlabel(
        "Time [s]"
    )

    ax.set_ylabel(
        "Normalized Pressure"
    )

    ax.grid(
        True,
        alpha=0.3
    )

    handles, labels = ax.get_legend_handles_labels()

    if "Piezo Position" in labels:

        idx = labels.index("Piezo Position")

        piezo_handle = handles.pop(idx)
        piezo_label = labels.pop(idx)

        handles.insert(0, piezo_handle)
        labels.insert(0, piezo_label)

    if show_legend:
        ax.legend(handles, labels)