# A simplified model with only technology jumps

As a simplified illustration of why the social planner's R&D investment response is so sensitive to uncertainty concerns, we consider a version of our model focused solely on the potential technology discovery. In this simplified setting, we assume that there is a single known damage curve, i.e. there is no damage information event. The constructed damage curve instead assumes that the additional curvature begins at a temperature anomaly of $2^{\circ} C$ with a value of $\lambda_3$ being the baseline average across the set of possible $\lambda_3(\ell)$'s. The resulting damage function is shown in {ref}`Figure 8 <fig-8>`. We also close down uncertainty aversion related to the diffusion contribution and the alternative climate models to further enhance the focus on the prospective technology discovery. We consider two variations of our previous computations. First, we entertain considerably larger specifications of uncertainty aversion (smaller values of $\xi_m$). Second, we allow for the technology discovery to occur only partially or in two stages instead of one.

(fig-8)=

<div id="fig-8" style="display:flex; justify-content:center; align-items:center;">
  <img src="../_static/paper/Figure8_Temperature_Anomaly_weighted.png"
       alt="Plot showing the single damage function in the simplified setting with additional curvature set at the average value and starting at 2.0 degrees Celsius"
       style="width:450px; max-width:100%; height:auto;">
</div>

Figure 8: The consumption impact of the single damage function constructed by imposing ${\hat y} = 2$ and the arithmetic average of the $\lambda_3(\ell)$'s. Formally, the vertical axis measures $\exp(-{\hat n})$. The damages range from no impact on consumption $(1.00)$ for a $0.0^{\circ}C$ temperature anomaly to a nearly 20% reduction in consumption $(\sim .80)$ for a $3.5^{\circ}C$ temperature anomaly.

(enhanced-aversion)=
## Enhanced uncertainty aversion

{ref}`Figure 9 <fig-9>` gives the baseline and two uncertainty-adjusted densities for the timing of the technology jump. This figure shows the delay in the prospective success under the uncertainty-adjusted probability measures. For example, the median in the baseline case is about 34.6 years. The enhanced medians for the less averse and more averse specifications are about 49.4 and 78.8 years, respectively. The uncertainty-adjusted densities make the R&D investment appear *less* attractive from a social valuation perspective.

(fig-9)=

<div id="fig-9" style="display:flex; justify-content:center; align-items:center;">
  <img src="../_static/paper/Figure9_tech_only_lambda_jacobian_baseline_allxi_Technology_technology_density.png"
       alt="Jump time densities across uncertainty aversion cases for the technology jump only model"
       style="width:450px; max-width:100%; height:auto;">
</div>

Figure 9: Jump time densities for the technology jump only model, including the baseline specification and uncertainty-adjusted densities for two alternative specifications of uncertainty aversion.

{ref}`Table 6 <table-6>` reports the three flow contributions to the SVRD for alternative aversions to uncertainty, along with the robustly optimal initial investments for R&D and capital. In this simplified model, we continue to see more R&D investment for greater uncertainty concerns. All three contributions to the SVRD increase with uncertainty concerns, including the flow ii term. In the absence of a damage information event, the flow ii term is now the major contributor to the SVRD, accounting for about two-thirds of overall valuations.

(table-6)=

```{include} ../_static/table/flow_decomposition_one_jump.md
```

Marginal changes in both capital states contribute to the outcomes reported in {ref}`Table 6 <table-6>` for SVRD. As we have seen, the marginal valuations can be decomposed by horizon, analogous to the measurements from impulse-response analyses. We display such horizon-based marginal valuation decompositions in {ref}`Figure 10 <fig-10>`. The left panel reports flow ii decompositions, and the right panel displays flow iii decompositions.

(fig-10)=

<div id="fig-10" style="display:flex; gap:18px; justify-content:center; align-items:flex-start; flex-wrap:wrap;">
  <figure style="margin:0; width:340px; max-width:100%;">
    <img src="../_static/paper/Figure10_tech_only_lambda_jacobian_baseline_allxi_Technology_flow_ii.png"
         alt="Horizon decomposition of the flow ii contribution to the SVRD across uncertainty aversion cases for the technology jump only model"
         style="width:100%; height:auto;">
    <figcaption style="text-align:center; font-size:0.85em;">(a) Horizon decomposition of the flow ii contribution to the SVRDs</figcaption>
  </figure>
  <figure style="margin:0; width:340px; max-width:100%;">
    <img src="../_static/paper/Figure10_tech_only_lambda_jacobian_baseline_allxi_Technology_flow_iii.png"
         alt="Horizon decomposition of the flow iii contribution to the SVRD across uncertainty aversion cases for the technology jump only model"
         style="width:100%; height:auto;">
    <figcaption style="text-align:center; font-size:0.85em;">(b) Horizon decomposition of the flow iii contribution to the SVRDs</figcaption>
  </figure>
