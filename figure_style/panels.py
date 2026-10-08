"""Figure/subplot creation locked to a fixed physical size, so panels import
into Illustrator at true scale (no resizing -> no stroke-width distortion).
"""

import matplotlib.pyplot as plt

from .style import get_active_profile


def new_panel(width_in=None, height_in=None, ncols=1, nrows=1, **subplot_kwargs):
    """
    Create a figure sized from the active style profile (call set_paper_style()
    or set_poster_style() first), unless width_in/height_in are given explicitly.

    Total figure size is (ncols * width_in) x (nrows * height_in), i.e.
    width_in/height_in are treated as the size of a single subplot panel.
    """
    profile = get_active_profile()
    if width_in is None:
        width_in = profile['default_width_in'] if profile else 2.0
    if height_in is None:
        height_in = profile['default_height_in'] if profile else 2.0

    figsize = (width_in * ncols, height_in * nrows)
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, **subplot_kwargs)
    return fig, axes
