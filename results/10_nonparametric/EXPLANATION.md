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
*   **Conclusion:** Human accuracy was significantly **worse** in the Gamified interface (degrading down to ~96%) compared to sitting at a flawless 100% in the sterile Lab interface.

**B. Game vs Lab Accuracy — Multiple Target (Wilcoxon Signed-Rank)**
*   **Exact Value:** $p = 0.1330$
*   **Is it significant?** NO. Since 0.1330 > 0.05, it is not significant. 
*   **Conclusion:** Under heavy visual loads (5 targets), the accuracy medians were statistically identical. The Game is neither better nor worse than the Lab.

### ANSWERING RQ2: Is performance significantly worse in the Multiple Target condition compared to the Single Target condition? (Part 2 - Accuracy)
**C. Single vs Multi Target — Phone (Mann-Whitney U)**
*   **Exact Value:** $p = 0.3593$
*   **Is it significant?** NO. Since 0.3593 > 0.05, it is not significant. 
*   **Conclusion:** Within the Gamified app, hunting for multiple targets was **neither better nor worse** for accuracy than hunting for single targets. The game shielded humans against accuracy loss.

**D. Single vs Multi Target — Lab (Mann-Whitney U)**
*   **Exact Value:** $p = 0.0006$
*   **Is it significant?** YES. Since 0.0006 < 0.05, it is highly significant. 
*   **Conclusion:** Within the sterile Lab environment, hunting for multiple targets yielded significantly **worse** accuracy than hunting for single targets.

**Final Conclusion to write for RQ2 (Accuracy):** Only in the Lab! Increasing the target load caused accuracy to become significantly **worse** in the sterile Lab environment. However, Gamifying the interface protected users from this failure, maintaining statistically identical accuracy levels regardless of task difficulty!