</div>

Figure 10: Horizon decompositions of the flow contributions for the SVRDs. To convert the marginal value contributions in Panel (a) from ${\hat r}$ to $r$ and put them in units of the damaged consumption numeraire, we scaled the Panel (a) trajectory by the initial period ratio of damaged consumption to the stock of knowledge. We did the analogous conversion for the Panel (b) trajectory. Each panel plots trajectories under the baseline ($\xi_m = \infty$) specification as well as two alternative specifications of uncertainty aversion.

From the left panel of {ref}`Figure 10 <fig-10>`, we see that smaller values of $\xi_m$ (greater uncertainty aversion) lead to greater horizon-specific contributions to the SVRDs except sometimes at very short horizons. As noted in {ref}`Section 8.4 <proactive>`, an increase in the difference $V^L - V$ gives a counteracting force to the delays in the jump time densities reported in {ref}`Figure 9 <fig-9>`.

The horizon decompositions in the right panel of {ref}`Figure 10 <fig-10>` provide a rather different accounting for flow iii. The marginal continuation-value contribution, $\frac {\partial V^L}{\partial {\hat k}} = 1$, is independent of $\xi_m$ due to the additive separability of $V^L$. The distorted jump intensity, however, remains an important contributor to this term. The locations of the peaks in the responses reflect the uncertainty-adjusted jump probabilities, which give more pessimistic assessments to the timing of an R&D success when uncertainty aversion is enhanced.

Uncertainty in the success date makes the investment less attractive. This force is more than offset by the net payoff to discovery, which increases because an R&D success eliminates an important source of uncertainty. Although the second force dominates in our calculations, this finding turns out to be sensitive to the range of aversions that are considered. {ref}`Figure 11 <fig-11>` shows that for very high misspecification concerns (high values of $1/\xi_m$), the first force can dominate, leading instead to a reduction in the R&D investment. The SVRD follows a similar pattern, which is to be expected given the first-order conditions for R&D investment.

(fig-11)=

<div id="fig-11" style="display:flex; justify-content:center; align-items:center;">
  <img src="../_static/paper/Figure11_rd_investment_vs_inverse_xi.png"
       alt="Plot of the smoothed cubic spline fit of R&amp;D investment as a function of the inverse of the robustness penalty parameter for the technology jump only model"
       style="width:450px; max-width:100%; height:auto;">
</div>

Figure 11: R&D investment as a function of the inverse of the robustness penalty parameter, $1/\xi_m$, for the technology jump only model. In constructing this figure, we first computed R&D investment-to-output ratios for a discrete set of $\xi_m$'s, and then we formed the blue curve by taking a smoothed cubic spline fit to the discrete set of computed outcomes.

(two-step)=
## Two-step technology discovery

Using this simplified model without a damage information event, we next explore the quantitative impact of altering our one-step technology advancement specification. We first entertain a two-step counterpart with three alternative jump intensity functions. In all cases, the first technology jump goes only part of the way to a successful green transition by setting $\phi_0$ in the output constraint to half of its original value. Only after the second technology jump is the full green transition achieved by setting $\phi_0$ to zero. Continuing to denote the one-jump model jump intensity as ${\mathcal J}^L$, we explore the following scenarios:

i) we use $2{\mathcal J}^L$ as the intensity for each of the jumps;

ii) we use ${\mathcal J}^L$ as the intensity for each of the jumps;

iii) we use $2{\mathcal J}^L$ as the intensity for each jump, but we reinitialize $R_t$ for the second jump at $R_0$.

In the third experiment, the initial advancement of the knowledge stock is assumed to be relevant only for the first technology jump, in contrast to the other two two-step specifications. We also include a fourth specification, which uses a one-step technology specification that allows for only a partial success:

iv) we use ${\mathcal J}^L$ as the intensity with a single jump of $\phi_0$ to half of its original value;

Appendix K of the paper and [Online Appendix O](13_online_o.md) provide additional results and full details for the model HJB equations.

In {ref}`Table 7 <table-7>`, we report the SVRDs and R&D investments relative to total output for each of these alternative jump specifications using $\xi_m$ equal to .05 and .1 as in our full model. We replicate the qualitative implications of our one-jump specifications, but quantitative magnitudes differ. We view two-jump specification i) as the closest counterpart to the one-jump versions of the model, and find that the baseline R&D investment/output ratios are very similar. While uncertainty aversion continues to lead to higher R&D investments than the baseline case, the increases are more modest than in the one-jump model.

In comparison to specification ii), the SVRDs and the implied investments are substantially reduced for specification iv). This outcome is to be anticipated because in the absence of a second jump, the rewards to R&D investment are greatly reduced. Nevertheless, the qualitative responses to increased uncertainty aversion remain for the aversions we report.

(table-7)=

```{include} ../_static/table/table7_two_jump.md
```

