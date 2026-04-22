"""
Step 1: Extract Accuracy and Reaction Time from all 4 datasets.
Computes per-participant mean accuracy (%) and mean RT (ms).
Saves extracted data to CSV files in the results/ folder.
"""

import pandas as pd
import numpy as np
import os
import re
import ast

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def get_participant_id(source_file):
    """Extract participant number from source_file name (e.g., '10_attentional...' -> 10)."""
    match = re.match(r"(\d+)_", source_file)
    return int(match.group(1)) if match else None


def parse_bracket_value(val):
    """Parse values like '[1.234]' or '[1.2, 3.4, 5.6]' from lab data."""
    if pd.isna(val):
        return []
    val = str(val).strip()
    try:
        result = ast.literal_eval(val)
        if isinstance(result, (list, tuple)):
            return [float(x) for x in result]
        return [float(result)]
    except:
        return []


# =============================================================================
# 1. SINGLE PHONE (Game) - Single Target
# =============================================================================
def extract_single_phone():
    print("=" * 60)
    print("Extracting: Single Phone (Game) - Single Target")
    print("=" * 60)
    
    df = pd.read_csv(os.path.join(DATA_DIR, "single_phone_combined.csv"))
    df["ParticipantID"] = df["source_file"].apply(get_participant_id)
    
    # Per participant: mean accuracy (SuccessRate%) and mean RT (InitialResponseTime)
    summary = df.groupby("ParticipantID").agg(
        Mean_Accuracy=("SuccessRate(%)", "mean"),
        Mean_RT=("InitialResponseTime(ms)", "mean"),
        Num_Trials=("SuccessRate(%)", "count")
    ).reset_index()
    
    summary["Condition"] = "Single_Phone"
    print(f"  Participants: {len(summary)}")
    print(f"  Accuracy range: {summary['Mean_Accuracy'].min():.2f}% - {summary['Mean_Accuracy'].max():.2f}%")
    print(f"  RT range: {summary['Mean_RT'].min():.0f} - {summary['Mean_RT'].max():.0f} ms")
    print()
    return summary


# =============================================================================
# 2. SINGLE LAB - Single Target
# =============================================================================
def extract_single_lab():
    print("=" * 60)
    print("Extracting: Single Lab - Single Target")
    print("=" * 60)
    
    df = pd.read_csv(os.path.join(DATA_DIR, "single_lab_combined.csv"))
    
    # Filter to trial rows only (where trials.thisN is not NaN)
    trial_rows = df[df["trials.thisN"].notna()].copy()
    trial_rows["ParticipantID"] = trial_rows["source_file"].apply(get_participant_id)
    
    # RT: Parse mouse.time (in seconds, stored as '[value]') -> convert to ms
    trial_rows["RT_ms"] = trial_rows["mouse.time"].apply(
        lambda x: parse_bracket_value(x)[0] * 1000 if parse_bracket_value(x) else np.nan
    )
    
    # Accuracy: In single target lab task, the participant always clicks on 'target'
    # The clicked_name is always "['target', 'target']" - meaning they found the target
    # target_col indicates whether it was a red or white target trial
    # Since all clicks successfully hit 'target', accuracy = 100% for all trials
    # However, we should check if any trials were missed or had wrong clicks
    trial_rows["Correct"] = trial_rows["mouse.clicked_name"].apply(
        lambda x: 1 if pd.notna(x) and "target" in str(x) else 0
    )
    
    # Per participant: mean accuracy and mean RT
    summary = trial_rows.groupby("ParticipantID").agg(
        Mean_Accuracy=("Correct", lambda x: x.mean() * 100),
        Mean_RT=("RT_ms", "mean"),
        Num_Trials=("Correct", "count")
    ).reset_index()
    
    summary["Condition"] = "Single_Lab"
    print(f"  Participants: {len(summary)}")
    print(f"  Accuracy range: {summary['Mean_Accuracy'].min():.2f}% - {summary['Mean_Accuracy'].max():.2f}%")
    print(f"  RT range: {summary['Mean_RT'].min():.0f} - {summary['Mean_RT'].max():.0f} ms")
    print()
    return summary


# =============================================================================
# 3. MULTIPLE PHONE (Game) - Multiple Targets
# =============================================================================
def extract_multiple_phone():
    print("=" * 60)
    print("Extracting: Multiple Phone (Game) - Multiple Targets")
    print("=" * 60)
    
    df = pd.read_csv(os.path.join(DATA_DIR, "multiple_phone_combined.csv"))
    df["ParticipantID"] = df["source_file"].apply(get_participant_id)
    
    # RT: For Multiple Targets in game, target counts vary. 
    # To compare fairly with Lab, we calculate the Average Search Time per Target.
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

    df["Avg_RT_Per_Target(ms)"] = df.apply(calc_avg_rt_per_target, axis=1)
    
    # Per participant: mean accuracy (SuccessRate%) and mean calculated RT
    summary = df.groupby("ParticipantID").agg(
        Mean_Accuracy=("SuccessRate(%)", "mean"),
        Mean_RT=("Avg_RT_Per_Target(ms)", "mean"),
        Num_Trials=("SuccessRate(%)", "count")
    ).reset_index()
    
    summary["Condition"] = "Multiple_Phone"
    print(f"  Participants: {len(summary)}")
    print(f"  Accuracy range: {summary['Mean_Accuracy'].min():.2f}% - {summary['Mean_Accuracy'].max():.2f}%")
    print(f"  RT range: {summary['Mean_RT'].min():.0f} - {summary['Mean_RT'].max():.0f} ms/target")
    print()
    return summary


