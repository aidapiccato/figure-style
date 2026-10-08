"""Export matplotlib figures as vector files ready for Illustrator placement."""

import os

from matplotlib.transforms import Bbox

from .style import get_active_profile_name


def _tight_bbox_inches(fig, pad_inches):
    """Compute a tight bbox (in inches) that fully includes axis labels.

    matplotlib's own bbox_inches='tight' relies on Axes.get_tightbbox(),
    which under-reports the extent of an axis label when the label is wider
    than the axes (e.g. a long xlabel on a narrow panel) -- the far edge of
    the label gets silently clipped in the saved file. Unioning in the
    label Text artists' own window extents works around it.
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    bboxes = [ax.get_tightbbox(renderer) for ax in fig.axes]
    for ax in fig.axes:
        if ax.xaxis.label.get_text():
            bboxes.append(ax.xaxis.label.get_window_extent(renderer))
        if ax.yaxis.label.get_text():
            bboxes.append(ax.yaxis.label.get_window_extent(renderer))

    full = Bbox.union(bboxes).transformed(fig.dpi_scale_trans.inverted())
    return full.padded(pad_inches)


def export_for_illustrator(fig, name, outdir=".", formats=("pdf",),
                            rasterize_artists=None, raster_dpi=400):
    """
    Save a figure as vector file(s) ready for Illustrator placement.

    fig: matplotlib Figure
    name: output filename stem (no extension)
    outdir: output directory. A subdirectory named after the active style
        profile ("paper" or "poster", set via set_paper_style()/
        set_poster_style()) is created under outdir and used to hold the
        exported file(s).
    formats: any of "pdf", "svg", "eps" -- PDF recommended as primary
             (better transparency/layering fidelity); SVG useful if you want
             to inspect/edit the XML or need per-element structure.
    rasterize_artists: optional list of matplotlib artists (e.g. a dense
        scatter PathCollection) to rasterize at high DPI while everything
        else (axes, labels, annotations) stays vector. Use this for panels
        with thousands of points so Illustrator doesn't choke on object count.
    raster_dpi: DPI for rasterized artists only.
    """
    if rasterize_artists:
        for artist in rasterize_artists:
            artist.set_rasterized(True)
        fig.set_dpi(raster_dpi)  # affects only rasterized elements at save time

    style_name = get_active_profile_name()
    if style_name is None:
        raise RuntimeError(
            "No style profile is active -- call set_paper_style() or "
            "set_poster_style() before export_for_illustrator()."
        )
    outdir = os.path.join(outdir.rstrip('/'), style_name)
    os.makedirs(outdir, exist_ok=True)

    pad_inches = 0.02
    bbox = _tight_bbox_inches(fig, pad_inches)
    for fmt in formats:
        path = f"{outdir.rstrip('/')}/{name}.{fmt}"
        fig.savefig(path, format=fmt, bbox_inches=bbox, transparent=True)
        print(os.path.abspath(path))
