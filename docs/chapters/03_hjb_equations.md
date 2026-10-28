# HJB Equations

This page is Appendix A of the paper.

As in the main text, throughout the appendix we let lower-case variables capture potential realizations of random vectors.

As part of dynamic programming backward induction, we start by giving the post-jump HJB equations. The post-jump value functions are then inputs into the pre-jump HJB equations. Recall that there are $L$ possible jump realizations from the pre-jump setting: $L-1$ potential damage curvature realizations and one technology jump realization.

(transformation)=
## A numerically convenient transformation

Prior to constructing post-damage curvature jump value functions, we describe two numerically convenient transformations. Note that the damage function in this setting depends upon the temperature at which the damage information event occurred, $\hat{y}$. This dependence has a special structure that we exploit in computations. At the time of the jump this new state variable will be initialized at $\overline{y}$. Integrating, we construct the log damage function:

$$
\hat{n}(y) = \left\{
\begin{matrix} & \lambda_1 y + \frac{\lambda_2}{2} y^2 & \textrm{pre damage event} \cr
& \lambda_1 y + \frac{\lambda_2}{2} \hat{y}^2 + \frac{\lambda_2}{2} (y - \hat{y} + \overline{y})^2 + \frac{\lambda_3(\ell)}{2} (y - \hat{y})^2 - \frac{\lambda_2}{2} (\overline{y})^2 & \textrm{post damage event}. \end{matrix} \right. \tag{19}
$$

Note that this construction depends implicitly on both $\ell$ and $\hat{y}$, a dependence that we now make more explicit. Define a new state variable by transforming the temperature anomaly:

$$
z \overset{\mathrm{def}}{=} y - \hat{y} + \overline{y}.
$$

We transform this log damage function for $y \ge \hat{y}$ by constructing:

$$
\begin{align*}
\hat{m}(z ; \ell) & \overset{\mathrm{def}}{=} \hat{n}(y ; \ell, \hat{y}) - (\lambda_1 \hat{y} + \frac{1}{2} \lambda_2 \hat{y}^2) \\
&= \lambda_1 (y - \hat{y}) + \frac{1}{2} \lambda_2 (y - \hat{y} + \overline{y})^2 + \frac{1}{2} \lambda_3(\ell) (y - \hat{y})^2 - \frac{1}{2} \lambda_2 (\overline{y})^2 \\
&= \lambda_1 (z - \overline{y}) + \frac{1}{2} \lambda_2 z^2 + \frac{1}{2} \lambda_3(\ell) (z - \overline{y})^2 - \frac{1}{2} \lambda_2 (\overline{y})^2
\end{align*}
$$

Importantly, the $\hat{m}$ is constructed so as to depend on $z$, but not separately on $y$ and $\hat{y}$.

We construct some post technology jump value functions by first using $z$ and $\hat{m}$ and then transforming these value functions by subtracting the adjustment:

$$
\lambda_1 \hat{y} + \frac{1}{2} \lambda_2 \hat{y}^2 .
$$

We subtract this term because log damages enter the HJB equations with a negative sign since damages reduce the utility of the planner. This two-step approach gives us a numerically convenient way to capture dependence of value functions on the temperature anomaly realization, $\hat{y}$, when the damage information event takes place.

(hjb-post-jump)=
## Post damage and technology jumps

We start with HJB equation after both a technology jump and one of the damage curvature jumps has taken place. Denote the resulting value function $V^{\ell,L,\hat{y}}$ for $1 \le \ell \le L-1$ and the value function counterpart constructed using $z$ and $\hat{m}$ as $W^{\ell,L}$. Importantly, $W^{\ell,L}$ does not depend on $\hat{y}$.

Since we are conditioning on the technology jump having already occurred, $\phi_0 = 0$, and there is no incentive for a further R&D investment targeted for the discovery of clean technology. The resulting output technology is:

$$
C_t + I_t^k = \alpha K_t .
$$

For the relevant state space, control set, and distortion set we use

$$
x = \{ z, \hat{k} \}, \qquad \Phi = \{ i^k \}, \qquad \Gamma = \{ h \}.
$$

Observe that temperature no longer varies over time. Since we use the transformed temperature variable $z$, we also use $\hat{m}$ instead of $\hat{n}$ in the HJB equation for $W^{\ell,L}$.

To compute $W^{\ell,L}$, we solve the HJB equation

$$
\begin{align*}
0 = & \max_{i^k}\min_{h^k}\ \delta\log(\alpha - i^k) + \delta\hat{k} - \delta\hat{m}(\cdot;\ell) - \delta W^{\ell,L} + \xi_m\frac{\left|h^k\right|^2}{2} \\
& + \frac{\partial W^{\ell,L}}{\partial\hat{k}}\left[-\mu_k + i^k - \frac{\kappa}{2}\left(i^k\right)^2 - \frac{\left|\sigma_k\right|^2}{2} + \sigma_k h\right] + \frac{\partial^2 W^{\ell,L}}{\partial\hat{k}^2}\frac{\left|\sigma_k\right|^2}{2}
\end{align*}
$$

Using guess and verify, the robustly optimal choice variables are given by:

$$
\begin{align*}
h^{*} = & -\frac{1}{\xi_m} \sigma_k \\
i^{k*} = & \frac{\left( 1 + \alpha \kappa \right) - \sqrt{\left( 1 + \alpha \kappa \right)^2 - 4 \kappa \left( \alpha - \delta \right)}}{2 \kappa},
\end{align*}
$$

and the value function by:

$$
W^{\ell,L}\left(z, \hat{k}\right) = \log \left( \alpha - i^{k*} \right) - \frac{1}{2 \delta \xi_m} \left|\sigma_k\right|^2 + \frac{1}{\delta} \left[ - \mu_k + i^{k*} - \frac{\kappa}{2} \left( i^{k*} \right)^2 - \frac{\left|\sigma_k\right|^2}{2} \right] + \hat{k} - \hat{m}(z;\ell) .
$$

As a second step, we then construct:

$$
V^{\ell,L,\hat{y}} = W^{\ell,L} - \left( \lambda_1 \hat{y} + \frac{1}{2} \lambda_2 \hat{y}^2 \right) ,
$$

which follows since the damage adjustment, $\hat{n}$, enters negatively into the discounted objective of the planner.

(post-damage)=
## Post-damage but pre-technology

We next compute each of the post-damage curvature jump, pre-technology jump value functions $V^{\ell,\hat{y}}$ where only a damage curvature jump has been realized for $\ell = 1,..., L-1$.

Again, we start with the HJB for the value functions $W^{\ell}$, $1 \le \ell \le L-1$ using $\hat{m}$. The modified state vector $x$, control set $\Phi$, and distortion set $\Gamma$ are

$$
x = \{ \hat{k}, z, \hat{r} \}, \qquad \Phi = \{ i^k, i^r, e \}, \qquad \Gamma = \{ h, q(\theta), g^L \}.
$$

with $0 \le e \le \beta \alpha k$, $q(\theta) \ge 0, \sum_{\theta \in \Theta} q(\theta)=1$, and $g^L \ge 0$. The function $W^\ell$ solves:

$$
\begin{align*}
0 = & \max_{i^k, i^r, e}\ \min_{h, q(\theta), g^L}\ \delta\log\left[\alpha - i^k - i^r - \alpha\phi_0\left(1 - \frac{e}{\beta\alpha k}\right)^{\phi_1}\right] + \delta\hat{k} - \delta\hat{m}(z;\ell) - \delta W^\ell(\hat{k}, z, \hat{r}) \\
& + \frac{\partial W^\ell}{\partial\hat{k}}(\hat{k}, z, \hat{r})\left[-\mu_k + i^k - \frac{\kappa}{2}\left(i^k\right)^2 - \frac{|\sigma_k|^2}{2} + \sigma_k h\right] + \frac{\partial^2 W^\ell}{\partial\hat{k}\,\partial\hat{k}'}(\hat{k}, z, \hat{r})\frac{|\sigma_k|^2}{2} \\
& + \frac{\partial W^\ell}{\partial y}(\hat{k}, z, \hat{r})\,e\left[\sum_{\theta\in\Theta}\theta q(\theta)\right] + \frac{\partial^2 W^\ell}{\partial y\,\partial y'}(\hat{k}, z, \hat{r})\frac{|\varsigma|^2}{2}e^2 \\
& + \frac{\partial W^\ell}{\partial\hat{r}}(\hat{k}, z, \hat{r})\left[-\zeta + \psi_0 (i^r)^{\psi_1}\exp\left(-\psi_1\left(\hat{r} - \hat{k}\right)\right) - \frac{|\sigma_r|^2}{2} + \sigma_r h\right] + \frac{\partial^2 W^\ell}{\partial\hat{r}\,\partial\hat{r}'}(\hat{k}, z, \hat{r})\frac{|\sigma_r|^2}{2} \\
& + \mathcal{J}^L g^L\left[W^{\ell,L}(\hat{k}, z, \hat{r}) - W^\ell(\hat{k}, z, \hat{r})\right] + \xi_m\mathcal{J}^L\left[1 - g^L + g^L\log g^L\right] + \frac{\xi_m}{2}h'h + \xi_a\sum_{\theta\in\Theta} q(\theta)\log\left(\frac{q(\theta)}{p(\theta)}\right).
\end{align*}
$$

where, as an input, we impose function $W^{\ell,L}$ as constructed in [Post damage and technology jumps](hjb-post-jump).

As a second step we compute:

$$
V^{\ell,\hat{y}}(\hat{k},y,\hat{r}) = W^{\ell}(\hat{k},\, y-\hat{y}+\bar{y},\, \hat{r}) - \left(\lambda_1{\hat y}+ \frac 1 2 \lambda_2 {\hat y}^2\right).
$$

Importantly,

$$
V^{\ell,L,\hat{y}} - V^{\ell,\hat{y}} = W^{\ell,L} - W^\ell,
$$

which is needed to make the HJB equation for $W^\ell$ relevant for the construction of $V^{\ell,\hat{y}}$.

(post-technology)=
## Post-technology but pre-damage

Let $V^L$ denote the pre-damage information event, post-technology jump value function. Once the technology jump has happened the subsequent damage curvature jumps are inconsequential. This is true because temperature anomaly no longer increases in response to economic production since $\phi_0^L = 0$ and it remains at a level for which damage curvature uncertainty is inconsequential.

In this case, we directly construct $V^L$ restricting the temperature anomaly to reside in $0 \le y < \hat{y}$. The function, $V^L$ can be computed in essentially the same way as $W^{\ell,L}$, described in [Post damage and technology jumps](hjb-post-jump). The state vector $x$, control set $\Phi$, and distortion set $\Gamma$ are

$$
x = \{ \hat{k} \}, \qquad \Phi = \{ i^k \}, \qquad \Gamma = \{ h \}.
$$

The HJB equation for $V^L$ is

$$
\begin{align*}
0 = & \max_{i^k}\min_{h^k}\ \delta\log(\alpha - i^k) + \delta\hat{k} - \delta\hat{n}(\cdot;\ell) - \delta V^L + \xi_m\frac{\left|h^k\right|^2}{2} \\
& + \frac{\partial V^L}{\partial\hat{k}}\left[-\mu_k + i^k - \frac{\kappa}{2}\left(i^k\right)^2 - \frac{\left|\sigma_k\right|^2}{2} + \sigma_k h\right] + \frac{\partial^2 V^L}{\partial\hat{k}^2}\frac{\left|\sigma_k\right|^2}{2},
\end{align*}
$$

which again can be solved using guess and verify, applying a close counterpart to the solution in [Post damage and technology jumps](hjb-post-jump). Note, from the construction of equation (19) that $\hat{n}$ does not depend on $\ell$ over the temperature anomaly domain $0 \le y < \hat{y}$.

(pre-jump)=
## Pre-technology and pre-damage

Finally, we present the HJB equation for the value function $V$ prior to any jump realization. We need as inputs to this equation the post jump value functions: $V^{\ell,\hat{y}}$ for $1 \le \ell \le L-1$ and $V^L$. Importantly, we only need the function $V^{\ell,\hat{y}}$ for $\hat{y} = y$ as prior to jumps being realized, the recursive equation compares the current continuation value, $V$, to what happens hypothetically at temperature anomaly $y$ if a jump happens to occur at $y$. Thus we define:

$$
V^{\ell} \overset{\mathrm{def}}{=} V^{\ell,y}
$$

for $\ell = 1, 2, ... L-1$. The state vector $x$, control set $\Phi$, and distortion set $\Gamma$ are

$$
x = \{ \hat{k}, y, \hat{r} \}, \qquad \Phi = \{ i^k, i^r, e \}, \qquad \Gamma = \{ h, q(\theta), (g^\ell)_{\ell=1}^{L} \}
$$

with $0 \le e \le \beta \alpha k$, $q(\theta) \ge 0, \sum_{\theta \in \Theta} q(\theta)=1$, $g^{\ell} \ge 0$, and $g^L \ge 0$. The complete HJB equation is:

$$
\begin{align*}
0 = & \max_{i^k, i^r, e}\ \min_{h, q(\theta), g^\ell, g^L}\ \delta\log\left[\alpha - i^k - i^r - \alpha\phi_0\left(1 - \frac{e}{\beta\alpha k}\right)^{\phi_1}\right] + \delta\hat{k} - \delta\hat{n}(y) - \delta V(\hat{k}, y, \hat{r}) \\
& + \frac{\partial V}{\partial\hat{k}}(\hat{k}, y, \hat{r})\left[-\mu_k + i^k - \frac{\kappa}{2}\left(i^k\right)^2 - \frac{|\sigma_k|^2}{2} + \sigma_k h\right] + \frac{\partial^2 V}{\partial\hat{k}\,\partial\hat{k}'}(\hat{k}, y, \hat{r})\frac{|\sigma_k|^2}{2} \\
& + \frac{\partial V}{\partial y}(\hat{k}, y, \hat{r})\,e\left[\sum_{\theta\in\Theta}\theta q(\theta)\right] + \frac{\partial^2 V}{\partial y\,\partial y'}(\hat{k}, y, \hat{r})\frac{|\varsigma|^2}{2}e^2 \\
& + \frac{\partial V}{\partial\hat{r}}(\hat{k}, y, \hat{r})\left[-\zeta + \psi_0 (i^r)^{\psi_1}\exp\left(-\psi_1\left(\hat{r} - \hat{k}\right)\right) - \frac{|\sigma_r|^2}{2} + \sigma_r h\right] + \frac{\partial^2 V}{\partial\hat{r}\,\partial\hat{r}'}(\hat{k}, y, \hat{r})\frac{|\sigma_r|^2}{2} \\
& + \sum_{\ell=1}^L \mathcal{J}^\ell g^\ell\left[V^\ell(\hat{k}, y, \hat{r}) - V(\hat{k}, y, \hat{r})\right] + \xi_m\sum_{\ell=1}^L \mathcal{J}^\ell\left[1 - g^\ell + g^\ell\log g^\ell\right] + \frac{\xi_m}{2}h'h + \xi_a\sum_{\theta\in\Theta} q(\theta)\log\left(\frac{q(\theta)}{p(\theta)}\right).
\end{align*}
$$
