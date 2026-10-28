# O. HJB Equations with 2 Technology Steps

As we are using the simplified model setting with only technology jumps, there are only three possible jump states to consider in this setting: the final technology state, the intermediate technology state, and the pre-technology jump state. We denote when the intermediate technology jump has occurred by a superscript $\tilde{L}$. This intermediate-technology jump realization corresponds to the state where the abatement technology parameter is given by $\tilde{\phi}_0 = \frac{1}{2}\phi_0$. We denote when the final technology jump has occurred by a superscript $L$. This final-technology jump realization corresponds to the state where the abatement technology parameter is given by $\phi^L_0 = 0$. As noted in [Section 9](09_technology_only.md), we close down all uncertainty channels except for the technology jump distortions in this simplified model setting with only technology jumps.

(final-technology)=
## Final technology

The value function characterization for the final-technology jump state is essentially identical to those given in the baseline post-damage, post-technology jump setting. This is because $\phi_0 = 0$, so full abatement and no R&D investment are the Planner's optimal choices. Therefore, temperature remains constant and R&D knowledge stock is irrelevant to the Planner and so the problem simplifies to the same capital-based settings as before. We refer the readers to [Appendix A](03_hjb_equations.md) for details related to this setting.

(intermediate-technology)=
## Intermediate technology and pre-technology jump

The remaining two cases are the HJB equation for the value function $V^{\tilde{L}}$ for after the intermediate technology jump realization and the value function $V$ prior to any jump realization in this two-step technology setting. For the intermediate technology state HJB equation, the value of the abatement technology parameter is $\tilde{\phi}_0$, the value function realized when a jump occurs is $V^{L}$, and the relevant jump intensity and probability distortion used for the jump process ambiguity concerns are given by $\mathcal{J}^{L}$ and $g^{L}$. For the pre-technology jump state HJB equation, the value of the abatement technology parameter is $\phi_0$, the value function realized when a jump occurs is $V^{\tilde{L}}$, and the relevant jump intensity and probability distortion used for the jump process ambiguity concerns are given by $\mathcal{J}^{\tilde{L}}$ and $g^{\tilde{L}}$.

Therefore, the complete HJB equation for the intermediate technology state is:

$$
\begin{align*}
0 = & \max_{i^k, i^r, e} \, \min_{g^L} \, \delta \log \left[\alpha -i^{k}-i^{r}-\alpha  \tilde{\phi}_0 \left(1-\frac{e}{\beta \alpha k}\right)^{\phi_1} \right] + \delta \hat{k} - \delta {\hat n}(y) - \delta V^{\tilde{L}}(\hat{k}, y, \hat{r})  \\
& + \frac{\partial V^{\tilde{L}}}{\partial \hat{k}}(\hat{k}, y, \hat{r})  \left[ -\mu_{k}+ i^{k}-\frac{\kappa}{2}\left(i^{k}\right)^{2}-\frac{|\sigma_{k}|^{2}}{2} \right] +  \frac{\partial^2 V^{\tilde{L}}}{\partial \hat{k} \, \partial \hat{k}'}(\hat{k}, y, \hat{r}) \frac{|\sigma_{k}|^{2}}{2} \\
& + \frac{\partial V^{\tilde{L}}}{\partial y}(\hat{k}, y, \hat{r})  \bar{\theta} e  + \frac{\partial^2 V^{\tilde{L}}}{\partial y \, \partial y'}(\hat{k}, y, \hat{r}) \frac{|\varsigma|^{2}}{2}e^{2} \\
& + \frac{\partial V^{\tilde{L}}}{\partial \hat{r}}(\hat{k}, y, \hat{r})  \left[ -\zeta + \psi_{0}(i^{r})^{\psi_{1}}\exp\left( -\psi_{1} \left(\hat{r} - \hat{k}\right)\right)-\frac{|\sigma_{r}|^{2}}{2} \right] +\frac{\partial^2 V^{\tilde{L}}}{\partial \hat{r} \, \partial \hat{r}'}(\hat{k}, y, \hat{r}) \frac{|\sigma_{r}|^{2}}{2} \\
& +  \mathcal{J}^{L} g^{L} \left[ V^{L}(\hat{k},y,\hat{r})-V^{\tilde{L}}(\hat{k},y,\hat{r}) \right] + \xi_m  \mathcal{J}^{L} \left[ 1-g^{L}+g^{L} \log g^{L} \right],
\end{align*}
$$

and the complete HJB equation for the pre-technology jump state is:

$$
\begin{align*}
0 = & \max_{i^k, i^r, e} \, \min_{g^{\tilde{L}}} \, \delta \log \left[\alpha -i^{k}-i^{r}-\alpha  \phi_0 \left(1-\frac{e}{\beta \alpha k}\right)^{\phi_1} \right] + \delta \hat{k} - \delta {\hat n}(y) - \delta V(\hat{k}, y, \hat{r})  \\
& + \frac{\partial V}{\partial \hat{k}}(\hat{k}, y, \hat{r})  \left[ -\mu_{k}+ i^{k}-\frac{\kappa}{2}\left(i^{k}\right)^{2}-\frac{|\sigma_{k}|^{2}}{2} \right] +  \frac{\partial^2 V}{\partial \hat{k} \, \partial \hat{k}'}(\hat{k}, y, \hat{r}) \frac{|\sigma_{k}|^{2}}{2} \\
& + \frac{\partial V}{\partial y}(\hat{k}, y, \hat{r}) \bar{\theta} e + \frac{\partial^2 V}{\partial y \, \partial y'}(\hat{k}, y, \hat{r}) \frac{|\varsigma|^{2}}{2}e^{2} \\
& + \frac{\partial V}{\partial \hat{r}}(\hat{k}, y, \hat{r})  \left[ -\zeta + \psi_{0}(i^{r})^{\psi_{1}}\exp\left( -\psi_{1} \left(\hat{r} - \hat{k}\right)\right)-\frac{|\sigma_{r}|^{2}}{2} \right] +\frac{\partial^2 V}{\partial \hat{r} \, \partial \hat{r}'}(\hat{k}, y, \hat{r}) \frac{|\sigma_{r}|^{2}}{2} \\
& +  \mathcal{J}^{\tilde{L}} g^{\tilde{L}} \left[ V^{\tilde{L}}(\hat{k},y,\hat{r})-V(\hat{k},y,\hat{r}) \right] + \xi_m  \mathcal{J}^{\tilde{L}} \left[ 1-g^{\tilde{L}}+g^{\tilde{L}} \log g^{\tilde{L}} \right].
\end{align*}
$$

Note that the constraints $0 \le e  \le \beta \alpha k$,  $g^{\tilde{L}} \ge 0$, and $g^L \ge 0$ still hold as in the main specification. In addition, the value of $R_t$ is reinitialized at $R_0$ in the intermediate technology state for specification {ref}`iii <two-step>`).
