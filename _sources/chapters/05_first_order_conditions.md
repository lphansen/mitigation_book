# First-order conditions and stochastic simulations

(first-order)=
## First-order conditions for robustly optimal policies

In addition to $CO_2$ emissions, the social planner has two investment opportunities to consider in our setup: investment in new capital and investment in R&D. We now investigate the first-order conditions prior to the realization of either the technology discovery or the damage information event. The first-order conditions for all three controls have a central role for the partial derivative of the value function with respect to an endogenous state, the logarithm of capital, the logarithm of the knowledge stock, or temperature.

The first-order conditions for investment in new capital are

$$
\frac 1 {K_t} \left[ \frac {\partial { V}}{ \partial {\hat k} } (X_t)\right] \left(1 - \kappa \, \frac {I_t^k}{K_t} \right) - \delta \, \left(\frac {1} {C_t}\right) = 0,
$$

where the initial division by $K_t$ occurs because of our choice of $\log K_t$ as a state variable. Thus, we obtain the formula for the investment-capital ratio:

$$
\frac {I_t^k}{K_t} = \frac 1 \kappa - \frac 1 \kappa \left(\frac{\delta K_t} {C_t \left[\frac {\partial {V}}{ \partial {\hat k} } (X_t)\right] } \right),
$$

where the term in brackets on the far right of this formula, when scaled by $N_t$, is the reciprocal of "Q" from the theory of investment expressed in units of damage consumption.

The first-order conditions for the socially efficient R&D investment are

$$
\frac {\partial {V}}{ \partial {\hat r} } (X_t) \psi_0 \psi_1 \left( {I_t^r} \right)^{\psi_1-1} (R_t)^{-\psi_1} - \left(\frac {\delta} {C_t} \right) = 0 . \tag{11}
$$

Thus

$$
\frac {I_t^r}{R_t} = \left(\psi_0 \psi_1 \right)^{\frac 1 {1 - \psi_1}} \left(\frac {C_t \left[\frac {\partial {V}}{ \partial {\hat r} } (X_t)\right] } {\delta R_t} \right)^\frac 1 {1 - \psi_1}.
$$

where the term on the far right in brackets, when scaled by $1/N_t$, is what we will refer to as the social value of the knowledge stock of R&D (SVRD). It is quantified by the marginal value of the knowledge stock and expressed in units of (damaged) consumption.

The first-order conditions for emissions depend on the uncertainty-adjusted dynamics for temperature:

$$
\left[ \frac {\partial {V}} {\partial y} (X_t) \right] {\tilde \theta_t^*} + {\mathcal E}_t \left[ \frac {\partial^2 { V}(X_t)}{\partial y^2 } \right]|\varsigma|^2 + \left(\frac \delta {C_t} \right) \frac {\phi_0 \phi_1} {\beta } \left( {B_t}\right)^{\phi_1 - 1}{\bf 1}_{\{ {\mathcal E}_t \le \beta \alpha K_t\} } =0
$$

where

$$
\tilde \theta_t^* = \int_\Theta \theta Q_t^*(\theta) dP_t(\theta)
$$

provided there is a nonnegative solution for emissions. Otherwise, emissions are zero. This equation continues to hold if we divide the terms by marginal utility of damaged consumption, $\delta N_t/C_t$. The implied social cost of carbon (SCC) is

$$
\left(\frac {C_t} {\delta N_t}\right) \left(\left[ -\frac {\partial {V}} {\partial y} (X_t) {\tilde \theta_t^*} \right] - {\mathcal E}_t \left[ \frac {\partial^2 { V}(X_t)}{\partial y^2 } \right]|\varsigma|^2 \right) , \tag{12}
$$

and the social benefit is

$$
{ \frac{1}{N_t}} \left(\frac {\phi_0 \phi_1} {\beta} \right) \left( {B_t} \right)^{\phi_1 - 1}{\bf 1}_{\{ {\mathcal E}_t \le \beta \alpha K_t\} },
$$

both expressed in terms of damage-adjusted consumption as the numeraire. Going forward, we refer to

$$
- \left(\frac {C_t} {\delta N_t}\right) \left[\frac {\partial {V}} {\partial y} (X_t) \right]
$$

as the social cost of global warming (SCGW), which is a central input into the SCC.

These marginal formulas are evaluated at the socially efficient allocation as is required for deducing the Pigouvian taxation, and they depend on the presumed ambiguity aversion. Notice also that the SCC (12) includes an explicit volatility adjustment because emissions in our model alter the local exposure to Brownian motion risk.

