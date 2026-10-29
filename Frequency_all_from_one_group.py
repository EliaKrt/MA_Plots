from Plot_Template import *
from plots import *

apply_style()


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

PANEL_TITLES_FREQ_ALL = {
    "A": "SP Concept 1",
    "B": "SP Concept 2",
    "C": "SP Concept 5",
    "D": "Cuff Concept 1",
    "E": "Cuff Concept 2",
    "F": "Cuff Concept 5"
}

fig, ax = create_layout(
    nplots=6,
    ncols=3,
    panel_titles=PANEL_TITLES_FREQ_ALL
)
plot_frequency_response_measurements(
    ax["A"],
    SP_groups["Concept1"],
    normalize=True,
    show_3db=True,
    show_legend=False,
)

plot_frequency_response_measurements(
    ax["B"],
    SP_groups["Concept2"],
    normalize=True,
    show_3db=True,
    show_legend=False,
)

plot_frequency_response_measurements(
    ax["C"],
    SP_groups["Concept5"],
    normalize=True,
    show_3db=True,
    show_legend=False,
)
plot_psst_frequency_response_measurements(
    ax["D"],
    Cuff_groups["Concept1"],
    normalize=True,
    show_3db=True,
    show_legend=False,
)

plot_psst_frequency_response_measurements(
    ax["E"],
    Cuff_groups["Concept2"],
    normalize=True,
    show_3db=True,
    show_legend=False,
)

plot_psst_frequency_response_measurements(
    ax["F"],
    Cuff_groups["Concept5"],
    normalize=True,
    show_3db=True,
    show_legend=False,
)

save_figure(fig, "Freq_all_from_one_group")