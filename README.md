<div align="center">
![demo](https://media.giphy.com/media/2seJUR7XBwK1OBHbnu/giphy.gif)
  
# AI4ALL Project: Chicago Food Inspections

### Predicting Restaurant Health Inspection Failures in Chicago and Auditing Where Enforcement Falls

**Group 11D**

</div>

<table align="center">
<tr>
<td valign="top">

Althan Nguyen<br>
Eva Wonsowicz<br>
Fareeha Gullany

</td>
<td valign="top">

Joshua Jacob<br>
Khizer Butt<br>
Snehal Agrawal

</td>
</tr>
</table>

<div align="center">

**Live app:** [chicago-food-inspections-11d.streamlit.app](https://chicago-food-inspections-11d.streamlit.app)<br>
**Notebook:** [Google Colab notebook]([https://drive.google.com/file/d/1qacWoNyvCLTDfvOuQjQKpOPdWaP87vTL/view?usp=sharing](https://colab.research.google.com/drive/1qacWoNyvCLTDfvOuQjQKpOPdWaP87vTL?authuser=4#scrollTo=VTuBk8T4Iqwi))

</div>

---

## Contents

1. [Topic and Summary](#topic-and-summary)
2. [What We Found](#what-we-found)
3. [Research Question](#research-question)
4. [Machine Learning Algorithms](#machine-learning-algorithms)
5. [Dataset](#dataset)
6. [Sources of Bias](#sources-of-bias)
7. [Mitigation Strategies](#mitigation-strategies)
8. [The Interactive App](#the-interactive-app)
9. [Why This Project Matters](#why-this-project-matters)
10. [Citations](#citations)

---

## Topic and Summary

We studied restaurant health inspections in Chicago. Using the City of Chicago's public record of past inspections, we built a model that predicts whether an inspection ends in a failure, learned which factors most drive failures, and then audited whether higher failure predictions in some neighborhoods reflect real food-safety risk or simply more frequent, complaint-driven inspection.

This topic matters because foodborne illness is a serious public-health problem. The CDC estimates that each year about **48 million** Americans get sick, **128,000** are hospitalized, and **3,000** die from foodborne illness *(Citation 6)*. Inspections are a main tool for catching problems early *(Citation 7)*, but cities have far too few inspectors to check every establishment often, so deciding where to send them first is a real and useful question.

We learned patterns from past inspections (the inputs) and their recorded outcome, Pass or Fail, to predict new cases and to rank which factors matter most. The potential impact is practical: when the City of Chicago deployed its own forecasting model on this exact dataset, that program found critical violations about **7.5 days earlier** and caught **69 percent** of the establishments with critical violations in the first half of inspections, compared with **55 percent** before *(Citations 2, 3, and 4)*. These are Chicago's results, not a promise of ours; they show the kind of benefit that better targeting can produce. The impact is two-sided, which is part of why it is worth studying: a model like this could help a city prioritize inspections, but it could also reinforce unequal enforcement if some neighborhoods are simply inspected more harshly, which is exactly what our fairness analysis examines.

The project became less about "can we predict failures" (the city already predicts well, with more data than we have) and more about **who the model gets wrong, and where**. What follows is what that audit found.

---

## What We Found

View in slideshow form here: https://docs.google.com/presentation/d/1BpQRJ5V7s5Za9eKW3ea6VNqafFI9tNsVMftGqZ8tGCk/edit

All results below are on a held-out test set, split by license number so the same establishment never appears in both training and testing.

- **The models work, but raise many false alarms.** Random Forest catches about **67 percent** of real failures and Logistic Regression about **70 percent**, versus **0 percent** for an "always-Pass" baseline. Precision is low (about **30 percent**), meaning many flagged establishments actually passed.

- **The models are over-confident.** When the model says a restaurant has a **95 percent** chance of failing, only about **49 percent** actually do. On log loss, both models score worse than a constant base-rate guess, so their confidence should be read as a ranking signal, not a calibrated probability.

- **The false alarms land very unevenly.** Citywide the false-positive rate is about **45 percent**, but per ZIP it runs from **2 percent to 67 percent**. A passing restaurant in the most-flagged ZIP (60620) has about a **67 percent** chance of being wrongly flagged, versus about **6 percent** in the Loop, roughly a **12x** gap, concentrated on the South and West sides.

- **It is not just about who gets inspected.** When we restrict to routine Canvass inspections only, the gap survives and even intensifies (the top ZIPs run about **79 percent to 99 percent**), and a ZIP's false-positive rate correlates **0.69** with how enforcement-heavy its inspection mix is. This is the feedback-loop mechanism: past enforcement is encoded in the ZIP feature and applied everywhere.

- **The obvious fix backfires.** Raising the decision threshold cuts overall false alarms (about **45 percent down to 16 percent**) but collapses recall (about **67 percent down to 31 percent**) and **widens** the neighborhood gap (from about **5.4x to 21.8x**). A single global cutoff cannot fix a per-neighborhood bias.

**Framing note.** These are geographic findings, described as an enforcement pattern, not evidence that these neighborhoods have worse food. Merging Census income and race by ZIP to describe who actually lives in the over-flagged areas is our next step, not a current claim.

Explore all of this interactively in the [live app](https://chicago-food-inspections-11d.streamlit.app).

---

## Research Question

> Which characteristics, namely facility type, assigned risk level, inspection type, and ZIP code, best predict whether a Chicago food establishment fails a health inspection, and do predicted failure rates differ across ZIP codes in a way that reflects real risk versus uneven enforcement?

**Supporting sub question:** Does the model rely more on the establishment's own attributes (risk level, facility type) or on its neighborhood, and what does that imply about fairness?

---

## Machine Learning Algorithms

This is a supervised classification project. The inputs are facility type, assigned risk level, inspection type, and ZIP code; the output is a predicted Fail or not-Fail. We used two algorithms:

- **Logistic Regression**, a simple and easy-to-explain baseline classifier.
- **Random Forest**, a stronger model that usually performs better and can rank which features most drive failure.

Logistic regression is interpretable but can underfit; random forest is usually more accurate and ranks feature importance but is less transparent and can overfit. We report the strengths and weaknesses of each and judge the models on how well they identify failures rather than on overall accuracy *(Citation 10 for the library; Citation 5 for an independent analysis of a model like ours)*. Permutation importance showed the model leans most on Inspection Type, then ZIP code, then Facility Type, with assigned Risk level the weakest of the four, which is what makes the fairness question live.

---

## Dataset

|            |                                                                                                                                                                                                                                                                                                     |
| :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Name**   | Food Inspections                                                                                                                                                                                                                                                                                    |
| **Source** | City of Chicago, Chicago Data Portal (Chicago Department of Public Health)                                                                                                                                                                                                                           |
| **Link**   | [https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5](https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5) *(Citation 1)*                                                                                                                    |
| **Size**   | 312,415 inspections as of the June 2026 export (about 267,000 usable after removing non-decision outcomes such as Out of Business and No Entry), one row per inspection, with columns including Results, Facility Type, Risk, Inspection Type, Zip, and Latitude/Longitude.                            |

**Training and testing:** about 267,000 usable rows across 43,356 distinct establishments is far more than enough to train a model and keep a separate test set. We split by license number using a grouped split, so that all inspections of the same establishment stay together in either training or testing and never both; this prevents the inflated, misleading scores that a plain random split would produce. We used only information available before an inspection and excluded the Violations field, since it is known only after the inspection.

---

## Sources of Bias

1. **Enforcement and selection bias:** some neighborhoods are inspected more often, for example after complaints or as re-inspections, so they can appear to fail more even when their food is not actually worse. This includes geographic and sampling bias *(Citations 8 and 9)*.

2. **Missing data and class imbalance:** most inspections pass (about 22 percent of usable inspections are failures), so a model can score well by ignoring the rarer failures, and some records have blank or incomplete fields.

---

## Mitigation Strategies

1. **Control for enforcement:** we included inspection type as a feature and compared establishments within routine inspections, so heavier enforcement in some areas is not mistaken for worse food safety. We present neighborhood differences as an enforcement pattern, not as proven hygiene differences, and we measured model error rates (false-positive and false-negative rates) separately for each ZIP code with Fairlearn.

2. **Handle imbalance and missing data:** we used class weights so the rarer failures count, judged the model on recall rather than overall accuracy, and cleaned or filled blank fields before training.

---

## The Interactive App

The full audit is a live, multi-page Streamlit app: [chicago-food-inspections-11d.streamlit.app](https://chicago-food-inspections-11d.streamlit.app). It walks through model performance, what drives predictions, the neighborhood effect, threshold tuning, the per-ZIP fairness audit, the enforcement check, and the conclusions, including an interactive map of Chicago shaded by observed fail rate. The app reads pre-exported results from the analysis notebook, so it runs without the raw 350 MB dataset.

---

## Why This Project Matters

Every year, millions of people become sick from foodborne illnesses, making restaurant inspections an essential part of protecting public health. However, health departments face a difficult challenge: there are far more food establishments than inspectors available to evaluate them. This is because inspections require significant time and resources and deciding which restaurants should be inspected first is a critical public health decision.

Machine learning has the potential to make this process more efficient by identifying establishments that may be at higher risk of failing an inspection. Though, **improving efficiency is only part of the solution.** When predictive models are trained on historical inspection data, they can also inherit patterns created by past enforcement decisions. If left unchecked, these systems may repeatedly target the same neighborhoods, even when those predictions do not accurately reflect current food safety risk.

Rather than asking whether we could simply predict inspection failures, our project focused on a more important question: **Who does the model get wrong, and are those mistakes distributed fairly?** By examining false positives and false negatives across Chicago ZIP codes, we evaluated whether prediction errors reflected genuine differences in food safety or whether they pointed to uneven enforcement patterns.

Working on this project changed the way we think about AI. We came into it expecting to focus on building a strong prediction model, but we left realizing that **understanding a model's limitations can be just as important as improving its performance.** It showed us that responsible AI isn't just a concept we learn about in class—it's something that should be considered whenever technology is used to make decisions that affect real people.

This project highlights an important principle in responsible AI: **a model can achieve strong predictive performance while still producing unequal outcomes for different communities.** Evaluating fairness alongside accuracy helps ensure that machine learning supports public health decisions without unintentionally reinforcing historical biases. Our goal is not only to build better predictive models but also to encourage more transparent, accountable, and equitable uses of AI in the public sector.

---
## Future Work

While our initial models established a functional baseline for failure prediction, our audit identified key data constraints and ethical feedback loops. To build a more robust, equitable, and deployment-ready system, we propose the following dated next steps across data expansion, temporal evaluation, and fairness post-processing.

Data Volume & Feature Expansion (Near-Term)
Our current baseline model relies on only 4 pre-inspection features (*Inspection Type*, *ZIP Code*, *Facility Type*, and *City Risk Level*). While predictive, this limited feature set restricts the model's ability to make fully informed decisions based on establishment-level context.

* **Historical Violation Engineering:** Extract and tokenize historical violation text and multi-year failure counts per business license to evaluate prior compliance history.
* **Establishment Metadata:** Incorporate establishment age, ownership shifts, and licensing duration to allow the model to make more nuanced predictions rather than relying primarily on spatial location.
* **Census Demographic Overlay (Task 6):** Merge U.S. Census Bureau (ACS 5-Year) median household income and racial demographics by ZIP code onto per-ZIP false-positive rates to formally quantify the socioeconomic impact across Chicago neighborhoods.

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
