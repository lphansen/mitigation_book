# Uncertainty assessments

We implement two complementary quantifications of uncertainty impacts. Since our model has multiple channels by which uncertainty can impact policy outcomes, we first consider the uncertainty consequences of the particular channels. We then formally inspect the uncertainty-adjusted probabilities.

(deconstruction)=
## Uncertainty deconstruction

As we delineate in the introduction of the paper, our model has four channels, each of which has its own distinct uncertainty input. We compare actions and outcomes when we activate each uncertainty channel by itself when solving the adversarial minimization problem to the corresponding actions and outcomes when all channels are activated simultaneously.

We used two penalization parameters to represent the uncertainty aversion: $\xi_m$ for misspecification concerns about the stochastic dynamics and $\xi_a$ for ambiguity in how to weight the alternative climate models. Since the outcome of the model ambiguity gives a counterpart to a drift distortion in the temperature evolution equation, to limit the scope of the sensitivity analysis, we do the following. For a given value of $\xi_m$, we choose $\xi_a$ to match the same magnitude of the drift distortion in the initial time period. In much of what follows we will illustrate results for three specifications of $\xi_m$ with the following labels or references — **baseline**: $\xi_m = \infty$; **less aversion**: $\xi_m = .1$; and **more aversion**: $\xi_m = .05$. In addition, reported outcomes are computed at the initial time period for our simulations unless otherwise stated. For results reported across time horizons, scaling factors used to compute the outcomes are based on values from the initial simulation time period.

{ref}`Table 1 <table-1>` gives the uncertainty decompositions for both the uncertainty contributions to the social values of research and development (SVRD) and the corresponding R&D investments for two values of $\xi_m$.

(table-1)=

```{include} ../_static/table/svrd_rd_decomposition.md
```

For both the social valuations and the implied actions, technological uncertainty accounts for the bulk of the uncertainty enhancement.

The R&D investment-output ratios reflect the dominant impact of technology uncertainty, and they *increase* in response to an enhanced aversion to misspecification uncertainty with one exception. Thus, the planner is more proactive in the R&D investment response when the uncertainty concerns are enhanced. When we activate only the uncertainty concerns about the productivity channel, R&D investment decreases slightly even relative to the baseline case, given the enhanced concerns about the overall productivity.

{ref}`Table 2 <table-2>` presents the results of the uncertainty decomposition for the SCGW and emissions.

(table-2)=

```{include} ../_static/table/scgw_emissions_decomposition.md
```

The patterns are very similar to those reported in {ref}`Table 1 <table-1>`. The technology channel is again the dominant contributor to the uncertainty responses. Emissions respond proportionately much less than R&D investment in the face of uncertainty concerns.

(adjusted-probabilities)=
## Uncertainty-adjusted probabilities

We next consider the implied uncertainty-adjusted probabilities that emerge from our analysis for the alternative sources of uncertainty aversion: Brownian shocks, climate model weights, and Poisson events. These probabilities are the solutions to the minimization problem, evaluated at the solutions to the maximization problem. These should not be viewed as "best-guess" distributions; but rather they are the "worst-case" distributions subject to penalization that are a vehicle by which the planner constructs robustly optimal courses of action. It is straightforward to run our solution code for other values of $\xi_m$.

While it is hard to interpret directly the magnitudes of $\xi_m$, we find it valuable to adopt an approach commonly used for robust Bayesian methods by inspecting worst-case probability specifications and isolating where the probability adjustments are most prominent. Formally, this is motivated by an application of the Min-max Theorem, which constructs a single probability specification under which robustly optimal decisions are optimal. In effect, $\xi_m$ provides a way to assess how consequential the various uncertainty inputs are to the decision problem.

We start by reporting the drift distortions for the two capital stock processes. These are given in {ref}`Table 3 <table-3>`.

(table-3)=

```{include} ../_static/table/drift_distortions.md
```

The negative drift distortions for capital and the knowledge stock highlight that worst-case concerns tilt towards reduced effectiveness of investment in capital and R&D. The negatives of drift distortions for the capital stock are interpretable as implied shadow Sharpe ratios induced by uncertainty aversion to the exposure of capital to Brownian risk, since the reported distortions are multiplied by the volatility exposure to the productivity shock. The magnitudes of the distortions for the knowledge stock are quantitatively small.

{ref}`Figure 4 <fig-4>` reports the baseline and uncertainty-adjusted relative probability density functions for two different values of $\xi_m$ relative to baseline probabilities that equally weight each of the 144 different model outcomes.

(fig-4)=

<div id="fig-4" style="display:flex; justify-content:center; align-items:center;">
  <img src="../_static/paper/Figure4_climate_model_relative_weights_year-0.png"
       alt="Uncertainty-adjusted relative density plots for 144 climate models for more and less aversion specifications relative to a uniform baseline density"
       style="width:450px; max-width:100%; height:auto;">
</div>

