# Statistical Validation Report

KS tests are reported for numeric variables. Categorical variables are validated with a Chi-square goodness-of-fit test comparing synthetic category proportions against the real (seed) proportions, which is the correct analogue of the KS test for categorical data.

| Variable | Test | Statistic | p-value | p > 0.05 |
|---|---|---|---|---|
| location | Chi-square | 2.7517 | 0.2526 | Yes |
| tablet_access | Chi-square | 0.3325 | 0.8468 | Yes |
| bandwidth | Chi-square | 1.3465 | 0.51 | Yes |
| resource_level | Chi-square | 4.4058 | 0.1105 | Yes |
| teacher_qualification | Chi-square | 2.319 | 0.5089 | Yes |

**All variables pass (p > 0.05):** Yes
