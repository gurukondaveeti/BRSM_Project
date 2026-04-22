import pandas as pd
import numpy as np
from scipy import stats
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
DATA_DIR = os.path.join(BASE_DIR, "data")

data_raw = pd.read_csv(os.path.join(RESULTS_DIR, "extracted_all_conditions.csv"))
data_clean = pd.read_csv(os.path.join(RESULTS_DIR, "cleaned_all_conditions.csv"))

conditions = ['Single_Phone', 'Single_Lab', 'Multiple_Phone', 'Multiple_Lab']

print("="*70)
print("ROBUST NORMALITY TESTING FOR REACTION TIME")
print("="*70)

for name, df in [("RAW DATA (No Outlier Removal)", data_raw), ("CLEANED DATA (3x IQR Removed)", data_clean)]:
    print(f"\n{name}")
    print("-" * 50)
    for cond in conditions:
        rt_vals = df[df["Condition"] == cond]["Mean_RT"].dropna().values
        if len(rt_vals) < 3:
            continue
            
        sw_stat, sw_p = stats.shapiro(rt_vals)
        res_ad = stats.anderson(rt_vals, dist='norm')
        ad_is_normal = res_ad.statistic < res_ad.critical_values[2] # 5% significance level
        ks_stat, ks_p = stats.kstest(rt_vals, 'norm', args=(np.mean(rt_vals), np.std(rt_vals, ddof=1)))
        
        print(f"Condition: {cond} (N={len(rt_vals)})")
        print(f"  - Shapiro-Wilk p-value : {sw_p:.4f} -> {'NORMAL' if sw_p > 0.05 else 'NOT NORMAL'}")
        print(f"  - Anderson-Darling     : stat={res_ad.statistic:.4f}, crit={res_ad.critical_values[2]:.4f} -> {'NORMAL' if ad_is_normal else 'NOT NORMAL'}")
        print(f"  - Kolmogorov-Smirnov p : {ks_p:.4f} -> {'NORMAL' if ks_p > 0.05 else 'NOT NORMAL'}")
        print()

