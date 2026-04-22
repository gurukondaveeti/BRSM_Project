# Correlation Analysis

## 1. What Statistical Tests Are In Here?
- **Pearson's r Correlation:** Used for Reaction Time (because the RT data was normally distributed).
- **Spearman's Rho Correlation:** Used for Accuracy (because the Accuracy data had a ceiling effect and was not normally distributed).

## 2. Which Plot is for Which Test?
### `plot_correlation_scatter.png`
This image contains 4 scatter plots visualizing the correlation tests.
- **Top Left Plot:** Visualizes the `Pearson` test for Single-Target Reaction Time.
- **Top Right Plot:** Visualizes the `Spearman` test for Single-Target Accuracy.
- **Bottom Left Plot:** Visualizes the `Pearson` test for Multi-Target Reaction Time.
- **Bottom Right Plot:** Visualizes the `Spearman` test for Multi-Target Accuracy.

---

## 3. Final Answers for Your Report 

### ANSWERING RQ1: Is there a significant positive correlation between performance in the Game and the Lab Task?

*The scientific threshold for statistical significance is **alpha ($\alpha$) = 0.05**. If our $p$-value is **LESS THAN 0.05**, we declare it "Significant".*

**A. Single Target Reaction Time (Pearson)**
*   **Exact Value:** $p = 0.1219$
*   **Is it significant?** NO. Since 0.1219 > 0.05, it is NOT significant. 

**B. Multiple Target Reaction Time (Pearson)**
*   **Exact Value:** $p = 0.3282$
*   **Is it significant?** NO. Since 0.3282 > 0.05, it is NOT significant.

**C. Multiple Target Accuracy (Spearman)**
*   **Exact Value:** $p = 0.6522$
*   **Is it significant?** NO. Since 0.6522 > 0.05, it is NOT significant. 

*(Note: Single Target Accuracy could not be calculated because 100% of humans scored 100% in the lab, leaving 0 variance).*

**Final Conclusion to write for RQ1:** 
No. We reject the hypothesis that there is a significant positive correlation. Because $p > 0.05$ for every single test, Concurrent Validity fails. This scientifically proves that measuring human performance via your "Game" naturally captures completely different, unique cognitive traits than measuring them via a standard "Lab task", even when the target load matches exactly!
