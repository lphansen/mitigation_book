# Marginal valuations as asset prices

We next describe a type of local sensitivity analysis that helps us interpret some of our main findings using an asset pricing perspective. In terms of an asset pricing analogy, we take an intertemporal cash flow rather than a one-period return perspective when deducing contributions and uncertainty implications to valuations.

We draw on an approach for representing intertemporal marginal values developed and justified in {cite:t}`HansenSouganidis:2025`. The representations of marginal valuation closely resemble intertemporal cash flow valuation under uncertainty.

Distinct marginal social valuations emerge in the three sets of first-order conditions for the planner controls: the value of capital $\left(\frac {\partial V} {\partial k} \right)$, the value of R&D $\left(\frac {\partial V} {\partial {r}}\right)$, and the cost of global warming $\left(- \frac {\partial V} {\partial y}\right)$. The asset-pricing type representations of the marginal valuations, expressed in terms of discounted social cash flows, allow us to inspect and deconstruct the contributions to these social valuations. We construct our marginal value representations prior to the first jump occurring.

The initial jump plays the role of a state-dependent terminal condition with an endogenously determined continuation value conditioned on the jump occurring. This initial jump could be any of the $L$ possible jump types. Given this perspective, we adjust the discounting to incorporate jump probabilities. The resulting discount rate we use for time $\tau$ is:

$$
\delta + \sum_{\ell = 1}^L G^{*\ell}_\tau {\mathcal J}^\ell (X_\tau) .
$$

with the date $t$, state-dependent discount factor given by:

$$
Dis_t \overset{\mathrm{def}}{=} \exp\left( - \int_0^t \left[\delta + \sum_{\ell = 1}^L G^{*\ell}_\tau {\mathcal J}^\ell (X_\tau) \right] d \tau \right).
$$

Recall that the $G^{*\ell}_\tau$'s are the uncertainty adjustment factors for the intensities. The adjustment:

$$
\exp\left( - \int_0^t \left[\sum_{\ell = 1}^L G^{*\ell}_\tau {\mathcal J}^\ell (X_\tau) \right] d \tau \right). \tag{13}
$$

to the subjective discounting gives the probability of there not being a jump until date $t.$ We include this term in the discount factor $Dis_t$ so that we can continue to exploit diffusion-based characterizations of marginal valuation.

The key inputs in this and other related forms of sensitivity analysis are marginal impulse response processes $\Lambda,$ which give the impacts on the future state vector $X$ of a marginal change in one of the initial states. When the state dynamics are nonlinear, $\Lambda$ is stochastic. We refer to it as the stochastic response process, as it is a generalization of the linear impulse responses commonly used in applied macroeconomics. By construction, the process $\Lambda$ has the same dimensionality as the number of components of $X$. It is built so that when we initialize it at a coordinate vector, it gives the responses to an initial change in the corresponding state variable.

We use the stochastic responses and state-dependent discounting in the marginal-valuation formula:

$$
\frac {\partial V}{\partial x}(X_0) \cdot \Lambda_0 = \widetilde{\mathbb E} \left[ \int_0^\infty Dis_t \left(\Lambda_t \cdot Scf_t \right) dt \mid X_0, \Lambda_0 \right] \tag{14}
$$

where the expectation $\widetilde{\mathbb E}$ reflects the diffusion dynamics incorporating the minimizing drift distortions, $H^*$, implied by robustness. Importantly, this expectation only features the diffusion dynamics and conditions on a jump that does not happen.

In this asset-pricing type formula, the stochastic flow process measures the impact of an initial change in a state variable as a product of two marginal calculations, loosely motivated by the chain rule:

$$
\Lambda_t \cdot Scf_t.
$$

In this calculation, $Scf_t$ is a three-dimensional vector with each entry measuring a marginal contribution of a date $t$ state variable to date $t$ cash flow. The dot product with $\Lambda_t$ reflects the stochastic response at date $t$ to an initial change in one of the state variables, or more generally a linear combination of state variables depending upon the initialization, $\Lambda_0.$ In light of this construction, we may divide $\Lambda_t \cdot Scf_t$ into contributions from each of the states since the dot product sums across vector entries. This decomposition shows how the state interdependencies are reflected in the marginal valuations.

