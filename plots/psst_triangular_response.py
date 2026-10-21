import os
import glob

import numpy as np
import matplotlib.pyplot as plt

from nptdms import TdmsFile


TRIANGULAR_FILE = "TriangularResponse.tdms"


def normalize_signal(values):

    values = np.asarray(
        values,
        dtype=float
    )

    minimum = np.nanmin(values)
    maximum = np.nanmax(values)

    if maximum == minimum:

        return np.zeros_like(
            values
        )

    return (
        values - minimum
    ) / (
        maximum - minimum
    )


def find_channel(
        group,
        candidates):

    for candidate in candidates:

        for channel in group.channels():

            if (
                    channel.name.lower()
                    ==
                    candidate.lower()
            ):
                return channel

    for candidate in candidates:

        for channel in group.channels():

            if (
                    candidate.lower()
                    in channel.name.lower()
            ):
                return channel

    return None


def get_channel_time(channel):

    try:

        return np.asarray(
            channel.time_track(),
            dtype=float
        )

    except Exception:
        pass

    try:

        dt = channel.properties[
            "wf_increment"
        ]

        n = len(channel)

        return (
            np.arange(n)
            * float(dt)
        )

    except Exception:
        pass

    return np.arange(
        len(channel),
        dtype=float
    )


def interpolate_to_time(
        time_source,
        signal,
        time_target):

    return np.interp(
        time_target,
        time_source,
        signal
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


def load_psst_triangular_response(
        filepath):

    tdms = TdmsFile.read(
        filepath
    )

    position_channel = None
    pressure_channel = None

    for group in tdms.groups():

        if position_channel is None:

            position_channel = find_channel(
                group,
                [
                    "Piezo Position",
                    "PiezoPosition",
                    "Position",
                    "Piezo_Pos",
                    "PiezoPos"
                ]
            )

        if pressure_channel is None:

            pressure_channel = find_channel(
                group,
                [
                    "Pressure",
                    "Pressure [mmHg]",
                    "Pressure_mmHg",
                    "PressuremmHg"
                ]
            )

    if position_channel is None:

        raise RuntimeError(
            f"No position channel found:\n{filepath}"
        )

    if pressure_channel is None:

        raise RuntimeError(
            f"No pressure channel found:\n{filepath}"
        )

    position = np.asarray(
        position_channel[:],
        dtype=float
    )

    pressure = np.asarray(
        pressure_channel[:],
        dtype=float
    )

    position_time = get_channel_time(
        position_channel
    )

    pressure_time = get_channel_time(
        pressure_channel
    )

    position_time = (
        position_time
        - position_time[0]
    )

    pressure_time = (
        pressure_time
        - pressure_time[0]
    )

    pressure = interpolate_to_time(
        pressure_time,
        pressure,
        position_time
    )

    return {
        "time": position_time,
        "position": normalize_signal(
            position
        ),
        "pressure": normalize_signal(
            pressure
        )
    }


def create_common_time_axis(
        measurements):

    shortest_time = min(
        measurement["time"][-1]
        for measurement in measurements
    )

    dt_values = []

    for measurement in measurements:

        dt_values.extend(
            np.diff(
                measurement["time"]
            )
        )

    dt = np.nanmedian(
        dt_values
    )

    return np.arange(
        0,
        shortest_time,
        dt
    )


def plot_psst_triangular_response(
        ax,
        groups,
        show_legend=True,
        show_std=True,
        show_position=True,
        time_range=None,
        exclude_dirs=None,
        valid_sizes=None):

    colors = plt.rcParams[
        "axes.prop_cycle"
    ].by_key()["color"]

    position_plotted = False

    for idx, (
            group_name,
            folders
    ) in enumerate(
        groups.items()
    ):

        color = colors[
            idx % len(colors)
        ]

        measurements = []

        for folder in folders:

            files = glob.glob(
                os.path.join(
                    folder,
                    "**",
                    TRIANGULAR_FILE
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

                    measurements.append(
                        load_psst_triangular_response(
                            file
                        )
                    )

                except Exception as e:

                    print(
                        f"Failed:\n{file}"
                    )

                    print(e)

                    continue

        if len(measurements) == 0:

            print(
                f"{group_name}: no valid measurements"
            )

            continue

        common_time = (
            create_common_time_axis(
                measurements
            )
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
                show_position
                and not position_plotted
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

    handles, labels = (
        ax.get_legend_handles_labels()
    )

    if "Piezo Position" in labels:

        idx = labels.index(
            "Piezo Position"
        )

        handles.insert(
            0,
            handles.pop(idx)
        )

        labels.insert(
            0,
            labels.pop(idx)
        )

    if show_legend:
        ax.legend(
            handles,
            labels
        )