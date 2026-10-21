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