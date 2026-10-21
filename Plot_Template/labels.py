import matplotlib.transforms as transforms

def label_panels(
        fig,
        ax_dict,
        panel_titles=None,
        panel_labels=None,
        xloc=0,
        yloc=1.0,
        fontsize=12):

    for key, ax in ax_dict.items():
        if panel_labels is None:
            shown_label = key

        else:
            shown_label = panel_labels.get(
                key,
                key
            )

        title = ""

        if (
            panel_titles is not None
            and key in panel_titles
        ):
            title = f" {panel_titles[key]}"

        trans = transforms.ScaledTranslation(
            -20 / 72,
            7 / 72,
            fig.dpi_scale_trans
        )

        ax.text(
            xloc,
            yloc,
            f"{shown_label} ",
            transform=ax.transAxes + trans,
            fontsize=fontsize,
            va="bottom",
            fontweight="bold"
        )

        ax.annotate(
            title,
            (xloc, yloc),
            xycoords=ax.transAxes + trans,
            xytext=(20, 0),
            textcoords="offset points",
            fontsize=fontsize,
            va="bottom"
        )