# Non-Parametric Accuracy Analysis

## 1. What Statistical Tests Are In Here?
Because human Accuracy suffered from a "Ceiling Effect" (where most people scored near 100%, breaking normal bell-curve distributions), we legally could not use Parametric ANOVAs or t-tests. This folder contains the **Robust Non-Parametric tests** answering RQ2 & RQ3 for Accuracy.
- **Wilcoxon Signed-Rank Test:** The non-parametric replacement for the Paired t-test. It compares Game vs Lab Accuracy (Answers RQ3).
- **Mann-Whitney U Test:** The non-parametric replacement for the Independent t-test. It compares Single vs Multiple Target accuracy (Answers RQ2).

### The Mathematical Formulas Used
**Mann-Whitney $U$ Test:** Ranks all scores across both independent groups from smallest to largest, then calculates the $U$ statistic based on the sum of the ranks ($R$) for each group.
$$ U_1 = n_1 n_2 + \frac{n_1(n_1 + 1)}{2} - R_1 $$
$$ U_2 = n_1 n_2 + \frac{n_2(n_2 + 1)}{2} - R_2 $$
*(The final $U$ statistic is the smaller value between $U_1$ and $U_2$)*.

**Wilcoxon Signed-Rank Test ($W$):** Calculates the absolute differences between paired scores, ranks those non-zero differences without considering their signs, and then sums the ranks associated with positive differences ($W^+$) and negative differences ($W^-$).
$$ W = \min(\sum R_+, \sum R_-) $$

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
