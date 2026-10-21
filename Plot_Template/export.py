def save_figure(
        fig,
        filename):

    if not filename.endswith(".svg"):
        filename += ".svg"

    fig.savefig(
        filename,
        dpi=fig.dpi,
        bbox_inches="tight"
    )