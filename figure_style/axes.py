"""Axis-tick helpers for panels where despine(trim=True) can clip the data."""

import numpy as np


def extend_linear_ticks(ax, values, axis='x', vmin=None, vmax=None):
    """Extend a linearly-scaled axis's major ticks to fully bracket `values`.

    Without this, sns.despine(trim=True) trims the spine to whatever ticks
    matplotlib happened to auto-generate, which can end short of the data's
    actual max/min and make points look like they fall outside the axis.
    Uses the spacing between the axis's existing (auto-generated) ticks and
    extends that same grid outward until it covers `values`.

    Args:
        ax: matplotlib Axes with a linearly-scaled `axis`.
        values: array-like of the plotted data (used to compute the tick range).
        axis: 'x' or 'y'.
        vmin: if given, clamp the lowest tick to this value instead of
            letting it extend below (e.g. vmin=0 when the data can't be
            negative, to avoid an uninformative tick below zero).
        vmax: if given, clamp the highest tick to this value instead of
            letting it extend above.

    Returns:
        The array of tick locations that was set.
    """
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    ticks = ax.get_xticks() if axis == 'x' else ax.get_yticks() if axis == 'y' else None
    if ticks is None:
        raise ValueError(f"axis must be 'x' or 'y', got {axis!r}")
    if len(ticks) < 2:
        raise ValueError('axis needs at least 2 existing ticks to infer spacing')

    step = ticks[1] - ticks[0]
    start, end = ticks[0], ticks[-1]
    start -= step * np.ceil(max(0.0, start - values.min()) / step)
    end += step * np.ceil(max(0.0, values.max() - end) / step)
    if vmin is not None:
        start = max(start, vmin)
    if vmax is not None:
        end = min(end, vmax)
    new_ticks = np.arange(start, end + step / 2, step)

    if axis == 'x':
        ax.set_xticks(new_ticks)
    else:
        ax.set_yticks(new_ticks)
    return new_ticks


def extend_log_ticks(ax, values, axis='x', vmin=None, vmax=None):
    """Extend a log-scaled axis's major ticks to fully bracket `values`.

    Without this, sns.despine(trim=True) trims the spine to whatever ticks
    matplotlib happened to auto-generate, which can end short of the data's
    actual max/min and make points look like they fall outside the axis.

    Args:
        ax: matplotlib Axes with a log-scaled `axis`.
        values: array-like of the plotted data (used to compute the tick range).
        axis: 'x' or 'y'.
        vmin: if given, clamp the lowest tick to this value (must be a power
            of ten) instead of extending below it.
        vmax: if given, clamp the highest tick to this value (must be a
            power of ten) instead of extending above it.

    Returns:
        The array of tick locations that was set.
    """
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    min_pow = int(np.floor(np.log10(values.min())))
    max_pow = int(np.ceil(np.log10(values.max())))
    if vmin is not None:
        min_pow = max(min_pow, int(round(np.log10(vmin))))
    if vmax is not None:
        max_pow = min(max_pow, int(round(np.log10(vmax))))
    ticks = 10.0 ** np.arange(min_pow, max_pow + 1)
    if axis == 'x':
        ax.set_xticks(ticks)
    elif axis == 'y':
        ax.set_yticks(ticks)
    else:
        raise ValueError(f"axis must be 'x' or 'y', got {axis!r}")
    return ticks
