# N. Sensitivity analysis details: ($\phi_0, \psi_0, \chi$)

From Appendix F of the paper:

To reduce the extensive computational cost of calculating the sensitivity analysis outcomes, we use a coarse grid resolution rather than the fine grid resolution applied for our main analysis. As shown in [Appendix G](04_computational_method.md), this grid choice has no impact on the qualitative implications of the model solutions, and only minor quantitative impacts that are most noticeable in the more risk aversion case.

We find that decreasing the value of $\phi_0$ leads to i) substantially less R&D as a fraction of output, ii) a more modest but notable proportional reduction in emissions, and iii) the same qualitative response to model uncertainty implications. These responses reflect the reduced output loss induced by a reduction in emissions that would occur for lower values of $\phi_0$.

Online Appendix N shows the numerical outcomes for changing the value of $\phi_0$ for different choices of the R&D knowledge stock related parameters, namely $\chi$ and $\psi_0$. Importantly, the qualitative implications for changing $\phi_0$ and for the impact of uncertainty aversion persist in these alternative parameter specifications.

<iframe
  id="phi0-rd-interactive"
  src="../_static/phi0_rd_interactive.html"
  title="Outcomes of Tables 38 to 40 across uncertainty aversion for each value of phi_0, given psi_0 and chi"
  width="100%"
  height="520"
  scrolling="no"
  style="display:block; margin:0 auto; border:none;"
></iframe>

The figure shows the numbers of Tables 38 to 40. Each line is one value of $\phi_0$ across the three settings of $\xi_m$. The menu selects the outcome and the buttons select $\psi_0$ and $\chi$. The full tables are in the panels below.

(table-38)=

````{dropdown} Table 38 (ξ<sub>m</sub> = ∞)
```{include} ../_static/table/table38_phi0_psi0_chi_xi_inf.md
```
````

(table-39)=

````{dropdown} Table 39 (ξ<sub>m</sub> = .1)
```{include} ../_static/table/table39_phi0_psi0_chi_xi_01.md
```
````

(table-40)=

````{dropdown} Table 40 (ξ<sub>m</sub> = .05)
```{include} ../_static/table/table40_phi0_psi0_chi_xi_005.md
```
````

::::{hidden}
## Reproducing the tables

To reproduce Tables 38, 39, and 40, run the command below from the root of the code repository after the `phi0_rd` block of `manifest_replication/master_sensitivity_no_calibration.sh`, described in {ref}`Sensitivity analyses <code-sensitivity>`, has finished, including its prepare, simulate, and plot stages.

~~~~bash
python3 python/make_sensitivity_tables.py
~~~~

After the run finishes, you should have output files named `phi0_rd_xi_infinity.tex` (Table 38), `phi0_rd_xi_0p1.tex` (Table 39), and `phi0_rd_xi_0p05.tex` (Table 40) under `output/tables/sensitivity_<dataset>/phi0_rd/`, where `<dataset>` is the Coarse grid directory of the full model, as listed in {ref}`Grids <code-grids>`. The script joins the emissions and R&D investment printed by the prepare jobs with the technology first probability and the conditional median year printed by the plot jobs. The command on [Online Appendix M](11_online_m.md) copies these files to `results_in_paper/` as `Table38_phi0_rd_xi_infinity.tex`, `Table39_phi0_rd_xi_0p1.tex`, and `Table40_phi0_rd_xi_0p05.tex`.

Source scripts:
* `python/make_sensitivity_tables.py`
* `python/models/full_model/full_model_solve_feymannkacs_prepare.py`
* `python/models/full_model/full_model_solve_feymannkacs_plot_composite.py`
::::
