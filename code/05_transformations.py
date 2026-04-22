"""
Step 5: Data Transformations for Normality
- Applies appropriate transformations based on skewness type
- Tests normality after each transformation
- Reports success/failure of each transformation
- Saves transformed data and comparison plots
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
import warnings
warnings.filterwarnings('ignore')

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")


def apply_transformation(values, transform_name, transform_func):
    """Apply a transformation and return results."""
    try:
        transformed = transform_func(values)
        # Remove any inf or nan
        valid_mask = np.isfinite(transformed)
        if valid_mask.sum() < 3:
            return None, None, None, "Too few valid values after transformation"
        
        transformed_valid = transformed[valid_mask]
        sw_stat, sw_p = stats.shapiro(transformed_valid)
        skewness = stats.skew(transformed_valid)
        
        return transformed_valid, sw_stat, sw_p, skewness
    except Exception as e:
        return None, None, None, str(e)


def get_transformations(values, skew_type):
    """Get the list of transformations to try based on skewness type."""
    k = np.max(values) + 1  # constant for negative skew transforms
    c = 1  # constant for zero-value adjustment
    min_val = np.min(values)
    
    transformations = []
    
    # Always try all relevant transformations, but order by recommendation
    if "Positive" in skew_type or "Symmetric" in skew_type:
        transformations.append(("sqrt(x)", lambda x: np.sqrt(x), "Moderately Positive Skew"))
        if min_val > 0:
            transformations.append(("log10(x)", lambda x: np.log10(x), "Substantially Positive Skew"))
        transformations.append((f"log10(x + {c})", lambda x: np.log10(x + c), "Substantially Positive Skew (with zeros)"))
    
    if "Negative" in skew_type or "Symmetric" in skew_type:
        transformations.append((f"sqrt({k:.2f} - x)", lambda x: np.sqrt(k - x), "Moderately Negative Skew"))
        transformations.append((f"log10({k:.2f} - x)", lambda x: np.log10(k - x), "Substantially Negative Skew"))
    
    # If symmetric but not normal, try all
    if "Symmetric" in skew_type:
        if min_val > 0:
            transformations.append(("log10(x)", lambda x: np.log10(x), "Substantially Positive Skew"))
        transformations.append((f"log10(x + {c})", lambda x: np.log10(x + c), "Substantially Positive Skew (with zeros)"))
        transformations.append(("1/x", lambda x: 1.0 / x, "Reciprocal"))
        transformations.append(("x^2", lambda x: x**2, "Square"))
    
    return transformations


def create_transformation_plot(original, transformed_dict, label, filename):
    """Create comparison plot of original vs transformed distributions."""
    n_transforms = len(transformed_dict)
    n_cols = min(n_transforms + 1, 4)
    n_rows = (n_transforms + 1 + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    elif n_cols == 1:
        axes = axes.reshape(-1, 1)
    
    # Original data
    ax = axes.flat[0]
    ax.hist(original, bins="auto", density=True, color="#C44E52", alpha=0.6, edgecolor="black")
    sw_stat, sw_p = stats.shapiro(original) if len(original) >= 3 else (np.nan, np.nan)
    skew = stats.skew(original)
    ax.set_title(f"Original\nSkew={skew:.2f}, SW p={sw_p:.4f}", fontsize=10, fontweight="bold")
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")
    
    # Add normal indicator
    if sw_p > 0.05:
        ax.text(0.95, 0.95, "✓ NORMAL", transform=ax.transAxes, fontsize=10,
                ha="right", va="top", color="green", fontweight="bold",
                bbox=dict(boxstyle="round", facecolor="lightgreen", alpha=0.8))
    else:
        ax.text(0.95, 0.95, "✗ NOT NORMAL", transform=ax.transAxes, fontsize=10,
                ha="right", va="top", color="red", fontweight="bold",
                bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))
    
    # Transformed data
    for idx, (name, (values, sw_s, sw_pp, skew_val)) in enumerate(transformed_dict.items()):
        ax = axes.flat[idx + 1]
        if values is not None:
            ax.hist(values, bins="auto", density=True, color="#4C72B0", alpha=0.6, edgecolor="black")
            ax.set_title(f"{name}\nSkew={skew_val:.2f}, SW p={sw_pp:.4f}", fontsize=10, fontweight="bold")
            
            if sw_pp > 0.05:
                ax.text(0.95, 0.95, "✓ NORMAL", transform=ax.transAxes, fontsize=10,
                        ha="right", va="top", color="green", fontweight="bold",
                        bbox=dict(boxstyle="round", facecolor="lightgreen", alpha=0.8))
            else:
                ax.text(0.95, 0.95, "✗ NOT NORMAL", transform=ax.transAxes, fontsize=10,
                        ha="right", va="top", color="red", fontweight="bold",
                        bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))
        else:
            ax.text(0.5, 0.5, f"Failed:\n{skew_val}", ha="center", va="center", fontsize=9)
            ax.set_title(f"{name}\n(Failed)", fontsize=10)
        ax.set_xlabel("Value")
    
    # Hide empty subplots
    for idx in range(n_transforms + 1, n_rows * n_cols):
        axes.flat[idx].set_visible(False)
    
    plt.suptitle(f"Transformation Comparison: {label}", fontsize=13, fontweight="bold")
    plt.tight_layout()
    filepath = os.path.join(RESULTS_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {filepath}")


def classify_skewness(skew):
    """Classify the type of skewness."""
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


if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# DATA TRANSFORMATIONS FOR NORMALITY")
    print("#" * 60 + "\n")
    
    # Load cleaned data
    cleaned_path = os.path.join(RESULTS_DIR, "cleaned_all_conditions.csv")
    if os.path.exists(cleaned_path):
        data = pd.read_csv(cleaned_path)
        print("Using cleaned data (after outlier removal)\n")
    else:
        data = pd.read_csv(os.path.join(RESULTS_DIR, "extracted_all_conditions.csv"))
        print("Using raw extracted data\n")
    
    conditions = ["Single_Phone", "Single_Lab", "Multiple_Phone", "Multiple_Lab"]
    metrics = {"Mean_Accuracy": "Accuracy (%)", "Mean_RT": "Reaction Time (ms)"}
    
    report_lines = []
    transformation_results = []
    
    for metric, ylabel in metrics.items():
        for cond in conditions:
            values = data[data["Condition"] == cond][metric].dropna().values
            label = f"{cond} - {ylabel}"
            
            if len(values) < 3:
                continue
            
            # Check if already normal
            sw_stat, sw_p = stats.shapiro(values)
            skewness = stats.skew(values)
            skew_type = classify_skewness(skewness)
            
            header = f"\n{'='*60}"
            report_lines.append(header); print(header)
            header = f"{label}"
            report_lines.append(header); print(header)
            header = f"{'='*60}"
            report_lines.append(header); print(header)
            
            line = f"  Original: Skewness = {skewness:.4f} ({skew_type}), Shapiro-Wilk p = {sw_p:.4f}"
            report_lines.append(line); print(line)
            
            if sw_p > 0.05:
                line = f"  *** ALREADY NORMAL - No transformation needed ***"
                report_lines.append(line); print(line)
                transformation_results.append({
                    "Condition": cond, "Metric": metric,
                    "Original_Skewness": skewness, "Original_SW_p": sw_p,
                    "Original_Normal": True, "Best_Transform": "None (already normal)",
                    "Transformed_SW_p": sw_p, "Transformed_Normal": True,
                    "Transformed_Skewness": skewness
                })
                continue
            
            line = f"  *** NOT NORMAL - Trying transformations ***"
            report_lines.append(line); print(line)
            
            # Get and apply transformations
            transformations = get_transformations(values, skew_type)
            
            transformed_dict = {}
            best_transform = None
            best_p = sw_p
            best_name = "None"
            best_skew = skewness
            
            for t_name, t_func, t_reason in transformations:
                t_values, t_sw, t_p, t_skew = apply_transformation(values, t_name, t_func)
                
                if t_values is not None:
                    transformed_dict[t_name] = (t_values, t_sw, t_p, t_skew)
                    is_normal_now = t_p > 0.05 if t_p is not None else False
                    
                    line = f"  {t_name}: SW p = {t_p:.4f}, Skew = {t_skew:.4f}"
                    if is_normal_now:
                        line += " ✓ NORMAL"
                    report_lines.append(line); print(line)
                    
                    # Track best transformation (highest p-value)
                    if t_p is not None and t_p > best_p:
                        best_p = t_p
                        best_name = t_name
                        best_skew = t_skew
                else:
                    line = f"  {t_name}: FAILED - {t_skew}"
                    report_lines.append(line); print(line)
                    transformed_dict[t_name] = (None, None, None, t_skew)
            
            is_success = best_p > 0.05
            if is_success:
                line = f"\n  *** SUCCESS: '{best_name}' achieved normality (p = {best_p:.4f}) ***"
            else:
                line = f"\n  *** FAILED: No transformation achieved normality. Best: '{best_name}' (p = {best_p:.4f}) ***"
            report_lines.append(line); print(line)
            
            transformation_results.append({
                "Condition": cond, "Metric": metric,
                "Original_Skewness": skewness, "Original_SW_p": sw_p,
                "Original_Normal": False, "Best_Transform": best_name,
                "Transformed_SW_p": best_p, "Transformed_Normal": is_success,
                "Transformed_Skewness": best_skew
            })
            
            # Create plot
            if transformed_dict:
                safe_label = label.replace(" ", "_").replace("(", "").replace(")", "").replace("%", "pct")
                create_transformation_plot(values, transformed_dict, label,
                                          f"plot_transform_{safe_label}.png")
    
    # ===== FINAL SUMMARY =====
    header = "\n\n" + "=" * 70
    report_lines.append(header); print(header)
    header = "FINAL TRANSFORMATION SUMMARY"
    report_lines.append(header); print(header)
    header = "=" * 70
    report_lines.append(header); print(header)
    
    results_df = pd.DataFrame(transformation_results)
    line = "\n" + results_df.to_string(index=False)
    report_lines.append(line); print(line)
    
    # Count successes
    originally_normal = results_df["Original_Normal"].sum()
    successfully_transformed = results_df[~results_df["Original_Normal"]]["Transformed_Normal"].sum()
    failed = len(results_df) - originally_normal - successfully_transformed
    
    line = f"\n\nOVERALL RESULTS:"
    report_lines.append(line); print(line)
    line = f"  Already normal:                {int(originally_normal)} / {len(results_df)}"
    report_lines.append(line); print(line)
    line = f"  Successfully transformed:      {int(successfully_transformed)} / {len(results_df)}"
    report_lines.append(line); print(line)
    line = f"  Could not normalize:           {int(failed)} / {len(results_df)}"
    report_lines.append(line); print(line)
    
    if failed > 0:
        line = "\nNote: For distributions that could not be normalized,"
        report_lines.append(line); print(line)
        line = "non-parametric tests (e.g., Mann-Whitney U, Wilcoxon, Kruskal-Wallis)"
        report_lines.append(line); print(line)
        line = "should be used instead of parametric tests."
        report_lines.append(line); print(line)
    
    # Save results
    results_df.to_csv(os.path.join(RESULTS_DIR, "transformation_results.csv"), index=False)
    
    with open(os.path.join(RESULTS_DIR, "transformation_report.txt"), "w") as f:
        f.write("\n".join(report_lines))
    print(f"\n  Report saved: {os.path.join(RESULTS_DIR, 'transformation_report.txt')}")
    
    print("\nTransformation analysis complete!")
