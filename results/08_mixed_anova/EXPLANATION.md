# 2x2 Mixed Factorial ANOVA Explanation

## Overview
This folder investigates both **RQ2 (Target Load)** and **RQ3 (Modality)** simultaneously for Reaction Time. It evaluates the "Main Effects" of each variable, and critically, the "Interaction Effect" between them.

## The Plot Explained
### `plot_interaction_rt.png`
This line graph is the most important plot in a Factorial ANOVA.
- **X-Axis:** The Interface Modality (Phone/Game on the left, Lab on the right).
- **The Blue Line:** The group searching for a Single Target.
- **The Red Line:** The group searching for Multiple Targets.
- **Understanding Interaction:** If the two lines were perfectly parallel, there is NO interaction. However, look at the plot! The Blue line steeply slopes downward from Phone to Lab, while the Red line tilts slightly UPWARD. **Because the lines cross or drastically alter their angle relative to each other, a massive Interaction Effect has occurred.**

## Key Outcomes (All Highly Significant, p < .0001)
1.  **Main Effect of Target Load:** The number of targets heavily alters average target processing time. 
2.  **Main Effect of Modality:** Gamifying the interface heavily alters the absolute reaction time.
3.  **The Interaction Effect:** Gamification does not just "make people faster" or "make people slower". Instead, Gamification affects you differently *depending on how hard the task is*. When there is 1 target, the Game is vastly slower than the Lab. But when there are 5 targets, the Game is actually slightly faster/more efficient per-target than the Lab! Gamification seems to help process high visual loads better than low visual loads.
