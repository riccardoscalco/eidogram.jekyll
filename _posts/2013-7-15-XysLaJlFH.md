---
layout: post
post: true
title: Confidence intervals of simple linear regression.
script: ['http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML', 'js/highlight/highlight.pack.js']
style: ['js/highlight/styles/github.css']
abstract: Simple linear regression and confidence intervals are derived from raw data with explicit formulas.
---

The following text is a brief summary of lectures 29,30 and 31 given by 
<a href="http://ocw.mit.edu/courses/mathematics/18-443-statistics-for-applications-fall-2003/index.htm">Dmitry Panchenko</a> at MIT.


Suppose we are given a set of observations $$\{(X_1,Y_1),\dots,(X_n,Y_n)\}$$, where $$X_i,Y_i \in \mathbb{R}$$.
We *assume* to model the random variable $$Y$$ as a linear function of the random variable $$X$$ with the presence of a random noise,
i.e. we are assuming

$$
Y_i = b_0 + b_1 X_i + \epsilon_i
$$

where $$b_0,b_1\in\mathbb{R}$$ and $$\epsilon_i\sim N(0,\sigma^2)$$ (that is $$\epsilon_i$$ is assumed to have normal distribution) are unknown parameters.
On the following we will estimate the unknown parameters and their confidence intervals, given the observations.

Let us think of the points $$X_i$$ as fixed and *non random* and deal only with the randomness that comes from the noise variables $$\epsilon_i$$.
In other words we deal only with the distribution $$P(Y_i)=f(X_i,b_0,b_1,\epsilon_i)$$, which is normal because the randomness comes from the normal variables $$\epsilon_i$$.

We want to find the estimates $$\hat{b_0}, \hat{b_1}$$ and $$\hat{\sigma}^2$$ that fits the observations best and one can define the measure of the quality of fit in different ways. Here we use the maximum likelihood estimates, which maximize the probability $$P(Y_1Y_2\dots Y_n)=P(Y_1)P(Y_2)\dots P(Y_n)$$
of the event $$Y_1 \text{ AND } Y_2 \text{ AND } \dots \text{ AND } Y_n$$.
The maximum likelihood estimates are

$$
\hat{b_1} = \frac{\bar{XY}-\bar{X}\bar{Y}}{\bar{X^2}-\bar{X}^2},\qquad

\hat{b_0} = \bar{Y} - \hat{b_1}\bar{X},\qquad

\hat{\sigma}^2 = \frac{1}{n}\sum^n_{i=1}(Y_i - \hat{b_0} - \hat{b_1}X_i)^2
$$

where $$\bar{X}$$ is the mean of $$X$$
(note that $$b_0$$ and $$b_1$$ are the same as found with the least-squares method).

*The knowledge of the estimates is enough to draw the line that fits the observations,
but an important further information (the confidence) comes from the distribution of the estimates.*
The estimates have a probability distribution because they are functions of $$Y_i$$, which have distributions $$P(Y_i)$$.

What are the confidence intervals? It will become apparent with an example. It can be proved that the random variable $$\hat{\sigma}^2$$ is independent of $$\hat{b_0}$$ and $$\hat{b_1}$$
and that it has a chi squared distribution with $$n-2$$ degrees of freedom. In formulas

$$
\frac{n\hat{\sigma}^2}{\sigma^2}\sim\chi^2_{n-2}.
$$

Note that $$\chi^2_{n-2}$$ is a well known distribution, i.e. we can calculate probabilities with it. For example, let be $$\alpha=0.025$$, if we find the values $$c_1$$ and $$c_2$$ such that
$$\int_0^{c_1}\chi^2_{n-2}dx=\alpha/2$$ and $$\int_{c_2}^{\infty}\chi^2_{n-2}dx=\alpha/2$$, then the probability of the remaining interval is $$\int_{c_1}^{c_2}\chi^2_{n-2}dx=1-\alpha = 0.95$$,
which means that

$$
P(c_1\leq\frac{n\hat{\sigma}^2}{\sigma^2}\leq c_2) = 0.95.
$$

*Solving for $$\sigma^2$$ we find the $$1-\alpha$$ confidence interval*

$$
\frac{n\hat{\sigma}^2}{c_2}\leq\sigma^2\leq\frac{n\hat{\sigma}^2}{c_1}.
$$

Note that the confidence interval is calculable.

With the same meaning, the $$1-\alpha$$ confidence intervals of $$b_1$$ and $$b_0$$ are

$$
\hat{b_1} - c \sqrt{\frac{\hat{\sigma}^2}{(n-2)(\bar{X^2}-\bar{X}^2)}} \leq b_1 \leq \hat{b_1} + c \sqrt{\frac{\hat{\sigma}^2}{(n-2)(\bar{X^2}-\bar{X}^2)}}
$$

$$
\hat{b_0} - c \sqrt{\frac{\hat{\sigma}^2}{n-2}\left(1+\frac{\bar{X}^2}{\bar{X^2}-\bar{X}^2}\right)} \leq b_0 \leq \hat{b_0} + c \sqrt{\frac{\hat{\sigma}^2}{n-2}\left(1+\frac{\bar{X}^2}{\bar{X^2}-\bar{X}^2}\right)}
$$

where the value $$c$$ originates from the Student distribution with $$n-2$$ degrees of freedom: $$t_{n-2}(-c,c)=1-\alpha$$.

This is a Python2 script that calculates the estimates and the confidence intervals, it makes use of the Scipy and Numpy libraries.

<script>hljs.initHighlightingOnLoad();</script>
<pre>
<code style="text-align:left; white-space:inherit">import scipy.stats, numpy
def linear_regression(x, y, prob):
    """
    Return the linear regression parameters and their <prob> confidence intervals.
    >>> linear_regression([.1,.2,.3],[10,11,11.5],0.95)
    """
    x = numpy.array(x)
    y = numpy.array(y)
    n = len(x)
    xy = x * y
    xx = x * x

    # estimates

    b1 = (xy.mean() - x.mean() * y.mean()) / (xx.mean() - x.mean()**2)
    b0 = y.mean() - b1 * x.mean()
    s2 = 1./n * sum([(y[i] - b0 - b1 * x[i])**2 for i in xrange(n)])
    print 'b0 = ',b0
    print 'b1 = ',b1
    print 's2 = ',s2
    
    #confidence intervals
    
    alpha = 1 - prob
    c1 = scipy.stats.chi2.ppf(alpha/2.,n-2)
    c2 = scipy.stats.chi2.ppf(1-alpha/2.,n-2)
    print 'the confidence interval of s2 is: ',[n*s2/c2,n*s2/c1]
    
    c = -1 * scipy.stats.t.ppf(alpha/2.,n-2)
    bb1 = c * (s2 / ((n-2) * (xx.mean() - (x.mean())**2)))**.5
    print 'the confidence interval of b1 is: ',[b1-bb1,b1+bb1]
    
    bb0 = c * ((s2 / (n-2)) * (1 + (x.mean())**2 / (xx.mean() - (x.mean())**2)))**.5
    print 'the confidence interval of b0 is: ',[b0-bb0,b0+bb0]
    return None
</code></pre>

