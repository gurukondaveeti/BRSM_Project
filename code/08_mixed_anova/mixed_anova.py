"""
Step 8: 2x2 Mixed Factorial ANOVA (RQ2 & RQ3)
- Between-Subjects Factor: Target Load (Single vs Multiple)
- Within-Subjects Factor: Modality (Game/Phone vs Lab)
- Tests main effects and interaction for Reaction Time
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
RESULTS_DIR = os.path.join(BASE_DIR, "results", "08_mixed_anova")
os.makedirs(RESULTS_DIR, exist_ok=True)

def manual_mixed_anova(data):
    """
    Manual 2x2 Mixed ANOVA calculation.
    Between factor: Load (Single vs Multiple)
    Within factor: Modality (Phone vs Lab)
    DV: Mean_RT
    """
    # Reshape data: each participant needs Phone and Lab scores
    single_phone = data[data["Condition"] == "Single_Phone"].set_index("ParticipantID")["Mean_RT"]
    single_lab = data[data["Condition"] == "Single_Lab"].set_index("ParticipantID")["Mean_RT"]
    multi_phone = data[data["Condition"] == "Multiple_Phone"].set_index("ParticipantID")["Mean_RT"]
    multi_lab = data[data["Condition"] == "Multiple_Lab"].set_index("ParticipantID")["Mean_RT"]
    
    # Get common participants for each load level
    single_ids = single_phone.index.intersection(single_lab.index)
    multi_ids = multi_phone.index.intersection(multi_lab.index)
    
    sp = single_phone.loc[single_ids].values
    sl = single_lab.loc[single_ids].values
    mp = multi_phone.loc[multi_ids].values
    ml = multi_lab.loc[multi_ids].values
    
    n1 = len(single_ids)  # Single group size
    n2 = len(multi_ids)   # Multiple group size
    N = n1 + n2            # Total participants
    
    # Cell means
    mean_sp = np.mean(sp)
    mean_sl = np.mean(sl)
    mean_mp = np.mean(mp)
    mean_ml = np.mean(ml)
    
    # Marginal means
    mean_single = (mean_sp + mean_sl) / 2
    mean_multi = (mean_mp + mean_ml) / 2
    mean_phone = (mean_sp * n1 + mean_mp * n2) / N
    mean_lab = (mean_sl * n1 + mean_ml * n2) / N
    grand_mean = (mean_sp * n1 + mean_sl * n1 + mean_mp * n2 + mean_ml * n2) / (2 * N)
    
    # Subject means
    subj_means_single = (sp + sl) / 2
    subj_means_multi = (mp + ml) / 2
    
    # --- SS Between-Subjects ---
    # SS Load (Between)
    SS_load = 2 * (n1 * (mean_single - grand_mean)**2 + n2 * (mean_multi - grand_mean)**2)
    df_load = 1
    
    # SS Subjects within groups (error for between)
    SS_subj_within = 2 * (np.sum((subj_means_single - mean_single)**2) + 
                          np.sum((subj_means_multi - mean_multi)**2))
    df_subj_within = N - 2
    
    # --- SS Within-Subjects ---
    # SS Modality (Within)
    SS_modality = N * ((mean_phone - grand_mean)**2 + (mean_lab - grand_mean)**2)
    # More precise calculation
    SS_modality = (n1 * (mean_sp - mean_single - mean_phone + grand_mean)**2 + 
                   n1 * (mean_sl - mean_single - mean_lab + grand_mean)**2 +
                   n2 * (mean_mp - mean_multi - mean_phone + grand_mean)**2 +
                   n2 * (mean_ml - mean_multi - mean_lab + grand_mean)**2)
    # Simpler: direct calculation
    phone_vals = np.concatenate([sp, mp])
    lab_vals = np.concatenate([sl, ml])
    mean_phone_actual = np.mean(phone_vals)
    mean_lab_actual = np.mean(lab_vals)
    grand_mean_actual = np.mean(np.concatenate([sp, sl, mp, ml]))
    
    SS_modality = N * ((mean_phone_actual - grand_mean_actual)**2 + (mean_lab_actual - grand_mean_actual)**2)
    df_modality = 1
    
    # SS Interaction (Load x Modality)
    SS_interaction = (n1 * ((mean_sp - mean_single - mean_phone_actual + grand_mean_actual)**2 +
                            (mean_sl - mean_single - mean_lab_actual + grand_mean_actual)**2) +
                      n2 * ((mean_mp - mean_multi - mean_phone_actual + grand_mean_actual)**2 +
                            (mean_ml - mean_multi - mean_lab_actual + grand_mean_actual)**2))
    df_interaction = 1
    
    # SS Error within (Modality x Subjects within groups)
    # Deviation of each score from its cell mean, adjusted
    dev_single = (sp - sl) - (mean_sp - mean_sl)
    dev_multi = (mp - ml) - (mean_mp - mean_ml)
    SS_error_within = 0.5 * (np.sum(dev_single**2) + np.sum(dev_multi**2))
    df_error_within = N - 2
    
    # Mean Squares
    MS_load = SS_load / df_load
    MS_subj_within = SS_subj_within / df_subj_within
    MS_modality = SS_modality / df_modality
    MS_interaction = SS_interaction / df_interaction
    MS_error_within = SS_error_within / df_error_within
    
    # F-ratios
    F_load = MS_load / MS_subj_within
    F_modality = MS_modality / MS_error_within
    F_interaction = MS_interaction / MS_error_within
    
    # p-values
    p_load = 1 - stats.f.cdf(F_load, df_load, df_subj_within)
    p_modality = 1 - stats.f.cdf(F_modality, df_modality, df_error_within)
    p_interaction = 1 - stats.f.cdf(F_interaction, df_interaction, df_error_within)
    
    # Effect sizes (partial eta squared)
    eta2_load = SS_load / (SS_load + SS_subj_within)
    eta2_modality = SS_modality / (SS_modality + SS_error_within)
    eta2_interaction = SS_interaction / (SS_interaction + SS_error_within)
    
    results = {
        "Source": ["Target Load (Between)", "Modality (Within)", "Load x Modality (Interaction)"],
        "SS": [SS_load, SS_modality, SS_interaction],
        "df_effect": [df_load, df_modality, df_interaction],
        "df_error": [df_subj_within, df_error_within, df_error_within],
        "MS": [MS_load, MS_modality, MS_interaction],
        "F": [F_load, F_modality, F_interaction],
        "p": [p_load, p_modality, p_interaction],
        "partial_eta2": [eta2_load, eta2_modality, eta2_interaction],
        "Significant": [p_load < 0.05, p_modality < 0.05, p_interaction < 0.05]
    }
    
    cell_means = {
        "Single_Phone": mean_sp, "Single_Lab": mean_sl,
        "Multiple_Phone": mean_mp, "Multiple_Lab": mean_ml,
        "n_single": n1, "n_multi": n2
    }
    
    return pd.DataFrame(results), cell_means


if __name__ == "__main__":
    data = pd.read_csv(CLEANED_PATH)
    
    print("=" * 70)
    print("RQ2 & RQ3: 2x2 MIXED FACTORIAL ANOVA (Reaction Time)")
    print("=" * 70)
    print("\nBetween-Subjects Factor: Target Load (Single vs Multiple)")
    print("Within-Subjects Factor: Modality (Phone/Game vs Lab)")
    print("Dependent Variable: Mean Reaction Time (ms/target)")
    
    anova_df, cell_means = manual_mixed_anova(data)
    
    print("\n" + "=" * 70)
    print("ANOVA TABLE")
    print("=" * 70)
    print(anova_df.to_string(index=False))
    
    # APA-style reporting
    print("\n" + "=" * 70)
    print("APA-STYLE RESULTS")
    print("=" * 70)
    for _, row in anova_df.iterrows():
        sig = "*" if row["Significant"] else "ns"
        apa = f"  {row['Source']}: F({int(row['df_effect'])}, {int(row['df_error'])}) = {row['F']:.2f}, p = {row['p']:.4f}, partial eta^2 = {row['partial_eta2']:.3f} [{sig}]"
        print(apa)
    
    anova_df.to_csv(os.path.join(RESULTS_DIR, "mixed_anova_results.csv"), index=False)
    
    # --- Interaction Plot ---
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x = [0, 1]
    labels_x = ["Phone (Game)", "Lab"]
    
    single_means = [cell_means["Single_Phone"], cell_means["Single_Lab"]]
    multi_means = [cell_means["Multiple_Phone"], cell_means["Multiple_Lab"]]
    
    ax.plot(x, single_means, "o-", color="#4C72B0", linewidth=2.5, markersize=10, label=f"Single Target (n={cell_means['n_single']})")
    ax.plot(x, multi_means, "s-", color="#C44E52", linewidth=2.5, markersize=10, label=f"Multiple Target (n={cell_means['n_multi']})")
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels_x, fontsize=12)
    ax.set_ylabel("Mean RT (ms/target)", fontsize=12)
    ax.set_title("Interaction Plot: Modality × Target Load\n(Reaction Time)", fontsize=13, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    
    # Annotate means
    for i, (s, m) in enumerate(zip(single_means, multi_means)):
        ax.annotate(f"{s:.0f}", (x[i], s), textcoords="offset points", xytext=(0, 12), ha="center", fontsize=10, fontweight="bold", color="#4C72B0")
        ax.annotate(f"{m:.0f}", (x[i], m), textcoords="offset points", xytext=(0, -18), ha="center", fontsize=10, fontweight="bold", color="#C44E52")
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "plot_interaction_rt.png"), dpi=150, bbox_inches="tight")
    plt.close()
    
    # Save report
    with open(os.path.join(RESULTS_DIR, "mixed_anova_report.txt"), "w") as f:
        f.write("2x2 MIXED FACTORIAL ANOVA - REACTION TIME\n")
        f.write("=" * 60 + "\n\n")
        f.write(anova_df.to_string(index=False))
        f.write("\n\nAPA-Style:\n")
        for _, row in anova_df.iterrows():
            sig = "*" if row["Significant"] else "ns"
            f.write(f"  {row['Source']}: F({int(row['df_effect'])}, {int(row['df_error'])}) = {row['F']:.2f}, p = {row['p']:.4f}, partial eta^2 = {row['partial_eta2']:.3f} [{sig}]\n")
    
    print(f"\nSaved to: {RESULTS_DIR}")
    print("Mixed ANOVA complete!")
