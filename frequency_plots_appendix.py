from Plot_Template import *
from plots import *

apply_style()

global_legend = True

SP_groups = {
    "Concept1": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_07_260827\01_RawData\SP_final_tester\Prototypes"],
    "Concept2": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_06_260730\01_RawData\SP_final_tester\Prototypes"],
    "Concept5": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_08_261009\01_RawData\SP_final_tester\Prototypes"],
    "Reference": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_06_260730\01_RawData\SP_final_tester\Reference",
                  r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_08_261009\01_RawData\SP_final_tester\Reference",
                  r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_04_260622\01_RawData\SP_A_reports_results",
                  ],
}

Cuff_groups = {
    "Concept1": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_07_260827\05_PSST_Tests\Prototypes"],
    "Concept2": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_06_260730\05_PSST_Tests\Prototypes"],
    "Concept5": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_08_261009\05_PSST_Tests\Prototypes"],
    "Reference": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - Test Results"],
    #"Reference": [r"C:\Users\320309817\OneDrive - Philips\Advanced Monitoring Cuff - 03_Elia_Krutti\03_Experiments\AMC_EK_06_260730\05_PSST_Tests\Reference"],
}

fig, ax = create_layout(
    nplots=2,
    ncols=2,
    global_legend=global_legend,
)

# ==================================
#       SP-Final Tester
# ==================================
'''
plot_group_frequency_response(
    ax["A"],
    groups = SP_groups,
    show_legend=not global_legend,
    normalize=False,
    show_std=True,
    show_3db=False
)

plot_group_frequency_response(
    ax["B"],
    groups = SP_groups,
    show_legend=not global_legend,
    normalize=False,
    show_std=True,
    show_3db=False,
    freq_range=(0,20)
)
add_global_legend(
    fig,
    ax,
    ncols=5
)

save_figure(fig, "Final_tester_not_normalized_frequency")
'''
# =================================================
#       PSST
# =================================================

plot_psst_frequency_response(
    ax["A"],
    groups = Cuff_groups,
    show_legend=not global_legend,
    normalize=False,
    show_std=True,
    show_3db=False,
    exclude_dirs=EXCLUDE_DIRS,
    valid_sizes=VALID_SIZES
)

plot_psst_frequency_response(
    ax["B"],
    groups = Cuff_groups,
    show_legend=not global_legend,
    normalize=False,
    show_std=True,
    show_3db=False,
    freq_range=(0,20),
    exclude_dirs=EXCLUDE_DIRS,
    valid_sizes=VALID_SIZES
)

add_global_legend(
    fig,
    ax,
    ncols=5
)

save_figure(fig, "PSST_not_normalized_frequency")
