# M. Sensitivity analysis details: IES

From Appendix B of the paper:

We adopt a recursive representation of preferences in continuous time for the planner extended to allow $\rho \ne 1.$ We start by forming the continuation value for each calendar date as follows:

$$
\exp(V_t) = \left( \delta \int_0^\infty \exp( - \delta \tau)  \left(C_{t+\tau}/N_{t+\tau} \right)^{1-\rho} d \tau
\right)^{\frac 1 {1-\rho}}
$$

where $\exp(V)$ gives an ordinally equivalent representation of preferences since $\exp(\cdot)$ is an increasing function.

From Appendix F of the paper:

To reduce the extensive computational cost of calculating the sensitivity analysis outcomes, we use a coarse grid resolution rather than the fine grid resolution applied for our main analysis. As shown in [Appendix G](04_computational_method.md), this grid choice has no impact on the qualitative implications of the model solutions, and only minor quantitative impacts that are most noticeable in the more risk aversion case.

{ref}`Table 19 <table-19>` shows the results for two alternative specifications of the IES that differ from unity: higher ($\rho = 3/4$) and lower ($\rho = 4/3$) IES scenarios. As expected from growth models, investments in both types of capital relative to output are higher when the elasticity is greater ($\rho$ is smaller). Conversely, emissions decrease when the elasticity is greater ($\rho$ is smaller).

(table-19)=

```{include} ../_static/table/table19_ies_investment.md
```

{ref}`Table 20 <table-20>` shows the social value of the R&D stock and the social cost of global warming for $\rho = 3/4$, $\rho = 1$, and $\rho = 4/3.$ The magnitude of the social valuations of the corresponding state variables increases when the elasticity is greater ($\rho$ is smaller).

(table-20)=

```{include} ../_static/table/table20_ies_valuations.md
```

(table-35)=

```{include} ../_static/table/table35_ies_xi_inf.md
```

(table-36)=

```{include} ../_static/table/table36_ies_xi_01.md
```

(table-37)=

```{include} ../_static/table/table37_ies_xi_005.md
```

::::{hidden}
## Reproducing the tables

To reproduce Tables 19, 20, 35, 36, and 37, run the script below from the root of the code repository after the `rho` block of `manifest_replication/master_sensitivity_no_calibration.sh`, described in {ref}`Sensitivity analyses <code-sensitivity>`, has finished through its prepare stage. The script formats these tables together with all other Coarse grid full model results, so those results, including the tables of [Online Appendix N](12_online_n.md), must exist as well. It also copies the Coarse grid versions of Figures 3 and 4 and Tables 1, 2, 3, 5, 24 to 26 and 31 to `results_in_paper/`, so run it before the Fine grid commands of the other pages, or run their `sbatch/update_results.sh` commands again after it. Those commands copy the Fine grid versions of Tables 3, 5 and 24 to 26 there, but not those of Figures 3 and 4 and Tables 1, 2 and 31, which stay in the output files listed in {ref}`Paper figures and tables <code-paper-items>`.

~~~~bash
bash ./sbatch/update_results.sh --model full_model --no-compile
~~~~

After the run finishes, you should have output files named `IES_initial_investment.tex` (Table 19), `IES_social_valuations_general_rho_scaling.tex` (Table 20), `IES_neutrality_general_rho_scaling.tex` (Table 35), `IES_less_aversion_general_rho_scaling.tex` (Table 36), and `IES_more_aversion_general_rho_scaling.tex` (Table 37) under `output/tables/sensitivity_<dataset>/rho/`, where `<dataset>` is the Coarse grid directory of the full model, as listed in {ref}`Grids <code-grids>`. Copies of these files go to `results_in_paper/` as `Table19_IES_initial_investment.tex`, `Table20_IES_social_valuations_general_rho_scaling.tex`, `Table35_IES_neutrality_general_rho_scaling.tex`, `Table36_IES_less_aversion_general_rho_scaling.tex`, and `Table37_IES_more_aversion_general_rho_scaling.tex`. The script reads the values from the prepare job outputs under `job-outs/sensitivity_<dataset>/rho/feymannkacs_prepare/lambda_jacobian_distorted/scheme_direct_HJB_direct/` for $\rho = .75$ and $1.33$ and under `job-outs/<dataset>/feymannkacs_prepare/lambda_jacobian_distorted/scheme_direct_HJB_direct/` for $\rho = 1$.

Source scripts:
* `sbatch/update_results.sh`
* `python/update_results.py`
* `python/models/full_model/full_model_solve_feymannkacs_prepare.py`
::::
