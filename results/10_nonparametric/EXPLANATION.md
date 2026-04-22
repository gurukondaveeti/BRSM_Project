# RQ2 & RQ3: Non-Parametric Accuracy Analysis

## 1. What Statistical Tests Are In Here?
Because your human test subjects scored perfectly (100%) so often, the accuracy bell curve broke. This meant we could not legally use ANOVAs or t-tests, so we had to use "Non-Parametric" math, which analyzes the Median instead of the Mean.
- **Wilcoxon Signed-Rank Test:** This is the non-parametric replacement for the Paired t-test. It compares Game vs Lab Accuracy.
- **Mann-Whitney U Test:** This is the non-parametric replacement for the Independent t-test. It compares Single vs Multiple Target accuracy.

## 2. Which Plot is for Which Test?
### `plot_nonparametric_accuracy.png`
- **Left Plot:** Visualizes the spread of Accuracy, mapping exactly to what the `Mann-Whitney U` sees. 
- **Right Plot:** Visualizes the Medians of all four groups. Both the `Mann-Whitney U` and the `Wilcoxon Signed-Rank` tests are mathematically checking to see if these median bars are statistically different heights. 

## 3. The Results & Why They Are (Or Aren't) Significant
*The scientific threshold for statistical significance is **alpha ($\alpha$) = 0.05**. If our $p$-value is **LESS THAN 0.05**, we declare it "Significant".*

**A. Game vs Lab Accuracy — Single Target (Wilcoxon Signed-Rank)**
*   **Exact Value:** $p = 0.0022$
*   **Is it significant?** YES. Since 0.0022 < 0.05, it is significant. 
*   **Outcome:** Human accuracy natively degraded down to ~96% in the Game, compared to sitting at a flawless 100% in the sterile Lab.

**B. Game vs Lab Accuracy — Multiple Target (Wilcoxon Signed-Rank)**
*   **Exact Value:** $p = 0.1330$
*   **Is it significant?** NO. Since 0.1330 > 0.05, it is not significant. 
*   **Outcome:** The accuracy medians (99.3% Lab vs 96.3% Game) are statistically identical under this test.

**C. Single vs Multi Target — Phone (Mann-Whitney U)**
*   **Exact Value:** $p = 0.3593$
*   **Is it significant?** NO. Since 0.3593 > 0.05, it is not significant. 
*   **Outcome:** The gamified app kept humans just as accurate at Level 1 as it did when evaluating 5 targets.

**D. Single vs Multi Target — Lab (Mann-Whitney U)**
*   **Exact Value:** $p = 0.0006$
*   **Is it significant?** YES. Since 0.0006 < 0.05, it is highly significant. 
*   **Outcome:** The sterile lab environment caused human accuracy to systematically degrade when evaluating 5 targets. Gamification somehow protected against this!
