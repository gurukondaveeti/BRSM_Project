"""
Step 2: Plot raw data points for Accuracy and Reaction Time.
Creates scatter/strip plots and box plots with individual data points overlaid.
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

def load_data():
    """Load extracted data from all conditions."""
    return pd.read_csv(os.path.join(RESULTS_DIR, "extracted_all_conditions.csv"))


def plot_strip_and_box(data, metric, ylabel, title, filename):
    """Create box plot with strip plot overlay for a given metric."""
    conditions = ["Single_Phone", "Single_Lab", "Multiple_Phone", "Multiple_Lab"]
    condition_labels = ["Single\nPhone (Game)", "Single\nLab", "Multiple\nPhone (Game)", "Multiple\nLab"]
    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data for box plot
    box_data = []
    for cond in conditions:
        values = data[data["Condition"] == cond][metric].dropna().values
        box_data.append(values)
    
    # Box plot
    bp = ax.boxplot(box_data, widths=0.5, patch_artist=True,
                     boxprops=dict(linewidth=1.5),
                     whiskerprops=dict(linewidth=1.5),
                     medianprops=dict(linewidth=2, color="black"),
                     capprops=dict(linewidth=1.5))
    
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.3)
    
    # Strip plot (individual data points) with jitter
    for i, (cond, color) in enumerate(zip(conditions, colors)):
        values = data[data["Condition"] == cond][metric].dropna().values
        participant_ids = data[data["Condition"] == cond]["ParticipantID"].values
        jitter = np.random.uniform(-0.15, 0.15, size=len(values))
        ax.scatter(np.full(len(values), i + 1) + jitter, values, 
                   c=color, edgecolor="black", linewidth=0.5,
                   s=50, alpha=0.8, zorder=5)
        
        # Label each point with participant ID
        for j, (x_val, y_val, pid) in enumerate(zip(
            np.full(len(values), i + 1) + jitter, values, participant_ids)):
            ax.annotate(str(int(pid)), (x_val, y_val), fontsize=6, 
                       ha="center", va="bottom", alpha=0.6)
    
    ax.set_xticks(range(1, len(conditions) + 1))
    ax.set_xticklabels(condition_labels, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
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


def plot_individual_scatter(data, metric, ylabel, title, filename):
    """Create scatter plot of individual participant data across conditions."""
    conditions = ["Single_Phone", "Single_Lab", "Multiple_Phone", "Multiple_Lab"]
    condition_labels = ["Single Phone", "Single Lab", "Multiple Phone", "Multiple Lab"]
    colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for i, (cond, color, label) in enumerate(zip(conditions, colors, condition_labels)):
        subset = data[data["Condition"] == cond].sort_values("ParticipantID")
        ax.scatter(range(len(subset)), subset[metric].values, 
                   c=color, edgecolor="black", linewidth=0.5,
                   s=80, alpha=0.8, label=label, zorder=5)
        
        # Connect with line
        ax.plot(range(len(subset)), subset[metric].values, 
                color=color, alpha=0.3, linewidth=1)
        
        # Label points
        for j, (pid, val) in enumerate(zip(subset["ParticipantID"], subset[metric])):
            ax.annotate(str(int(pid)), (j, val), fontsize=6,
                       ha="center", va="bottom", alpha=0.6)
    
    ax.set_xlabel("Participant Index (sorted by ID)", fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(fontsize=10, loc="best")
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    filepath = os.path.join(RESULTS_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {filepath}")


if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# DATA VISUALIZATION - Raw Data Points")
    print("#" * 60 + "\n")
    
    data = load_data()
    
    print("Creating plots...")
    
    # Box + Strip plots
    plot_strip_and_box(data, "Mean_Accuracy", "Accuracy (%)", 
                       "Mean Accuracy by Condition (with Individual Data Points)",
                       "plot_accuracy_boxstrip.png")
    
    plot_strip_and_box(data, "Mean_RT", "Reaction Time (ms)",
                       "Mean Reaction Time by Condition (with Individual Data Points)",
                       "plot_rt_boxstrip.png")
    
    # Individual scatter plots
    plot_individual_scatter(data, "Mean_Accuracy", "Accuracy (%)",
                           "Individual Participant Accuracy Across Conditions",
                           "plot_accuracy_scatter.png")
    
    plot_individual_scatter(data, "Mean_RT", "Reaction Time (ms)",
                           "Individual Participant RT Across Conditions",
                           "plot_rt_scatter.png")
    
    print("\nAll plots saved to results/ folder.")
