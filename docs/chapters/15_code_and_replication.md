# Code and replication

This page collects the commands that solve the models of the paper and reproduce its figures and tables with the code repository that accompanies it. Solve chains that several pages share are written once here, each page that shows paper figures or tables ends with the commands for them, and {ref}`Paper figures and tables <code-paper-items>` lists every figure and table of the paper. The repository keeps copies of the generated figures and tables in `results_in_paper/`, named by their paper numbers. Its `README.md` and `manifest_replication/procedure.md` document the workflow, and `manifest_replication/master_HJB.sh`, `manifest_replication/master_post_HJB.sh` and `manifest_replication/master_sensitivity_no_calibration.sh` list the commands in full, with the continuations and alternatives that this page leaves out.

(code-environment)=
## Environment

The code runs on a Slurm cluster. Most wrappers in `sbatch/` write job scripts that include one of the settings files in `setting/`: the HJB, Feynman Kac and simulation wrappers take the file that `sbatch/grid_profiles.sh` selects for the grid, most plot and table wrappers take `setting/server_settings.sh`, and `sbatch/stochastic_trajectories_plot.sh` takes `setting/server_settings_sto_plot.sh`.

| Settings file | Grid or wrapper | Memory | Time limit |
|---|---|---|---|
| `setting/server_settings.sh` | Coarse grid, plots and tables | 8G | 1 day |
| `setting/server_settings_grid_sensitivity.sh` | Medium grid | 16G | 2 days |
| `setting/server_settings_double_resolution.sh` | Fine grid | 32G | 2 days |
| `setting/server_settings_sto_plot.sh` | `sbatch/stochastic_trajectories_plot.sh` | 80G | 12 hours |

All four files request one CPU per task on the partition `standard` of the Slurm account `pi-lhansen` and load the modules `python/booth/3.12` and `gcc/14.1.0`. Change these lines for another cluster or account, and the same settings that `sbatch/diagnostics/collect_full_model_fk_terminal.sh`, `sbatch/diagnostics/run_full_model_fk_terminal.sh` and `sbatch/experiments/no_jump_temperature/run_damage_density_panels.sh` set in their own lines.

The HJB solvers import the compiled extensions `petsc4py`, `petsclinearsystem` and `SolveLinSys`. The source of `SolveLinSys` is in `src/cppcore/`, and `petsc_install.sh` records the steps that built PETSc and the extensions on the cluster, with the paths of that installation. The repository `README.md` warns that `src/linearsystemcore/setup.py`, which builds `petsclinearsystem`, "still depends on native sources that are not present in this checkout, so a clean clone cannot rebuild that extension without restoring those files or using an existing server install." The missing sources are the files `src/petsclinearsystem.pyx`, `src/petsclinearsystemimpl.c` and `src/petsclinearsystem.h` inside `src/linearsystemcore/` that this setup file names.

(code-running)=
## Running the scripts

Run every command from the root of the code repository. Each `sbatch/` wrapper returns as soon as its Slurm jobs are submitted, without dependencies between the jobs, and most wrappers keep the generated job scripts under `bash/`. Run the commands of a block in order and start each one only after the jobs of the previous one have finished.

Wrappers that accept `--model` (`full_model`, `tech_only`, `2stage_tech` or `partial_tech`) need it as their first option, and `full_model` is the default. The wrappers of the baseline figures, the stochastic and zero shock paths and the date value tables serve only the full model and take no `--model`.

After each HJB stage, run the `check_all_pretech.sh` command that follows it in the blocks below. It reads the solver logs and writes a table with the status and the latest PDE and false transient errors of every job under `job-outs/check_all_pretech/`. A job that Slurm reports as finished may not have converged, so check the statuses and errors before you move on. Continue unconverged jobs with the matching `sbatch/postdamage_sub.sh` or `sbatch/predamage_sub.sh` command of `manifest_replication/master_HJB.sh` and check again.

Slurm logs go to `job-outs/`, most of them to `job-outs/<dataset>/<wrapper>/`, figures go to `output/figures/<dataset>/` and tables to `output/tables/<dataset>/`, with `<dataset>` as defined in {ref}`Grids <code-grids>`. HJB solutions, Feynman Kac inputs and simulated paths go to `/scratch/<user>/<model>/<dataset>/`, where `<user>` is the output of `id -un` and `<model>` is the `--model` value.

`sbatch/update_results.sh` registers finished results and copies them to `results_in_paper/` under their paper numbers. With most options it also compiles the comparison files `manifest_replication/mitigation_rerun_comparison.tex` and `manifest_replication/appendix_rerun.tex` with `pdflatex` at the end of the job, so add `--no-compile` where `pdflatex` is not available.

(code-grids)=
## Grids

From Appendix F of the paper:

To reduce the extensive computational cost of calculating the sensitivity analysis outcomes, we use a coarse grid resolution rather than the fine grid resolution applied for our main analysis. As shown in [Appendix G](04_computational_method.md), this grid choice has no impact on the qualitative implications of the model solutions, and only minor quantitative impacts that are most noticeable in the more risk aversion case. The exception to this grid choice are the results reported in Figure 11 and Table 21, which use the fine grid resolution.

The wrappers select the grid with `--grid-profile` and use the Coarse grid without it. The node counts follow the order of Table 27. The Coarse grid serves the $\xi_a$ calibration, the sensitivity analyses and the initial guesses of the Fine grid solves, the Medium grid serves the grid comparisons and the initial guesses of the technology jump only model, and the Fine grid gives the main results.

| Grid | `--grid-profile` | Nodes after the damage jump | Nodes before the damage jump | `<steps>` | `<suffix>` |
|---|---|---|---|---|---|
| Coarse | `baseline` | $26 \times 101 \times 36$ | $26 \times 51 \times 36$ | `0.2,0.05,0.2` | none |
| Medium | `finer_grid` | $33 \times 127 \times 45$ | $33 \times 64 \times 45$ | `0.1563,0.0397,0.1591` | `_GridProfile_finer_grid` |
| Fine | `double_resolution` | $51 \times 201 \times 71$ | $51 \times 101 \times 71$ | `0.1,0.025,0.1` | `_GridProfile_double_resolution` |

