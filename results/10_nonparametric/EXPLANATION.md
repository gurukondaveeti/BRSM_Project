# Non-Parametric Accuracy Analysis Explanation

## Overview
Because human Accuracy suffered from a "Ceiling Effect" (where most people scored near 100%, breaking normal bell-curve distributions), we legally could not use Parametric ANOVAs. This folder contains the **Robust Non-Parametric tests** matching RQ2 & RQ3 for Accuracy.

## The Plot Explained
### `plot_nonparametric_accuracy.png`
This image contains two visualizations evaluating Accuracy distributions:
1.  **Left (Distribution Box Plots):** Notice how "squished" the boxes are at the very top of the graph (near 100%). You can see the individual black dots scattered downwards, representing the few students who scored an 85% or 90%. Single Lab has no box, just a flat line, because 100% of humans scored 100%.
2.  **Right (Median Bar Chart):** Non-parametric tests evaluate the **Median** instead of the Mean. This chart shows the medians are all sitting comfortably between 96% and 100%.

## Key Outcomes
1.  **Wilcoxon Signed-Rank (Game vs Lab):** Only the Single Target group was significant (p = 0.002). The Lab single-target was slightly more accurate (100% median) than the Game single-target (~97% median). For multiple targets, the interface didn't alter accuracy.
2.  **Mann-Whitney U (Single vs Multiple):** The Phone Game showed no accuracy difference between 1 and 5 targets. However, the Lab software *did* show a significant drop (p = 0.0005) when moving from 1 to 5 targets.
3.  **Conclusion:** The gamified app protected players from losing accuracy as target load increased, whereas the sterile Lab environment caused accuracy to degrade significantly when the task got harder!
