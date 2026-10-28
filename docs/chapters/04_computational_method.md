# Computational method

This page is Appendix G of the paper.

(policy-iteration)=
## Policy iteration

For simplicity, we denote the state space, control set, and distortion set by:

$$
X = \{\log k, y, \log r \}, \qquad \Phi = \{ i^k, i^r, \mathcal{E} \}, \qquad \Gamma = \{ h, q(\theta), g^\ell \} .
$$

State variables, controls, and distortions that are not applicable to an HJB equation at a particular jump state are omitted. The value function $\hat{v}(X)$ depends on the state $X$.

A pseudo-code of the numerical algorithm for solving the HJB equation via policy iteration is given in Algorithm 1. The algorithm involves an iterative process that alternates between policy improvement and policy evaluation steps.

---

**Algorithm 1** Solving the HJB equation via policy iteration.\
**Input:** Initial guesses $\hat{v}^0$, $\Phi^0$, $\Gamma^0$; values for $\Delta \tau$, $\varepsilon_{relax}$, $\epsilon_{KSP}$, $\epsilon_{outer}$, $N_{max}$\
**Output:** Optimal value function $\hat{v}^*$\
&emsp;$\hat{v} \gets \hat{v}^0$\
&emsp;**Repeat**\
&emsp;&emsp;Step 1: Compute optimal actions $\Phi^*$ from the first-order condition of the maximization problem using $\hat{v}$, $\Phi$, $\Gamma$. Update using numerical relaxation scheme with weight $\varepsilon_{relax}$.\
&emsp;&emsp;Step 2: Compute optimal probability distortions $\Gamma^*$ from the first-order condition of the minimization problem using $\hat{v}$, $\Phi^*$, $\Gamma$.\
&emsp;&emsp;Step 3: Update the value function $\hat{v}^*$ by solving (conditionally) the HJB PDE with a false transient method. $\hat{v}$, $\Phi^*$, $\Gamma^*$ are used in the PDE. Convergence tolerance given by $\epsilon_{KSP}$.\
&emsp;&emsp;Step 4: $\hat{v}^{prior} \gets \hat{v} \quad \hat{v} \gets \hat{v}^* \quad \Phi \gets \Phi^* \quad \Gamma \gets \Gamma^*$\
&emsp;**Until** $\left\|\frac{\hat{v}^* - \hat{v}^{prior}}{\Delta\tau}\right\|_\infty \le \epsilon_{outer}$ or $N \ge N_{max}$

---

(updating-rules)=
## Updating rules for $\Phi$ and $\Gamma$ at policy improvement steps

In solving HJB equations, we often encounter complex, highly non-linear equations for our optimal control choices that do not admit analytical solutions. To address this challenge, we implement a numerical relaxation updating scheme. The relaxation weight $\varepsilon$ determines the updating rate of the control vector $\Phi$. The control vector is updated according to

$$
\Phi_{n+1} = \varepsilon_{relax} \Phi^* + (1 - \varepsilon_{relax}) \Phi_n
$$

where $\Phi_{n+1}$ is the next iteration's optimal control vector, $\Phi^*$ is the updating optimal control vector value using the current value function solution, and $\Phi_n$ is the previous iteration's optimal control vector. The control updating is embedded in the outer policy/false-transient iteration. For emissions, the implementation also compares feasible stationary and boundary candidates before applying the relaxation update.

We note that every probability distortion from misspecification aversion has an analytical expression as a function of the value function and its derivatives. These can be computed and plugged in directly to the HJB expressions, and the iterative process for the HJB equation solution updates these values as the value function is updated until convergence is achieved.

(linear-pde)=
## Solving the linear PDE equation at the policy evaluation step

Updating value functions, given the state variables, controls, and distortions, is done by solving the linear PDE implicitly. To mitigate the potential instability of the non-linear HJB, we add a false transient (time) dimension and iterate the solution with an implicit time stepping procedure until the false time derivative converges to zero. In addition, we solve the linear system using a stabilized Bi-Conjugate Gradient solver with the ILU preconditioner provided by PETSc, a widely used software library developed by researchers at Argonne National laboratory to efficiently solve sparse linear/nonlinear systems.

First, note that we can write the HJB equation from our model using the following form:

