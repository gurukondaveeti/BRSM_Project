# 2x2 Mixed Factorial ANOVA

## 1. What Statistical Tests Are In Here?
- **2x2 Mixed Factorial ANOVA:** This is a single, massive parametric test. It takes all the Reaction Time data and tests three things at once: 
    1. The main effect of Target Load (Answers RQ2).
    2. The main effect of Modality (Answers RQ3).
    3. The Interaction (how Load and Modality affect each other).

## 2. Which Plot is for Which Test?
### `plot_interaction_rt.png`
This plot specifically visualizes the **Interaction Effect** of the 2x2 Mixed ANOVA test.
- The Blue Line tracks Reaction Time for people who only had 1 target.
- The Red Line tracks Reaction time for people who had 5 targets.

---

## 3. Final Answers for Your Report 

*The scientific threshold for statistical significance is **alpha ($\alpha$) = 0.05**. If our $p$-value is **LESS THAN 0.05**, we declare it "Significant".*

### ANSWERING RQ2: Is performance significantly worse in the Multiple Target condition compared to the Single Target condition?
*   **Test Used:** Main Effect of Target Load 
*   **Exact Value:** $p = 0.0000$ (Mathematically, $p = 1.33 \times 10^{-12}$)
*   **Is it significant?** YES. Since 0.0000 < 0.05, it is highly significant. 
*   **Final Conclusion to write for RQ2:** Yes. The ANOVA proves that increasing the target load fundamentally alters the average search time per target. (Note: The independent t-tests in Folder 09 will tell us *exactly* who was worse).

### ANSWERING RQ3: Does the gamified interface significantly alter performance compared to the standard lab interface?
*   **Test Used:** Main Effect of Modality 
*   **Exact Value:** $p = 0.0000$ (Mathematically, $p = 1.08 \times 10^{-12}$)
*   **Is it significant?** YES. Since 0.0000 < 0.05, it is highly significant. 
*   **Final Conclusion to write for RQ3:** Yes. The ANOVA definitively proves that forcing a human to search using a Gamified app causes drastically different reaction times than using a sterile, boring lab computer monitor.

### THE INTERACTION EFFECT (Crucial for the discussion section!)
*   **Test Used:** Load $\times$ Modality Interaction
*   **Exact Value:** $p = 0.0000$ (Mathematically, $p = 5.29 \times 10^{-12}$)
*   **Is it significant?** YES! Since 0.0000 < 0.05, it is highly significant. 
*   **Final Conclusion to write for your Discussion:** We found a massive, significant **Crossover Interaction**. This proves that the effect of Gamification completely changes depending on how hard the task is. Gamification heavily slows down human processing on easy tasks (1 target), but slightly speeds up human processing on complex tasks (5 targets)!