(aversion-sensitivity)=
## Uncertainty aversion sensitivity

This section is Appendix F.3 of the paper.

To further detail the model sensitivity to uncertainty aversion, we provide the numerical values for the SVRD and R&D investment outcomes corresponding to {ref}`Figure 11 <fig-11>`. The numerical values, provided in {ref}`Table 21 <table-21>`, show the responses to increasing uncertainty aversion (decreasing $\xi_m$) for the technology jump only model where the only uncertainty channel is the technology jump channel. The SVRD increases to more than double the baseline case at its maximum, and then diminishes to about 30% higher than the baseline case for the smallest value of $\xi_m$ that we examine. The R&D investment value rises to nearly $5.5$ times higher than the baseline case at its maximum, and then decreases to a value just under double the baseline case for the smallest value of $\xi_m$ that we examine.

(table-21)=

```{include} ../_static/table/svrd_nonmonotone.md
```

The implied SVRD totals from this table differ from those reported in {ref}`Table 6 <table-6>` by between 1.2 and 5.6 percent because of our use of simulation methods to compute the flow decompositions.

::::{hidden}
## Reproducing the figures and tables

To reproduce Figures 9, 10, and 11 and Tables 6, 7, and 21, run the scripts below from the root of the code repository after the {ref}`technology jump only solutions <code-tech-only>` and the {ref}`two step and partial technology solutions <code-two-step>` on the Fine grid have finished. Each script submits Slurm jobs and returns at once, so start each script only after the jobs of the previous one have finished. The first five scripts reproduce Figures 9, 10, and 11 and Tables 6 and 21, and the last three reproduce Table 7. Figure 8 comes from the script on [Example economy](01_example_economy.md).

~~~~bash
bash ./sbatch/feymannkacs_prepare.sh --model tech_only --grid-profile double_resolution --xi-t-values 100000.,0.1,0.05,0.02,0.015,0.01,0.009,0.008,0.007,0.006,0.005
bash ./sbatch/feymannkacs_simulate.sh --model tech_only --grid-profile double_resolution
bash ./sbatch/feymannkacs_plot_composite.sh --model tech_only --grid-profile double_resolution
bash ./sbatch/update_results.sh --model tech_only --grid-profile double_resolution --main-only --no-compile
bash ./sbatch/tech_only_nonmonotonicity_plot.sh --grid-profile double_resolution
bash ./sbatch/feymannkacs_prepare.sh --model partial_tech --grid-profile double_resolution
bash ./sbatch/stochastic_trajectories_2stage_prepare.sh --grid-profile double_resolution --experiment-cases double,baseline,double_reset_r
bash ./sbatch/update_results.sh --model 2stage_tech --grid-profile double_resolution --main-only --no-compile
~~~~

After the run finishes, you should have output files named `tech_only_lambda_jacobian_distorted_allxi_Technology_technology_density.png` (Figure 9), `tech_only_lambda_jacobian_distorted_allxi_Technology_flow_ii.png` and `tech_only_lambda_jacobian_distorted_allxi_Technology_flow_iii.png` (Figure 10) under `output/figures/<dataset>/feymannkacs_plot_composite/`, `only_tech_jump.tex` (Table 6) under `output/tables/<dataset>/feymannkacs_plot_composite/`, and `only_tech_nonmonotonicity.tex` (Table 21) under `output/tables/<dataset>/feymannkacs_prepare/` for the technology jump only model, and `rd_investment_vs_inverse_xi.png` (Figure 11) under `output/figures/tech_only_nonmonotonicity/`. For Table 7, you should have `partial_tech_initial_values.tex` under `output/tables/<dataset>/feymannkacs_prepare/` for the partial technology model and `two_stage_technology.tex` under `output/tables/<dataset>/stochastic_trajectories_2stage_prepare/` for the two step model. In each case `<dataset>` is the Fine grid directory of the model named, as listed in {ref}`Grids <code-grids>`.

Source scripts:
* `sbatch/feymannkacs_prepare.sh`
* `sbatch/feymannkacs_simulate.sh`
* `sbatch/feymannkacs_plot_composite.sh`
* `sbatch/update_results.sh`
* `sbatch/tech_only_nonmonotonicity_plot.sh`
* `sbatch/stochastic_trajectories_2stage_prepare.sh`
* `python/models/tech_only/tech_only_solve_feymannkacs_prepare.py`
* `python/models/tech_only/tech_only_solve_feymannkacs_simulate.py`
* `python/models/tech_only/tech_only_solve_feymannkacs_plot_composite.py`
* `python/tech_only_nonmonotonicity_plot.py`
* `python/models/partial_tech/partial_tech_solve_feymannkacs_prepare.py`
* `python/models/two_stage_tech/two_stage_tech_stochastic_trajectories_prepare.py`
* `python/update_results.py`
::::
