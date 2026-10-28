| error source | nature | error size | behavior |
|---|---|---|---|
| numerical derivative approximation | discretization error in the FK representation | $\approx 1\%$ ($\xi_m=\infty$); $\approx 2\%$–$5\%$ (finite $\xi_m$) | $\sim$ halves when grid spacing halves; grows as $\xi_m$ falls |
| time discretization, boundary approximation | residual numerical errors | $\lesssim 0.3\%$ | small but statistically distinguishable from zero |
| Monte Carlo sampling | random error | $\approx 0.05$–$0.07\%$ (s.e.) | falls as $1/\sqrt{N}$; irrelevant |

Table 30: Decomposition of the direct-vs-indirect discrepancy for the full model with fine grid resolution.
