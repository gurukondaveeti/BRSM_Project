"""
Step 10: Non-Parametric Tests (RQ2 & RQ3 for Accuracy)
- Wilcoxon Signed-Rank: Game vs Lab Accuracy (within-subjects, RQ3)
- Mann-Whitney U: Single vs Multiple Accuracy (between-subjects, RQ2)
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
RESULTS_DIR = os.path.join(BASE_DIR, "results", "10_nonparametric")
os.makedirs(RESULTS_DIR, exist_ok=True)


def rank_biserial_r(U, n1, n2):
    """Effect size for Mann-Whitney U."""
    return 1 - (2 * U) / (n1 * n2)


if __name__ == "__main__":
    data = pd.read_csv(CLEANED_PATH)
    
    print("=" * 70)
    print("NON-PARAMETRIC TESTS (Accuracy)")
    print("=" * 70)
    
    results = []
    report = []
    
    single_phone = data[data["Condition"] == "Single_Phone"].set_index("ParticipantID")
    single_lab = data[data["Condition"] == "Single_Lab"].set_index("ParticipantID")
    multi_phone = data[data["Condition"] == "Multiple_Phone"].set_index("ParticipantID")
    multi_lab = data[data["Condition"] == "Multiple_Lab"].set_index("ParticipantID")
    
    single_common = single_phone.index.intersection(single_lab.index)
    multi_common = multi_phone.index.intersection(multi_lab.index)
    
    # ====== WILCOXON SIGNED-RANK (RQ3: Game vs Lab Accuracy - Within Subjects) ======
    print("\n--- RQ3: WILCOXON SIGNED-RANK (Game vs Lab Accuracy) ---")
    report.append("--- RQ3: WILCOXON SIGNED-RANK (Game vs Lab Accuracy) ---")
    
    # Single Target: Phone vs Lab
    sp_acc = single_phone.loc[single_common, "Mean_Accuracy"].values
    sl_acc = single_lab.loc[single_common, "Mean_Accuracy"].values
    diff = sp_acc - sl_acc
    nonzero_diff = diff[diff != 0]
    
    if len(nonzero_diff) > 0:
        w_stat, p_val = stats.wilcoxon(sp_acc, sl_acc)
        res = f"  Single Target: W = {w_stat:.1f}, p = {p_val:.4f}, N_nonzero = {len(nonzero_diff)}"
        res += " -> SIGNIFICANT" if p_val < 0.05 else " -> Not significant"
        print(res); report.append(res)
        results.append({"Test": "Wilcoxon Signed-Rank", "Comparison": "Single: Phone vs Lab Accuracy",
                         "Statistic": w_stat, "p": p_val, "N": len(single_common), "Significant": p_val < 0.05})
    else:
        res = "  Single Target: CANNOT COMPUTE (All differences = 0; Lab accuracy = 100% for all)"
        print(res); report.append(res)
        results.append({"Test": "Wilcoxon Signed-Rank", "Comparison": "Single: Phone vs Lab Accuracy",
                         "Statistic": np.nan, "p": np.nan, "N": len(single_common), "Significant": False})
    
    # Multiple Target: Phone vs Lab
    mp_acc = multi_phone.loc[multi_common, "Mean_Accuracy"].values
    ml_acc = multi_lab.loc[multi_common, "Mean_Accuracy"].values
    w_stat, p_val = stats.wilcoxon(mp_acc, ml_acc)
    res = f"  Multiple Target: W = {w_stat:.1f}, p = {p_val:.4f}"
    res += " -> SIGNIFICANT" if p_val < 0.05 else " -> Not significant"
    print(res); report.append(res)
    results.append({"Test": "Wilcoxon Signed-Rank", "Comparison": "Multiple: Phone vs Lab Accuracy",
                     "Statistic": w_stat, "p": p_val, "N": len(multi_common), "Significant": p_val < 0.05})
    
    # ====== MANN-WHITNEY U (RQ2: Single vs Multiple Accuracy - Between Subjects) ======
    print("\n--- RQ2: MANN-WHITNEY U (Single vs Multi Accuracy) ---")
    report.append("\n--- RQ2: MANN-WHITNEY U (Single vs Multi Accuracy) ---")
    
    # Phone: Single vs Multiple
    all_sp_acc = data[data["Condition"] == "Single_Phone"]["Mean_Accuracy"].values
    all_mp_acc = data[data["Condition"] == "Multiple_Phone"]["Mean_Accuracy"].values
    u_stat, p_val = stats.mannwhitneyu(all_sp_acc, all_mp_acc, alternative="two-sided")
    r_effect = rank_biserial_r(u_stat, len(all_sp_acc), len(all_mp_acc))
    res = f"  Phone (Game): U = {u_stat:.1f}, p = {p_val:.4f}, r = {r_effect:.3f}"
    res += " -> SIGNIFICANT" if p_val < 0.05 else " -> Not significant"
    print(res); report.append(res)
    results.append({"Test": "Mann-Whitney U", "Comparison": "Phone: Single vs Multiple Accuracy",
                     "Statistic": u_stat, "p": p_val, "N": len(all_sp_acc)+len(all_mp_acc),
                     "Significant": p_val < 0.05})
    
    # Lab: Single vs Multiple
    all_sl_acc = data[data["Condition"] == "Single_Lab"]["Mean_Accuracy"].values
    all_ml_acc = data[data["Condition"] == "Multiple_Lab"]["Mean_Accuracy"].values
    u_stat, p_val = stats.mannwhitneyu(all_sl_acc, all_ml_acc, alternative="two-sided")
    r_effect = rank_biserial_r(u_stat, len(all_sl_acc), len(all_ml_acc))
    res = f"  Lab: U = {u_stat:.1f}, p = {p_val:.4f}, r = {r_effect:.3f}"
    res += " -> SIGNIFICANT" if p_val < 0.05 else " -> Not significant"
    print(res); report.append(res)
    results.append({"Test": "Mann-Whitney U", "Comparison": "Lab: Single vs Multiple Accuracy",
                     "Statistic": u_stat, "p": p_val, "N": len(all_sl_acc)+len(all_ml_acc),
                     "Significant": p_val < 0.05})
    
    # Save results
    res_df = pd.DataFrame(results)
    res_df.to_csv(os.path.join(RESULTS_DIR, "nonparametric_results.csv"), index=False)
    print("\n" + res_df.to_string(index=False))
    
    # --- Plots ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Paired accuracy (Game vs Lab)
    ax = axes[0]
    conditions_paired = ["Single\n(Phone)", "Single\n(Lab)", "Multiple\n(Phone)", "Multiple\n(Lab)"]
    acc_data = [sp_acc, sl_acc, mp_acc, ml_acc]
    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
    bp = ax.boxplot(acc_data, labels=conditions_paired, widths=0.6, patch_artist=True)
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    # Overlay individual points
    for i, d in enumerate(acc_data):
        x = np.random.normal(i+1, 0.04, size=len(d))
        ax.scatter(x, d, alpha=0.5, color="black", s=20, zorder=5)
    ax.set_ylabel("Accuracy (%)", fontsize=11)
    ax.set_title("Accuracy Distribution by Condition\n(Wilcoxon / Mann-Whitney)", fontsize=12, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    
    # Plot 2: Median comparison bar chart
    ax = axes[1]
    medians = [np.median(d) for d in acc_data]
    bars = ax.bar(conditions_paired, medians, color=colors, edgecolor="black", alpha=0.8)
    for bar, med in zip(bars, medians):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{med:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_ylabel("Median Accuracy (%)", fontsize=11)
    ax.set_title("Median Accuracy Comparison", fontsize=12, fontweight="bold")
    ax.set_ylim(85, 102)
    ax.grid(axis="y", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "plot_nonparametric_accuracy.png"), dpi=150, bbox_inches="tight")
    plt.close()
    
    with open(os.path.join(RESULTS_DIR, "nonparametric_report.txt"), "w") as f:
        f.write("\n".join(report))
    
    print(f"\nSaved to: {RESULTS_DIR}")
    print("Non-parametric tests complete!")