We report investment as a ratio to output, where our measure of output is $\alpha K$ for a given capital realization $K$. This measure deliberately abstracts from the energy input in production. Because energy use is the source of the externality, we report the resulting emissions separately rather than incorporating an abatement adjustment into output.

(simulations)=
## Stochastic simulations

{ref}`Figure 3 <fig-3>` gives four stochastic pathways for the robustly optimal choice of R&D investment and emissions. The simulations are chosen to illustrate a range of possible outcomes, rather than to represent typical trajectories. The pathways were generated using the baseline probabilities with the investment and emissions decision rules computed under a choice of $\xi_m$ that we refer to as the less averse specification.

(fig-3)=

<div id="fig-3" style="
     display:flex;
     gap:18px;
     justify-content:center;
     align-items:flex-start;
     flex-wrap:wrap;
">
  <figure style="margin:0; width:340px; max-width:100%;">
    <img src="../_static/paper/Figure3_rd_investment_paths.png"
         alt="Four illustrative simulated stochastic pathways for R&amp;D investment as a fraction of output"
         style="width:100%; height:auto;">
    <figcaption style="text-align:center; font-size:0.85em;">(a) R&amp;D investment-output ratio</figcaption>
  </figure>
  <figure style="margin:0; width:340px; max-width:100%;">
    <img src="../_static/paper/Figure3_emissions_paths.png"
         alt="Four illustrative simulated stochastic pathways for emissions in gigatons of carbon (GtC)"
         style="width:100%; height:auto;">
    <figcaption style="text-align:center; font-size:0.85em;">(b) Emissions</figcaption>
  </figure>
</div>

Figure 3: Illustrative stochastic pathways computed with baseline probabilities and controls given by the $\xi_m=.1$, or less uncertainty aversion, specification. Panel (a) shows the robustly optimal R&D investment choices expressed as ratio of output abstracting from the energy input ($\alpha K$) for the stochastic simulation pathways. Panel (b) shows the robustly optimal emissions choices for the stochastic simulation pathways. Path 1 (dark blue) is a case with no jumps. Path 2 (red) is a case with a technology jump at year 14. Path 3 (green) is a case with a damage curvature jump ($\lambda_3=.053$) at year 34. Path 4 (light blue) is a case with a damage curvature jump ($\lambda_3=.298$) at year 36.

On path 3, the news about damage curvature at the jump date is good (a low value of $\lambda_3$), and the path for R&D investment shows a substantial drop. Along path 4, the news about damage curvature is bad (a high value of $\lambda_3$), and there is a prominent increase in R&D investment, presumably because of the forthcoming pronounced damages.

With the exception of the path 2 technological breakthrough, the emissions responses depicted in Panel (b) of {ref}`Figure 3 <fig-3>` are more muted than the R&D investment responses. When there is good news about damages, as in path 3, we see a negligible impact on emissions. In contrast, for path 4, when there is a bad news realization about damages, there is a notable drop in emissions.

::::{hidden}
## Reproducing the figure

To reproduce Figure 3, run the scripts below from the root of the code repository after the {ref}`full model solutions <code-full-model>` on the Fine grid have finished. The simulation script submits 200 jobs for each of $\xi_m = \infty$, $.1$ and $.05$ and waits while the queue is full, so run it in a persistent shell such as tmux and start the plot script after all simulation jobs have finished.

~~~~bash
bash ./sbatch/stochastic_trajectories_simulate.sh --grid-profile double_resolution
bash ./sbatch/stochastic_trajectories_plot.sh --grid-profile double_resolution
~~~~

After the run finishes, you should have output files named `rd_investment_paths.png` and `emissions_paths.png` under `output/figures/<dataset>/stochastic_trajectories_plot/stochastic-trajectories/aversion/p0-0.10583_p1-0.5_ci-1091.1_phi0-0.5_rho-1.0_delta-0.01_horizon-65_direct_direct/less-aversion/`, where `<dataset>` is the Fine grid directory of the full model, as listed in {ref}`Grids <code-grids>`.

Source scripts:
* `sbatch/stochastic_trajectories_simulate.sh`
* `sbatch/stochastic_trajectories_plot.sh`
* `python/stochastic_trajectories_simulate.py`
* `python/stochastic_trajectories_plot.py`
::::