# =============================================================================
# 4. MULTIPLE LAB - Multiple Targets
# =============================================================================
def extract_multiple_lab():
    print("=" * 60)
    print("Extracting: Multiple Lab - Multiple Targets")
    print("=" * 60)
    
    df = pd.read_csv(os.path.join(DATA_DIR, "multiple_lab_combined.csv"))
    
    # Filter to trial rows only
    trial_rows = df[df["trials.thisN"].notna()].copy()
    trial_rows["ParticipantID"] = trial_rows["source_file"].apply(get_participant_id)
    
    # RT: Because Game and Lab have differing target counts,
    # we use "Average Search Time per Target" to normalize across tasks.
    def get_avg_rt_per_target(val):
        times = parse_bracket_value(val)
        if not times:
            return np.nan
        total_time_ms = max(times) * 1000
        n_targets_clicked = len(times)
        return total_time_ms / n_targets_clicked
    
    trial_rows["Avg_RT_Per_Target(ms)"] = trial_rows["mouse.time"].apply(get_avg_rt_per_target)
    
    # Accuracy: Count how many targets were found vs expected
    # mouse.clicked_name contains list of clicked targets
    # Each trial should have 5 targets (target_0 through target_4)
    def count_correct_clicks(clicked_name_str):
        if pd.isna(clicked_name_str):
            return 0
        try:
            items = ast.literal_eval(clicked_name_str)
            # Count unique target clicks
            targets = set()
            for item in items:
                if "target" in str(item):
                    targets.add(item)
            return len(targets)
        except:
            return 0
    
    trial_rows["Targets_Found"] = trial_rows["mouse.clicked_name"].apply(count_correct_clicks)
    trial_rows["Accuracy_Pct"] = (trial_rows["Targets_Found"] / 5.0) * 100  # 5 targets expected
    
    # Per participant: mean accuracy and mean RT
    summary = trial_rows.groupby("ParticipantID").agg(
        Mean_Accuracy=("Accuracy_Pct", "mean"),
        Mean_RT=("Avg_RT_Per_Target(ms)", "mean"),
        Num_Trials=("Accuracy_Pct", "count")
    ).reset_index()
    
    summary["Condition"] = "Multiple_Lab"
    print(f"  Participants: {len(summary)}")
    print(f"  Accuracy range: {summary['Mean_Accuracy'].min():.2f}% - {summary['Mean_Accuracy'].max():.2f}%")
    print(f"  RT range: {summary['Mean_RT'].min():.0f} - {summary['Mean_RT'].max():.0f} ms/target")
    print()
    return summary


# =============================================================================
# MAIN: Extract all and save
# =============================================================================
if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# DATA EXTRACTION - Attention Task Validation Project")
    print("#" * 60 + "\n")
    
    single_phone = extract_single_phone()
    single_lab = extract_single_lab()
    multiple_phone = extract_multiple_phone()
    multiple_lab = extract_multiple_lab()
    
    # Save individual condition files
    single_phone.to_csv(os.path.join(RESULTS_DIR, "extracted_single_phone.csv"), index=False)
    single_lab.to_csv(os.path.join(RESULTS_DIR, "extracted_single_lab.csv"), index=False)
    multiple_phone.to_csv(os.path.join(RESULTS_DIR, "extracted_multiple_phone.csv"), index=False)
    multiple_lab.to_csv(os.path.join(RESULTS_DIR, "extracted_multiple_lab.csv"), index=False)
    
    # Combine all into one master file
    all_data = pd.concat([single_phone, single_lab, multiple_phone, multiple_lab], ignore_index=True)
    all_data.to_csv(os.path.join(RESULTS_DIR, "extracted_all_conditions.csv"), index=False)
    
    print("=" * 60)
    print("EXTRACTION COMPLETE!")
    print("=" * 60)
    print(f"\nFiles saved to: {RESULTS_DIR}")
    print(f"  - extracted_single_phone.csv")
    print(f"  - extracted_single_lab.csv")
    print(f"  - extracted_multiple_phone.csv")
    print(f"  - extracted_multiple_lab.csv")
    print(f"  - extracted_all_conditions.csv")
    
    print("\n--- SUMMARY TABLE ---")
    print(all_data.to_string(index=False))
