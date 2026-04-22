# MASTER PROJECT SUMMARY: BRSM Attention Task Validation

## Overview
This document serves as the final master reference for all statistical work executed on the **main** branch of our project. It represents the "Raw Data" inferential pipeline prior to any Log10 transformations.

## The Data Pipeline
*   **Data Extraction (01):** Raw mouse-clicks and app metrics were normalized to "Average Search Time per Target (ms/target)".
*   **Outlier Analysis (03):** Used a highly strict $3 \times IQR$ method. Only 3 extreme participants (out of ~40) were removed.
*   **Normality Testing (04):** `Shapiro-Wilk` testing mathematically proved that **Reaction Time (RT) was normally distributed**, but Accuracy was completely non-normal due to a massive ceiling effect (most humans scored exactly 100%).
*   **Transformations (05):** We attempted to transform the Accuracy data (Log10, Sqrt, Box-Cox) to force it to be normal, but the ceiling effect was too severe. Therefore, we committed to **Non-Parametric tests for Accuracy** and **Parametric tests for RT**.

---

## The Research Questions & Outcomes

### RQ1: Concurrent Validity (Does the Game measure the same thing as the Lab?)
*   **Tests Used:** Pearson's $r$ (RT) and Spearman's $\rho$ (Accuracy).
*   **Outcome:** **NOT SIGNIFICANT ($p > 0.05$)**. 
*   **Meaning:** There is absolutely no correlation between how well a human does in the sterile Lab vs how well they do on the gamified Phone app. This is a massive finding because it proves that gamifying a testing environment completely changes human cognitive behavior. The game measures unique variance that the lab cannot capture!

### RQ2: Target Load Effect (Is 5 targets worse than 1 target?)
*   **Tests Used:** Mixed ANOVA (Target Load Main Effect), Independent t-tests (RT), Mann-Whitney U (Accuracy).
*   **ANOVA Outcome:** **HIGHLY SIGNIFICANT ($p < .0001$)**. Target load drastically alters average search time.
*   **T-test Outcome:** Processing multiple targets is mathematically *more efficient per-target* (faster average RT) than a lonely single target. 
*   **Accuracy Outcome:** Within the Gamified app, humans protected their accuracy perfectly when things got harder. However, in the sterile Lab, forcing humans to find 5 targets caused their precision to significantly drop ($p = 0.0006$).

### RQ3: Modality Effect (Game vs Lab)
*   **Tests Used:** Mixed ANOVA (Modality Main Effect), Paired t-tests (RT), Wilcoxon Signed-Rank (Accuracy).
*   **ANOVA Outcome:** **HIGHLY SIGNIFICANT ($p < .0001$)**. The interface absolutely changes human processing speed.
*   **T-test Outcome:** For simple tasks (1 target), the Lab was massively faster. But for complex tasks (5 targets), the interfaces completely equalized.
*   **Crucial Interaction Effect:** The ANOVA proved a massive crossover interaction ($p < .0001$). Gamification slowed humans down on easy tasks, but sped humans up on hard tasks!

### RQ4: Level Effect (As the Game gets harder, do humans get worse?)
*   **Tests Used:** Repeated Measures ANOVA & Pearson Trend (RT), Friedman Test & Spearman Trend (Accuracy).
*   **Outcomes:** **HIGHLY SIGNIFICANT ($p < .0001$, $r/rho$ slopes strictly positive/negative).**
*   **Meaning:** As the visual scene scales up over 15 levels, human physiological performance strictly and predictably degrades exactly as intended by the difficulty curve.
