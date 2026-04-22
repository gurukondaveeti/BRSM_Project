# Descriptive Statistics Explanation

## Overview
This folder contains the baseline descriptive statistics (Means, Medians, Standard Deviations, Minimums, and Maximums) for both Reaction Time (RT) and Accuracy across all four experimental conditions.

## The Plots Explained
### `plot_descriptive_bars.png`
This plot provides a side-by-side bar chart for Accuracy and Reaction Time. 
- **The Bars:** The height of each bar represents the **Mean** score for that specific group (e.g., Single Phone, Multiple Lab).
- **The Error Bars (Black lines):** The vertical lines protruding from the top of the bars represent **±1 Standard Deviation (SD)**. This visualizes the spread or variance of the data. A taller error bar means the participants in that group had wildly different scores, while a short error bar means everyone performed very similarly.
- **Noteworthy Finding:** Notice the `Single_Lab` accuracy has no error bar because every single participant scored exactly 100% (zero variance).

### `plot_descriptive_table.png`
This is simply a clean, presentation-ready image of the data table for easy pasting into your final report or slides.

## Key Outcomes
1. **Reaction Time Natively Differs:** Single Phone (Game) has heavily inflated Reaction Times (~2957 ms) compared to the Single Lab (~1527 ms). The phone app naturally demands longer active visual scanning, likely due to screen sizes or object density.
2. **Ceiling Effects in Accuracy:** The data fundamentally shows that participants are scoring between 95% and 100% across almost all conditions, proving the cognitive tasks are generally "easy" enough to complete, forcing us to rely on our Non-Parametric tests for Accuracy downstream.