Each model and grid has its own dataset directory, written `<dataset>` on this site:

| Model | `--model` | `<dataset>` |
|---|---|---|
| Full model | `full_model` | `2jump_step_4.00,9.00_0.0,5.0_1.0,8.0_0.0,2.5_SS_<steps>_LR_0.1_Boundary_phi0_0.5<suffix>` |
| Technology jump only model | `tech_only` | `ga_0.1667_4.00,9.00_0.0,5.0_1.0,8.0_0.0,2.5_SS_<steps>_LR_0.1_NewPlug_phi0_0.5<suffix>` |
| Two step model | `2stage_tech` | `two_stage_ga_0.1667_4.00,9.00_0.0,5.0_1.0,8.0_0.0,2.5_SS_<steps>_LR_0.1_phi0_0.5<suffix>` |
| Partial technology model | `partial_tech` | `partial_ga_0.1667_4.00,9.00_0.0,5.0_1.0,8.0_0.0,2.5_SS_<steps>_LR_0.1_phi0_0.5<suffix>` |

For example, the Fine grid directory of the full model is `2jump_step_4.00,9.00_0.0,5.0_1.0,8.0_0.0,2.5_SS_0.1,0.025,0.1_LR_0.1_Boundary_phi0_0.5_GridProfile_double_resolution`. The sensitivity analyses write their tables under `output/tables/sensitivity_<dataset>/<profile>/`, with the Coarse grid directory of the full model as `<dataset>`.

(code-full-model)=
## Full model

From Appendix E of the paper:

In constructing Table 8 of the paper, we set the model ambiguity parameter $\xi_a$ so that at the initial date, the implied increase in the model average matched a run with model ambiguity aversion replaced by model misspecification concerns for all of the evolution equations, including the temperature evolution equation. We performed the computation for each choice of $\xi_m.$

Calibration case `1` solves the full model on the Coarse grid for $\xi_m = \infty$, $.1$ and $.05$ with $\xi_a = \infty$ and the temperature penalty `xi_y` equal to $\xi_m$, and its prepare jobs compute the implied $\xi_a$. Case `3` solves the model with the implied $\xi_a$ and an infinite `xi_y`, starting from the case `1` solutions. The calibration repeats case `3` with the newly implied $\xi_a$ until it changes by less than $10^{-7}$. The case `3` arrays in `sbatch/postdamage_sub.sh`, `sbatch/predamage.sh` and `sbatch/feymannkacs_prepare.sh` already hold the final values $\xi_a = .0034917$ for $\xi_m = .1$ and $\xi_a = .0017469$ for $\xi_m = .05$, so one round reproduces the paper. To check them, open the case `3` prepare job outputs under `job-outs/<dataset>/feymannkacs_prepare/` of the Coarse grid: each prints `new_xi_a`, the implied value, and `last_round_xi_a`, the value used in the solve, and the two should differ by less than $10^{-7}$. The Fine grid solves keep these values and start from the Coarse grid solutions.

~~~~bash
# Coarse grid, calibration case 1
bash ./sbatch/postdamage.sh --model full_model
bash ./sbatch/postdamage_sub.sh --model full_model calibrating_xia 1
bash ./check_all_pretech.sh --model full_model postdamage calibrating_xia
bash ./sbatch/predamage.sh --model full_model calibrating_xia 1
bash ./check_all_pretech.sh --model full_model predamage calibrating_xia
bash ./sbatch/feymannkacs_prepare.sh --model full_model 1
# Coarse grid, calibration case 3 with the final values
bash ./sbatch/postdamage_sub.sh --model full_model calibrating_xia 3
bash ./check_all_pretech.sh --model full_model postdamage calibrating_xia
bash ./sbatch/predamage.sh --model full_model calibrating_xia 3
bash ./check_all_pretech.sh --model full_model predamage calibrating_xia
bash ./sbatch/feymannkacs_prepare.sh --model full_model 3
# Fine grid, started from the Coarse grid solutions
bash ./sbatch/postdamage.sh --model full_model --grid-profile double_resolution --initial-guess-grid-profile baseline
bash ./check_all_pretech.sh --model full_model --grid-profile double_resolution postdamage baseline_xia
bash ./sbatch/predamage.sh --model full_model --grid-profile double_resolution --initial-guess-grid-profile baseline baseline_xia
bash ./check_all_pretech.sh --model full_model --grid-profile double_resolution predamage baseline_xia
~~~~

Source scripts: `python/models/full_model/full_model_solve_postdamage.py`, `python/models/full_model/full_model_solve_postdamage_sub.py` and `python/predamage.py` run the HJB solvers of [HJB Equations](03_hjb_equations.md) and [Computational method](04_computational_method.md). The solvers are `python/src/postsolver_new_rho1.py` for the value after the technology jump and `python/src/presolver_crs2_new_rho1.py` for the value before it. `python/models/full_model/full_model_solve_feymannkacs_prepare.py` computes the implied $\xi_a$.

(code-channels)=
## Channel decompositions

Tables 1 and 2 on [Uncertainty assessments](06_uncertainty_assessments.md) activate one uncertainty channel at a time. The code switches on the climate channel with `xi_a` at its calibrated value, the damage channel with `xi_d`, the productivity channel with `xi_k` and the technology channel with `xi_r` and `xi_t` together, and leaves all other penalties infinite, `xi_y` included. On the Coarse grid the modes `single_channel_*`, `double_channel_*` and `triple_channel_*` solve the coalitions of one, two and three channels for $\xi_m = .05$ (`more_aversion`) and $\xi_m = .1$ (`less_aversion`), starting from the post damage solutions of calibration cases `1` and `3` of the {ref}`full model <code-full-model>`, so run them after the Coarse grid calibration has finished. They give the initial guesses of the Fine grid modes `non_climate_channels` and `climate_channels`, which solve the seven coalitions without the climate channel and the seven coalitions with it other than all channels, each for both values of $\xi_m$. The rows without uncertainty and with all channels come from the {ref}`full model <code-full-model>` solutions, and the same solves give Table 31 of the paper.

