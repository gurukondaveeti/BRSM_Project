"""
Step 7: Correlation Analysis (RQ1 - Concurrent Validity)
- Pearson's r for RT (normal data)
- Spearman's rho for Accuracy (non-normal data)
- Scatter plots with regression lines
"""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLEANED_PATH = os.path.join(BASE_DIR, "results", "03_outlier_analysis", "cleaned_all_conditions.csv")
RESULTS_DIR = os.path.join(BASE_DIR, "results", "07_correlation")
os.makedirs(RESULTS_DIR, exist_ok=True)

if __name__ == "__main__":
    data = pd.read_csv(CLEANED_PATH)
    
    print("=" * 70)
    print("RQ1: CONCURRENT VALIDITY - CORRELATION ANALYSIS")
    print("=" * 70)
    
    report = []
    
    # We need paired data: same participant did both Game and Lab
    # Single condition: participants 1-21
    # Multiple condition: participants 22-37
    
    single_phone = data[data["Condition"] == "Single_Phone"].set_index("ParticipantID")
    single_lab = data[data["Condition"] == "Single_Lab"].set_index("ParticipantID")
    multi_phone = data[data["Condition"] == "Multiple_Phone"].set_index("ParticipantID")
    multi_lab = data[data["Condition"] == "Multiple_Lab"].set_index("ParticipantID")
    
    # Find common participants
    single_common = single_phone.index.intersection(single_lab.index)
    multi_common = multi_phone.index.intersection(multi_lab.index)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    correlations = []
    
    # ====== SINGLE TARGET CONDITION ======
    print(f"\n--- SINGLE TARGET (N={len(single_common)}) ---")
    report.append(f"\n--- SINGLE TARGET (N={len(single_common)}) ---")
    
    # RT: Pearson (normal)
    game_rt = single_phone.loc[single_common, "Mean_RT"].values
    lab_rt = single_lab.loc[single_common, "Mean_RT"].values
    r_val, p_val = stats.pearsonr(game_rt, lab_rt)
    result_str = f"  RT Pearson's r = {r_val:.4f}, p = {p_val:.4f}"
    if p_val < 0.05:
        result_str += " -> SIGNIFICANT"
    else:
        result_str += " -> Not significant"
    print(result_str); report.append(result_str)
    correlations.append({"Condition": "Single", "Metric": "RT", "Test": "Pearson r",
                         "r": r_val, "p": p_val, "Significant": p_val < 0.05, "N": len(single_common)})
    
    # Plot RT correlation
    ax = axes[0, 0]
    ax.scatter(game_rt, lab_rt, c="#4C72B0", s=60, edgecolors="black", alpha=0.7, zorder=5)
    z = np.polyfit(game_rt, lab_rt, 1)
    p_line = np.poly1d(z)
    x_range = np.linspace(game_rt.min(), game_rt.max(), 100)
    ax.plot(x_range, p_line(x_range), "r--", linewidth=2, alpha=0.8)
    ax.set_xlabel("Game RT (ms/target)", fontsize=11)
    ax.set_ylabel("Lab RT (ms/target)", fontsize=11)
    ax.set_title(f"Single Target: RT Correlation\nr = {r_val:.3f}, p = {p_val:.4f}", fontsize=12, fontweight="bold")
    ax.grid(alpha=0.3)
    
    # Accuracy: Spearman (non-normal)
    game_acc = single_phone.loc[single_common, "Mean_Accuracy"].values
    lab_acc = single_lab.loc[single_common, "Mean_Accuracy"].values
    # Note: Single Lab accuracy is 100% for all, so correlation is undefined
    if np.std(lab_acc) == 0:
        result_str = "  Accuracy Spearman's rho: CANNOT COMPUTE (Single Lab accuracy = 100% for all)"
        print(result_str); report.append(result_str)
        correlations.append({"Condition": "Single", "Metric": "Accuracy", "Test": "Spearman rho",
                             "r": np.nan, "p": np.nan, "Significant": False, "N": len(single_common)})
        ax = axes[0, 1]
        ax.text(0.5, 0.5, "Cannot compute correlation:\nLab Accuracy = 100% for all participants\n(zero variance)",
                ha="center", va="center", fontsize=11, transform=ax.transAxes,
                bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))
        ax.set_title("Single Target: Accuracy Correlation\n(Not Applicable)", fontsize=12, fontweight="bold")
        ax.set_xlabel("Game Accuracy (%)")
        ax.set_ylabel("Lab Accuracy (%)")
    else:
        rho, p_rho = stats.spearmanr(game_acc, lab_acc)
        result_str = f"  Accuracy Spearman's rho = {rho:.4f}, p = {p_rho:.4f}"
        print(result_str); report.append(result_str)
        correlations.append({"Condition": "Single", "Metric": "Accuracy", "Test": "Spearman rho",
                             "r": rho, "p": p_rho, "Significant": p_rho < 0.05, "N": len(single_common)})
    
    # ====== MULTIPLE TARGET CONDITION ======
    print(f"\n--- MULTIPLE TARGET (N={len(multi_common)}) ---")
    report.append(f"\n--- MULTIPLE TARGET (N={len(multi_common)}) ---")
    
    # RT: Pearson (normal)
    game_rt_m = multi_phone.loc[multi_common, "Mean_RT"].values
    lab_rt_m = multi_lab.loc[multi_common, "Mean_RT"].values
    r_val_m, p_val_m = stats.pearsonr(game_rt_m, lab_rt_m)
    result_str = f"  RT Pearson's r = {r_val_m:.4f}, p = {p_val_m:.4f}"
    if p_val_m < 0.05:
        result_str += " -> SIGNIFICANT"
    else:
        result_str += " -> Not significant"
    print(result_str); report.append(result_str)
    correlations.append({"Condition": "Multiple", "Metric": "RT", "Test": "Pearson r",
                         "r": r_val_m, "p": p_val_m, "Significant": p_val_m < 0.05, "N": len(multi_common)})
    
    # Plot RT correlation
    ax = axes[1, 0]
    ax.scatter(game_rt_m, lab_rt_m, c="#C44E52", s=60, edgecolors="black", alpha=0.7, zorder=5)
    z = np.polyfit(game_rt_m, lab_rt_m, 1)
    p_line = np.poly1d(z)
    x_range = np.linspace(game_rt_m.min(), game_rt_m.max(), 100)
    ax.plot(x_range, p_line(x_range), "r--", linewidth=2, alpha=0.8)
    ax.set_xlabel("Game RT (ms/target)", fontsize=11)
    ax.set_ylabel("Lab RT (ms/target)", fontsize=11)
    ax.set_title(f"Multiple Target: RT Correlation\nr = {r_val_m:.3f}, p = {p_val_m:.4f}", fontsize=12, fontweight="bold")
    ax.grid(alpha=0.3)
    
    # Accuracy: Spearman (non-normal)
    game_acc_m = multi_phone.loc[multi_common, "Mean_Accuracy"].values
    lab_acc_m = multi_lab.loc[multi_common, "Mean_Accuracy"].values
    rho_m, p_rho_m = stats.spearmanr(game_acc_m, lab_acc_m)
    result_str = f"  Accuracy Spearman's rho = {rho_m:.4f}, p = {p_rho_m:.4f}"
    if p_rho_m < 0.05:
        result_str += " -> SIGNIFICANT"
    else:
        result_str += " -> Not significant"
    print(result_str); report.append(result_str)
    correlations.append({"Condition": "Multiple", "Metric": "Accuracy", "Test": "Spearman rho",
                         "r": rho_m, "p": p_rho_m, "Significant": p_rho_m < 0.05, "N": len(multi_common)})
    
    ax = axes[1, 1]
    ax.scatter(game_acc_m, lab_acc_m, c="#C44E52", s=60, edgecolors="black", alpha=0.7, zorder=5)
    z = np.polyfit(game_acc_m, lab_acc_m, 1)
    p_line = np.poly1d(z)
    x_range = np.linspace(game_acc_m.min(), game_acc_m.max(), 100)
    ax.plot(x_range, p_line(x_range), "r--", linewidth=2, alpha=0.8)
    ax.set_xlabel("Game Accuracy (%)", fontsize=11)
    ax.set_ylabel("Lab Accuracy (%)", fontsize=11)
    ax.set_title(f"Multiple Target: Accuracy Correlation\nrho = {rho_m:.3f}, p = {p_rho_m:.4f}", fontsize=12, fontweight="bold")
    ax.grid(alpha=0.3)
    
    plt.suptitle("RQ1: Concurrent Validity - Game vs Lab Correlations", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "plot_correlation_scatter.png"), dpi=150, bbox_inches="tight")
    plt.close()
    
    # Save results
    corr_df = pd.DataFrame(correlations)
    corr_df.to_csv(os.path.join(RESULTS_DIR, "correlation_results.csv"), index=False)
    print(corr_df.to_string(index=False))
    
    with open(os.path.join(RESULTS_DIR, "correlation_report.txt"), "w") as f:
        f.write("\n".join(report))
    
    print(f"\nSaved to: {RESULTS_DIR}")
    print("Correlation analysis complete!")
