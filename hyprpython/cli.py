#!/usr/bin/env python
"""
Command-line helpers for Hyprland windows.

Two entry points are exposed via setup.py:
  * hypr-pull-class
  * hypr-focus-class
"""
import argparse
from . import core as hp


# ── helpers ──────────────────────────────────────────────────────────────────
def _parse():
    p = argparse.ArgumentParser()
    p.add_argument("window_class", help="Hyprland WM_CLASS to operate on")
    return p.parse_args().window_class


# ── hypr-pull-class entry point ──────────────────────────────────────────────
def pull_window_by_class() -> None:            # noqa: N802 (CLI name is fine)
    wclass = _parse()
    active_ws      = hp.Workspaces.current()
    clients        = hp.Clients.byFocusID()

    targets = [
        c for c in clients
        if c.wm_class == wclass and c.workspace.id != active_ws.id
    ]
    if targets:
        hp.Hyprctl.move_to_workspace_silent(targets[0].address, active_ws.id)
        hp.Hyprctl.focus_window(targets[0].address)


# ── hypr-focus-class entry point ─────────────────────────────────────────────
def focus_window_by_class() -> None:           # noqa: N802
    import os, pickle, pathlib, itertools

    wclass = _parse()
    filepath = pathlib.Path(f"/tmp/{wclass}.pkl")

    client_ordered  = hp.Clients.byFocusID()
    current_window  = hp.Clients.focused()
    focus_list      = [w for w in client_ordered
                       if w.wm_class == wclass and w.workspace.id > 0]

    if current_window.wm_class != wclass:
        filepath.write_bytes(pickle.dumps(focus_list))
        hp.Hyprctl.focus_window(focus_list[0].address)
        return

    # rotating through the list
    stored = pickle.loads(filepath.read_bytes()) if filepath.exists() else focus_list
    cycle  = itertools.cycle(stored)
    for win in cycle:
        if win.address == current_window.address:          # found current
            nxt = next(cycle)
            hp.Hyprctl.focus_window(nxt.address)
            break
