# RQ2 & RQ3: 2x2 Mixed Factorial ANOVA

## 1. What Statistical Tests Are In Here?
- **2x2 Mixed Factorial ANOVA:** This is a single, massive parametric test. It takes all the Reaction Time data and tests three things at once: 
    1. The effect of Target Load (1 vs 5)
    2. The effect of Modality (Game vs Lab)
    3. The Interaction (how Load and Modality affect each other)

## 2. Which Plot is for Which Test?
### `plot_interaction_rt.png`
This plot specifically visualizes the **Interaction Effect** of the 2x2 Mixed ANOVA test.
- The Blue Line tracks Reaction Time for people who only had 1 target.
- The Red Line tracks Reaction time for people who had 5 targets.

## 3. The Results & Why They Are Significant
*The scientific threshold for statistical significance is **alpha ($\alpha$) = 0.05**. If our $p$-value is **LESS THAN 0.05**, we declare it "Significant".*

**A. Main Effect of Target Load**
*   **Exact Value:** $p = 0.0000$ (Mathematically, $p = 1.33 \times 10^{-12}$)
*   **Is it significant?** YES. Since 0.0000 < 0.05, it is highly significant. 
*   **Outcome:** Making a human search for 5 targets physically changes their average search time compared to searching for 1 target.

**B. Main Effect of Modality (Game vs Lab interface)**
*   **Exact Value:** $p = 0.0000$ (Mathematically, $p = 1.08 \times 10^{-12}$)
*   **Is it significant?** YES. Since 0.0000 < 0.05, it is highly significant. 
*   **Outcome:** A gamified interface causes drastically different reaction times than a sterile, boring lab interface.

**C. Interaction Effect (Load $\times$ Modality)**
*   **Exact Value:** $p = 0.0000$ (Mathematically, $p = 5.29 \times 10^{-12}$)
*   **Is it significant?** YES! Since 0.0000 < 0.05, it is highly significant. 
*   **Outcome:** The effect of Gamification completely changes depending on how hard the level is (how many targets there are) which is called a **Crossover Interaction**. Gamification slows you down on easy tasks, but equals out or slightly speeds you up on complex tasks.