$$
A \hat{v}
+B_{\hat{k}} \frac{\partial \hat{v}}{\partial \hat{k}}
+B_{y}\frac{\partial \hat{v}}{\partial y}
+B_{\hat{r}} \frac{\partial \hat{v}}{\partial \hat{r}}
+C_{\hat{k}} \frac{\partial^2 \hat{v}}{\partial \hat{k} \, \partial \hat{k}'}
+C_{y} \frac{\partial^2 \hat{v}}{\partial y \, \partial y'}
+C_{\hat{r}} \frac{\partial^2 \hat{v}}{\partial \hat{r} \, \partial \hat{r}'}
+D =0.
$$

More generally, our system can be expressed in the conditionally linear form:

$$
\begin{align*}
0 &= V_t(x) + \mathbb{A}(x;V,V_x,V_{xx})V(x) + \mathbb{B}(x;V,V_x,V_{xx})V_x(x) \\
& \quad + \frac{1}{2}tr[\mathbb{C}(x;V,V_x,V_{xx})'V_{xx}(x)\mathbb{C}(x;V,V_x,V_{xx})] + \mathbb{D}(x;V,V_x,V_{xx})
\end{align*}
$$

where $x$ is our state variable vector, $V_x(x)=\frac{\partial V}{\partial x}(x)$ and $V_{xx}(x)=\frac{\partial^2 V}{\partial x \partial x'}(x)$ are used for notational simplicity. The solution is obtained by finding a $V(x)$ such that the HJB equality, first-order condition, and $V_t(x) = 0$ hold. Conditional on an initial guess, $V^0(x)$, we calculate the coefficients $\mathbb{A}, \mathbb{B}, \mathbb{C}$ and $\mathbb{D}$ based on the flow utility and the evolution of the state variables. We substitute the calculated coefficients, rearrange the terms, and apply a backward finite difference to $V^0_t(x)$ to obtain the final expression

$$
\begin{align*}
\hat{V}(x) &= V^0(x) + [ \mathbb{A}(x,V^0,V^0_x,V^0_{xx})\hat{V}(x) + \mathbb{B}(x,V^0,V^0_x,V^0_{xx})\hat{V}_x(x) \\
& \quad + \frac{1}{2}tr[\mathbb{C}(x,V^0,V^0_x,V^0_{xx})'\hat{V}_{xx}(x)\mathbb{C}(x,V^0,V^0_x,V^0_{xx})] + \mathbb{D}(x,V^0,{V^0_x},V^0_{xx}) ] \Delta t .
\end{align*}
$$

We solve numerically for $\hat{V}(x)$ from this linear HJB system using the Preconditioned Bi-Conjugate Gradient Stabilized (BCGS) Krylov subspace (KSP) method from van der Vorst (1992), with ILU preconditioner.

The relative KSP residual tolerance statistic used to determine convergence of the solution for the linear system is given by

$$
\frac{\left\|P^{-1}(AV_n - b)\right\|_2}{\left\|P^{-1}(AV_0 - b)\right\|_2} \le \epsilon_{KSP},
$$

where $P^{-1}$ represents the ILU pre-conditioner and $AV=b$ represents the conditional linear system for a given value function $V$. The implementation of this step terminates when this statistic is less than $\epsilon_{KSP}$.

The false-transient residual is the statistic used to determine convergence for the "outer loop" of the algorithm. This statistic is computed as

$$
\left\|\frac{(V^{n+1}-V^n)}{\Delta\tau}\right\|_\infty \le \epsilon_{outer}
$$

where $V^{n+1}$ is the next iteration's value function, $V^n$ is the previous iteration's value function, and $\Delta \tau$ is the false transient step size. The implementation of this step terminates when this statistic is less than $\epsilon_{outer}$ or when the stated maximum iteration count is reached.

(finite-differences)=
## Finite-differences scheme

For calculating first- and second-order derivatives used to compute optimal controls, we use central differences at all interior points in the state space. At boundary points corresponding to the minimum state values we use forward differences, and at the maximum boundary values we apply backward differences. The benefit of using central differences is that they provide greater accuracy in approximating derivatives than one-sided differences, while also leading to faster convergence in iterative numerical algorithms when the algorithm converges.

Central differences, however, can generate spurious oscillations. Therefore, for each of our drift terms $\mathbb{B}_n(x;V,V_x,V_{xx})V_{x_n}(x)$, where $x_n \in \{\hat{k}, y, \hat{r}\}$, we use an implicit upwind finite-difference scheme that selects forward or backward differences depending on the sign of $\mathbb{B}_n$. This is implemented in the matrix assembly step for the PetSc solver by switching which neighbor enters the stencil based on the sign of $\mathbb{B}_n$. This yields a monotone discretization of the first-order part of the HJB operator at interior grid points. The second derivatives are approximated with central differences at all interior points in the state space, forward differences at minimum boundary values, and backward differences at maximum boundary values. The controls used in policy evaluation are computed from the model's first-order conditions using the derivative approximations described above.

Finally, we note two additional features that improve the numerical stability of our algorithm. First, our model includes non-trivial volatility terms, which help disperse local truncation errors. Second, we use relatively small time steps for the false-transient terms in our algorithm, which help dampen spurious oscillations and feedback loops. Together with the implicit upwind finite-difference scheme, these features promote numerical stability.

(boundary-conditions)=
## Boundary Conditions

Boundary conditions in our algorithm come in two forms. First, the specification of the damage information event introduces an explicit "physical" or "economic" boundary value at $\bar{y}$ in the form of a value matching condition. The value matching condition is given by the robust (certainty equivalent) boundary aggregation of the $L-1$ post-damage curvature jump continuation values

$$
V = -\xi_m \log \left[ \frac{1}{L-1} \sum_{\ell=1}^{L-1} \exp \left( -\frac{V^{\ell}}{\xi_m} \right) \right],
$$

which is achieved in the limit as the jump intensity goes to infinity. Numerically, this condition can be approximated by imposing a large (but finite) value of the damage information event arrival rate while maintaining the robust jump terms in the HJB equation. We use this approximation of the true value matching condition for the pre-damage curvature jump settings based on the values of the post-jump value function at $\bar{y}$ across the $\hat{k}$ and $\hat{r}$ dimensions of the state space.

Along the remaining boundaries of the state space, there are no obvious "physical" or "economic" boundary conditions to impose. Therefore, with the PDE operator discretized up to the boundary, we use the "natural" one-sided finite difference closure implied by our upwind finite-difference scheme at all remaining boundary points of the state space. Specifically, we apply forward differences at boundary points corresponding to the minimum state values and backward differences while at the maximum boundary values for both first- and second-order derivatives. To test the potential impact of these boundary conditions on the achieved numerical solutions, we informally explore different grid sizes and bounds on the state space and find essentially no change in the outcomes for these sensitivity analyses.

(numerical-accuracy)=
## Hyperparameters and numerical accuracy

{ref}`Table 24 <table-24>` shows the state variable domain space, the number of grid points used within the state domain, and the discretization step size along the state and false transient domains. {ref}`Table 25 <table-25>` provides the values used for the relaxation weight, the relative KSP residual tolerance, the false-transient residual tolerance, and the maximum iterations for each scenario. The "initial" and "warm" designations indicate the value-function initialization type. "Initial" denotes the first solve using the stage-specific initialization implemented by the solver: the default state-dependent guess for $W^{\ell}$ and the mean of the post-damage continuation values for $V$. "Warm" denotes initialization from an existing solution for the corresponding equation on the same grid. We note that the post-technology jump cases $W^{\ell,L}$ and $V^L$ have analytic solutions which we use in our main results. Thus, we do not include these cases in Tables {ref}`24 <table-24>` and {ref}`25 <table-25>` as no false-transient step size, relaxation weight, KSP residual tolerance, outer stopping tolerance, or maximum iterations are needed in those settings. The state domain, grid points, and grid spacing used to compute the numerical solutions for those settings match the pre-technology jump counterparts ($W^{\ell,L}$ uses the same values as $W^\ell$ and $V^L$ uses the same values as $V$). Importantly, the reported values reflect the choice of a broad state space domain with sufficient discretization to derive accurate numerical solutions.

(table-24)=

```{include} ../_static/table/table24_discretization.md
```

(table-25)=

```{include} ../_static/table/table25_convergence.md
```

{ref}`Table 26 <table-26>` shows the number of equations corresponding to each type of value function solved, the maximum absolute KSP residual, the maximum false-transient residual, and the maximum reported outer iterations. Note that the maximum absolute KSP residual provided by PETSc that we report can exceed or be significantly smaller than the relative KSP residual tolerance that is used as the stopping criteria statistic. The central takeaway from these reported values is that each of these outcomes demonstrates a high level of accuracy achieved in deriving our solutions, emphasizing reliability of the numerical solutions we have computed.

(table-26)=

```{include} ../_static/table/table26_residuals.md
```

Tables {ref}`27 <table-27>` - {ref}`28 <table-28>` provide details for additional accuracy results via a grid-refinement check. For these tests, we compare social valuation, optimal control, and value function outcomes across state space grid resolutions. {ref}`Table 27 <table-27>` summarizes the two different grid specifications used in this comparison. The grid used in the main body of the paper is $(n_{\hat{k}}, n_z, n_{\hat{r}}) = (51,201,71)$ for the post-damage curvature jump state and $(n_{\hat{k}}, n_Y, n_{\hat{r}}) = (51,101,71)$ for the pre-damage curvature jump state. We compare these results, referred to as the fine grid resolution case, with those for a coarse grid resolution with corresponding grids of $(n_{\hat{k}}, n_z, n_{\hat{r}}) = (26,101,36)$ for the post-damage curvature jump state and $(n_{\hat{k}}, n_Y, n_{\hat{r}}) = (26,51,36)$ for the pre-damage curvature jump state.

(table-27)=

```{include} ../_static/table/table27_grids.md
```

{ref}`Table 28 <table-28>` provides the value function, social valuation, and optimal control results for the two grid specifications. The magnitudes for differences in the value function outcomes are very modest, ranging between $.02\%$ and $.14\%$. The differences in social valuations and controls across grid resolutions are also relatively small, though somewhat larger than the value function outcomes. For the SVRD and SCGW, the differences range between $.15\%$ and $3.01\%$ in absolute value. For R&D investment and emissions, the differences range between $.02\%$ and $6.13\%$ in absolute value. The slightly larger differences reflect the impact of needing numerical derivatives to compute the social valuation and optimal control outcomes from the value function solutions. These results show that the grid choice for our model results provides a high level of accuracy for all of the main outcomes derived from our numerical solutions.

(table-28)=

```{include} ../_static/table/table28_grid_refinement.md
```

Our final accuracy check comes from evaluating the two methods used to compute our marginal social valuations. The first method is a "direct" computation using the finite-difference derivative of the HJB value function at the initial state, computed on the HJB solution grid. The second method is an "indirect" calculation based on the Monte Carlo evaluation of the marginal valuation formula given by

$$
\frac{\partial V}{\partial x}(X_0)\cdot\Lambda_0
\;=\;
\widetilde{E}\!\left[\int_0^{\infty} \mathrm{Dis}_t\,\big(\Lambda_t\cdot \mathrm{Scf}_t\big) dt
\;\Big|\; X_0,\Lambda_0\right].
$$

Summing over the flow i, ii and iii terms computed in this manner, and normalizing by marginal utility, we get an expression in the same units as our direct method. While the two methods are identical mathematically, the second method carries additional numerical errors from

* i) numerical derivative approximation (e.g., finite differences and grid discretization)
* ii) simulation-based approximation (e.g., time discretization and finite time boundary)
* iii) Monte Carlo sampling (e.g., sampling noise from finite stochastic pathways)

We first note that the Monte Carlo standard errors, computed from the cross-sectional dispersion of the simulation pathways, are sufficiently small ($0.002$–$0.006$) as to be inconsequential for the overall numerical error. To evaluate the "numerical derivatives" errors, we again use grid refinement to compare outcomes across specifications. If the gap between the indirect and direct methods is driven by derivative approximation, enhanced state variable grid resolution refinement should systematically shrink the difference between the results from the two specifications. We therefore compute the social valuations based on the indirect and direct methods using the two grid resolutions outlined in {ref}`Table 27 <table-27>` for each specification. As the fine grid solution has $2.0 \times$ the number of nodes along each dimension as the coarse grid solution, the first-order discretization errors should roughly halve between the coarse- and fine-grid solutions.

(table-29)=

```{include} ../_static/table/table29_indirect_direct.md
```

{ref}`Table 29 <table-29>` shows the results of our grid-refinement audit of the numerical discrepancies between the "direct" and "indirect" social valuation calculations for the technology jump only and full model specifications. The top panel, 29a, shows the outcomes for the technology jump only model. The bottom panel, 29b, shows the outcomes for the full model. Note that an accurate characterization of the grid refinement effect across methods requires an additional adjustment for the full model setting. Because the full model includes the damage information event, simulations are terminated at the sooner of the temperature anomaly threshold $\bar{y}$ or year 65, whichever comes first. This differs from the technology only jump model, for which we terminate the simulations at 120 years. This introduces a small negative terminal value error for the indirect method in the full model. We adjust for this error in the full model calculation under the indirect method by adding an interpolated value gradient term at the final simulation point. While overall this additional error is quite small, without this adjustment the grid refinement can appear to make the error gap worse in the baseline uncertainty aversion case because of the offsetting signs of the error term components. The grid refinement comparison across methods highlights the following main outcomes:

* Halving the grid spacing roughly halves the gap, consistent with first-order discretization error.

* The valuation gap between methods grows as $\xi_m$ falls, coinciding with evaluating enhanced nonlinearities from uncertainty aversion on the same grid generating larger approximation errors.

* The direct derivative valuations move by at most $3.0\%$ across grids, highlighting that most of the improvement in valuation discrepancy is coming from the indirect method errors.

While grid-refinement generates clear improvement in the numerical discrepancies across methods, we investigate the remaining errors to better understand the sources of numerical inaccuracies. We calculate implied derivative approximation errors from the "indirect" method by computing and aggregating up the point-wise residual derivative errors along each step of the simulation-based marginal social valuation construction. Removing this residual derivative approximation error captures nearly all of the remaining error. Therefore, the remaining errors after accounting for numerical derivative approximation ($-0.16\%$ to $-0.30\%$) must pertain to sources such as monthly Euler step for simulations, interpolation of outcomes to off-grid points, the evaluation of the terminal term at the last monthly node rather than at the exact boundary-crossing time, and right-endpoint accumulation of the jump-augmented discounting term.

(table-30)=

```{include} ../_static/table/table30_discrepancy.md
```

We characterize the nature and magnitude of these different error components in {ref}`Table 30 <table-30>`. Altogether, our characterization of the numerical errors highlights two key results. First, our numerical results appear to have a high level of accuracy. Second, neither the ordering of the social valuations across $\xi_m$ nor the relative importance of the three flows in our decompositions is affected by remaining numerical errors.

(value-derivatives)=
## Value function derivatives

The two sets of surfaces below are supplemental results that are not in the paper. They show the derivatives of the value function $V$ with respect to $\hat{r}$ and $y$ for the technology jump only model ([A simplified model with only technology jumps](09_technology_only.md)) on the Fine grid, sliced at the initial log capital, for $\xi_m = \infty$, $.1$ and $.05$. The axes labeled logR and Y show $\hat{r} = \log R$ and $y$.

```{raw} html
<style>
  .surface-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5em;
    margin-bottom: 1em;
  }
  .surface-buttons button {
    padding: 0.5em 1em;
    border: 2px solid #007acc;
    border-radius: 0.5em;
    background: white;
    color: #007acc;
    font-size: 1rem;
    cursor: pointer;
  }
  .surface-buttons button.active,
  .surface-buttons button:hover {
    background: #007acc;
    color: white;
  }
</style>
```

### $\frac{\partial V}{\partial \hat{r}}$

<div class="surface-switch">
  <div class="surface-buttons">
    <button type="button" data-case="inf" class="active">baseline (ξ<sub>m</sub> = ∞)</button>
    <button type="button" data-case="0.1">less aversion (ξ<sub>m</sub> = .1)</button>
    <button type="button" data-case="0.05">more aversion (ξ<sub>m</sub> = .05)</button>
  </div>
  <div class="surface-pane" data-case="inf">
    <iframe src="../_static/df_V_m3_surface_xik1e+05.html" title="Derivative of V with respect to log R for ξm = ∞" width="100%" height="470" style="border:none;"></iframe>
  </div>
  <div class="surface-pane" data-case="0.1" style="display:none;">
    <iframe src="../_static/df_V_m3_surface_xik0.1.html" title="Derivative of V with respect to log R for ξm = .1" width="100%" height="470" style="border:none;"></iframe>
  </div>
  <div class="surface-pane" data-case="0.05" style="display:none;">
    <iframe src="../_static/df_V_m3_surface_xik0.05.html" title="Derivative of V with respect to log R for ξm = .05" width="100%" height="470" style="border:none;"></iframe>
  </div>
</div>

### $\frac{\partial V}{\partial y}$

<div class="surface-switch">
  <div class="surface-buttons">
    <button type="button" data-case="inf" class="active">baseline (ξ<sub>m</sub> = ∞)</button>
    <button type="button" data-case="0.1">less aversion (ξ<sub>m</sub> = .1)</button>
    <button type="button" data-case="0.05">more aversion (ξ<sub>m</sub> = .05)</button>
  </div>
  <div class="surface-pane" data-case="inf">
    <iframe src="../_static/df_V_m2_surface_xik1e+05.html" title="Derivative of V with respect to y for ξm = ∞" width="100%" height="470" style="border:none;"></iframe>
  </div>
  <div class="surface-pane" data-case="0.1" style="display:none;">
    <iframe src="../_static/df_V_m2_surface_xik0.1.html" title="Derivative of V with respect to y for ξm = .1" width="100%" height="470" style="border:none;"></iframe>
  </div>
  <div class="surface-pane" data-case="0.05" style="display:none;">
    <iframe src="../_static/df_V_m2_surface_xik0.05.html" title="Derivative of V with respect to y for ξm = .05" width="100%" height="470" style="border:none;"></iframe>
  </div>
</div>

```{raw} html
<script>
  document.querySelectorAll(".surface-switch").forEach(function (group) {
    var buttons = group.querySelectorAll(".surface-buttons button");
    var panes = group.querySelectorAll(".surface-pane");
    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        buttons.forEach(function (other) {
          other.classList.toggle("active", other === button);
        });
        panes.forEach(function (pane) {
          pane.style.display = pane.dataset.case === button.dataset.case ? "block" : "none";
        });
      });
    });
  });
</script>
```

::::{hidden}
## Reproducing the tables

To reproduce Tables 24 to 30, run the scripts below from the root of the code repository after the {ref}`full model solutions <code-full-model>` on the Fine grid, the {ref}`grid comparison runs <code-grid-comparisons>` and the Fine grid simulations of [Uncertainty assessments](06_uncertainty_assessments.md) and [A simplified model with only technology jumps](09_technology_only.md) have finished. Each script submits Slurm jobs and returns at once, so start each script only after the jobs of the previous one have finished. Table 30 also uses the derivative audits kept in the repository under `output/diagnostics/full_model_fk_derivative/double_resolution/`.

~~~~bash
bash ./sbatch/update_results.sh --model full_model --grid-profile double_resolution --full-model-numerics-only --no-compile
bash ./sbatch/diagnostics/collect_full_model_grid_refinement.sh --paper-tables-only
bash ./sbatch/diagnostics/collect_full_model_fk_terminal.sh --scratch "/scratch/$(id -un)/full_model"
bash ./sbatch/diagnostics/collect_tech_only_grid_refinement.sh --comparison-grid finer_grid
bash ./sbatch/diagnostics/collect_tech_only_grid_refinement.sh --comparison-grid double_resolution
bash ./sbatch/diagnostics/collect_full_model_fk_terminal.sh --paper-comparison-only
~~~~

After the run finishes, you should have output files named `numerical_discretization.tex`, `numerical_convergence_criteria.tex` and `convergence_diagnostics.tex` (Tables 24 to 26) under `output/tables/<dataset>/`, and `grid_specifications.tex`, `grid_refinement_comparison.tex`, `indirect_direct_comparison.tex` and `error_summary.tex` (Tables 27 to 30) under `output/tables/<dataset>/grid_refinement/`, where `<dataset>` is the Fine grid directory of the full model, as listed in {ref}`Grids <code-grids>`. Copies named `Table24_numerical_discretization.tex` to `Table30_error_summary.tex` are written to `results_in_paper/`.

Source scripts:
* `sbatch/update_results.sh`
* `python/update_results.py`
* `sbatch/diagnostics/collect_full_model_grid_refinement.sh`
* `python/diagnostics/collect_grid_refinement.py`
* `sbatch/diagnostics/collect_full_model_fk_terminal.sh`
* `python/diagnostics/collect_full_model_fk_terminal.py`
* `sbatch/diagnostics/collect_tech_only_grid_refinement.sh`
* `python/diagnostics/collect_tech_only_grid_refinement.py`
::::
