ReopenSense

An Empirical Study of Reopened Changes in Gerrit Code Review

##Abstract

Code review systems such as Gerrit structure collaborative software development through iterative evaluation of proposed changes. While much attention has been given to merged and abandoned changes, less focus has been placed on abandoned changes that are later reopened.

This project investigates the phenomenon of reopened changes in the LibreOffice Gerrit repository. The objective is to characterize their temporal patterns, structural properties, and review dynamics, and to explore whether simple activity based signals can help predict short-term reopenings.

##Research Motivation

In collaborative development environments, abandonment typically signals the end of a change’s lifecycle. However, reopening events represent a reversal in that process. Understanding these reversals may provide insight into:

Reviewer–author interaction dynamics

Decision instability in code review

Temporal effects in collaborative workflows

Signals associated with change persistence

This study treats reopenings as first-class behavioral events rather than edge cases.

##Data Collection

Data was collected from the Gerrit REST API for the LibreOffice project.

For each change, the full review history was analyzed to extract:

Abandonment events

Reopening events

Timestamps of lifecycle transitions

Patchset counts prior to abandonment

Reviewer participation prior to abandonment

From this raw history, a structured dataset was constructed to support both descriptive and predictive analysis.

##Dataset Description

The final dataset includes, among others, the following attributes:

change_id

project

owner_id

abandon_ts

reopen_ts

reopen_delay_days

num_patchsets_before_abandon

reviewer_count_before_abandon

final_status

Derived variables were computed to quantify review activity and temporal delay.

##Exploratory Findings

Preliminary analysis suggests:

Reopenings are temporally concentrated shortly after abandonment.

A substantial proportion of reopened changes ultimately reach the merged state.

Review activity prior to abandonment (e.g., number of patchsets and reviewers) is positively associated with the likelihood of reopening.

These findings indicate that reopenings are not random events, but may reflect latent continuation of collaborative negotiation.

##Predictive Modeling

A binary classification task was formulated:

Task: Predict whether an abandoned change will be reopened within 90 days.

Features used:

Number of patchsets before abandonment

Reviewer count before abandonment

Models evaluated:

Logistic Regression

Random Forest

Dummy baseline classifier

The evaluated models outperform the baseline, suggesting that even simple structural indicators of review activity contain predictive information.

##Repository Structure
data/        Generated datasets  
notebooks/   Exploratory and modeling notebooks  
src/         Data extraction and preprocessing scripts  

##Reproducibility

To reproduce the analysis:

pip install -r requirements.txt
jupyter notebook notebooks/reopensense_Analysis.ipynb

##Author

Emna Ismail