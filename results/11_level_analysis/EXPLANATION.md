# RQ4: Level Analysis (Phone Game Tracking)

## 1. What Statistical Tests Are In Here?
This folder exclusively evaluates if performance fundamentally decays as the levels progress from 1 to 15.
- **Repeated Measures (RM) ANOVA:** Tracks Reaction Time changes over level progressions.
- **Friedman Test:** The non-parametric equivalent of an RM ANOVA, tracking Accuracy over level progressions.
- **Trend Correlations (Pearson/Spearman):** These tell us the "Slope" (direction) of the progression line. Does time go strictly *up*, and does accuracy go strictly *down*? 

## 2. Which Plot is for Which Test?
### `plot_level_single_phone.png` & `plot_level_multiple_phone.png`
- **Left Plots (Reaction Time):** The Blue dots map to the `Repeated Measures ANOVA` test. The Red dashed trendline maps to the `Pearson` correlation slope test.
- **Right Plots (Accuracy):** The Green dots map to the `Friedman` test. The Red dashed trendline maps to the `Spearman` correlation slope test.

## 3. The Results & Why They Are Significant
*The scientific threshold for statistical significance is **alpha ($\alpha$) = 0.05**. If our $p$-value is **LESS THAN 0.05**, we declare it "Significant".*

**A. Reaction Time Deterioration (Repeated Measures ANOVA & Pearson Trend)**
*   **Exact Values:** The ANOVA yielded an astronomical $p = 0.0000$ (e.g. $p = 1.11 \times 10^{-16}$). The Pearson slope was strongly significant as well ($p = 0.0001$ for Single target). 
*   **Is it significant?** YES. Since 0.0000 < 0.05, it is massively significant. 
*   **Outcome:** Both tests prove that as your visual game scales up the levels, human search time strictly, predictably worsens (takes longer). 

**B. Accuracy Deterioration (Friedman Test & Spearman Trend)**
*   **Exact Values:** The Friedman score was $p = 0.0001$. The Spearman slope yielded $p = 0.0145$. 
*   **Is it significant?** YES. Since 0.0001 < 0.05, and 0.0145 < 0.05, they are strongly significant. 
*   **Outcome:** Both tests prove that as visual congestion scales up in later levels, human accuracy predictably degrades (decays downwards). The game difficulty naturally defeats human cognitive ceilings.
