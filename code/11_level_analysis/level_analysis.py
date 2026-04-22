"""
Step 11: Level Analysis (RQ4)
- One-Way Repeated Measures ANOVA: Effect of Level on RT
- Friedman Test: Effect of Level on Accuracy (non-parametric)
- Trend Correlations: Pearson (RT) & Spearman (Accuracy) vs Level
- Plots: Line plots with error bars showing performance across levels
"""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import re
import ast
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results", "11_level_analysis")
os.makedirs(RESULTS_DIR, exist_ok=True)


def get_participant_id(source_file):
    match = re.match(r"(\d+)_", source_file)
    return int(match.group(1)) if match else None


if __name__ == "__main__":
    print("=" * 70)
    print("RQ4: EFFECT OF GAME LEVEL ON PERFORMANCE")
    print("=" * 70)
    
    report = []
    
    # ====== SINGLE PHONE (Game) ======
    print("\n--- SINGLE PHONE (Game) ---")
    report.append("--- SINGLE PHONE (Game) ---")
    
    df_sp = pd.read_csv(os.path.join(DATA_DIR, "single_phone_combined.csv"))
    df_sp["ParticipantID"] = df_sp["source_file"].apply(get_participant_id)
    
    # Per level, per participant
    level_data_sp = df_sp.groupby(["ParticipantID", "Level"]).agg(
        Accuracy=("SuccessRate(%)", "mean"),
        RT=("InitialResponseTime(ms)", "mean")
    ).reset_index()
    
    # ====== MULTIPLE PHONE (Game) ======
    print("\n--- MULTIPLE PHONE (Game) ---")
    report.append("\n--- MULTIPLE PHONE (Game) ---")
    
    df_mp = pd.read_csv(os.path.join(DATA_DIR, "multiple_phone_combined.csv"))
    df_mp["ParticipantID"] = df_mp["source_file"].apply(get_participant_id)
    
    def calc_avg_rt_per_target(row):
        try:
            hits_str = str(row["HitPositions(x,y)"]).strip()
            if pd.isna(row["HitPositions(x,y)"]) or hits_str == "nan" or not hits_str:
                n_hits = 0
            else:
                n_hits = len(hits_str.split(";"))
            initial_rt = row["InitialResponseTime(ms)"]
            inter_rt = row["AvgInterTargetTime(ms)"]
            if n_hits == 0:
                return np.nan
            if n_hits == 1:
                return initial_rt
            total_rt = initial_rt + (inter_rt * (n_hits - 1))
            return total_rt / n_hits
        except:
            return np.nan
    
    df_mp["Avg_RT_Per_Target"] = df_mp.apply(calc_avg_rt_per_target, axis=1)
    
    level_data_mp = df_mp.groupby(["ParticipantID", "Level"]).agg(
        Accuracy=("SuccessRate(%)", "mean"),
        RT=("Avg_RT_Per_Target", "mean")
    ).reset_index()
    
    # ====== ANALYSIS FOR EACH GAME TYPE ======
    all_results = []
    
    for label, level_data in [("Single_Phone", level_data_sp), ("Multiple_Phone", level_data_mp)]:
        print(f"\n{'='*60}")
        print(f"LEVEL ANALYSIS: {label}")
        print(f"{'='*60}")
        report.append(f"\n{'='*60}")
        report.append(f"LEVEL ANALYSIS: {label}")
        report.append(f"{'='*60}")
        
        # Find levels completed by ALL participants (for RM ANOVA)
        level_counts = level_data.groupby("Level")["ParticipantID"].nunique()
        max_participants = level_counts.max()
        common_levels = level_counts[level_counts == max_participants].index.tolist()
        common_levels.sort()
        
        print(f"  Total participants: {level_data['ParticipantID'].nunique()}")
        print(f"  Levels completed by all ({max_participants} participants): {common_levels}")
        report.append(f"  Levels completed by all ({max_participants} participants): {common_levels}")
        
        # ====== TREND CORRELATION ======
        # Aggregate: mean RT and Accuracy per level across participants
        level_means = level_data.groupby("Level").agg(
            Mean_RT=("RT", "mean"),
            SD_RT=("RT", "std"),
            Mean_Accuracy=("Accuracy", "mean"),
            SD_Accuracy=("Accuracy", "std"),
            N=("ParticipantID", "nunique")
        ).reset_index()
        
        # Pearson correlation: Level vs RT
        r_rt, p_rt = stats.pearsonr(level_means["Level"], level_means["Mean_RT"])
        res = f"  RT Trend (Pearson): r = {r_rt:.4f}, p = {p_rt:.4f}"
        res += " -> SIGNIFICANT" if p_rt < 0.05 else " -> Not significant"
        print(res); report.append(res)
        all_results.append({"Game": label, "Metric": "RT", "Test": "Pearson Trend",
                            "Statistic": r_rt, "p": p_rt, "Significant": p_rt < 0.05})
        
        # Spearman correlation: Level vs Accuracy
        rho_acc, p_acc = stats.spearmanr(level_means["Level"], level_means["Mean_Accuracy"])
        res = f"  Accuracy Trend (Spearman): rho = {rho_acc:.4f}, p = {p_acc:.4f}"
        res += " -> SIGNIFICANT" if p_acc < 0.05 else " -> Not significant"
        print(res); report.append(res)
        all_results.append({"Game": label, "Metric": "Accuracy", "Test": "Spearman Trend",
                            "Statistic": rho_acc, "p": p_acc, "Significant": p_acc < 0.05})
        
        # ====== REPEATED MEASURES ANOVA (RT) ======
        if len(common_levels) >= 3:
            # Build wide-format matrix: rows = participants, columns = levels
            balanced = level_data[level_data["Level"].isin(common_levels)]
            pivot_rt = balanced.pivot_table(index="ParticipantID", columns="Level", values="RT")
            pivot_rt = pivot_rt.dropna()
            
            if len(pivot_rt) >= 3 and len(common_levels) >= 3:
                # Use scipy's f_oneway with repeated measures approach
                # For proper RM ANOVA, we use the manual calculation
                k = len(common_levels)
                n = len(pivot_rt)
                data_matrix = pivot_rt.values
                
                grand_mean = np.mean(data_matrix)
                
                # SS Total
                SS_total = np.sum((data_matrix - grand_mean) ** 2)
                
                # SS Between levels (Treatment)
                level_means_arr = np.mean(data_matrix, axis=0)
                SS_levels = n * np.sum((level_means_arr - grand_mean) ** 2)
                df_levels = k - 1
                
                # SS Between subjects
                subj_means = np.mean(data_matrix, axis=1)
                SS_subjects = k * np.sum((subj_means - grand_mean) ** 2)
                df_subjects = n - 1
                
                # SS Error (Residual)
                SS_error = SS_total - SS_levels - SS_subjects
                df_error = (k - 1) * (n - 1)
                
                MS_levels = SS_levels / df_levels
                MS_error = SS_error / df_error
                
                F_stat = MS_levels / MS_error
                p_rm = 1 - stats.f.cdf(F_stat, df_levels, df_error)
                eta2 = SS_levels / (SS_levels + SS_error)
                
                res = f"  RM ANOVA (RT across {k} levels, N={n}): F({df_levels}, {df_error}) = {F_stat:.3f}, p = {p_rm:.4f}, eta^2 = {eta2:.3f}"
                res += " -> SIGNIFICANT" if p_rm < 0.05 else " -> Not significant"
                print(res); report.append(res)
                all_results.append({"Game": label, "Metric": "RT", "Test": "RM ANOVA",
                                    "Statistic": F_stat, "p": p_rm, "Significant": p_rm < 0.05})
        
        # ====== FRIEDMAN TEST (Accuracy) ======
        if len(common_levels) >= 3:
            pivot_acc = balanced.pivot_table(index="ParticipantID", columns="Level", values="Accuracy")
            pivot_acc = pivot_acc.dropna()
            
            if len(pivot_acc) >= 3:
                friedman_stat, p_friedman = stats.friedmanchisquare(*[pivot_acc[col].values for col in pivot_acc.columns])
                res = f"  Friedman Test (Accuracy across {len(pivot_acc.columns)} levels, N={len(pivot_acc)}): chi2 = {friedman_stat:.3f}, p = {p_friedman:.4f}"
                res += " -> SIGNIFICANT" if p_friedman < 0.05 else " -> Not significant"
                print(res); report.append(res)
                all_results.append({"Game": label, "Metric": "Accuracy", "Test": "Friedman",
                                    "Statistic": friedman_stat, "p": p_friedman, "Significant": p_friedman < 0.05})
        
        # ====== PLOTS: Performance across levels ======
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # RT across levels
        ax = axes[0]
        ax.errorbar(level_means["Level"], level_means["Mean_RT"], yerr=level_means["SD_RT"],
                     fmt="o-", color="#4C72B0", linewidth=2, markersize=6, capsize=4, capthick=1.5)
        # Add trend line
        z = np.polyfit(level_means["Level"], level_means["Mean_RT"], 1)
        p_line = np.poly1d(z)
        ax.plot(level_means["Level"], p_line(level_means["Level"]), "--", color="#C44E52", linewidth=2, alpha=0.7,
                label=f"Trend: r={r_rt:.3f}, p={p_rt:.4f}")
        ax.set_xlabel("Level", fontsize=12)
        ax.set_ylabel("Mean RT (ms/target)", fontsize=12)
        ax.set_title(f"{label}: RT Across Levels (±1 SD)", fontsize=13, fontweight="bold")
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        
        # Accuracy across levels
        ax = axes[1]
        ax.errorbar(level_means["Level"], level_means["Mean_Accuracy"], yerr=level_means["SD_Accuracy"],
                     fmt="s-", color="#55A868", linewidth=2, markersize=6, capsize=4, capthick=1.5)
        z = np.polyfit(level_means["Level"], level_means["Mean_Accuracy"], 1)
        p_line = np.poly1d(z)
        ax.plot(level_means["Level"], p_line(level_means["Level"]), "--", color="#C44E52", linewidth=2, alpha=0.7,
                label=f"Trend: rho={rho_acc:.3f}, p={p_acc:.4f}")
        ax.set_xlabel("Level", fontsize=12)
        ax.set_ylabel("Mean Accuracy (%)", fontsize=12)
        ax.set_title(f"{label}: Accuracy Across Levels (±1 SD)", fontsize=13, fontweight="bold")
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        
        plt.suptitle(f"RQ4: Performance Across Game Levels - {label}", fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, f"plot_level_{label.lower()}.png"), dpi=150, bbox_inches="tight")
        plt.close()
        
        level_means.to_csv(os.path.join(RESULTS_DIR, f"level_means_{label.lower()}.csv"), index=False)
    
    # Save all results
    res_df = pd.DataFrame(all_results)
    res_df.to_csv(os.path.join(RESULTS_DIR, "level_analysis_results.csv"), index=False)
    print("\n" + res_df.to_string(index=False))
    
    with open(os.path.join(RESULTS_DIR, "level_analysis_report.txt"), "w") as f:
        f.write("\n".join(report))
    
    print(f"\nSaved to: {RESULTS_DIR}")
    print("Level analysis complete!")