~~~~bash
# Coarse grid coalitions, the initial guesses of the Fine grid
bash ./sbatch/postdamage_sub.sh --model full_model single_channel_more_aversion
bash ./sbatch/postdamage_sub.sh --model full_model single_channel_less_aversion
bash ./sbatch/postdamage_sub.sh --model full_model double_channel_more_aversion
bash ./sbatch/postdamage_sub.sh --model full_model double_channel_less_aversion
bash ./sbatch/postdamage_sub.sh --model full_model triple_channel_more_aversion
bash ./sbatch/postdamage_sub.sh --model full_model triple_channel_less_aversion
bash ./check_all_pretech.sh --model full_model postdamage single_channel
bash ./check_all_pretech.sh --model full_model postdamage double_channel
bash ./check_all_pretech.sh --model full_model postdamage triple_channel
bash ./sbatch/predamage.sh --model full_model single_channel_more_aversion
bash ./sbatch/predamage.sh --model full_model single_channel_less_aversion
bash ./sbatch/predamage.sh --model full_model double_channel_more_aversion
bash ./sbatch/predamage.sh --model full_model double_channel_less_aversion
bash ./sbatch/predamage.sh --model full_model triple_channel_more_aversion
bash ./sbatch/predamage.sh --model full_model triple_channel_less_aversion
bash ./check_all_pretech.sh --model full_model predamage single_channel
bash ./check_all_pretech.sh --model full_model predamage double_channel
bash ./check_all_pretech.sh --model full_model predamage triple_channel
# Fine grid coalitions
bash ./sbatch/postdamage.sh --model full_model --grid-profile double_resolution --initial-guess-grid-profile baseline non_climate_channels
bash ./sbatch/postdamage.sh --model full_model --grid-profile double_resolution --initial-guess-grid-profile baseline climate_channels
bash ./sbatch/postdamage_sub.sh --model full_model --grid-profile double_resolution non_climate_channels "0-19" i
bash ./sbatch/postdamage_sub.sh --model full_model --grid-profile double_resolution climate_channels "0-19" i
bash ./check_all_pretech.sh --model full_model --grid-profile double_resolution postdamage non_climate_channels
bash ./check_all_pretech.sh --model full_model --grid-profile double_resolution postdamage climate_channels
bash ./sbatch/predamage.sh --model full_model --grid-profile double_resolution --initial-guess-grid-profile baseline non_climate_channels
bash ./sbatch/predamage.sh --model full_model --grid-profile double_resolution --initial-guess-grid-profile baseline climate_channels
bash ./check_all_pretech.sh --model full_model --grid-profile double_resolution predamage non_climate_channels
bash ./check_all_pretech.sh --model full_model --grid-profile double_resolution predamage climate_channels
~~~~

Source scripts: `sbatch/full_model_channels.sh` defines the Fine grid coalitions, and the solves run the code of the {ref}`full model <code-full-model>`.

(code-tech-only)=
## Technology jump only model

The model of [A simplified model with only technology jumps](09_technology_only.md) has one known damage curve, no pre damage stage and no $\xi_a$ calibration. Its penalty `xi_t` takes the values of $\xi_m$, and all other penalties stay infinite. The Fine grid solves for $\xi_m = \infty$, $.1$ and $.05$ start from the Medium grid solutions. The values $.01$ to $.005$ of $\xi_m$ in Table 21 start from the converged Fine grid solution for $\xi_m = .05$, and the values $.02$ and $.015$ from the one for $\xi_m = .01$. `manifest_replication/master_HJB.sh` has no command for these two values, so the last solve follows the example in the header of `sbatch/postdamage_sub.sh`.

~~~~bash
# Medium grid, the initial guesses of the Fine grid
bash ./sbatch/postdamage.sh --model tech_only --grid-profile finer_grid
bash ./check_all_pretech.sh --model tech_only --grid-profile finer_grid postdamage one_jump_baseline
# Fine grid, baseline, less aversion and more aversion
bash ./sbatch/postdamage.sh --model tech_only --grid-profile double_resolution --initial-guess-grid-profile finer_grid
bash ./check_all_pretech.sh --model tech_only --grid-profile double_resolution postdamage one_jump_baseline
# Fine grid for the other values of Table 21
bash ./sbatch/postdamage_sub.sh --model tech_only --grid-profile double_resolution --xi-t-values 0.01,0.009,0.008,0.007,0.006,0.005 --warm-xi-t 0.05 0 i
bash ./check_all_pretech.sh --model tech_only --grid-profile double_resolution postdamage one_jump_baseline
bash ./sbatch/postdamage_sub.sh --model tech_only --grid-profile double_resolution --xi-t-values 0.02,0.015 --warm-xi-t 0.01 0 i
bash ./check_all_pretech.sh --model tech_only --grid-profile double_resolution postdamage one_jump_baseline
~~~~

Source scripts: `python/models/tech_only/tech_only_solve_postdamage.py` and `python/models/tech_only/tech_only_solve_postdamage_sub.py`, with the HJB solvers of the {ref}`full model <code-full-model>`.

(code-two-step)=
## Two step and partial technology models

