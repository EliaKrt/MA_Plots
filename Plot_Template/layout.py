import math
import string

import matplotlib.pyplot as plt

from .style import FIG_WIDTH


def create_layout(
        nplots,
        ncols=2,
        fig_width=FIG_WIDTH,
        row_height=2.6,
        dpi=300,
        label_panels_flag=True,
        global_legend=False,
        panel_titles=None,
        panel_labels=None,):

    nrows = math.ceil(nplots / ncols)

    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(
            fig_width,
            nrows * row_height
        ),
        dpi=dpi,
        constrained_layout=True
    )

    if nplots == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    panel_names = list(string.ascii_uppercase)

    ax_dict = {}

    for i in range(nplots):
        ax_dict[panel_names[i]] = axes[i]

    for i in range(nplots, len(axes)):
        axes[i].axis("off")

    if label_panels_flag:
        from .labels import label_panels
        label_panels(fig, ax_dict, panel_titles=panel_titles, panel_labels=panel_labels)

    return fig, ax_dict

def add_global_legend(
        fig,
        ax_dict,
        ncols=4):

    handles = []
    labels = []

    for ax in ax_dict.values():

        h, l = ax.get_legend_handles_labels()

        for handle, label in zip(h, l):

            if label not in labels:

                handles.append(handle)
                labels.append(label)

    fig.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.05),
        ncol=ncols,
        frameon=False
    )