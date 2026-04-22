# Non-Parametric Accuracy Analysis

## 1. What Statistical Tests Are In Here?
Because human Accuracy suffered from a "Ceiling Effect" (where most people scored near 100%, breaking normal bell-curve distributions), we legally could not use Parametric ANOVAs or t-tests. This folder contains the **Robust Non-Parametric tests** answering RQ2 & RQ3 for Accuracy.
- **Wilcoxon Signed-Rank Test:** The non-parametric replacement for the Paired t-test. It compares Game vs Lab Accuracy (Answers RQ3).
- **Mann-Whitney U Test:** The non-parametric replacement for the Independent t-test. It compares Single vs Multiple Target accuracy (Answers RQ2).

## 2. Which Plot is for Which Test?
### `plot_nonparametric_accuracy.png`
- **Left Plot:** Visualizes the spread of Accuracy, mapping exactly to what the `Mann-Whitney U` sees. 
- **Right Plot:** Visualizes the Medians of all four groups. Both the `Mann-Whitney U` and the `Wilcoxon Signed-Rank` tests are mathematically checking to see if these median bars are statistically different heights. 

---

## 3. Final Answers for Your Report 

*The scientific threshold for statistical significance is **alpha ($\alpha$) = 0.05**. If our $p$-value is **LESS THAN 0.05**, we declare it "Significant".*

### ANSWERING RQ3: Does the gamified interface significantly alter performance compared to the standard lab interface? (Part 2 - Accuracy)
**A. Game vs Lab Accuracy — Single Target (Wilcoxon Signed-Rank)**
*   **Exact Value:** $p = 0.0022$
*   **Is it significant?** YES. Since 0.0022 < 0.05, it is significant. 
*   **Conclusion:** Human accuracy natively degraded down to ~96% in the Game, compared to sitting at a flawless 100% in the sterile Lab.

**B. Game vs Lab Accuracy — Multiple Target (Wilcoxon Signed-Rank)**
*   **Exact Value:** $p = 0.1330$
*   **Is it significant?** NO. Since 0.1330 > 0.05, it is not significant. 
*   **Conclusion:** The accuracy medians (99.3% Lab vs 96.3% Game) are statistically identical under this heavy visual load.

### ANSWERING RQ2: Is performance significantly worse in the Multiple Target condition compared to the Single Target condition? (Part 2 - Accuracy)
**C. Single vs Multi Target — Phone (Mann-Whitney U)**
*   **Exact Value:** $p = 0.3593$
*   **Is it significant?** NO. Since 0.3593 > 0.05, it is not significant. 
*   **Conclusion:** The gamified app kept humans just as accurate at Level 1 as it did when evaluating 5 targets.

**D. Single vs Multi Target — Lab (Mann-Whitney U)**
*   **Exact Value:** $p = 0.0006$
*   **Is it significant?** YES. Since 0.0006 < 0.05, it is highly significant. 
*   **Conclusion:** The sterile lab environment caused human accuracy to systematically degrade when evaluating 5 targets. 

**Final Conclusion to write for RQ2 (Accuracy):** Yes, but only in the Lab! Gamification somehow protected humans from losing accuracy as target load increased, whereas the sterile Lab environment caused accuracy to measurably degrade when tasks got harder!
