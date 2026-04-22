"""
Step 4: Normality Testing
- Shapiro-Wilk test (best for small samples)
- Q-Q plots
- Histograms with normal curve overlay
- Reports skewness and kurtosis
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")


def test_normality(values, label):
    """Perform comprehensive normality testing."""
    n = len(values)
    mean = np.mean(values)
    std = np.std(values, ddof=1)
    skewness = stats.skew(values)
    kurtosis = stats.kurtosis(values)
    
    # Shapiro-Wilk test
    if n >= 3:
        sw_stat, sw_p = stats.shapiro(values)
    else:
        sw_stat, sw_p = np.nan, np.nan
    
    return {
        "label": label,
        "n": n,
        "mean": mean,
        "std": std,
        "skewness": skewness,
        "kurtosis": kurtosis,
        "shapiro_W": sw_stat,
        "shapiro_p": sw_p,
        "is_normal": sw_p > 0.05 if not np.isnan(sw_p) else None,
        "skew_type": classify_skewness(skewness)
    }


def classify_skewness(skew):
    """Classify the type of skewness for transformation guidance."""
    if abs(skew) < 0.5:
        return "Approximately Symmetric"
    elif 0.5 <= skew < 1.0:
        return "Moderately Positive Skew"
    elif skew >= 1.0:
        return "Substantially Positive Skew"
    elif -1.0 < skew <= -0.5:
        return "Moderately Negative Skew"
    elif skew <= -1.0:
        return "Substantially Negative Skew"
    return "Unknown"


def create_normality_plots(data, conditions, metric, ylabel, filename_prefix):
    """Create Q-Q plots and histograms for each condition."""
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    condition_labels = ["Single Phone", "Single Lab", "Multiple Phone", "Multiple Lab"]
    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
    
    for i, (cond, label, color) in enumerate(zip(conditions, condition_labels, colors)):
        values = data[data["Condition"] == cond][metric].dropna().values
        
        # Row 1: Histogram with normal curve
        ax = axes[0, i]
        ax.hist(values, bins="auto", density=True, color=color, alpha=0.6, edgecolor="black")
        
        # Overlay normal curve
        if len(values) >= 3 and np.std(values) > 0:
            x = np.linspace(values.min() - np.std(values), values.max() + np.std(values), 100)
            ax.plot(x, stats.norm.pdf(x, np.mean(values), np.std(values)), 
                    "k-", linewidth=2, label="Normal fit")
        
        skew = stats.skew(values)
        ax.set_title(f"{label}\n(skew={skew:.2f})", fontsize=11, fontweight="bold")
        ax.set_xlabel(ylabel, fontsize=9)
        ax.set_ylabel("Density", fontsize=9)
        ax.legend(fontsize=8)
        
        # Row 2: Q-Q Plot
        ax = axes[1, i]
        if len(values) >= 3:
            stats.probplot(values, dist="norm", plot=ax)
            ax.set_title(f"Q-Q Plot: {label}", fontsize=11, fontweight="bold")
        else:
            ax.text(0.5, 0.5, "Too few data points", ha="center", va="center")
            ax.set_title(f"Q-Q Plot: {label}", fontsize=11)
    
    plt.suptitle(f"Normality Assessment: {ylabel}", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    filepath = os.path.join(RESULTS_DIR, f"{filename_prefix}.png")
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {filepath}")


if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# NORMALITY TESTING")
    print("#" * 60 + "\n")
    
    # Load cleaned data
    cleaned_path = os.path.join(RESULTS_DIR, "cleaned_all_conditions.csv")
    if os.path.exists(cleaned_path):
        data = pd.read_csv(cleaned_path)
        print("Using cleaned data (after outlier removal)\n")
    else:
        data = pd.read_csv(os.path.join(RESULTS_DIR, "extracted_all_conditions.csv"))
        print("Using raw extracted data (no outlier removal done)\n")
    
    conditions = ["Single_Phone", "Single_Lab", "Multiple_Phone", "Multiple_Lab"]
    metrics = {"Mean_Accuracy": "Accuracy (%)", "Mean_RT": "Reaction Time (ms)"}
    
    all_results = []
    report_lines = []
    
    for metric, ylabel in metrics.items():
        header = f"\n{'='*60}"
        report_lines.append(header); print(header)
        header = f"NORMALITY TESTS FOR: {ylabel}"
        report_lines.append(header); print(header)
        header = f"{'='*60}"
        report_lines.append(header); print(header)
        
        for cond in conditions:
            values = data[data["Condition"] == cond][metric].dropna().values
            result = test_normality(values, f"{cond}_{metric}")
            all_results.append(result)
            
            line = f"\n  {cond}:"
            report_lines.append(line); print(line)
            line = f"    N = {result['n']}, Mean = {result['mean']:.2f}, SD = {result['std']:.2f}"
            report_lines.append(line); print(line)
            line = f"    Skewness = {result['skewness']:.4f} ({result['skew_type']})"
            report_lines.append(line); print(line)
            line = f"    Kurtosis = {result['kurtosis']:.4f}"
            report_lines.append(line); print(line)
            line = f"    Shapiro-Wilk: W = {result['shapiro_W']:.4f}, p = {result['shapiro_p']:.4f}"
            report_lines.append(line); print(line)
            
            if result['is_normal']:
                line = f"    *** RESULT: Data IS normally distributed (p > 0.05) ***"
            else:
                line = f"    *** RESULT: Data is NOT normally distributed (p <= 0.05) ***"
            report_lines.append(line); print(line)
    
    # Create summary table
    header = f"\n\n{'='*60}"
    report_lines.append(header); print(header)
    header = "NORMALITY SUMMARY TABLE"
    report_lines.append(header); print(header)
    header = f"{'='*60}"
    report_lines.append(header); print(header)
    
    summary_df = pd.DataFrame(all_results)
    summary_df = summary_df[["label", "n", "mean", "std", "skewness", "kurtosis", 
                              "shapiro_W", "shapiro_p", "is_normal", "skew_type"]]
    
    line = "\n" + summary_df.to_string(index=False)
    report_lines.append(line); print(line)
    
    # Save summary
    summary_df.to_csv(os.path.join(RESULTS_DIR, "normality_test_results.csv"), index=False)
    
    # Recommendation for transformations
    header = f"\n\n{'='*60}"
    report_lines.append(header); print(header)
    header = "TRANSFORMATION RECOMMENDATIONS"
    report_lines.append(header); print(header)
    header = f"{'='*60}"
    report_lines.append(header); print(header)
    
    non_normal = [r for r in all_results if not r['is_normal']]
    if non_normal:
        line = f"\n{len(non_normal)} distributions are NOT normal and need transformation:"
        report_lines.append(line); print(line)
        for r in non_normal:
            skew_type = r['skew_type']
            if "Moderately Positive" in skew_type:
                transform = "sqrt(x)"
            elif "Substantially Positive" in skew_type:
                if any(data[data["Condition"] == r['label'].split('_Mean')[0].replace('_Accuracy','').replace('_RT','')]["Mean_Accuracy"].min() == 0 for _ in [0]):
                    transform = "log10(x + c)"
                else:
                    transform = "log10(x)"
            elif "Moderately Negative" in skew_type:
                transform = "sqrt(k - x) where k = max + 1"
            elif "Substantially Negative" in skew_type:
                transform = "log10(k - x) where k = max + 1"
            else:
                transform = "Try multiple transformations"
            
            line = f"\n  {r['label']}:"
            report_lines.append(line); print(line)
            line = f"    Skewness: {r['skewness']:.4f} ({skew_type})"
            report_lines.append(line); print(line)
            line = f"    Recommended transformation: {transform}"
            report_lines.append(line); print(line)
    else:
        line = "\nAll distributions are normal! No transformation needed."
        report_lines.append(line); print(line)
    
    # Save report
    with open(os.path.join(RESULTS_DIR, "normality_test_report.txt"), "w") as f:
        f.write("\n".join(report_lines))
    print(f"\n  Report saved: {os.path.join(RESULTS_DIR, 'normality_test_report.txt')}")
    
    # Create plots
    print("\nCreating normality plots...")
    for metric, ylabel in metrics.items():
        create_normality_plots(data, conditions, metric, ylabel, f"plot_normality_{metric.lower()}")
    
    print("\nNormality testing complete!")
