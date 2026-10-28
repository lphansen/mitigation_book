# Comparison to a real options formulation

This page is Appendix L of the paper.

As we noted in Section 10 of the paper, there are similarities, but also differences, in our R&D investment problem and a real options problem.

The decision-maker decides when to exercise the option with a known cost of doing so. Other than access to this stochastic payoff, the decision-maker can invest in a riskless technology. In the first specification, exercising the option provides a discrete payoff. In the second specification, exercising the option entitles the decision maker with access to a stochastic flow. To support our investigation, we make the two payoffs comparable by scaling the flow so that the present values of the discrete payoff and flow payoff processes are the same in the absence of uncertainty about the payoff dynamics.

(discrete-payoff)=
## Discrete-payoff model

Consider a robust counterpart to Model I in {cite:t}`MiaoWang:2007`. We let the utility be linear in consumption and the income process be:

$$
dY_t = \nu dt +\sigma dW_t.
$$

For purposes of illustration, we set $\nu = .1$ and $\sigma = .3$. When the option is exercised, we assume a payoff equal to the discounted present value (with a constant discount rate $\delta$) of current and future $Y_t$ minus a prespecified cost $I$. In our illustration, we set $I = 10$. The risk-free rate and subjective rate of discount are the same, which we set as $\delta = .02$. We refer to this as the *discrete-payoff model*.

The post exercise value function satisfies:

$$
\max_c - \delta V^0 + \delta c + V^0_w(\delta w - c) = 0,
$$

which can be solved by setting $V^0(w) = \delta w$. The value function, $V$, prior to exercising the option solves the HJB equation:

$$
\max_c \min_h - \delta V + \delta c + V_w( \delta w - c) + V_y \nu + \sigma h V_y + \frac{\xi_m}{2} h^2 + \frac {\sigma^2}{2} V_{yy} .
$$

Guess that $V(w,y) = \delta[ w + G(y)]$. Then

$$
0= - \delta G + G_y \nu + \frac {\sigma^2} 2 G_{yy} - \frac {\sigma^2 \delta } {2 \xi_m} (G_y)^2 \tag{29}
$$

where the minimizing $h$ solves:

$$
h^* = - \frac {\sigma} {\xi_m} V_y = - \frac {\sigma \delta } {\xi_m} G_y. \tag{30}
$$

The discounted expected value of the option payoff with income realization, $y$, is

$$
\frac 1 \delta y + \frac \nu {\delta^2}
$$

obtained by solving the Feynman-Kac equation:

$$
0 = - \delta F + y + \nu F_y + \frac {\sigma^2} 2 F_{yy}.
$$

Thus, value matching gives:

$$
\delta G({\bar y}) = \bar y + \frac \nu {\delta} - \delta I,
$$

and smooth pasting gives

$$
\delta G_y ({\bar y}) = 1.
$$

(flow-payoff)=
## Flow-payoff model

We next change the payoff on the investment by letting it be continuous, given by the $Y$ process. We refer to this as the *flow-payoff model.* The value function, $V^o$, after exercising satisfies the HJB equation:

$$
\max_c \min_h - \delta V^o + \delta c + V^o_w( \delta w + y - c) + \nu V^o_y + \sigma h V_y^o +{\frac 1 2}\sigma^2 V^o_{yy} + \frac{\xi_m}{2} h^2 = 0.
$$

We guess that $V^o(w,y) = \delta[w + F(y)]$. With this guess, we solve

$$
0= - \delta F + y + F_y \nu + \frac {\sigma^2} 2 F_{yy} - \frac {\sigma^2 \delta } {2 \xi_m} (F_y)^2
$$

where

$$
h^* = - \frac{\sigma}{\xi_m} V^o_y = - \frac{\delta \sigma}{\xi_m} F_y.
$$

The solution for $F$ is:

$$
F(y) = {\frac 1 \delta} \left[ y + \frac \nu {\delta} - \frac {\sigma^2}{2 \xi_m \delta} \right] ,
$$

implying that $h^* = - \sigma/\xi_m$.

As with the discrete-payoff specification, the value function prior to the option being exercised solves (29) with $V(w,y) = \delta[ w + G(y)]$. The minimizing $h^*$ is given by formula (30). The value-matching condition is:

$$
\delta G({\bar y}) = \delta [F({\bar y}) - I] = \bar y + \frac \nu {\delta} - \frac {\sigma^2}{2 \xi_m \delta } - \delta I
$$

and the smooth-pasting condition is:

$$
\delta G_y({\bar y}) = \delta F_y({\bar y}) = 1 .
$$

(thresholds)=
## Exercise thresholds

Notice that the value matching condition is the same for both models in the limiting case in which $\xi_m \rightarrow \infty$. In both models, the exercise threshold $\bar y$ satisfies: $\delta G_y\left( \bar y \right) = 1$ even for $\xi_m < \infty$, but, of course, the $G$ functions are different. {ref}`Figure 13 <fig-13>` plots the derivatives for each model specification and for alternative values of the robustness parameter, $\xi_m$. For the discrete-payoff model, the derivatives decrease with $\xi_m$, resulting in higher values of $y$ when the option is exercised. For the stochastic flow-payoff model the derivatives increase with $\xi_m$, resulting in lower values of the threshold $\bar y$.

