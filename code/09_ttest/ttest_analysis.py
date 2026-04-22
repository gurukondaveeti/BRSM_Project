"""
Step 9: t-Test Analysis (RQ2 & RQ3 Post-hoc follow-ups for RT)
- Paired Samples t-test: Game vs Lab RT (within-subjects, RQ3)
- Independent Samples t-test: Single vs Multiple RT (between-subjects, RQ2)
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
RESULTS_DIR = os.path.join(BASE_DIR, "results", "09_ttest")
os.makedirs(RESULTS_DIR, exist_ok=True)


def cohens_d_paired(x, y):
    diff = x - y
    return np.mean(diff) / np.std(diff, ddof=1)


def cohens_d_independent(x, y):
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx-1)*np.std(x, ddof=1)**2 + (ny-1)*np.std(y, ddof=1)**2) / (nx + ny - 2))
    return (np.mean(x) - np.mean(y)) / pooled_std


if __name__ == "__main__":
    data = pd.read_csv(CLEANED_PATH)
    
    print("=" * 70)
    print("t-TEST ANALYSIS (Reaction Time)")
    print("=" * 70)
    
    results = []
    report = []
    
    single_phone = data[data["Condition"] == "Single_Phone"].set_index("ParticipantID")
    single_lab = data[data["Condition"] == "Single_Lab"].set_index("ParticipantID")
    multi_phone = data[data["Condition"] == "Multiple_Phone"].set_index("ParticipantID")
    multi_lab = data[data["Condition"] == "Multiple_Lab"].set_index("ParticipantID")
    
    single_common = single_phone.index.intersection(single_lab.index)
    multi_common = multi_phone.index.intersection(multi_lab.index)
    
    # ====== PAIRED t-tests (RQ3: Game vs Lab - Within Subjects) ======
    print("\n--- RQ3: PAIRED SAMPLES t-TEST (Game vs Lab RT) ---")
    report.append("--- RQ3: PAIRED SAMPLES t-TEST (Game vs Lab RT) ---")
    
    # Single Target: Phone vs Lab
    sp_rt = single_phone.loc[single_common, "Mean_RT"].values
    sl_rt = single_lab.loc[single_common, "Mean_RT"].values
    t_stat, p_val = stats.ttest_rel(sp_rt, sl_rt)
    d = cohens_d_paired(sp_rt, sl_rt)
    res = f"  Single Target: t({len(single_common)-1}) = {t_stat:.3f}, p = {p_val:.4f}, Cohen's d = {d:.3f}"
    res += " -> SIGNIFICANT" if p_val < 0.05 else " -> Not significant"
    print(res); report.append(res)
    results.append({"Test": "Paired t-test", "Comparison": "Single: Phone vs Lab", 
                     "t": t_stat, "df": len(single_common)-1, "p": p_val, "Cohen_d": d,
                     "Mean_Diff": np.mean(sp_rt) - np.mean(sl_rt), "Significant": p_val < 0.05})
    
    # Multiple Target: Phone vs Lab
    mp_rt = multi_phone.loc[multi_common, "Mean_RT"].values
    ml_rt = multi_lab.loc[multi_common, "Mean_RT"].values
    t_stat, p_val = stats.ttest_rel(mp_rt, ml_rt)
    d = cohens_d_paired(mp_rt, ml_rt)
    res = f"  Multiple Target: t({len(multi_common)-1}) = {t_stat:.3f}, p = {p_val:.4f}, Cohen's d = {d:.3f}"
    res += " -> SIGNIFICANT" if p_val < 0.05 else " -> Not significant"
    print(res); report.append(res)
    results.append({"Test": "Paired t-test", "Comparison": "Multiple: Phone vs Lab",
                     "t": t_stat, "df": len(multi_common)-1, "p": p_val, "Cohen_d": d,
                     "Mean_Diff": np.mean(mp_rt) - np.mean(ml_rt), "Significant": p_val < 0.05})
    
    # ====== INDEPENDENT t-tests (RQ2: Single vs Multiple - Between Subjects) ======
    print("\n--- RQ2: INDEPENDENT SAMPLES t-TEST (Single vs Multiple RT) ---")
    report.append("\n--- RQ2: INDEPENDENT SAMPLES t-TEST (Single vs Multiple RT) ---")
    
    # Phone: Single vs Multiple
    all_single_phone_rt = data[data["Condition"] == "Single_Phone"]["Mean_RT"].values
    all_multi_phone_rt = data[data["Condition"] == "Multiple_Phone"]["Mean_RT"].values
    t_stat, p_val = stats.ttest_ind(all_single_phone_rt, all_multi_phone_rt)
    d = cohens_d_independent(all_single_phone_rt, all_multi_phone_rt)
    res = f"  Phone (Game): t({len(all_single_phone_rt)+len(all_multi_phone_rt)-2}) = {t_stat:.3f}, p = {p_val:.4f}, Cohen's d = {d:.3f}"
    res += " -> SIGNIFICANT" if p_val < 0.05 else " -> Not significant"
    print(res); report.append(res)
    results.append({"Test": "Independent t-test", "Comparison": "Phone: Single vs Multiple",
                     "t": t_stat, "df": len(all_single_phone_rt)+len(all_multi_phone_rt)-2, "p": p_val, 
                     "Cohen_d": d, "Mean_Diff": np.mean(all_single_phone_rt) - np.mean(all_multi_phone_rt),
                     "Significant": p_val < 0.05})
    
    # Lab: Single vs Multiple
    all_single_lab_rt = data[data["Condition"] == "Single_Lab"]["Mean_RT"].values
    all_multi_lab_rt = data[data["Condition"] == "Multiple_Lab"]["Mean_RT"].values
    t_stat, p_val = stats.ttest_ind(all_single_lab_rt, all_multi_lab_rt)
    d = cohens_d_independent(all_single_lab_rt, all_multi_lab_rt)
    res = f"  Lab: t({len(all_single_lab_rt)+len(all_multi_lab_rt)-2}) = {t_stat:.3f}, p = {p_val:.4f}, Cohen's d = {d:.3f}"
    res += " -> SIGNIFICANT" if p_val < 0.05 else " -> Not significant"
    print(res); report.append(res)
    results.append({"Test": "Independent t-test", "Comparison": "Lab: Single vs Multiple",
                     "t": t_stat, "df": len(all_single_lab_rt)+len(all_multi_lab_rt)-2, "p": p_val,
                     "Cohen_d": d, "Mean_Diff": np.mean(all_single_lab_rt) - np.mean(all_multi_lab_rt),
                     "Significant": p_val < 0.05})
    
    # Save results
    res_df = pd.DataFrame(results)
    res_df.to_csv(os.path.join(RESULTS_DIR, "ttest_results.csv"), index=False)
    print("\n" + res_df.to_string(index=False))
    
    # --- Plot: Paired comparison plots ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Paired differences (Game vs Lab)
    ax = axes[0]
    diff_single = sp_rt - sl_rt
    diff_multi = mp_rt - ml_rt
    positions = [1, 2]
    bp = ax.boxplot([diff_single, diff_multi], positions=positions, widths=0.6, patch_artist=True)
    bp["boxes"][0].set_facecolor("#4C72B0")
    bp["boxes"][1].set_facecolor("#C44E52")
    ax.axhline(y=0, color="black", linestyle="--", alpha=0.5)
    ax.set_xticklabels(["Single Target", "Multiple Target"], fontsize=11)
    ax.set_ylabel("RT Difference (Game - Lab) (ms)", fontsize=11)
    ax.set_title("Paired Differences: Game vs Lab RT", fontsize=12, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    
    # Plot 2: Group comparison (Single vs Multiple)
    ax = axes[1]
    data_groups = [all_single_phone_rt, all_multi_phone_rt, all_single_lab_rt, all_multi_lab_rt]
    group_labels = ["Single\nPhone", "Multi\nPhone", "Single\nLab", "Multi\nLab"]
    colors_box = ["#4C72B0", "#C44E52", "#55A868", "#8172B2"]
    bp = ax.boxplot(data_groups, labels=group_labels, widths=0.6, patch_artist=True)
    for patch, color in zip(bp["boxes"], colors_box):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_ylabel("Mean RT (ms/target)", fontsize=11)
    ax.set_title("RT Comparison Across All Conditions", fontsize=12, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "plot_ttest_comparison.png"), dpi=150, bbox_inches="tight")
    plt.close()
    
    with open(os.path.join(RESULTS_DIR, "ttest_report.txt"), "w") as f:
        f.write("\n".join(report))
    
    print(f"\nSaved to: {RESULTS_DIR}")
    print("t-test analysis complete!")
