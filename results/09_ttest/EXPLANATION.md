# t-Test Analysis Explanation

## Overview
This folder contains the post-hoc follow-up tests for Reaction Time to pinpoint exactly *where* the significant differences in the ANOVA actually occurred in isolation. 
- **Paired t-tests** were used for Within-Subjects comparisons (Game vs Lab).
- **Independent t-tests** were used for Between-Subjects comparisons (Single vs Multi).

## The Plot Explained
### `plot_ttest_comparison.png`
This image contains two specific charts:
1.  **Left (Paired Differences):** This shows the absolute difference between a participant's Game RT and their Lab RT. Because the boxes sit entirely above the '0' dashed vertical line for Single Targets, it visually proves that the Game was consistently slower than the Lab for that task.
2.  **Right (Group Comparison):** Standard box-and-whisker plots comparing the absolute spreads of RT across the four independent cells. It clearly visualizes that "Single Phone" is sitting astronomically higher on the Y-Axis than the other three conditions.

## Key Outcomes
1.  **Single Phone vs Single Lab (Paired t-test):** Massively significant (p < .0001). The Gamified version was ~1422 ms slower per target. 
2.  **Multiple Phone vs Multiple Lab (Paired t-test):** NOT significant (p = 0.136). When the cognitive load increased to 5 targets, the interface (Game vs Lab) no longer mattered! Search times completely equalized.
3.  **Single vs Multi (Independent t-tests):** Both the Phone and the Lab showed significant differences depending on target count. 

**Conclusion:** The massive ANOVA main effects were almost entirely driven by the fact that the "Single Phone" (Level 1) searches took participants an unusually long time to orient themselves to compared to the sterile Lab.
