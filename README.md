<div align="center">

# Project Proposal: Chicago Food Inspections

### Predicting Restaurant Health Inspection Failures in Chicago and Auditing Where Enforcement Falls

**Group 11D**

</div>

<table align="center">
<tr>
<td valign="top">

Althan Nguyen<br>
Eva Wonsowicz<br>
Fareeha Gullany<br>
Joshua Jacob

</td>
<td valign="top">

Khizer Butt<br>
Rodas<br>
Snehal Agrawal

</td>
</tr>
</table>

---

## Contents

1. [Topic and Summary](#topic-and-summary)
2. [Research Question](#research-question)
3. [Machine Learning Algorithms](#machine-learning-algorithms)
4. [Dataset](#dataset)
5. [Sources of Bias](#sources-of-bias)
6. [Mitigation Strategies](#mitigation-strategies)
7. [Citations](#citations)

---

## Topic and Summary

We are studying restaurant health inspections in Chicago. Using the City of Chicago's public record of past inspections, we will build a model that predicts whether an inspection ends in a failure, learn which factors most drive failures, and check whether higher failure rates in some neighborhoods reflect real food safety risk or simply more frequent, complaint driven inspection.

This topic matters because foodborne illness is a serious public health problem. The CDC estimates that each year about **48 million** Americans get sick, **128,000** are hospitalized, and **3,000** die from foodborne illness *(Citation 6)*. Inspections are a main tool for catching problems early, but cities have far too few inspectors to check every establishment often, so deciding where to send them first is a real and useful question.

We will use the data to learn patterns from past inspections (the inputs) and their recorded outcome, Pass or Fail, then to predict new cases and to rank which factors matter most. The potential impact is practical: when the City of Chicago deployed its own forecasting model on this exact dataset, that program found critical violations about **7.5 days earlier** and caught **69 percent** of the establishments with critical violations in the first half of inspections, compared with **55 percent** before *(Citations 2 and 4)*. These are Chicago's results, not a promise of ours; they show the kind of benefit that better targeting can produce. The impact is two sided, which is part of why it is worth studying: a model like this could help a city prioritize inspections, but it could also reinforce unequal enforcement if some neighborhoods are simply inspected more harshly, which is exactly what our fairness analysis examines.

---

## Research Question

> Which characteristics, namely facility type, assigned risk level, inspection type, and ZIP code, best predict whether a Chicago food establishment fails a health inspection, and do predicted failure rates differ across ZIP codes in a way that reflects real risk versus uneven enforcement?

**Supporting sub question:** Does the model rely more on the establishment's own attributes (risk level, facility type) or on its neighborhood, and what does that imply about fairness?

---

## Machine Learning Algorithms

This is a supervised classification project. The inputs are facility type, assigned risk level, inspection type, and ZIP code; the output is a predicted Fail or not Fail. We will use two algorithms:

- **Logistic Regression**, a simple and easy to explain baseline classifier.
- **Random Forest**, a stronger model that usually performs better and can rank which features most drive failure.

Logistic regression is interpretable but can underfit; random forest is usually more accurate and ranks feature importance but is less transparent and can overfit. We will report the strengths and weaknesses of each and choose a primary model based on how well it identifies failures *(Citation 10 for the library; Citation 5 for an independent analysis of a model like ours)*.

---

## Dataset

|            |                                                                                                                                                                                                                                                                                                     |
| :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Name**   | Food Inspections                                                                                                                                                                                                                                                                                    |
| **Source** | City of Chicago, Chicago Data Portal (Chicago Department of Public Health)                                                                                                                                                                                                                           |
| **Link**   | [https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5) *(Citation 1)*                                                                                                                    |
| **Size**   | 312,415 inspections as of the June 2026 export (about 268,000 after removing non-decision outcomes such as Out of Business and No Entry), one row per inspection, with columns including Results, Facility Type, Risk, Inspection Type, Zip, and Latitude/Longitude.                                  |

**Training and testing:** about 268,000 usable rows (after removing non-decision outcomes) is far more than enough to train a model and keep a separate test set. We will split by license number using a grouped split, so that all inspections of the same establishment stay together in either training or testing and never both; this prevents the inflated, misleading scores that a plain random split would produce. We will use only information available before an inspection and will exclude the Violations field, since it is known only after the inspection.

---

## Sources of Bias

1. **Enforcement and selection bias:** some neighborhoods are inspected more often, for example after complaints or as re inspections, so they can appear to fail more even when their food is not actually worse. This includes geographic and sampling bias *(Citations 8 and 9)*.

2. **Missing data and class imbalance:** most inspections pass (about 22 percent of usable inspections are failures), so a model can score well by ignoring the rarer failures, and some records have blank or incomplete fields.

---

## Mitigation Strategies

1. **Control for enforcement:** we include inspection type as a feature and compare establishments within the same inspection type, so heavier enforcement in some areas is not mistaken for worse food safety. We will present neighborhood differences as an enforcement pattern, not as proven hygiene differences, and we will measure model error rates (false positive and false negative rates) separately for each ZIP code and facility type.

2. **Handle imbalance and missing data:** we use class weights so the rarer failures count, we judge the model on recall rather than overall accuracy, and we clean or fill blank fields before training.

---

## Citations

1. City of Chicago. "Food Inspections." *Chicago Data Portal*, Chicago Department of Public Health, [data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5). Accessed 23 June 2026.

2. City of Chicago, Department of Public Health, and Department of Innovation and Technology. "Food Inspection Forecasting: Optimizing Inspections with Analytics." *City of Chicago*, 2017, [chicago.github.io/food-inspections-evaluation/](https://chicago.github.io/food-inspections-evaluation/). Accessed 23 June 2026.

3. City of Chicago. "Chicago/food-inspections-evaluation." *GitHub*, 2015, [github.com/Chicago/food-inspections-evaluation](https://github.com/Chicago/food-inspections-evaluation). Accessed 23 June 2026.

4. City of Chicago, Office of the Mayor. "Mayor Emanuel Announces New Innovative System to Prioritize Food Safety Health Inspections." *Chicago.gov*, July 2015, [www.chicago.gov/city/en/depts/mayor/press_room/press_releases/2015/july/mayor-emanuel-announces-new-innovative-system-to-prioritize-food.html](https://www.chicago.gov/city/en/depts/mayor/press_room/press_releases/2015/july/mayor-emanuel-announces-new-innovative-system-to-prioritize-food.html). Accessed 23 June 2026.

5. Kannan, Vinesh, Matthew A. Shapiro, and Mustafa Bilgic. "Hindsight Analysis of the Chicago Food Inspection Forecasting Model." *arXiv*, 10 Oct. 2019, [arxiv.org/abs/1910.04906](https://arxiv.org/abs/1910.04906). Accessed 23 June 2026.

6. Centers for Disease Control and Prevention. "Food Safety Basics." *CDC*, 2026, [www.cdc.gov/food-safety/about/index.html](https://www.cdc.gov/food-safety/about/index.html). Accessed 23 June 2026.

7. Jones, Timothy F., et al. "Restaurant Inspection Scores and Foodborne Disease." *Emerging Infectious Diseases*, vol. 10, no. 4, 2004, pp. 688 to 692, [wwwnc.cdc.gov/eid/article/10/4/03-0343_article](https://wwwnc.cdc.gov/eid/article/10/4/03-0343_article).

8. Ensign, Danielle, et al. "Runaway Feedback Loops in Predictive Policing." *Proceedings of the 1st Conference on Fairness, Accountability and Transparency*, PMLR, vol. 81, 2018, pp. 160 to 171, [proceedings.mlr.press/v81/ensign18a.html](https://proceedings.mlr.press/v81/ensign18a.html).

9. Richardson, Rashida, Jason M. Schultz, and Kate Crawford. "Dirty Data, Bad Predictions: How Civil Rights Violations Impact Police Data, Predictive Policing Systems, and Justice." *New York University Law Review Online*, vol. 94, 2019, pp. 15 to 55, [ainowinstitute.org/publications/dirty-data-bad-predictions-how-civil-rights-violations-impact-police-data](https://ainowinstitute.org/publications/dirty-data-bad-predictions-how-civil-rights-violations-impact-police-data).

10. Pedregosa, Fabian, et al. "Scikit-learn: Machine Learning in Python." *Journal of Machine Learning Research*, vol. 12, 2011, pp. 2825 to 2830, [www.jmlr.org/papers/v12/pedregosa11a.html](https://www.jmlr.org/papers/v12/pedregosa11a.html).