Table 7 reports specifications i) to iv) of [A simplified model with only technology jumps](09_technology_only.md). Specifications i), ii) and iii) are the cases `double`, `baseline` and `double_reset_r` of the two step model of [Online Appendix O](13_online_o.md) (`--model 2stage_tech`), and specification iv) is the partial technology model (`--model partial_tech`). Both models keep the known damage curve of the technology jump only model and have no pre damage stage. The Coarse grid solves give the initial guesses of the Fine grid solves, and the two continuations of the two step model are those of `manifest_replication/master_HJB.sh`.

~~~~bash
# Coarse grid
bash ./sbatch/postdamage.sh --model 2stage_tech
bash ./check_all_pretech.sh --model 2stage_tech postdamage two_stage_technology
bash ./sbatch/postdamage.sh --model partial_tech
bash ./check_all_pretech.sh --model partial_tech postdamage one_partial_jump
# Fine grid, partial technology model
bash ./sbatch/postdamage.sh --model partial_tech --grid-profile double_resolution --initial-guess-grid-profile baseline
bash ./check_all_pretech.sh --model partial_tech --grid-profile double_resolution postdamage one_partial_jump
bash ./sbatch/postdamage_sub.sh --model partial_tech --grid-profile double_resolution 0 i
bash ./check_all_pretech.sh --model partial_tech --grid-profile double_resolution postdamage one_partial_jump
# Fine grid, two step model
bash ./sbatch/postdamage.sh --model 2stage_tech --grid-profile double_resolution --initial-guess-grid-profile baseline --experiment-cases double,baseline,double_reset_r
bash ./check_all_pretech.sh --model 2stage_tech --grid-profile double_resolution postdamage two_stage_technology
bash ./sbatch/postdamage_sub.sh --model 2stage_tech --grid-profile double_resolution --experiment-cases baseline,double_reset_r --xi-t-values 0.1,100000. --warm-xi-t 0.05 all
bash ./check_all_pretech.sh --model 2stage_tech --grid-profile double_resolution postdamage two_stage_technology
bash ./sbatch/postdamage_sub.sh --model 2stage_tech --grid-profile double_resolution --experiment-cases double --xi-t-values 100000.,0.1,0.05 --warm-experiment-case double_reset_r all
bash ./check_all_pretech.sh --model 2stage_tech --grid-profile double_resolution postdamage two_stage_technology
~~~~

Source scripts: `python/models/two_stage_tech/two_stage_tech_solve_postdamage.py`, `python/models/two_stage_tech/two_stage_tech_solve_postdamage_sub.py` and `python/models/two_stage_tech/two_stage_tech_hjb.py` for the two step model, and `python/models/partial_tech/partial_tech_solve_postdamage.py`, `python/models/partial_tech/partial_tech_solve_postdamage_sub.py` and `python/models/partial_tech/partial_tech_hjb.py` for the partial technology model.

(code-sensitivity)=
## Sensitivity analyses

The sensitivity analyses of Appendix F of the paper, [Online Appendix M](11_online_m.md) and [Online Appendix N](12_online_n.md) solve the full model again on the Coarse grid. Each profile of `sbatch/appendix_sensitivity.sh` has its own rows of parameter values and keeps the other parameters at their baseline values:

| Profile | Rows | Paper tables |
|---|---|---|
| `delta` | $\delta = .015, .02$ | Table 18 |
| `rho` | $\rho = .75, 1.33$ | Tables 19, 20 and 35 to 37 |
| `phi0` | $\phi_0 = .3, .1$ | Table 22 |
| `rd` | $\psi_0 \in \{.07, .11, .15\}$ and $\chi \in \{.0014, .0009, .0007\}$ | Table 23 |
| `phi0_rd` | the `rd` rows for $\phi_0 \in \{.1, .3, .5\}$ | Tables 38 to 40 |

Every row keeps the three settings $\xi_m = \infty$, $.1$ and $.05$ with the final $\xi_a$ values of the {ref}`full model <code-full-model>` (the mode `baseline_xia`) and no new calibration. The post damage solves start from the Coarse grid solutions of the full model, which also give the baseline values $\delta = .01$, $\rho = 1$ and $\phi_0 = .5$ in Tables 18 and 22 of the paper and Tables 19, 20 and 35 to 37. The commands for the profile `rho` are:

~~~~bash
bash ./sbatch/appendix_sensitivity.sh rho postdamage_sub -- baseline_xia
bash ./check_all_pretech.sh --model full_model --sensitivity-profile rho postdamage baseline_xia
bash ./sbatch/appendix_sensitivity.sh rho predamage -- baseline_xia
bash ./check_all_pretech.sh --model full_model --sensitivity-profile rho predamage baseline_xia
bash ./sbatch/appendix_sensitivity.sh rho prepare -- baseline_xia
~~~~

The other profiles run the same stages. `manifest_replication/master_sensitivity_no_calibration.sh` lists them all, with the profiles `rd` and `phi0_rd` submitted in batches of rows (`--rows`) and followed by the stages `simulate`, one row at a time (`--row`), and `plot`. `python3 python/make_sensitivity_tables.py` writes the tables of the profile `phi0_rd`, and with `--profile rd --table23-only` the table of the profile `rd`. The Coarse grid registration `bash ./sbatch/update_results.sh --model full_model --no-compile` then writes the tables of the profiles `delta`, `rho` and `phi0`. It reads the tables of the profiles `rd` and `phi0_rd`, the logs of the Coarse grid solves and prepare jobs of the {ref}`full model <code-full-model>` and the solutions they saved, and the logs of the commands below, which run on the Coarse grid after the Coarse grid paths of {ref}`grid comparisons <code-grid-comparisons>` have finished. The stochastic path simulation among them waits while the queue is full, so run it in a persistent shell. The registration also copies the Coarse grid versions of Figures 3 and 4 and Tables 1, 2, 3, 5, 24 to 26 and 31 to `results_in_paper/`, so run it before the Fine grid commands of the other pages, as [Online Appendix M](11_online_m.md) explains.

