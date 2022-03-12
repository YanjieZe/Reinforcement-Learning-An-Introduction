# 2 多臂赌博机

# 2.1
$$
\operatorname{Pr}[a_{optimal}]=1-\epsilon=0.5
$$

# 2.2

$$
A_1=1, R_1=-1, Q_1=-1,optimal=\{234\}
$$

$$
A_2=2, R_2=1, Q_2=1,optimal=\{2\}
$$

$$
A_3=2, R_3=-2, Q_2=(1-2)/2=-0.5,optimal=\{34\}
$$

$$
A_4=2, R_4=2, Q_2=-0.5 + (2+0.5)/3\approx0.33,optimal=\{2\}
$$

$$
A_5=3,...
$$

可见，t=4和t=5的时候都没有选择最佳策略，肯定是探索。

t=2的时候从3个optimal中只选了一个，也有可能是探索。

*注：刚才用到了一个增量式求平均的方法，可参考书Eq (2.4)。

# 2.3

估算了一下图里的值。

| epsilon | average reward | best action % |
| ------- | -------------- | ------------- |
| 0       | 1              | 35%           |
| 0.01    | 1.4            | 50%           |
| 0.1     | 1.5            | 80%           |

# 2.4

$$
\begin{aligned}
Q_{n+1}&=Q_n+\alpha_n[R_n - Q_n]\\
&=  \alpha_n R_n + (1-\alpha_n)Q_n\\
&=\alpha_n R_n + (1-\alpha_n)(\alpha_{n-1} R_{n-1} + (1-\alpha_{n-1})Q_{n-1})\\
&=\alpha_n R_n + (1-\alpha_n)\alpha_{n-1} R_{n-1} + (1-\alpha_n)(1-\alpha_{n-1})Q_{n-1}\\
&=\dots
\end{aligned}
$$
因此，对于$R_i(1\leq i\leq n)$，系数是
$$
(1-\alpha_n)(1-\alpha_{n-1})\dots(1-\alpha_{i+1})\alpha_{i}
$$

# 2.5
代码见`2.5.py`。

每个episode取100步，总共50000个episode。

best action rate就暂时不画了，反正也是fixed step size比较好。

结论：对于这种reward随时间改变的bandit，采取fixed step size可以有效遗忘很早的知识，更关注于近期的知识。


![](result.jpg)

# 2.6

因为“乐观初始值”，当我们pull到了best arm之后，我们对它的Q值的估计立刻下降，导致我们去pull其他的arm。

所以在前期会有比较多的震荡。

# 2.7 
$$
\begin{aligned}
\beta_n&=\alpha / o_n \\
o_n &= o_{n-1}+\alpha(1-o_{n-1}), o_0=0 \\
Q_{n+1}&=Q_{n} + \beta_n(R_n-Q_n)\\
&=\beta_n R_n + (1-\beta_n)Q_n\\
&=\beta_nR_n+(1-\beta_n)(\beta_{n-1}R_{n-1}+(1-\beta_{n-1})Q_{n-1} )\\
&=\beta_nR_n+(1-\beta_n)\beta_{n-1}R_{n-1}+(1-\beta_n)(1-\beta_{n-1})Q_{n-1}\\
&=\dots
\end{aligned}
$$
然后$Q_1$的weight是：
$$
\begin{aligned}
(1-\beta_{n})(1-\beta_{n-1})\dots(1-\beta_{2})(1-\beta_1)
\end{aligned}
$$
这个weight很明显是收敛到0的。

（置疑：如果只要收敛到0，书中的Eq (2.6)也可以，为什么还要让我们做这个呢？）

# 2.8
这个尖峰其实就来源于UCB算法。

前10步，其实每个arm都被探索了一次（10次）。那么第11步，肯定是best arm的Q最大，因此算法选择了best arm，这导致了尖峰的出现。这导致best arm的Q迅速减小。

而后，算法会去探索其他arm。由于ln(t)这个factor的增长速度小于N(a)，还得多探索一会才会又到best arm，这导致了后续若干步会减少。