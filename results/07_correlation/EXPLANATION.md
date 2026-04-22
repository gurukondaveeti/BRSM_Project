# Correlation Analysis (Concurrent Validity) Explanation

## Overview
This folder investigates **Research Question 1 (RQ1):** *Is there a significant positive correlation between performance in the Game and the Lab Task?*
Concurrent validity evaluates whether your new testing tool (the Game) measures the exact same cognitive constructs as the established gold-standard tool (the Lab task).

## The Plot Explained
### `plot_correlation_scatter.png`
This image holds four scatter plots mapping how a participant scored on the Game (X-axis) versus how they scored on the Lab Task (Y-axis).
- **The Dots:** Each dot represents a single human participant. 
- **The Red Dashed Line:** This is the regression trend line (line of best fit). If Concurrent Validity was perfectly proven, this line would go diagonally sharply from the bottom-left to the top-right.
- **The Findings:** As you can see, the dots are scattered almost randomly. The line is relatively flat. 

## Key Outcomes
*   **Reaction Time (Pearson's r):** Neither the Single Targets (p = 0.12) nor the Multiple Targets (p = 0.32) showed a significant relationship. 
*   **Accuracy (Spearman's rho):** Not significant for Multiple Targets (p = 0.65). It could not be computed for Single targets because everyone scored 100% in the lab.
*   **Conclusion:** Your gamified interface is **not** strongly correlated with the Lab task at an individual level. While this fails Concurrent Validity, it is a fascinating research outcome! It suggests the "Game" is capturing a highly unique cognitive variance—perhaps measuring 'sustained engagement' or 'gamified motivation'—rather than pure, isolated visual search physics like the Lab task does.
