# Human vs Algorithmic Fairness in Hiring Decisions
## Overview

This project investigates the relationship between human hiring decisions and a merit-based computational evaluation model. The study explores whether human judgments align with formally defined performance criteria when selecting between two candidates in structured hiring scenarios.

The project combines experimental design, behavioral data analysis, and computational modeling within a Cognitive Science and AI framework.

## Research Question

Do human hiring decisions align with a formal merit-based computational model that evaluates candidates using performance-relevant attributes while excluding demographic information?

## Study Design

- Participants: N = 13

- Scenarios: 15 structured candidate comparisons

- Position: Entry-level Data Analyst

Each scenario presented two candidates described using:

- Test Score

- Years of Experience

- Degree Field (Statistics, Computer Science, Data Science, Mathematics)

- Leadership Experience (Yes/No)

- Gender

Participants selected one candidate per scenario and rated the importance of each attribute at the end of the survey.

## Computational Model

A deterministic merit model was implemented to operationalize candidate evaluation.

Merit was defined as a weighted linear combination of:

- Normalized test score

- Professional experience

- Leadership presence

- Degree relevance

Gender was explicitly excluded from the merit calculation to simulate a demographic-blind evaluation system.

The model selects the candidate with the higher computed merit score.

## Results Summary

The analysis compares:

- Human hiring choices

- Merit model predictions

- Overall alignment rate

Additional descriptive analyses include:

- Average fairness ratings

- Self-reported attribute importance

This study is exploratory and intended as a pilot demonstration of computational fairness analysis.

## Reproducibility

Install dependencies
```
pip install -r requirements.txt
```

Run preprocessing:
```
python code/preprocess.py
```

## License

This project is licensed under the _MIT License_.

See the LICENSE file for details.

## Author

Tcaciuc Andrea Elena

2026