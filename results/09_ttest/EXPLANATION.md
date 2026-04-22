# RQ2 & RQ3: t-Test Follow-up Analysis

## 1. What Statistical Tests Are In Here?
Because the massive ANOVA test in Folder 08 proved that "differences exist", it is scientifically standard to use **t-tests** to hunt down exactly where those differences are.
- **Paired Samples t-test:** Used to compare Game vs Lab (because the exact same participant played the Game and sat at the Lab).
- **Independent Samples t-test:** Used to compare Single Target vs Multiple Target (because different, unconnected participants did those respective tasks).

## 2. Which Plot is for Which Test?
### `plot_ttest_comparison.png`
- **Left Plot:** Visualizes the `Paired Samples t-tests`. It charts the physical time difference between identical participants jumping from the Phone to the Lab.
- **Right Plot:** Visualizes the `Independent Samples t-tests`. It just maps the raw group spreads.

## 3. The Results & Why They Are (Or Aren't) Significant
*The scientific threshold for statistical significance is **alpha ($\alpha$) = 0.05**. If our $p$-value is **LESS THAN 0.05**, we declare it "Significant".*

**A. Phone (Game) vs Lab — Single Target (Paired t-test)**
*   **Exact Value:** $p = 0.0000$ (Mathematically, $p = 9.13 \times 10^{-11}$)
*   **Is it significant?** YES. Since 0.0000 < 0.05, it is massively significant. 
*   **Outcome:** For simple 1-target searches, the Lab was significantly faster (~1422 ms faster) than the Game.

**B. Phone (Game) vs Lab — Multiple Target (Paired t-test)**
*   **Exact Value:** $p = 0.1366$
*   **Is it significant?** NO! Since 0.1366 > 0.05, it is not significant. 
*   **Outcome:** As soon as you increase cognitive load to 5 targets, the interface (Game vs Lab) completely stops mattering. Reaction times equalized.

**C. Single vs Multi — Phone (Independent t-test)**
*   **Exact Value:** $p = 0.0000$ (Mathematically, $p = 1.52 \times 10^{-14}$)
*   **Is it significant?** YES. Since 0.0000 < 0.05, it is highly significant. 

**D. Single vs Multi — Lab (Independent t-test)**
*   **Exact Value:** $p = 0.0001$ 
*   **Is it significant?** YES. Since 0.0001 < 0.05, it is highly significant.
