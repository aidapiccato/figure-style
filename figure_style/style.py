"""Paper vs. poster/presentation rcParams profiles.

Call set_paper_style() or set_poster_style() once before generating any
figures. new_panel() (see panels.py) reads the active profile's default
per-subplot size.
"""

import matplotlib as mpl
import seaborn as sns

_PROFILES = {
    'paper': dict(
        base_font_size=8,
        linewidth=1.0,
        axes_linewidth=0.75,
        tick_length=3,
        marker_size=4,
        dpi=150,
        default_width_in=2.0,
        default_height_in=2.0,
    ),
    'poster': dict(
        base_font_size=20,
        linewidth=2.5,
        axes_linewidth=1.75,
        tick_length=8,
        marker_size=10,
        dpi=150,
        default_width_in=4.0,
        default_height_in=4.0,
    ),
}

_active_profile = None
_active_profile_name = None


def _build_rcparams(p):
    base_font_size = p['base_font_size']
    return {
        # --- Keep text editable in Illustrator (critical) ---
        'svg.fonttype': 'none',
        'pdf.fonttype': 42,   # TrueType outlines, editable in AI (not Type 3 bitmap)
        'ps.fonttype': 42,

        # --- Font ---
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': base_font_size,
        'axes.titlesize': base_font_size + 1,
        'axes.labelsize': base_font_size,
        'xtick.labelsize': base_font_size - 1,
        'ytick.labelsize': base_font_size - 1,
        'legend.fontsize': base_font_size - 1,

        # --- Line/marker consistency across panels ---
        'lines.linewidth': p['linewidth'],
        'lines.markersize': p['marker_size'],
        'axes.linewidth': p['axes_linewidth'],
        'xtick.major.width': p['axes_linewidth'],
        'ytick.major.width': p['axes_linewidth'],
        'xtick.major.size': p['tick_length'],
        'ytick.major.size': p['tick_length'],

        # --- Aesthetics ---
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': False,
        'axes.edgecolor': 'black',
        'xtick.color': 'black',
        'ytick.color': 'black',
        'text.color': 'black',
        'axes.labelcolor': 'black',
        'savefig.transparent': True,   # no white box; layer cleanly in Illustrator
        'figure.dpi': p['dpi'],        # screen preview only; export dpi set separately
    }


def _apply_profile(name):
    global _active_profile, _active_profile_name
    _active_profile = _PROFILES[name]
    _active_profile_name = name
    sns.set_style('ticks')
    sns.set_context('paper' if name == 'paper' else 'poster')
    mpl.rcParams.update(_build_rcparams(_active_profile))


def set_paper_style():
    """Journal-style: 8pt fonts, thin strokes, 2x2 in. default panels."""
    _apply_profile('paper')


def set_poster_style():
    """Poster/presentation style: 20pt fonts, thick strokes, 6x6 in. default panels."""
    _apply_profile('poster')


def get_active_profile():
    """Return the currently active profile dict, or None if no style has been set yet."""
    return _active_profile


def get_active_profile_name():
    """Return the currently active profile name ('paper' or 'poster'), or None if unset."""
    return _active_profile_name
