"""
Step 6: Descriptive Statistics
- Generates Mean, SD, Median, Min, Max tables for all conditions
- Saves formatted tables for direct use in the report
"""
import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLEANED_PATH = os.path.join(BASE_DIR, "results", "03_outlier_analysis", "cleaned_all_conditions.csv")
RESULTS_DIR = os.path.join(BASE_DIR, "results", "06_descriptive_stats")
os.makedirs(RESULTS_DIR, exist_ok=True)

if __name__ == "__main__":
    data = pd.read_csv(CLEANED_PATH)
    
    print("=" * 70)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 70)
    
    conditions = ["Single_Phone", "Single_Lab", "Multiple_Phone", "Multiple_Lab"]
    metrics = {"Mean_Accuracy": "Accuracy (%)", "Mean_RT": "Reaction Time (ms/target)"}
    
    rows = []
    for metric, label in metrics.items():
        for cond in conditions:
            vals = data[data["Condition"] == cond][metric].dropna().values
            rows.append({
                "Metric": label,
                "Condition": cond,
                "N": len(vals),
                "Mean": np.mean(vals),
                "SD": np.std(vals, ddof=1),
                "Median": np.median(vals),
                "Min": np.min(vals),
                "Max": np.max(vals)
            })
    
    desc_df = pd.DataFrame(rows)
    print(desc_df.to_string(index=False))
    desc_df.to_csv(os.path.join(RESULTS_DIR, "descriptive_statistics.csv"), index=False)
    
    # --- Create a visual table plot ---
    fig, axes = plt.subplots(2, 1, figsize=(12, 6))
    
    for idx, (metric, label) in enumerate(metrics.items()):
        ax = axes[idx]
        sub = desc_df[desc_df["Metric"] == label]
        ax.axis("off")
        table_data = sub[["Condition", "N", "Mean", "SD", "Median", "Min", "Max"]].values
        col_labels = ["Condition", "N", "Mean", "SD", "Median", "Min", "Max"]
        table_data_fmt = []
        for row in table_data:
            table_data_fmt.append([
                row[0], int(row[1]),
                f"{row[2]:.2f}", f"{row[3]:.2f}", f"{row[4]:.2f}",
                f"{row[5]:.2f}", f"{row[6]:.2f}"
            ])
        
        tbl = ax.table(cellText=table_data_fmt, colLabels=col_labels,
                       cellLoc="center", loc="center")
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(10)
        tbl.scale(1, 1.5)
        for key, cell in tbl.get_celld().items():
            if key[0] == 0:
                cell.set_facecolor("#4C72B0")
                cell.set_text_props(color="white", fontweight="bold")
            else:
                cell.set_facecolor("#f0f0f0" if key[0] % 2 == 0 else "white")
        ax.set_title(f"Descriptive Statistics: {label}", fontsize=13, fontweight="bold", pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "plot_descriptive_table.png"), dpi=150, bbox_inches="tight")
    plt.close()
    
    # --- Bar chart with error bars ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
    
    for idx, (metric, label) in enumerate(metrics.items()):
        ax = axes[idx]
        means = []
        sds = []
        labels = []
        for cond in conditions:
            vals = data[data["Condition"] == cond][metric].dropna().values
            means.append(np.mean(vals))
            sds.append(np.std(vals, ddof=1))
            labels.append(cond.replace("_", "\n"))
        
        bars = ax.bar(labels, means, yerr=sds, capsize=8, color=colors,
                      edgecolor="black", linewidth=0.8, alpha=0.85)
        ax.set_ylabel(label, fontsize=12)
        ax.set_title(f"Mean {label} by Condition (±1 SD)", fontsize=13, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        
        for bar, m, s in zip(bars, means, sds):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + s + 0.5,
                    f"{m:.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "plot_descriptive_bars.png"), dpi=150, bbox_inches="tight")
    plt.close()
    
    print(f"\nSaved to: {RESULTS_DIR}")
    print("Descriptive statistics complete!")