~~~~bash
bash ./sbatch/feymannkacs_plot_composite.sh --model full_model Technology
bash ./sbatch/stochastic_trajectories_simulate.sh
bash ./sbatch/stochastic_trajectories_plot.sh
bash ./sbatch/zeroshock_trajectories_simulate.sh true false false
bash ./sbatch/zeroshock_trajectories_plot.sh
~~~~

Source scripts: `sbatch/appendix_sensitivity.sh` and `sbatch/appendix_sensitivity_overrides.sh`, with the code of the {ref}`full model <code-full-model>`, which calls `python/src/postsolver_new.py` and `python/src/presolver_crs2_new.py` for $\rho \ne 1$.

(code-grid-comparisons)=
## Grid comparisons

Tables 27 to 30 on [Computational method](04_computational_method.md) compare the Coarse and Fine grids. Their collectors also read Medium grid runs, so the commands below solve the full model on the Medium grid and the technology jump only model on the Coarse grid, and run the Feynman Kac steps on the Coarse and Medium grids. The Medium grid solves of the technology jump only model come from {ref}`Technology jump only model <code-tech-only>`, and the Fine grid runs from the reproduction commands of [Uncertainty assessments](06_uncertainty_assessments.md) and [A simplified model with only technology jumps](09_technology_only.md).

~~~~bash
# Full model on the Medium grid
bash ./sbatch/postdamage.sh --model full_model --grid-profile finer_grid
bash ./check_all_pretech.sh --model full_model --grid-profile finer_grid postdamage baseline_xia
bash ./sbatch/predamage.sh --model full_model --grid-profile finer_grid baseline_xia
bash ./check_all_pretech.sh --model full_model --grid-profile finer_grid predamage baseline_xia
bash ./sbatch/feymannkacs_prepare.sh --model full_model --grid-profile finer_grid baseline_xia
bash ./sbatch/feymannkacs_simulate.sh --model full_model --grid-profile finer_grid Technology
# Full model paths on the Coarse grid
bash ./sbatch/feymannkacs_prepare.sh --model full_model baseline_xia
bash ./sbatch/feymannkacs_simulate.sh --model full_model Technology
# Technology jump only model on the Coarse grid
bash ./sbatch/postdamage.sh --model tech_only
bash ./check_all_pretech.sh --model tech_only postdamage one_jump_baseline
bash ./sbatch/feymannkacs_prepare.sh --model tech_only
bash ./sbatch/feymannkacs_simulate.sh --model tech_only
bash ./sbatch/feymannkacs_plot_composite.sh --model tech_only
# Technology jump only model on the Medium grid
bash ./sbatch/feymannkacs_prepare.sh --model tech_only --grid-profile finer_grid
bash ./sbatch/feymannkacs_simulate.sh --model tech_only --grid-profile finer_grid
bash ./sbatch/feymannkacs_plot_composite.sh --model tech_only --grid-profile finer_grid
~~~~

`sbatch/diagnostics/collect_full_model_fk_terminal.sh` reads the simulated paths of the full model from a fixed default directory, so give it `--scratch /scratch/<user>/full_model`. Table 30 also reads the derivative audits stored in the repository under `output/diagnostics/full_model_fk_derivative/double_resolution/`.

Source scripts: `python/models/full_model/full_model_solve_feymannkacs_simulate.py` and `python/models/tech_only/tech_only_solve_feymannkacs_simulate.py` for the paths, and the collectors listed on [Computational method](04_computational_method.md).

(code-paper-items)=
## Paper figures and tables

Each row gives the page that shows a figure or table, the commands that produce it after the solves it names, the file they write and the code that computes it. In the output paths `<dataset>` is the directory of the model and grid that the commands select, as listed in {ref}`Grids <code-grids>`, and the Coarse grid directory of the full model for commands without `--model` and `--grid-profile`. The tables that appear only in the PDF of the paper close the list.

