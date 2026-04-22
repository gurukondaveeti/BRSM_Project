# t-Test Follow-up Analysis

## 1. What Statistical Tests Are In Here?
Because the massive ANOVA test in Folder 08 proved that "differences exist" for RQ2 and RQ3, we use **t-tests** to hunt down exactly where those differences hit the hardest.
- **Paired Samples t-test:** Used to compare Game vs Lab (Answers RQ3).
- **Independent Samples t-test:** Used to compare Single vs Multiple Targets (Answers RQ2).

## 2. Which Plot is for Which Test?
### `plot_ttest_comparison.png`
- **Left Plot:** Visualizes the `Paired Samples t-tests`. It charts the physical time difference between identical participants jumping from the Phone to the Lab.
- **Right Plot:** Visualizes the `Independent Samples t-tests`. It maps the raw group spreads.

---

## 3. Final Answers for Your Report 

*The scientific threshold for statistical significance is **alpha ($\alpha$) = 0.05**. If our $p$-value is **LESS THAN 0.05**, we declare it "Significant".*

### ANSWERING RQ3: Does the gamified interface significantly alter performance compared to the standard lab interface? (Part 1 - Reaction Time)

**A. Phone (Game) vs Lab — Single Target (Paired t-test)**
*   **Exact Value:** $p = 0.0000$ (Mathematically, $p = 9.13 \times 10^{-11}$)
*   **Is it significant?** YES. Since 0.0000 < 0.05, it is massively significant. 
*   **Conclusion to write:** For simple 1-target searches, the Lab was significantly **faster** (~1422 ms faster) than the Gamified interface.

**B. Phone (Game) vs Lab — Multiple Target (Paired t-test)**
*   **Exact Value:** $p = 0.1366$
*   **Is it significant?** NO! Since 0.1366 > 0.05, it is not significant. 
*   **Conclusion to write:** As soon as you increase cognitive load to 5 targets, the interface completely stops mattering. Reaction times statistically equalized, meaning neither the Gamified interface nor the Lab interface was faster or slower.

### ANSWERING RQ2: Is performance significantly worse in the Multiple Target condition compared to the Single Target condition? (Part 1 - Reaction Time)

**C. Single vs Multi — Phone (Independent t-test)**
*   **Exact Value:** $p = 0.0000$ (Mathematically, $p = 1.52 \times 10^{-14}$)
*   **Is it significant?** YES. Since 0.0000 < 0.05, it is highly significant. 

**D. Single vs Multi — Lab (Independent t-test)**
*   **Exact Value:** $p = 0.0001$ 
*   **Is it significant?** YES. Since 0.0001 < 0.05, it is highly significant.

**Final Conclusion to write for RQ2 (Reaction Time):** Yes. When explicitly breaking down the data, processing multiple targets is significantly **faster (more efficient per-target)** than processing a single target, and this mathematically holds true regardless of whether the participant is using the Gamified Phone application or the sterile Lab environment.
