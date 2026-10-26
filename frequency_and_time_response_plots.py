from Plot_Template import *
from plots import *

apply_style()

global_legend = True

SP_groups = {
    "Concept1": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_07_260827\01_RawData\SP_final_tester\Prototypes"],
    "Concept2": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_06_260730\01_RawData\SP_final_tester\Prototypes"],
    "Concept3": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_08_261009\01_RawData\SP_final_tester\Prototypes"],
    "Reference": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_06_260730\01_RawData\SP_final_tester\Reference",
                  r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_08_261009\01_RawData\SP_final_tester\Reference",
                  r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_04_260622\01_RawData",
                  ],
}

Cuff_groups = {
    "Concept1": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_07_260827\05_PSST_Tests\Prototypes"],
    "Concept2": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_06_260730\05_PSST_Tests\Prototypes"],
    "Concept3": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_08_261009\05_PSST_Tests\Prototypes"],
    "Reference": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - Test Results"],
    #"Reference": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_06_260730\05_PSST_Tests\Reference"],
}

fig, ax = create_layout(
    nplots=8,
    ncols=4,
    global_legend=global_legend,
    panel_titles=PANEL_TITLES_8,
    panel_labels=PANEL_LABELS_8,
)

plot_group_frequency_response(
    ax["A"],
    groups = SP_groups,
    show_legend=not global_legend,
    normalize=True,
    show_std=True,
    show_3db=True
)

plot_group_frequency_response(
    ax["B"],
    groups = SP_groups,
    show_legend=not global_legend,
    normalize=True,
    show_std=True,
    show_3db=False,
    freq_range=(0,20)
)

plot_triangular_response(
    ax["C"],
    groups = SP_groups,
    show_legend=not global_legend,
    show_std=True,
    show_position=True
)

plot_triangular_response(
    ax["D"],
    groups = SP_groups,
    show_legend=not global_legend,
    show_values=False,
    show_std=False,
    show_position=True,
    time_range=(0.09, 0.11)
)

plot_psst_frequency_response(
    ax["E"],
    groups = Cuff_groups,
    show_legend=not global_legend,
    normalize=True,
    show_std=True,
    show_3db=True,
    exclude_dirs=EXCLUDE_DIRS,
    valid_sizes=VALID_SIZES
)

plot_psst_frequency_response(
    ax["F"],
    groups = Cuff_groups,
    show_legend=not global_legend,
    normalize=True,
    show_std=True,
    show_3db=False,
    freq_range=(0,20),
    exclude_dirs=EXCLUDE_DIRS,
    valid_sizes=VALID_SIZES
)

plot_psst_triangular_response(
    ax["G"],
    groups = Cuff_groups,
    show_legend=not global_legend,
    show_std=True,
    show_position=True,
    exclude_dirs=EXCLUDE_DIRS,
    valid_sizes=VALID_SIZES
)

plot_psst_triangular_response(
    ax["H"],
    groups = Cuff_groups,
    show_legend=not global_legend,
    show_values=False,
    show_std=False,
    show_position=True,
    time_range=(0.09, 0.11),
    exclude_dirs=EXCLUDE_DIRS,
    valid_sizes=VALID_SIZES
)

add_global_legend(
    fig,
    ax,
    ncols=5
)

save_figure(fig, "test")

'''
fig, ax = create_layout(
    nplots=4,
    ncols=2,
    global_legend=global_legend,
    panel_labels=PANEL_LABELS_4,
    panel_titles=PANEL_TITLES_4_FREQ,
)

plot_group_frequency_response(
    ax["A"],
    groups = SP_groups,
    show_legend=not global_legend,
    normalize=True,
    show_std=True,
    show_3db=True
)

plot_group_frequency_response(
    ax["B"],
    groups = SP_groups,
    show_legend=not global_legend,
    normalize=True,
    show_std=True,
    freq_range=(0,20)
)

plot_psst_frequency_response(
    ax["C"],
    groups = Cuff_groups,
    show_legend=not global_legend,
    normalize=True,
    show_std=True,
    show_3db=True,
    exclude_dirs=EXCLUDE_DIRS,
    valid_sizes=VALID_SIZES
)

plot_psst_frequency_response(
    ax["D"],
    groups = Cuff_groups,
    show_legend=not global_legend,
    normalize=True,
    show_std=True,
    show_3db=True,
    freq_range=(0,20),
    exclude_dirs=EXCLUDE_DIRS,
    valid_sizes=VALID_SIZES
)

add_global_legend(
    fig,
    ax,
    ncols=5
)

save_figure(fig, "frequency")
'''