Figure 4: Uncertainty-adjusted densities for $\theta$. The baseline and two uncertainty-adjusted densities are relative to a uniform baseline density. The resulting model averages are 1.86 for $\xi_m = \infty$, 1.89 for $\xi_m = .1$, and 1.97 for $\xi_m = .05$.

By construction, the baseline relative density is constant at a value of one. The two relative densities of interest slope upward to the right, placing more probability on the higher values of $\theta$. This implies an increase in the mean. While the relative densities show substantive divergence from unity for values of $\theta$ near $1$ and $2.5$, these turn out to be very *atypical* values of $\theta$ as we displayed in {ref}`Figure 1 <fig-1>`. As a result, the mean increases are quite modest, as reported in {ref}`Figure 4 <fig-4>`, especially for $\xi_m = .1$ (less aversion).

Our model allows for multiple jumps with state-dependent intensities. We compute the relative contributions for the timing of the first jump. This first jump could be either one of the damage curvature jumps or a technology jump. Using the formulas provided in {ref}`Appendix D <jump-densities>`, we report additive decompositions of the jump-time densities (relative to uniform densities) for the damage information event and technology jump contributions. The damage information event aggregates over all possible damage curvature jumps.

(jump-densities)=

The following derivation, up to {ref}`Figure 5 <fig-5>`, is Appendix D of the paper.

The contributions to the *ex ante* density (relative to a uniform density) for the first jump time are computed as follows. First, by conditioning on the state variable history, we find that the *ex post* probability that any of the jumps has occurred in the time period $t$ to be:

$$
F_t = 1 - \exp \left[ - \int_0^t \sum_{\ell = 1}^{L} G^{*\ell}_\tau {\mathcal J}^\ell(X_\tau) d\tau \right],
$$

which increases in $t$. We then compute the probability for any of the jumps occurring by differentiating $F_t$ with respect to $t$:

$$
f_t = \sum_{\ell = 1}^{L} G^{*\ell}_t {\mathcal J}^\ell(X_t) \exp \left[ - \int_0^t \sum_{{\hat \ell} = 1}^{L} G_\tau^{*{\hat \ell}} {\mathcal J}^{\hat \ell}(X_\tau) d\tau \right].
$$

We unpack this density construction so as to apply to each of the separate jump possibilities,

$$
f^\ell_t \overset{\mathrm{def}}{=} G_t^{*\ell} {\mathcal J}^\ell(X_t) \exp \left[ - \int_0^t \sum_{{\hat \ell} = 1}^{L} G_\tau^{*{\hat \ell}} {\mathcal J}^{\hat \ell}(X_\tau) d\tau \right], \qquad \ell = 1,...,L \tag{23}
$$

which can be viewed as contributions to a density with respect to a uniform measure over the possible time horizons and a uniform measure over discrete states. To obtain the corresponding contributions to the *ex ante* densities of interest, we take conditional expectations over the future values of the state variables.

{ref}`Figure 5 <fig-5>` plots the *ex ante* density contributions for the first jump time.

(fig-5)=

<div id="fig-5" style="
     display:flex;
     gap:18px;
     justify-content:center;
     align-items:flex-start;
     flex-wrap:wrap;
">
  <figure style="margin:0; width:340px; max-width:100%;">
    <img src="../_static/paper/Figure5_all_channel_on_0.1lambda_jacobian_distorted_CompositeTechnology0.083_Discount_nodeltadt_tech_Processs_dt.png"
         alt="Additive decomposition of the jump-time densities, contribution of the technology jump"
         style="width:100%; height:auto;">
    <figcaption style="text-align:center; font-size:0.85em;">(a) Contribution of technology jump.</figcaption>
  </figure>
  <figure style="margin:0; width:340px; max-width:100%;">
    <img src="../_static/paper/Figure5_all_channel_on_0.1lambda_jacobian_distorted_CompositeTechnology0.083_Discount_nodeltadt_damage_Processs_dt.png"
         alt="Additive decomposition of the jump-time densities, contribution of the damage information event"
         style="width:100%; height:auto;">
    <figcaption style="text-align:center; font-size:0.85em;">(b) Contribution of the damage information event.</figcaption>
  </figure>
</div>

Figure 5: Additive decomposition of the jump-time densities under the baseline probability and uncertainty-adjusted probabilities for two specifications of uncertainty aversion. By design, the density contributions across the two panels sum to one. The technology discovery contribution is 60% for the baseline specification, 42% for less aversion, and 12% for more aversion.

The jump time density is the sum of these two contributions. Uncertainty aversion pertaining to the technology contribution makes a successful discovery appear more likely to be delayed, reflected in the uncertainty-adjusted density in the left panel. The delayed prospects for success make R&D investment *less attractive*. Consistent with these probabilistic delays, as we increase the uncertainty aversion, the contribution of the damage information event becomes much higher under the uncertainty-adjusted probability measures.

