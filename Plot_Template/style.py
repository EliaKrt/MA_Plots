from matplotlib import pyplot as plt, rcParams
from cycler import cycler


FIG_WIDTH = 7.5

TINY_SIZE = 6
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

# Standard-Linienbreite
LINEWIDTH = 1.5

# Farbpalette
COLORS = [
    "#005293",  # Blau
    "#E37222",  # Orange
    "#A2AD00",  # Grün
    "#D61313",  # Dunkelrot
    "#64A0C8",  # Hellblau
    "#000000"   # Schwarz
]


def apply_style():

    plt.rc('font', size=SMALL_SIZE)

    plt.rc(
        'axes',
        titlesize=TINY_SIZE,
        titleweight='bold',
        prop_cycle=cycler(color=COLORS)
    )

    plt.rc('axes', labelsize=SMALL_SIZE)
    plt.rc('xtick', labelsize=TINY_SIZE)
    plt.rc('ytick', labelsize=TINY_SIZE)
    plt.rc('legend', fontsize=TINY_SIZE)

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']

    rcParams['axes.spines.top'] = False
    rcParams['axes.spines.right'] = False

    plt.rcParams['lines.linewidth'] = LINEWIDTH

    # Grid ähnlich wie in deinem Scatterplot
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = ':'
