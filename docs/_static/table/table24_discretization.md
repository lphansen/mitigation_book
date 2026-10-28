| Value Function | State domain $[\hat{k}] \times [Y/z] \times [\hat{r}]$ | Grid points $n_{\hat{k}} \times n_Y/n_z \times n_{\hat{r}}$ | Grid spacing $(\Delta \hat{k},\Delta Y/\Delta z,\Delta \hat{r})$ | False-transient step $(\Delta \tau)$ |
|---|---:|---:|---:|---:|
| $W^\ell$ (initial) | $[4,9]\times[0,5]\times[1,8]$ | $51\times201\times71$ | $(0.1,0.025,0.1)$ | $0.1$ |
| $W^\ell$ (warm start) | $[4,9]\times[0,5]\times[1,8]$ | $51\times201\times71$ | $(0.1,0.025,0.1)$ | $0.025$ |
| $V$ (initial and warm) | $[4,9]\times[0,2.5]\times[1,8]$ | $51\times101\times71$ | $(0.1,0.025,0.1)$ | $0.05$ |

Table 24: Numerical discretization criteria. Reported values are for the full-model baseline-parameter solutions. The middle entries for columns 2-4 are denoted by the labels $Y/z$, $n_Y/n_z$, and $\Delta Y/\Delta z$ to reflect that the post-damage state vector is $(\log K,z,\log R)$, while the pre-damage state vector is $(\log K,Y,\log R)$.
