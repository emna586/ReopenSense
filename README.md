
# ReopenSense

Analysis and prediction of reopened code changes in the LibreOffice Gerrit repository.

## Project Overview

This project studies abandoned code changes that are later reopened in a collaborative review environment.

The objective is to understand behavioral patterns in code review and explore whether reopenings can be predicted using simple activity-based features.

## Dataset

The dataset contains information about:

- Change identifiers
- Abandonment timestamps
- Reopen timestamps
- Delay between abandon and reopen
- Number of patchsets before abandon
- Number of reviewers before abandon

## Structure

data/        -> Generated datasets  
notebooks/   -> Analysis and modeling  
src/         -> Data extraction scripts  

## Machine Learning

A simple classification task was performed to predict whether an abandoned change would be reopened within 90 days.

Models tested:
- Logistic Regression
- Random Forest
- Baseline classifier

## Author

Emna Ismail
