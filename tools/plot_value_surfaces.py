#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Draw the value function derivative surfaces shown on the Computational method page of the book.

The surfaces are those of the technology jump only model (Section 9 of the
paper): the pre-technology value function V(k_hat, y, r_hat) is sliced at the
grid point closest to the initial log capital k_hat_0 = log K_0, and the
partial derivatives dV/dr_hat (``m3``) and dV/dy (``m2``) on that slice are
plotted against y and r_hat for the three uncertainty aversion specifications
(xi_m = 0.05, 0.1, infinity).

The grid and the finite differences come from the replication repository
(``python/src/state_grid.py`` and ``python/src/utility.py``), so the surfaces
use exactly the discretization of the HJB solver. The HJB solutions are the
Fine grid (``double_resolution``) outputs of ``bash ./sbatch/postdamage.sh
--model tech_only --grid-profile double_resolution``. The plot follows the
legacy prepare step ``legacy/tech_only_python/FeymannKacs_prepare_NewPlug.py``,
which the current code no longer produces.

Usage (Mercury login node, shared environment of the replication repository):

    source /project/lhansen/mitigation.sh
    python tools/plot_value_surfaces.py [--repo DIR] [--solution-dir DIR] [--out-dir DIR]

Defaults use the repository clone in ~/two-capital-climate-change, read the
solutions from Jessie's scratch, and write the six html files into
docs/_static/ under the names the notebook references:
df_V_m3_surface_xik{0.05,0.1,1e+05}.html and df_V_m2_surface_xik{...}.html.
"""
import argparse
import os
import pickle
import sys

import numpy as np
import plotly.graph_objects as go

BOOK_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CODE_REPO = os.path.expanduser("~/two-capital-climate-change")

# Fine grid tech-only solutions of the replication repository.
DEFAULT_SOLUTION_DIR = (
    "/scratch/jessiel0/tech_only/ga_0.1667_4.00,9.00_0.0,5.0_1.0,8.0_0.0,2.5"
    "_SS_0.1,0.025,0.1_LR_0.1_NewPlug_phi0_0.5_GridProfile_double_resolution"
)
SOLUTION_FILE = (
    "xa100000.0_xk100000.0_xy100000.0_xr100000.0_xt{xi_m}_p00.10583_p10.5"
    "_ci1091.1_rh1.0_de0.01_tech_only_predamage_pretech"
)
# html file suffix used by the notebook -> xi_m value in the solution file name
XI_M_CASES = {"0.05": "0.05", "0.1": "0.1", "1e+05": "100000.0"}

# State grid (k_hat, y, r_hat) of the tech-only solver, as passed by
# sbatch/grid_profiles.sh (minima, maxima) and the double_resolution profile
# (steps); the profile fixes the node counts to 51 x 201 x 71.
GRID_MINIMA = (4.0, 0.0, 1.0)
GRID_MAXIMA = (9.0, 5.0, 8.0)
GRID_STEPS = (0.1, 0.025, 0.1)
GRID_PROFILE = "double_resolution"

# Initial capital K_0 = 85 / 0.115 (Appendix E, state variable initial values).
K_HAT_0 = np.log(85 / 0.115)

# Derivative name -> (array axis of the state, z axis label)
SURFACES = {"m3": (2, "∂V/∂logR"), "m2": (1, "∂V/∂Y")}


def import_repo_functions(code_repo):
    """Import the grid builder and finite-difference routine of the code repo.

    Parameters
    ----------
    code_repo : str
        Path to a clone of two-capital-climate-change.

    Returns
    -------
    tuple
        ``(build_state_axes, finiteDiff_3D)`` from ``python/src``.
    """
    sys.path.insert(0, os.path.join(code_repo, "python"))
    from src.state_grid import build_state_axes
    from src.utility import finiteDiff_3D
    return build_state_axes, finiteDiff_3D


def load_value_function(solution_dir, xi_m):
    """Load the pre-technology value function of one tech-only solution.

    Parameters
    ----------
    solution_dir : str
        Directory holding the ``*_tech_only_predamage_pretech`` pickles.
    xi_m : str
        Robustness penalty as written in the file name (``0.05``, ``0.1``,
        ``100000.0``).

    Returns
    -------
    ndarray
        V on the (k_hat, y, r_hat) grid, shape (n_k, n_y, n_r).
    """
    path = os.path.join(solution_dir, SOLUTION_FILE.format(xi_m=xi_m))
    with open(path, "rb") as handle:
        return pickle.load(handle)["value"]


def derivative_slice(value, axes, axis, finite_diff):
    """Differentiate V along one state and slice at k_hat closest to K_HAT_0.

    Parameters
    ----------
    value : ndarray
        Value function on the (k_hat, y, r_hat) grid.
    axes : tuple of ndarray
        The three state axes from ``build_state_axes``.
    axis : int
        Array axis of the state to differentiate (1 for y, 2 for r_hat).
    finite_diff : callable
        ``finiteDiff_3D`` of the code repository.

    Returns
    -------
    ndarray
        The first derivative on the k_hat slice, shape (n_y, n_r).
    """
    step = axes[axis][1] - axes[axis][0]
    derivative = finite_diff(value, axis, 1, step)  # order 1: first derivative
    k_idx = int(np.argmin(np.abs(axes[0] - K_HAT_0)))
    return derivative[k_idx]


def surface_figure(axes, z_slice, z_label):
    """Build the plotly surface of a derivative slice against y and r_hat.

    Parameters
    ----------
    axes : tuple of ndarray
        The three state axes from ``build_state_axes``.
    z_slice : ndarray
        Derivative values, shape (n_y, n_r).
    z_label : str
        Vertical axis title.

    Returns
    -------
    plotly.graph_objects.Figure
        The surface figure with the layout used by the book.
    """
    y_mesh, r_mesh = np.meshgrid(axes[1], axes[2], indexing="ij")
    fig = go.Figure(data=[go.Surface(x=y_mesh, y=r_mesh, z=z_slice,
                                     colorscale="Viridis")])
    fig.update_layout(scene=dict(xaxis_title="Y", yaxis_title="logR",
                                 zaxis_title=z_label),
                      autosize=True, margin=dict(l=0, r=0, b=0, t=30))
    return fig


def main():
    """Parse arguments and write the six surface html files."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--repo", default=DEFAULT_CODE_REPO,
                        help="clone of two-capital-climate-change")
    parser.add_argument("--solution-dir", default=DEFAULT_SOLUTION_DIR,
                        help="directory with the tech-only Fine grid solutions")
    parser.add_argument("--out-dir", default=os.path.join(BOOK_REPO, "docs", "_static"),
                        help="where to write the html files")
    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    build_state_axes, finite_diff = import_repo_functions(args.repo)
    axes = build_state_axes(GRID_MINIMA, GRID_MAXIMA, GRID_STEPS, GRID_PROFILE)

    for suffix, xi_m in XI_M_CASES.items():
        value = load_value_function(args.solution_dir, xi_m)
        if value.shape != tuple(len(axis) for axis in axes):
            raise ValueError(f"solution grid {value.shape} does not match {GRID_PROFILE}")
        for name, (axis, z_label) in SURFACES.items():
            z_slice = derivative_slice(value, axes, axis, finite_diff)
            path = os.path.join(args.out_dir, f"df_V_{name}_surface_xik{suffix}.html")
            # plotly.js is loaded from its CDN to keep each file around 0.5 MB.
            surface_figure(axes, z_slice, z_label).write_html(path, include_plotlyjs="cdn")
            print(f"wrote {path}  z range {z_slice.min():.4f} .. {z_slice.max():.4f}")


if __name__ == "__main__":
    main()
