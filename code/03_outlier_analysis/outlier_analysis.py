"""
Step 3: Outlier Analysis
- Uses IQR method to identify outliers
- Conservative removal: Only removes extreme outliers (>3×IQR) given small sample size
- Creates before/after comparison plots
- Saves cleaned data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")


def identify_outliers_iqr(values, multiplier=1.5):
    """Identify outliers using IQR method. Returns boolean mask."""
    Q1 = np.percentile(values, 25)
    Q3 = np.percentile(values, 75)
    IQR = Q3 - Q1
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR
    return (values < lower) | (values > upper), lower, upper, Q1, Q3, IQR


def analyze_outliers_for_condition(data, condition, metric, multiplier=1.5):
    """Analyze outliers for a specific condition and metric."""
    subset = data[data["Condition"] == condition][metric].dropna()
    pids = data[data["Condition"] == condition]["ParticipantID"]
    
    is_outlier, lower, upper, Q1, Q3, IQR = identify_outliers_iqr(subset.values, multiplier)
    
    outlier_pids = pids[is_outlier].values
    outlier_vals = subset[is_outlier].values
    
    return {
        "condition": condition,
        "metric": metric,
        "n": len(subset),
        "Q1": Q1, "Q3": Q3, "IQR": IQR,
        "lower_fence": lower, "upper_fence": upper,
        "multiplier": multiplier,
        "n_outliers": sum(is_outlier),
        "outlier_pids": outlier_pids,
        "outlier_values": outlier_vals,
        "is_outlier_mask": is_outlier
    }


def print_outlier_report(results, report_lines):
    """Print detailed outlier report."""
    line = f"\n{'='*60}"
    print(line); report_lines.append(line)
    line = f"Condition: {results['condition']} | Metric: {results['metric']}"
    print(line); report_lines.append(line)
    line = f"{'='*60}"
    print(line); report_lines.append(line)
    line = f"  N = {results['n']}"
    print(line); report_lines.append(line)
    line = f"  Q1 = {results['Q1']:.2f}, Q3 = {results['Q3']:.2f}, IQR = {results['IQR']:.2f}"
    print(line); report_lines.append(line)
    line = f"  Lower Fence ({results['multiplier']}×IQR): {results['lower_fence']:.2f}"
    print(line); report_lines.append(line)
    line = f"  Upper Fence ({results['multiplier']}×IQR): {results['upper_fence']:.2f}"
    print(line); report_lines.append(line)
    line = f"  Outliers found: {results['n_outliers']}"
    print(line); report_lines.append(line)
    
    if results['n_outliers'] > 0:
        for pid, val in zip(results['outlier_pids'], results['outlier_values']):
            line = f"    -> Participant {int(pid)}: {val:.2f}"
            print(line); report_lines.append(line)
    else:
        line = f"    -> No outliers detected"
        print(line); report_lines.append(line)


def create_outlier_comparison_plot(data, cleaned_data, metric, ylabel, filename):
    """Create before/after outlier removal comparison plot."""
    conditions = ["Single_Phone", "Single_Lab", "Multiple_Phone", "Multiple_Lab"]
    condition_labels = ["Single\nPhone", "Single\nLab", "Multiple\nPhone", "Multiple\nLab"]
    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
    
    for ax, df, title_suffix in zip(axes, [data, cleaned_data], ["BEFORE Removal", "AFTER Removal"]):
        box_data = []
        for cond in conditions:
            values = df[df["Condition"] == cond][metric].dropna().values
            box_data.append(values)
        
        bp = ax.boxplot(box_data, widths=0.5, patch_artist=True,
                         medianprops=dict(linewidth=2, color="black"),
                         boxprops=dict(linewidth=1.5))
        
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.3)
        
        for i, (cond, color) in enumerate(zip(conditions, colors)):
            values = df[df["Condition"] == cond][metric].dropna().values
            jitter = np.random.uniform(-0.15, 0.15, size=len(values))
            ax.scatter(np.full(len(values), i + 1) + jitter, values,
                       c=color, edgecolor="black", linewidth=0.5,
                       s=50, alpha=0.8, zorder=5)
        
        ax.set_xticks(range(1, len(conditions) + 1))
        ax.set_xticklabels(condition_labels, fontsize=10)
        ax.set_title(f"{ylabel} - {title_suffix}", fontsize=13, fontweight="bold")
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(axis="y", alpha=0.3)
        
        # Add count annotations
        for i, vals in enumerate(box_data):
            ax.text(i + 1, ax.get_ylim()[0], f"n={len(vals)}",
                    ha="center", va="top", fontsize=9, fontweight="bold")
    
    plt.tight_layout()
    filepath = os.path.join(RESULTS_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {filepath}")


if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# OUTLIER ANALYSIS - Conservative Approach")
    print("#" * 60 + "\n")
    
    data = pd.read_csv(os.path.join(RESULTS_DIR, "extracted_all_conditions.csv"))
    
    conditions = ["Single_Phone", "Single_Lab", "Multiple_Phone", "Multiple_Lab"]
    metrics = ["Mean_Accuracy", "Mean_RT"]
    
    report_lines = []
    all_outlier_info = []
    
    # ===== STEP 1: Detect outliers using standard 1.5×IQR =====
    header = "\n" + "#" * 60
    report_lines.append(header); print(header)
    header = "# STANDARD OUTLIER DETECTION (1.5 × IQR)"
    report_lines.append(header); print(header)
    header = "#" * 60
    report_lines.append(header); print(header)
    
    for metric in metrics:
        for cond in conditions:
            result = analyze_outliers_for_condition(data, cond, metric, multiplier=1.5)
            print_outlier_report(result, report_lines)
            all_outlier_info.append(result)
    
    # ===== STEP 2: Detect extreme outliers using 3×IQR =====
    header = "\n\n" + "#" * 60
    report_lines.append(header); print(header)
    header = "# EXTREME OUTLIER DETECTION (3 × IQR)"
    report_lines.append(header); print(header)
    header = "#" * 60
    report_lines.append(header); print(header)
    
    extreme_outlier_info = []
    for metric in metrics:
        for cond in conditions:
            result = analyze_outliers_for_condition(data, cond, metric, multiplier=3.0)
            print_outlier_report(result, report_lines)
            extreme_outlier_info.append(result)
    
    # ===== STEP 3: Decision Making =====
    header = "\n\n" + "#" * 60
    report_lines.append(header); print(header)
    header = "# OUTLIER REMOVAL DECISION"
    report_lines.append(header); print(header)
    header = "#" * 60
    report_lines.append(header); print(header)
    
    line = "\nStrategy: Conservative approach due to small sample sizes (N=16-21)"
    report_lines.append(line); print(line)
    line = "- Only remove EXTREME outliers (> 3×IQR) that are clearly erroneous"
    report_lines.append(line); print(line)
    line = "- Keep mild outliers (1.5-3×IQR) as they may represent natural variation"
    report_lines.append(line); print(line)
    line = "- Flag all outliers in the report for transparency"
    report_lines.append(line); print(line)
    
    # Create cleaned dataset - remove only extreme outliers (> 3×IQR)
    cleaned_data = data.copy()
    removed_count = 0
    
    for result in extreme_outlier_info:
        if result["n_outliers"] > 0:
            cond = result["condition"]
            metric = result["metric"]
            for pid, val in zip(result["outlier_pids"], result["outlier_values"]):
                # Remove entire participant row if any metric is an extreme outlier
                mask = (cleaned_data["Condition"] == cond) & (cleaned_data["ParticipantID"] == pid)
                if mask.any():
                    line = f"\n  REMOVING: Participant {int(pid)} from {cond} (extreme outlier in {metric}: {val:.2f})"
                    report_lines.append(line); print(line)
                    cleaned_data = cleaned_data[~mask]
                    removed_count += 1
    
    if removed_count == 0:
        line = "\n  No extreme outliers found. All data points retained."
        report_lines.append(line); print(line)
        line = "  Standard outliers (1.5×IQR) are kept due to small sample size."
        report_lines.append(line); print(line)
    
    line = f"\n  Original data points: {len(data)}"
    report_lines.append(line); print(line)
    line = f"  After cleaning: {len(cleaned_data)}"
    report_lines.append(line); print(line)
    line = f"  Points removed: {len(data) - len(cleaned_data)}"
    report_lines.append(line); print(line)
    
    # Save cleaned data
    cleaned_data.to_csv(os.path.join(RESULTS_DIR, "cleaned_all_conditions.csv"), index=False)
    
    # Save outlier report
    with open(os.path.join(RESULTS_DIR, "outlier_analysis_report.txt"), "w") as f:
        f.write("\n".join(report_lines))
    print(f"\n  Report saved: {os.path.join(RESULTS_DIR, 'outlier_analysis_report.txt')}")
    
    # Create comparison plots
    print("\nCreating outlier comparison plots...")
    create_outlier_comparison_plot(data, cleaned_data, "Mean_Accuracy",
                                   "Accuracy (%)", "plot_outlier_accuracy.png")
    create_outlier_comparison_plot(data, cleaned_data, "Mean_RT",
                                   "Reaction Time (ms)", "plot_outlier_rt.png")
    
    print("\nOutlier analysis complete!")
