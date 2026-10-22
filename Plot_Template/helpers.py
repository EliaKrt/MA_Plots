import numpy as np

def standard_axis(
        ax,
        xlabel="",
        ylabel="",
        title=""):

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    ax.grid(True)

    return ax

def autoscale_y(
        ax,
        xmin,
        xmax,
        margin=0.05):

    ymin = np.inf
    ymax = -np.inf

    for line in ax.get_lines():

        x = line.get_xdata()
        y = line.get_ydata()

        x = np.asarray(x)
        y = np.asarray(y)

        mask = (
            (x >= xmin)
            & (x <= xmax)
        )

        if np.any(mask):

            ymin = min(
                ymin,
                np.min(y[mask])
            )

            ymax = max(
                ymax,
                np.max(y[mask])
            )

    delta = ymax - ymin

    ax.set_ylim(
        ymin - margin * delta,
        ymax + margin * delta
    )