(fig-13)=

<div id="fig-13" style="
     display:flex;
     gap:18px;
     justify-content:center;
     align-items:flex-start;
     flex-wrap:wrap;
">
  <figure style="margin:0; width:340px; max-width:100%;">
    <img src="../_static/paper/Figure13_model1_derivative.png"
         alt="Plots of the value function derivatives across different uncertainty aversion values for the discrete-payoff real options model example"
         style="width:100%; height:auto;">
    <figcaption style="text-align:center; font-size:0.85em;">(A) discrete-payoff model</figcaption>
  </figure>
  <figure style="margin:0; width:340px; max-width:100%;">
    <img src="../_static/paper/Figure13_model3_derivative.png"
         alt="Plots of the value function derivatives across different uncertainty aversion values for the flow-payoff real options model example"
         style="width:100%; height:auto;">
    <figcaption style="text-align:center; font-size:0.85em;">(B) flow-payoff model</figcaption>
  </figure>
</div>

Figure 13: Plots of $\delta G_y$ for different values of $\xi_m$.

Consistent with this finding, we report in {ref}`Figure 14 <fig-14>` that uncertainty aversion has opposite implications for the threshold $\bar y$ for the two payoff specifications. The implied uncertainty aversion for low values of $\xi_m$ makes the investor more bullish on the investment for the discrete payoff specification in the sense that there is a lower investment threshold. The outcome gets reversed with the stochastic flow payoff: the investor is less bullish on the investment and exercises the option at a higher threshold with enhanced aversion. By design, the two curves converge when $\xi_m \rightarrow \infty$.

(fig-14)=

<div id="fig-14" style="display:flex; justify-content:center; align-items:center;">
  <img src="../_static/paper/Figure14_threshold_plot.png"
       alt="Exercise threshold solution for each real option example model as a function of the uncertainty aversion parameter"
       style="width:450px; max-width:100%; height:auto;">
</div>

Figure 14: Solution of exercise threshold $\overline{y}$ for each model as functions of the robustness parameter, $\xi_m$.

We plot the pre-exercise drift distortions $h^*$ in {ref}`Figure 15 <fig-15>`. The post-jump distortions are zero for the discrete-payoff specification, and, by the smooth pasting condition, equal to the distortion at the time the option is exercised for the flow-payoff specification. Recall that the $h^*$'s are expressed as drifts in a standard Brownian increment. They are not extreme for these illustrations, as the magnitude of the local mean distortion never exceeds ten percent of the standard deviation. The drift distortions prior to exercise are a bit larger in magnitude for the discrete-payoff specification.

(fig-15)=

<div id="fig-15" style="
     display:flex;
     gap:18px;
     justify-content:center;
     align-items:flex-start;
     flex-wrap:wrap;
">
  <figure style="margin:0; width:340px; max-width:100%;">
    <img src="../_static/paper/Figure15_model1_distortion.png"
         alt="Plots of the probability distortions across different uncertainty aversion values for the discrete-payoff real options model example"
         style="width:100%; height:auto;">
    <figcaption style="text-align:center; font-size:0.85em;">(A) discrete-payoff model</figcaption>
  </figure>
  <figure style="margin:0; width:340px; max-width:100%;">
    <img src="../_static/paper/Figure15_model3_distortion.png"
         alt="Plots of the probability distortions across different uncertainty aversion values for the flow-payoff real options model example"
         style="width:100%; height:auto;">
    <figcaption style="text-align:center; font-size:0.85em;">(B) flow-payoff model</figcaption>
  </figure>
</div>

Figure 15: Plots of $h^*$ for different values of $\xi_m$.

In both cases, robustness concerns induce more cautious assessments of the payoff prospects. In the discrete-payoff specification, the uncertainty is resolved as soon as the payoff is exercised, increasing the valuation; while in the flow-payoff specification, the post exercise valuation is diminished under robustness concerns because of the continued uncertainty about future payoffs.

Although there are intriguing similarities between this comparison of real options in different environments and our findings, the investment opportunities are quite different. Rather than an exercise decision, our social planner can make investments that increase the likelihood of a discovery. Uncertainty aversion makes the planner skeptical about the payoff horizon in our analysis. These differences make our uncertainty aversion impact not monotone as displayed in {ref}`Table 21 <table-21>` and in contrast to the real options findings reported in {ref}`Figure 14 <fig-14>`.

::::{hidden}
## Reproducing the figures

To reproduce Figures 13, 14, and 15, run the script below from the root of the code repository, as described in {ref}`Running the scripts <code-running>`. The script does not need any model solutions.

~~~~bash
bash ./sbatch/appendix_illustrations.sh
~~~~

After the run finishes, you should have output files named `model1_derivative.png` and `model3_derivative.png` (Figure 13), `threshold_plot.png` (Figure 14), and `model1_distortion.png` and `model3_distortion.png` (Figure 15) under `output/figures/<dataset>/appendix_illustrations/`, where `<dataset>` is the Coarse grid directory of the full model, as listed in {ref}`Grids <code-grids>`. The same run also writes Figures 16, 17, and 18 of [Online Appendix P](14_online_p.md).

Source scripts:
* `sbatch/appendix_illustrations.sh`
* `python/appendix_illustrations.py`
::::
