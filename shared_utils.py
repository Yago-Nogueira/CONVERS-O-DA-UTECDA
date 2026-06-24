#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Shared utilities extracted from duplicated patterns across comp_* modules.

Provides reusable helpers for:
- Matplotlib tick parameter configuration
- Axis locator configuration
- Axes limit configuration
- Tick label picker setup
- Colormap creation
- Grid interpolation
- Date ordering
- File path construction
- Dict-based list accumulation
- Threaded task execution
- Colorbar level/tick computation
- Matplotlib cleanup
"""

import copy
import queue
from collections import defaultdict
from threading import Thread

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib import cm
from scipy.interpolate import griddata


def apply_tick_params(axes, settings, section):
    """Apply tick parameter configuration from settings to axes.

    Reads fWidthTickMinor_X, fHeightTickMinor_X, fWidthTickMajor_X, etc.
    from ``settings[section]`` and calls ``axes.tick_params`` for each
    axis/which combination.
    """
    s = settings[section]
    axes.tick_params(
        axis='x', which='minor',
        width=s["fWidthTickMinor_X"],
        size=s["fHeightTickMinor_X"],
    )
    axes.tick_params(
        axis='x', which='major',
        width=s["fWidthTickMajor_X"],
        size=s["fHeightTickMajor_X"],
        labelsize=s["fSizeLabelsTick_X"],
    )
    axes.tick_params(
        axis='y', which='minor',
        width=s["fWidthTickMinor_Y"],
        size=s["fHeightTickMinor_Y"],
    )
    axes.tick_params(
        axis='y', which='major',
        width=s["fWidthTickMajor_Y"],
        size=s["fHeightTickMajor_Y"],
        labelsize=s["fSizeLabelsTick_Y"],
    )


def configure_axis_locator(axis, settings, section, axis_name, default):
    """Configure a major locator on *axis* from temp settings.

    Checks ``fValue_Passo_Ticks_{axis_name}_temp`` (MultipleLocator),
    then ``iValue_Num_Ticks_{axis_name}_temp`` (LinearLocator),
    falling back to *default*.

    Parameters
    ----------
    axis : matplotlib axis object (e.g. ``axes.xaxis``)
    settings : dict  -- the full Settings dict
    section : str    -- e.g. "INDIVIDUAL", "EIA"
    axis_name : str  -- "X" or "Y"
    default : ticker.Locator instance
    """
    try:
        passo_key = "fValue_Passo_Ticks_%s_temp" % axis_name
        num_key = "iValue_Num_Ticks_%s_temp" % axis_name
        if settings[section].get(passo_key):
            axis.set_major_locator(
                ticker.MultipleLocator(settings[section][passo_key])
            )
        elif settings[section].get(num_key):
            axis.set_major_locator(
                ticker.LinearLocator(settings[section][num_key])
            )
        else:
            axis.set_major_locator(default)
    except KeyError:
        axis.set_major_locator(default)


def apply_axes_limits(axes, settings, section, x_scale=1.0, y_scale=1.0):
    """Apply temporary axis limits from settings if present.

    Parameters
    ----------
    x_scale, y_scale : float
        Multiplier applied to the stored limit values (e.g. 60 for converting
        hours to minutes on the Y axis in INDIVIDUAL plots).
    """
    try:
        axes.set_xlim(
            settings[section]["fValueMin_Axes_X_temp"] * x_scale,
            settings[section]["fValueMax_Axes_X_temp"] * x_scale,
        )
    except KeyError:
        pass
    try:
        axes.set_ylim(
            settings[section]["fValueMin_Axes_Y_temp"] * y_scale,
            settings[section]["fValueMax_Axes_Y_temp"] * y_scale,
        )
    except KeyError:
        pass


def setup_tick_label_pickers(axes, section):
    """Mark x/y tick labels as pickable and assign gid strings."""
    for label in axes.get_xticklabels():
        label.set_picker(True)
        label.set_gid("ticks_x:%s" % section)
    for label in axes.get_yticklabels():
        label.set_picker(True)
        label.set_gid("ticks_y:%s" % section)


def create_jet_colormap():
    """Return a 'jet' colormap copy with white under and darkred over."""
    cmap = copy.copy(cm.get_cmap("jet"))
    cmap.set_under("white")
    cmap.set_over("darkred")
    return cmap


def interpolate_grid(x, y, z, numcols=100, numrows=100):
    """Two-pass linear grid interpolation filling masked regions.

    Returns (xi, yi, GD1) meshgrid arrays.
    """
    xi = np.linspace(x.min(), x.max(), numcols)
    yi = np.linspace(y.min(), y.max(), numrows)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((x, y), z, (xi, yi), method='linear')
    zi = np.ma.masked_invalid(zi)
    x1 = xi[~zi.mask]
    y1 = yi[~zi.mask]
    newarr = zi[~zi.mask]
    GD1 = griddata((x1, y1), newarr.ravel(), (xi, yi), method='linear')
    return xi, yi, GD1


def ensure_date_order(data_inicial, data_final):
    """Return (earlier, later) regardless of input order."""
    if data_inicial > data_final:
        return data_final, data_inicial
    return data_inicial, data_final


def build_std_filepath(directory, sigla, date_obj):
    """Build a .Std file path from a directory, station code, and date."""
    dia_ano = date_obj.timetuple().tm_yday
    filename = "%s%.3i-%i-%.2i-%.2i.Std" % (
        sigla.lower(), dia_ano, date_obj.year, date_obj.month, date_obj.day,
    )
    return directory + "/" + filename


def build_cmn_filepath(directory, sigla, date_obj):
    """Build a .Cmn file path from a directory, station code, and date."""
    dia_ano = date_obj.timetuple().tm_yday
    filename = "%s%.3i-%s-%.2i-%.2i.Cmn" % (
        sigla.lower(), dia_ano, date_obj.year, date_obj.month, date_obj.day,
    )
    return directory + "/" + filename


def dict_list_append(d, key, value):
    """Append *value* to ``d[key]``, creating the list if needed.

    Replaces the repeated try/except KeyError pattern.
    """
    try:
        d[key].append(value)
    except KeyError:
        d[key] = [value]


def run_threaded_tasks(items, target_func, extra_args=(), max_threads=10):
    """Run *target_func* over *items* using a thread-pool with a Queue.

    Each worker receives ``(queue, *extra_args)``; items are ``(index, item)``
    tuples placed on the queue.
    """
    total = len(items)
    if total == 0:
        return
    q = queue.Queue(maxsize=0)
    num_threads = min(max_threads, total)
    for i, item in enumerate(items):
        q.put((i, item))
    for _ in range(num_threads):
        Thread(target=target_func, args=(q, *extra_args), daemon=True).start()
    q.join()


def compute_colorbar_levels(settings, section, data_key):
    """Compute contour levels and colorbar ticks from settings.

    Parameters
    ----------
    data_key : str
        e.g. "VTEC", "ROT", "ROTI" -- used to look up
        ``iTicksCbar_{data_key}``, ``iDivTicks_{data_key}``,
        ``fValueMax_B_{data_key}``, ``fValueMin_B_{data_key}``.

    Returns
    -------
    levels, ticks, vm_min, vm_max
    """
    s = settings[section]
    ticks_cbar = s["iTicksCbar_%s" % data_key]
    ticks_div = s["iDivTicks_%s" % data_key]
    vm_max = s["fValueMax_B_%s" % data_key]
    vm_min = s["fValueMin_B_%s" % data_key]
    levels = np.linspace(
        vm_min, vm_max,
        int(ticks_cbar + ((ticks_cbar - 1) * (ticks_div - 1))),
    )
    ticks = np.linspace(vm_min, vm_max, int(ticks_cbar))
    return levels, ticks, vm_min, vm_max


def cleanup_matplotlib():
    """Close and clear all matplotlib figures."""
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()


def organize_cmn_data(dado_cmn, prns_cmn, dados_organizados, date_key, station):
    """Parse CMN data into the nested dados_organizados dict.

    Shared between comp_MAPA and comp_GRADE_MAPA thread workers.
    """
    dados_organizados[date_key][station] = {}
    for prn in prns_cmn:
        str_prn = str(prn)
        dados_organizados[date_key][station][str_prn] = {}
        for hora in dado_cmn[str_prn + ".time"]:
            dados_organizados[date_key][station][str_prn][hora] = {}
            ind = dado_cmn[str_prn + ".time"].index(hora)
            dados_organizados[date_key][station][str_prn][hora]['lon'] = dado_cmn[str_prn + ".lon"][ind]
            dados_organizados[date_key][station][str_prn][hora]['lat'] = dado_cmn[str_prn + ".lat"][ind]
            dados_organizados[date_key][station][str_prn][hora]['vtec'] = dado_cmn[str_prn + ".vtec"][ind]


def collect_plot_data_vtec(dados_organizados, dados_organizados_plot, date_key, station, prns):
    """Collect lon/lat/vtec into flat plot-data lists, skipping NaN vtec."""
    for prn in prns:
        str_prn = str(prn)
        for hora in dados_organizados[date_key][station][str_prn].keys():
            entry = dados_organizados[date_key][station][str_prn][hora]
            if not np.isnan(entry['vtec']):
                dict_list_append(dados_organizados_plot[date_key], hora + ".lat", entry['lat'])
                dict_list_append(dados_organizados_plot[date_key], hora + ".lon", entry['lon'])
                dict_list_append(dados_organizados_plot[date_key], hora + ".vtec", entry['vtec'])
