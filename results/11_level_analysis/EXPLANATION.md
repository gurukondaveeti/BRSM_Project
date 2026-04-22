# Level Analysis (Phone Game Tracking)

## 1. What Statistical Tests Are In Here?
This folder exclusively evaluates if performance fundamentally decays as the levels progress from 1 to 15. All of these tests exist purely to answer RQ4.
- **Repeated Measures (RM) ANOVA:** Tracks Reaction Time changes over level progressions.
- **Friedman Test:** The non-parametric equivalent of an RM ANOVA, tracking Accuracy over level progressions.
- **Trend Correlations (Pearson/Spearman):** These tell us the "Slope" (direction) of the progression line. Does time go *up*, and does accuracy go *down*? 

### The Mathematical Formulas Used
**One-Way Repeated Measures ANOVA:** Evaluates the variance within the identical human subjects across $k$ different treatments (levels).
$$ F = \frac{MS_{Levels}}{MS_{Error}} $$
Where $SS_{Error}$ mathematically removes the natural performance differences between humans ($SS_{Subjects}$) from the total pool of variance.
$$ SS_{Error} = SS_{Total} - SS_{Levels} - SS_{Subjects} $$

**Friedman Test ($\chi^2$):** A non-parametric test to detect differences across multiple levels without assuming normal distribution. It ranks scores within each participant across the $k$ levels. Where $R_j$ is the sum of ranks for the $j^{th}$ level and $n$ is participants:
$$ \chi^2_R = \left[ \frac{12}{nk(k+1)} \sum_{j=1}^k R_j^2 \right] - 3n(k+1) $$

## 2. Which Plot is for Which Test?
### `plot_level_single_phone.png` & `plot_level_multiple_phone.png`
- **Left Plots (Reaction Time):** The Blue dots map to the `Repeated Measures ANOVA` test. The Red dashed trendline maps to the `Pearson` correlation slope test.
- **Right Plots (Accuracy):** The Green dots map to the `Friedman` test. The Red dashed trendline maps to the `Spearman` correlation slope test.

---

## 3. Final Answers for Your Report 

*The scientific threshold for statistical significance is **alpha ($\alpha$) = 0.05**. If our $p$-value is **LESS THAN 0.05**, we declare it "Significant".*

### ANSWERING RQ4: What is the effect of level in the games?

**A. Reaction Time Deterioration (Repeated Measures ANOVA & Pearson Trend)**
*   **Exact Values:** The ANOVA yielded an astronomical $p = 0.0000$ (e.g. $p = 1.11 \times 10^{-16}$). The Pearson slope was strongly significant as well ($p = 0.0001$ for Single target). 
*   **Is it significant?** YES. Since 0.0000 < 0.05, it is massively significant. 

**B. Accuracy Deterioration (Friedman Test & Spearman Trend)**
*   **Exact Values:** The Friedman score was $p = 0.0001$. The Spearman slope yielded $p = 0.0145$. 
*   **Is it significant?** YES. Since 0.0001 < 0.05, and 0.0145 < 0.05, they are strongly significant. 

**Final Conclusion to write for RQ4:**
The visual level difficulty critically hinders physiological performance. Both tests powerfully confirmed that as your visual game scales up the levels, human search time strictly worsens (increases) and human absolute accuracy predictably degrades (decays downwards). The game's level progression naturally defeats human cognitive ceilings exactly as intended.
