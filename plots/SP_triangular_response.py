import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from nptdms import TdmsFile

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

    position_time -= position_time[0]
    pressure_time -= pressure_time[0]
    force_time -= force_time[0]

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

    shortest_time = min(
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
        0,
        shortest_time,
        dt
    )

def plot_triangular_response(
        ax,
        groups,
        show_legend=True,
        show_std=True,
        show_position=True,
        time_range=None):

    position_plotted = False

    colors = plt.rcParams[
        "axes.prop_cycle"
    ].by_key()["color"]

    for idx, (group_name, folders) in enumerate(
            groups.items()):

        color = colors[
            idx % len(colors)
        ]

        measurements = []

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

                    try:

                        measurements.append(
                            load_triangular_response(
                                file
                            )
                        )

                    except Exception:

                        continue

        if len(measurements) == 0:
            continue

        common_time = create_common_time_axis(
            measurements
        )

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

        ax.plot(
            common_time,
            mean_curve,
            color=color,
            label=group_name
        )

        if show_std:

            ax.plot(
                common_time,
                mean_curve + std_curve,
                "--",
                color=color,
                alpha=0.6
            )

            ax.plot(
                common_time,
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
                common_time,
                position_mean,
                "--",
                color="black",
                linewidth=1.5,
                label="Piezo Position"
            )

            position_plotted = True

    if time_range is not None:

        ax.set_xlim(
            time_range[0],
            time_range[1]
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