Since there are multiple potential damage curves, we report how misspecification aversion shifts the weights of the unknown damage curve parameter, $\lambda_3$. The baseline ($\xi_m=\infty$) distribution for $\lambda_3$ is uniform $[0,.33]$. We used twenty equally spaced discrete support points in our computations. As we see in {ref}`Figure 6 <fig-6>` the uncertainty-adjusted probabilities are tilted to the right, with a quite extreme shift when $\xi_m=.05$. The adjustment $\xi_m = .1$, while more modest, is still quite notable. The distributional shifts for the potential damage curvature turn out to be much more consequential than the climate model uncertainty.

(fig-6)=

<div id="fig-6" style="display:flex; justify-content:center; align-items:center;">
  <img src="../_static/paper/Figure6_all_channel_on_0.1lambda_jacobian_distorted_Technologydamage_curve_year_splines_0_allxi.png"
       alt="Uncertainty-adjusted probabilities across the alternative damage curve possibilities"
       style="width:450px; max-width:100%; height:auto;">
</div>

Figure 6: Uncertainty-adjusted probabilities across the alternative $\lambda_{3}$'s for the baseline probabilities and two specifications of uncertainty aversion. The resulting $\lambda_{3}$ averages are .167 for the baseline specification, .221 for less aversion, and .285 for more aversion.

::::{hidden}
## Reproducing the figures and tables

To reproduce Tables 1, 2 and 3 and Figures 4, 5 and 6, run the scripts below from the root of the code repository after the {ref}`full model solutions <code-full-model>` and the {ref}`channel decompositions <code-channels>` on the Fine grid have finished. Each script submits Slurm jobs and returns at once, so start each script only after the jobs of the previous one have finished.

~~~~bash
bash ./sbatch/zeroshock_trajectories_simulate.sh --grid-profile double_resolution true false false
bash ./sbatch/zeroshock_trajectories_simulate.sh --grid-profile double_resolution non_climate_channels
bash ./sbatch/zeroshock_trajectories_simulate.sh --grid-profile double_resolution climate_channels
bash ./sbatch/datevaluereport_table.sh --grid-profile double_resolution
bash ./sbatch/zeroshock_trajectories_plot.sh --grid-profile double_resolution
bash ./sbatch/feymannkacs_prepare.sh --model full_model --grid-profile double_resolution baseline_xia
bash ./sbatch/update_results.sh --model full_model --grid-profile double_resolution --full-model-drift-only --no-compile
bash ./sbatch/feymannkacs_simulate.sh --model full_model --grid-profile double_resolution Technology
bash ./sbatch/feymannkacs_plot_composite.sh --model full_model --grid-profile double_resolution Technology
~~~~

After the run finishes, you should have these output files, where `<dataset>` is the Fine grid directory of the full model, as listed in {ref}`Grids <code-grids>`:

* Tables 1 and 2: `matrix_scrd_latex.tex` and `matrix_scgw_latex.tex` under `output/tables/<dataset>/datevaluereport_table/`.
* Table 3: `h_values_initial.tex` under `output/tables/<dataset>/feymannkacs_prepare/`. The prepare job outputs under `job-outs/<dataset>/feymannkacs_prepare/lambda_jacobian_distorted/scheme_direct_HJB_direct/` print the unrounded values as `h_k(X0)` and `h_r(X0)`.
* Figure 4: `climate_model_relative_weights_year-0.png` under `output/figures/<dataset>/zeroshock_trajectories_plot/zero-shock-trajectories/aversion-calibration-pair/p0-0.10583_p1-0.5_ci-1091.1_phi0-0.5_rho-1.0_delta-0.01_horizon-40_direct_direct/model-distributions/`.
* Figure 5: `all_channel_on_0.1lambda_jacobian_distorted_CompositeTechnology0.083_Discount_nodeltadt_tech_Processs_dt.png` (panel (a)) and `all_channel_on_0.1lambda_jacobian_distorted_CompositeTechnology0.083_Discount_nodeltadt_damage_Processs_dt.png` (panel (b)) under `output/figures/<dataset>/feymannkacs_plot_composite/`.
* Figure 6: `all_channel_on_0.1lambda_jacobian_distorted_Technologydamage_curve_year_splines_0_allxi.png` under the same directory as Figure 5.

Source scripts:
* `sbatch/zeroshock_trajectories_simulate.sh`
* `sbatch/datevaluereport_table.sh`
* `sbatch/zeroshock_trajectories_plot.sh`
* `sbatch/feymannkacs_prepare.sh`
* `sbatch/update_results.sh`
* `sbatch/feymannkacs_simulate.sh`
* `sbatch/feymannkacs_plot_composite.sh`
* `python/zeroshock_trajectories_simulate.py`
* `python/datevaluereport_table.py`
* `python/zeroshock_trajectories_plot.py`
* `python/models/full_model/full_model_solve_feymannkacs_prepare.py`
* `python/update_results.py`
* `python/models/full_model/full_model_solve_feymannkacs_simulate.py`
* `python/models/full_model/full_model_solve_feymannkacs_plot_composite.py`
::::