| Paper item | Page | Commands | Output | Code |
|---|---|---|---|---|
| Figure 1 | [Example economy](01_example_economy.md) | `bash ./sbatch/baseline_plot.sh` | `Climate_Sensitivity.png` in `output/figures/<dataset>/baseline_plot/` | `python/frequency_plot.py` |
| Figure 2 | [Example economy](01_example_economy.md) | As Figure 1 | `Temperature Anomaly.png`, same directory | `python/frequency_plot.py` |
| Figure 3 | [First-order conditions and stochastic simulations](05_first_order_conditions.md) | After {ref}`full model <code-full-model>`: `bash ./sbatch/stochastic_trajectories_simulate.sh --grid-profile double_resolution`, then `bash ./sbatch/stochastic_trajectories_plot.sh --grid-profile double_resolution` | `rd_investment_paths.png` and `emissions_paths.png` under `output/figures/<dataset>/stochastic_trajectories_plot/` | `python/stochastic_trajectories_simulate.py`, `python/stochastic_trajectories_plot.py` |
| Figure 4 | [Uncertainty assessments](06_uncertainty_assessments.md) | After {ref}`full model <code-full-model>`: `bash ./sbatch/zeroshock_trajectories_simulate.sh --grid-profile double_resolution true false false`, then `bash ./sbatch/zeroshock_trajectories_plot.sh --grid-profile double_resolution` | `climate_model_relative_weights_year-0.png` under `output/figures/<dataset>/zeroshock_trajectories_plot/` | `python/zeroshock_trajectories_simulate.py`, `python/zeroshock_trajectories_plot.py` |
| Figure 5 | [Uncertainty assessments](06_uncertainty_assessments.md) | After {ref}`full model <code-full-model>`: `bash ./sbatch/feymannkacs_prepare.sh --model full_model --grid-profile double_resolution baseline_xia`, `bash ./sbatch/feymannkacs_simulate.sh --model full_model --grid-profile double_resolution Technology`, then `bash ./sbatch/feymannkacs_plot_composite.sh --model full_model --grid-profile double_resolution Technology` | `all_channel_on_0.1lambda_jacobian_distorted_CompositeTechnology0.083_Discount_nodeltadt_tech_Processs_dt.png` and `all_channel_on_0.1lambda_jacobian_distorted_CompositeTechnology0.083_Discount_nodeltadt_damage_Processs_dt.png` in `output/figures/<dataset>/feymannkacs_plot_composite/` | `python/models/full_model/full_model_solve_feymannkacs_simulate.py`, `python/models/full_model/full_model_solve_feymannkacs_plot_composite.py` |
| Figure 6 | [Uncertainty assessments](06_uncertainty_assessments.md) | As Figure 5 | `all_channel_on_0.1lambda_jacobian_distorted_Technologydamage_curve_year_splines_0_allxi.png`, same directory | As Figure 5 |
| Figure 7 | [Acting now or waiting?](07_acting_now_or_waiting.md) | `bash ./sbatch/experiments/no_jump_temperature/submit_damage_density_panels.sh --ratio`, then `bash ./sbatch/experiments/no_jump_temperature/submit_damage_density_panels.sh --respective-states` | `emissions_respective_states.png` and `rd_respective_states.png` in `output/experiments/no_jump_temperature/figure7_panels/respective_states/no_dots/` | `python/experiments/no_jump_temperature/figure7_panels/respective_states.py` |
| Figure 8 | [A simplified model with only technology jumps](09_technology_only.md) | As Figure 1 | `Temperature Anomaly weighted.png`, same directory as Figure 1 | `python/frequency_plot.py` |
| Figure 9 | [A simplified model with only technology jumps](09_technology_only.md) | After {ref}`technology jump only model <code-tech-only>`: `bash ./sbatch/feymannkacs_prepare.sh --model tech_only --grid-profile double_resolution --xi-t-values 100000.,0.1,0.05,0.02,0.015,0.01,0.009,0.008,0.007,0.006,0.005`, `bash ./sbatch/feymannkacs_simulate.sh --model tech_only --grid-profile double_resolution`, then `bash ./sbatch/feymannkacs_plot_composite.sh --model tech_only --grid-profile double_resolution` | `tech_only_lambda_jacobian_distorted_allxi_Technology_technology_density.png` in `output/figures/<dataset>/feymannkacs_plot_composite/` | `python/models/tech_only/tech_only_solve_feymannkacs_simulate.py`, `python/models/tech_only/tech_only_solve_feymannkacs_plot_composite.py` |
| Figure 10 | [A simplified model with only technology jumps](09_technology_only.md) | As Figure 9 | `tech_only_lambda_jacobian_distorted_allxi_Technology_flow_ii.png` and `tech_only_lambda_jacobian_distorted_allxi_Technology_flow_iii.png`, same directory | `python/models/tech_only/tech_only_solve_feymannkacs_plot_composite.py` |
| Figure 11 | [A simplified model with only technology jumps](09_technology_only.md) | As Table 21, then `bash ./sbatch/tech_only_nonmonotonicity_plot.sh --grid-profile double_resolution` | `rd_investment_vs_inverse_xi.png` in `output/figures/tech_only_nonmonotonicity/` | `python/tech_only_nonmonotonicity_plot.py` |
| Figure 12 | [Acting now or waiting?](07_acting_now_or_waiting.md) | `bash ./sbatch/experiments/no_jump_temperature/submit_damage_density_panels.sh --ratio` | `emissions_state_neutrality.png`, `emissions_state_less_aversion.png`, `rd_state_neutrality.png` and `rd_state_less_aversion.png` in `output/experiments/no_jump_temperature/figure7_panels/ratio/no_dots/` | `python/experiments/no_jump_temperature/figure7_panels/export_ratio.py` |
| Figure 13 | [Comparison to a real options formulation](10_real_options.md) | `bash ./sbatch/appendix_illustrations.sh` | `model1_derivative.png` and `model3_derivative.png` in `output/figures/<dataset>/appendix_illustrations/` | `python/appendix_illustrations.py` |
| Figure 14 | [Comparison to a real options formulation](10_real_options.md) | As Figure 13 | `threshold_plot.png`, same directory | `python/appendix_illustrations.py` |
| Figure 15 | [Comparison to a real options formulation](10_real_options.md) | As Figure 13 | `model1_distortion.png` and `model3_distortion.png`, same directory | `python/appendix_illustrations.py` |
| Figure 16 | [Online Appendix P](14_online_p.md) | As Figure 13 | `d_alpha.png`, same directory as Figure 13 | `python/appendix_illustrations.py` |
| Figure 17 | [Online Appendix P](14_online_p.md) | As Figure 13 | `intensity_d_1_sensitivity.png`, same directory as Figure 13 | `python/appendix_illustrations.py` |
| Figure 18 | [Online Appendix P](14_online_p.md) | As Figure 13 | `density_d_1_sensitivity.png`, same directory as Figure 13 | `python/appendix_illustrations.py` |
| Table 1 | [Uncertainty assessments](06_uncertainty_assessments.md) | After {ref}`full model <code-full-model>` and {ref}`channel decompositions <code-channels>`: `bash ./sbatch/zeroshock_trajectories_simulate.sh --grid-profile double_resolution true false false`, `bash ./sbatch/zeroshock_trajectories_simulate.sh --grid-profile double_resolution non_climate_channels`, `bash ./sbatch/zeroshock_trajectories_simulate.sh --grid-profile double_resolution climate_channels`, then `bash ./sbatch/datevaluereport_table.sh --grid-profile double_resolution` | `matrix_scrd_latex.tex` in `output/tables/<dataset>/datevaluereport_table/` | `python/zeroshock_trajectories_simulate.py`, `python/datevaluereport_table.py` |
| Table 2 | [Uncertainty assessments](06_uncertainty_assessments.md) | As Table 1 | `matrix_scgw_latex.tex`, same directory | As Table 1 |
| Table 3 | [Uncertainty assessments](06_uncertainty_assessments.md) | After {ref}`full model <code-full-model>`: `bash ./sbatch/feymannkacs_prepare.sh --model full_model --grid-profile double_resolution baseline_xia`, then `bash ./sbatch/update_results.sh --model full_model --grid-profile double_resolution --full-model-drift-only --no-compile` | `h_values_initial.tex` in `output/tables/<dataset>/feymannkacs_prepare/` | `python/models/full_model/full_model_solve_feymannkacs_prepare.py`, `python/update_results.py` |
| Table 4 | [Acting now or waiting?](07_acting_now_or_waiting.md) | `bash ./sbatch/update_results.sh --model full_model --grid-profile double_resolution --table4-only --no-compile` | `paper_pre_post.tex` in `output/experiments/no_jump_temperature/figure7_panels/ratio/` | `python/experiments/no_jump_temperature/figure7_panels/table.py` |
| Table 5 | [Marginal valuations as asset prices](08_marginal_valuations.md) | As Figure 5, then `bash ./sbatch/update_results.sh --model full_model --grid-profile double_resolution --full-model-composite-only` | `tech_flow_terms_split.tex` in `output/tables/<dataset>/feymannkacs_plot_composite/` | `python/models/full_model/full_model_solve_feymannkacs_plot_composite.py`, `python/update_results.py` |
| Table 6 | [A simplified model with only technology jumps](09_technology_only.md) | As Figure 9, then `bash ./sbatch/update_results.sh --model tech_only --grid-profile double_resolution --main-only --no-compile` | `only_tech_jump.tex` in `output/tables/<dataset>/feymannkacs_plot_composite/` | `python/models/tech_only/tech_only_solve_feymannkacs_prepare.py`, `python/models/tech_only/tech_only_solve_feymannkacs_plot_composite.py`, `python/update_results.py` |
| Table 7 | [A simplified model with only technology jumps](09_technology_only.md) | After {ref}`two step and partial technology models <code-two-step>`: `bash ./sbatch/feymannkacs_prepare.sh --model partial_tech --grid-profile double_resolution`, `bash ./sbatch/stochastic_trajectories_2stage_prepare.sh --grid-profile double_resolution --experiment-cases double,baseline,double_reset_r`, then `bash ./sbatch/update_results.sh --model 2stage_tech --grid-profile double_resolution --main-only --no-compile` | `two_stage_technology.tex` in `output/tables/<dataset>/stochastic_trajectories_2stage_prepare/` | `python/models/two_stage_tech/two_stage_tech_stochastic_trajectories_prepare.py`, `python/models/partial_tech/partial_tech_solve_feymannkacs_prepare.py`, `python/update_results.py` |
| Table 19 | [Online Appendix M](11_online_m.md) | As Table 35 | `IES_initial_investment.tex`, same directory as Table 35 | As Table 35 |
| Table 20 | [Online Appendix M](11_online_m.md) | As Table 35 | `IES_social_valuations_general_rho_scaling.tex`, same directory as Table 35 | As Table 35 |
| Table 21 | [A simplified model with only technology jumps](09_technology_only.md) | As Table 6 | `only_tech_nonmonotonicity.tex` in `output/tables/<dataset>/feymannkacs_prepare/` | `python/models/tech_only/tech_only_solve_feymannkacs_prepare.py`, `python/update_results.py` |
| Table 24 | [Computational method](04_computational_method.md) | After {ref}`full model <code-full-model>`: `bash ./sbatch/update_results.sh --model full_model --grid-profile double_resolution --full-model-numerics-only --no-compile` | `numerical_discretization.tex` in `output/tables/<dataset>/` | `python/update_results.py` |
| Table 25 | [Computational method](04_computational_method.md) | As Table 24 | `numerical_convergence_criteria.tex`, same directory | `python/update_results.py` |
| Table 26 | [Computational method](04_computational_method.md) | As Table 24 | `convergence_diagnostics.tex`, same directory | `python/update_results.py` |
| Table 27 | [Computational method](04_computational_method.md) | As Table 24 | `grid_specifications.tex` in `output/tables/<dataset>/grid_refinement/` | `python/update_results.py` |
| Table 28 | [Computational method](04_computational_method.md) | After {ref}`grid comparisons <code-grid-comparisons>` and the prepare command of Figure 5: `bash ./sbatch/diagnostics/collect_full_model_grid_refinement.sh --paper-tables-only` | `grid_refinement_comparison.tex`, same directory as Table 27 | `python/diagnostics/collect_grid_refinement.py` |
| Table 29 | [Computational method](04_computational_method.md) | After {ref}`grid comparisons <code-grid-comparisons>` and the commands of Figures 5 and 9: `bash ./sbatch/diagnostics/collect_full_model_fk_terminal.sh --scratch /scratch/<user>/full_model`, `bash ./sbatch/diagnostics/collect_tech_only_grid_refinement.sh --comparison-grid finer_grid`, `bash ./sbatch/diagnostics/collect_tech_only_grid_refinement.sh --comparison-grid double_resolution`, then `bash ./sbatch/diagnostics/collect_full_model_fk_terminal.sh --paper-comparison-only` | `indirect_direct_comparison.tex`, same directory as Table 27 | `python/diagnostics/collect_full_model_fk_terminal.py`, `python/diagnostics/collect_tech_only_grid_refinement.py` |
| Table 30 | [Computational method](04_computational_method.md) | As Table 29 | `error_summary.tex`, same directory | `python/diagnostics/collect_full_model_fk_terminal.py` |
| Table 32 | [Acting now or waiting?](07_acting_now_or_waiting.md) | As Table 4 | `paper_two_state_pre_post.tex`, same directory as Table 4 | `python/experiments/no_jump_temperature/figure7_panels/table.py` |
| Table 35 | [Online Appendix M](11_online_m.md) | After all profiles of {ref}`sensitivity analyses <code-sensitivity>`, `python3 python/make_sensitivity_tables.py --profile rd --table23-only`, the command of Table 38 and all other Coarse grid results of the full model: `bash ./sbatch/update_results.sh --model full_model --no-compile` | `IES_neutrality_general_rho_scaling.tex` in `output/tables/sensitivity_<dataset>/rho/` | `python/models/full_model/full_model_solve_feymannkacs_prepare.py`, `python/update_results.py` |
| Table 36 | [Online Appendix M](11_online_m.md) | As Table 35 | `IES_less_aversion_general_rho_scaling.tex`, same directory | As Table 35 |
| Table 37 | [Online Appendix M](11_online_m.md) | As Table 35 | `IES_more_aversion_general_rho_scaling.tex`, same directory | As Table 35 |
| Table 38 | [Online Appendix N](12_online_n.md) | After the profile `phi0_rd` of {ref}`sensitivity analyses <code-sensitivity>`: `python3 python/make_sensitivity_tables.py` | `phi0_rd_xi_infinity.tex` in `output/tables/sensitivity_<dataset>/phi0_rd/` | `python/make_sensitivity_tables.py` |
| Table 39 | [Online Appendix N](12_online_n.md) | As Table 38 | `phi0_rd_xi_0p1.tex`, same directory | `python/make_sensitivity_tables.py` |
| Table 40 | [Online Appendix N](12_online_n.md) | As Table 38 | `phi0_rd_xi_0p05.tex`, same directory | `python/make_sensitivity_tables.py` |
| Tables 8 to 16 | PDF only | None, these tables list model inputs | | |
| Table 17 | PDF only | After {ref}`full model <code-full-model>`: `bash ./sbatch/stochastic_trajectories_worst_simulate.sh`, then `bash ./sbatch/stochastic_trajectories_worst_plot.sh` | `risk_free_rates.tex` under `output/tables/<dataset>/appendix-e7-risk-free-rate/` | `python/stochastic_trajectories_worst_simulate.py`, `python/stochastic_trajectories_worst_plot.py` |
| Tables 18, 22, 23 | PDF only | As Table 35 | under `output/tables/sensitivity_<dataset>/` | `python/make_sensitivity_tables.py`, `python/update_results.py` |
| Table 31 | PDF only | As Table 1 | `shapley_decompositions.tex`, same directory as Table 1 | `python/datevaluereport_table.py` |
| Table 33 | PDF only | After the `stochastic_trajectories_2stage_prepare.sh` command of Table 7: `bash ./sbatch/stochastic_trajectories_2stage_simulate.sh --grid-profile double_resolution double`, the same with `baseline` and with `double_reset_r`, then `bash ./sbatch/stochastic_trajectories_2stage_plot.sh --grid-profile double_resolution` | `two_stage_first_jump_investment_quantiles.tex` in `output/tables/<dataset>/stochastic_trajectories_2stage_plot/` | `python/models/two_stage_tech/two_stage_tech_stochastic_trajectories_simulate.py`, `python/models/two_stage_tech/two_stage_tech_stochastic_trajectories_plot.py` |
| Table 34 | PDF only | After the `partial_tech` prepare command of Table 7: `bash ./sbatch/update_results.sh --grid-profile double_resolution --partial-tech-table-only` | `partial_tech_paper_values.tex` in `output/tables/<dataset>/feymannkacs_prepare/` of the partial technology model | `python/models/partial_tech/partial_tech_table.py` |