There are three sources of date $t$ contributions to the stochastic flow vector $Scf_t:$

* i) marginal utility;
* ii) marginal impact of a jump;
* iii) marginal impact when you jump.

(marginal-utility)=
## Marginal-utility flow

Flow i measures the impact of a marginal change in a state variable on future contributions to utility after adjusting for damages:

$$
\textrm{flow i} \overset{\mathrm{def}}{=} \delta \left( \frac {\partial \log c} {\partial x} - \frac {\partial {\hat n}}{\partial x}\right), \tag{15}
$$

which is the date $t$ vector of partial derivatives of the utility of damaged consumption with respect to each state variable, where $\delta$ is a convenient utility scaling.

Again using the chain rule, we write the term (15) as the following product:

$$
\textrm{flow i} = \delta \left[ \frac {\partial \log (c/n) } {\partial (c/n) }\right] \left[\frac {\partial (c/n) } {\partial x} \right] = \delta \left(\frac { n} c \right) \left[\frac {\partial (c/n)} {\partial x} \right] .
$$

where $n = \exp[{\hat n}(y)]$, and $c/n$ is the adjusted consumption for damages. The first term on the right is the marginal utility of (damaged) consumption, which appears as the familiar construction of a stochastic discount factor process in asset pricing, while the second term captures the dependence of (damaged) consumption on the state vector.

(jump-contributions)=
## Prospective jump contributions

Prospective Poisson jumps also introduce cash-flow contributions to this valuation. These additional terms account for state-dependent responses operating through uncertainty in the jump intensity functions and the continuation value functions, as outlined below.

### Marginal impact of a jump

A marginal change in the state vector in the current time period alters the jump intensities, contributing the following term to the marginal valuation:

$$
\textrm{flow ii} = \xi_m \sum_{\ell=1}^L {\mathcal J}^\ell\left( 1 - \exp \left[ - {\frac{1}{\xi_m}} \left( V^\ell - V \right) \right] \right) \left(\frac {\partial \log {\mathcal J}^\ell}{\partial x} \right). \tag{16}
$$

Specifically, the intensities ${\mathcal J}^\ell$ for $\ell = 1, 2, ..., L-1$ capture the stochastic dynamics of the prospective damage curvature jumps. These intensities depend only on the temperature, which simplifies the contribution of $\frac {\partial \log {\mathcal J}^\ell}{\partial x}$ to the marginal impact formula (16). Analogously, ${\mathcal J}^L$ depends only on the knowledge stock. This latter contribution is important for understanding the impacts of uncertainty on investment in R&D. Since the implied dynamical system has interactions over states, a marginal change in the initial period knowledge stock will impact all future states, inducing cross effects in the valuation.

### Marginal impact when there is a jump

A marginal change in the state vector in the current time period alters the continuation values conditioned on a jump happening:

$$
\textrm{flow iii} \overset{\mathrm{def}}{=} \sum_{\ell=1} ^L g^{*\ell} {\mathcal J}^\ell \frac {\partial V^\ell} {\partial x} \tag{17}
$$

where the $g^{*\ell}$'s are the robust adjustments to the intensities given by:

$$
g^{*\ell} \overset{\mathrm{def}}{=} \exp \left[ - {\frac{1}{\xi_m}} \left( V^\ell - V \right) \right] \textrm{ where } G^{*\ell}_t = g^{*\ell}(X_t).
$$

Notice that this term captures future marginal contributions to valuation as we may deduce post-jump marginal valuation counterparts as reflected in the partial derivatives: $\frac {\partial V^\ell} {\partial x}$ for the alternative $\ell$'s. Once a technology discovery happens, there is no direct marginal contribution of the flow iii term to valuation.

Notice that the flow ii and flow iii terms include a scaling by the uncertainty-adjusted intensities. This inclusion is consistent with {ref}`formula (23) given in Appendix D <jump-densities>` where these intensities in conjunction with the contribution (13) to the factor, $Dis_t,$ account for the uncertainty-adjusted jump density.

(flow-decompositions)=
## Decompositions

The integral representation (14) gives a horizon-based decomposition of marginal values. The flow terms open the door to three additional types of additive decompositions: one based on the flow type, another based on the jump type $\ell$, and a third on which future values of states are impacted.

