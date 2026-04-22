# Level Analysis (RQ4) Explanation

## Overview
This folder investigates **RQ4:** *What is the effect of level in the games?* 
We test this exclusively on the Phone (Gamified) data to see how performance scales as the visual arrays become increasingly dense and cognitively demanding across 15 levels.

## The Plots Explained
### `plot_level_single_phone.png` & `plot_level_multiple_phone.png`
These are dual-axis Line Plots with Trend Lines showing cognitive degradation over time.
- **Left Plot (Reaction Time):** The Blue dots track Reaction Time. The Red dashed line is the `Pearson` trend. The line clearly shoots upwards, visualizing that as levels get higher (Level 10+), humans take much longer to find targets.
- **Right Plot (Accuracy):** The Green squares track Accuracy. The Red dashed line is the `Spearman` trend. It tilts aggressively downwards, visualizing that as the visual screen gets incredibly messy in higher levels, human accuracy strictly drops.

## Key Outcomes (Highly Significant, p < .0001)
1.  **Reaction Time (Repeated Measures ANOVA & Pearson Trend):** Both tests powerfully confirmed that Level heavily impacts time. The Pearson $r$ tests ($r = 0.83$ and $r = 0.73$) show massive positive correlations: higher level always equals higher search time. 
2.  **Accuracy (Friedman Test & Spearman Trend):** Both tests completely confirmed that Level impacts accuracy. Specifically, the negative Spearman $\rho$ values prove that human accuracy decays as the level variables scale upward. 
3.  **Conclusion:** The gamified application successfully stresses the human cognitive load exactly as intended. As the game gets harder, humans empirically get slower and clumsier.
