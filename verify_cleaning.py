import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

BEFORE_CSV = "Banglore_traffic_Dataset.csv"
AFTER_CSV = "Banglore_traffic_Cleaned.csv"
OUT_DIR = r"C:\Users\dhana\.gemini\antigravity\brain\f889126e-ec14-4944-9e93-490ef575f614"

def make_verification_report():
    df_before = pd.read_csv(BEFORE_CSV)
    df_after = pd.read_csv(AFTER_CSV)

    columns_to_compare = ['Traffic Volume', 'Average Speed']

    print("=== SUMMARY STATISTICS ===")
    for col in columns_to_compare:
        print(f"\n[{col}]")
        print(f"BEFORE -> Min: {df_before[col].min():.2f}, Max: {df_before[col].max():.2f}, Mean: {df_before[col].mean():.2f}")
        print(f"AFTER  -> Min: {df_after[col].min():.2f}, Max: {df_after[col].max():.2f}, Mean: {df_after[col].mean():.2f}")

    df_before['State'] = 'Before Cleaning'
    df_after['State'] = 'After Cleaning'
    df_combined = pd.concat([df_before[[*columns_to_compare, 'State']], df_after[[*columns_to_compare, 'State']]])

    os.makedirs(OUT_DIR, exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df_combined, x='State', y='Traffic Volume', palette=['#ff9999', '#66b3ff'])
    plt.title('Distribution of Traffic Volume (Before vs After)')
    plt.savefig(os.path.join(OUT_DIR, "traffic_volume_boxplot.png"), dpi=150)
    plt.close()
    
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df_combined, x='State', y='Average Speed', palette=['#ff9999', '#66b3ff'])
    plt.title('Distribution of Average Speed (Before vs After)')
    plt.savefig(os.path.join(OUT_DIR, "average_speed_boxplot.png"), dpi=150)
    plt.close()
    
    print("\n[SUCCESS] Plots saved.")

if __name__ == "__main__":
    make_verification_report()