(code-notation)=
## Paper notation in the code

The code and its outputs use these names for the states, parameters and solution fields of the paper.

| Code | Paper | Note |
|---|---|---|
| `logK`, `Y`, `logR` | $\widehat K_t$, $Y_t$, $\widehat R_t$ | the code orders the state as `(logK, Y, logR)`, the paper as $X_t = [\widehat K_t, \widehat R_t, Y_t]'$ |
| `xi_a` | $\xi_a$ | `100000.`, `0.0034917` and `0.0017469` for $\xi_m = \infty$, $.1$ and $.05$, printed as $\infty$, .00349 and .00175 in Table 8 of the paper |
| `xi_k`, `xi_r` | $\xi_m$ | penalties on the Brownian shocks to capital and to the knowledge stock |
| `xi_d`, `xi_t` | $\xi_m$ | penalties on the damage curvature jumps $\ell = 1, \ldots, L-1$ and on the technology jump $\ell = L$ |
| `xi_y` | $\xi_m$ | penalty on the Brownian shock to temperature, equal to $\xi_m$ only in calibration case `1` and infinite in all reported results |
| `100000.` | $\infty$ | the value of an infinite penalty |
| `chi_inv` | $1/\chi$ | the technology jump intensity is $\mathcal{J}^L(R_t) = \chi R_t$ |
| `lambda_3`, `y_hat` | $\lambda_3$, $\hat y$ | `0.1667` and `2.0` in the models with only technology jumps, the arithmetic average of the $\lambda_3(\ell)$'s and $\hat y = 2$ of Figure 8 |
| `h_k`, `h_r` | entries of $H_t^*$ | drift distortions for the capital stock and the knowledge stock in the HJB solutions, reported at the initial state in Table 3 |
| `g_damage`, `g_tech` | $G_t^{\ell *}$ for $\ell = 1, \ldots, L-1$, and $G_t^{L *}$ | distortions of the damage and technology jump intensities in the HJB solutions |
| `scrd` | $\frac{C_t}{\delta} \frac{\partial V}{\partial \hat r}(X_t)$ | field of the zero shock paths written by `python/zeroshock_trajectories_simulate.py`, and SVRD is `scrd` divided by $N_t R_t$ |
| `scgw` | $-\frac{C_t}{\delta} \frac{\partial V}{\partial y}(X_t)$ | field of the same paths, and SCGW is `scgw` divided by $N_t$ |