{ref}`Table 5 <table-5>` shows the quantitative importance of the three flow terms for SVRD as well as two additional refinements. The contributions of flow ii, the marginal impact of a jump, and flow iii, the marginal impact when you jump, dominate the direct marginal utility contribution given by flow i. This reflects how important the longer-term contributions of the uncertain jump processes are to the SVRDs.

(table-5)=

```{include} ../_static/table/table5_tech_flow_terms_split.md
```

As we see from Panel (a), the flow ii impact on valuation is primarily due to the prospective technology jump. Although flow ii increases with stronger concerns about robustness, such concerns have an even more dramatic impact on flow iii.

(proactive)=
## Why do enhanced uncertainty concerns induce a proactive R&D response?

From the first-order conditions for R&D investment in {ref}`(11) <first-order>`, we see a dependence on the social value of research and development (SVRD) as quantified by the marginal value of the knowledge stock. Consider flow ii of the SVRD as given by (16) to see how uncertainty aversion alters optimal R&D investment. The partial derivative of interest multiplies the robustly adjusted post-jump continuation value contribution:

$$
{\mathcal J}^L \xi_m \left(1 -\exp \left[ - {\frac{1}{\xi_m}} \left( V^L - V \right) \right] \right) \le {\mathcal J}^L \left(V^L - V\right) . \tag{18}
$$

This inequality is a direct implication of the solution to {ref}`Problem 3.3 <jump>`. It reflects the planner's cautious view of the potential success of a green technological innovation being realized and reflects the planner's *reduced* incentive to invest in R&D.

Uncertainty concerns, however, also impact the planner's view of a technology success should it happen. This is manifested in the robust adjustments to the continuation values, $V^L$ and $V$. Although increasing the uncertainty aversion (decreasing $\xi_m$) decreases both $V^L$ and $V,$ it has a much greater impact on $V$ as there is a substantial decrease in the exposure to uncertainty once the new clean technology is in place. This boost in the planner's payoff to the R&D investment *increases* the planner's incentive to invest.

To summarize, we have isolated two potentially counteracting contributions to the SVRD.

* The uncertainty-adjusted probabilities of a technology discovery assign more weight to distant successes relative to more recent ones as the aversion is enhanced. This carries over to the robust adjustment to the HJB equation as reflected in inequality (18).

* The endogenously determined net utility outcome from a potential successful discovery, measured by $V^L - V,$ increases as aversion increases due to a reduction in the pre-jump value function $V$. The reduction in $V$ dominates any reduction in $V^L$ since, post-jump, there is less exposure to uncertainty.

The first of these makes the R&D investment less attractive and the second one more attractive. Quantitatively, the second channel dominates in our calculations presented so far.

::::{hidden}
## Reproducing the table

To reproduce Table 5, run the script below from the root of the code repository after the {ref}`full model solutions <code-full-model>` on the Fine grid and the `sbatch/feymannkacs_plot_composite.sh` jobs for Figures 5 and 6 on [Uncertainty assessments](06_uncertainty_assessments.md) have finished.

~~~~bash
bash ./sbatch/update_results.sh --model full_model --grid-profile double_resolution --full-model-composite-only
~~~~

After the run finishes, you should have an output file named `tech_flow_terms_split.tex` under `output/tables/<dataset>/feymannkacs_plot_composite/` and its copy `Table5_tech_flow_terms_split.tex` under `results_in_paper/`. The entries of Panels (a) and (b) are the scaled values that the composite jobs print under `FLOW AND JUMP-CHANNEL DECOMPOSITION` and `FLOW-BY-STATE DECOMPOSITION` in the files ending in `_xim100000.out` ($\xi_m = \infty$), `_xim0.1.out` and `_xim0.05.out` under `job-outs/<dataset>/feymannkacs_plot_composite/lambda_jacobian_distorted/scheme_direct_HJB_direct/`. In both paths `<dataset>` is the Fine grid directory of the full model, as listed in {ref}`Grids <code-grids>`.

Source scripts:
* `sbatch/update_results.sh`
* `python/update_results.py`
* `python/models/full_model/full_model_solve_feymannkacs_plot_composite.py`
::::
