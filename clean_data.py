import pandas as pd
import numpy as np

def clean_bengaluru_traffic_data(input_csv, output_csv):
    """
    Cleans the Bengaluru Traffic Dataset by optimizing data types, handling boolean
    fields, and dealing with extreme outliers in numerical columns.
    """
    print(f"Loading '{input_csv}'...")
    df = pd.read_csv(input_csv)

    print("\n--- 1. Datetime Conversion ---")
    # Using format='mixed' to handle potentially inconsistent date formats gracefully.
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    print("Datatype of 'Date' changed to:", df['Date'].dtype)

    print("\n--- 2. Boolean Mapping ---")
    # Replace the text "Yes" and "No" with actual boolean True/False values
    # We use a dictionary mapping with the .replace() method
    cleanup_nums = {"Roadwork and Construction Activity": {"Yes": True, "No": False}}
    df = df.replace(cleanup_nums)
    # Ensure the column type is actually treated as a Python bool
    df['Roadwork and Construction Activity'] = df['Roadwork and Construction Activity'].astype(bool)
    print("Unique values in 'Roadwork and Construction Activity':", df['Roadwork and Construction Activity'].unique())

    print("\n--- 3. Categorical Variables Optimization ---")
    # Convert string columns with limited unique values to 'category' datatype
    categorical_cols = ['Area Name', 'Road/Intersection Name', 'Weather Conditions']
    for col in categorical_cols:
        df[col] = df[col].astype('category')
        print(f"Converted '{col}' to category. Memory optimized.")

    print("\n--- 4. Outlier Detection & Handling (IQR Method) ---")
    # We will compute the IQR for numerical fields like 'Traffic Volume'
    # And then we "clip" the outliers to the upper and lower fences.
    # Traffic Volume handling (IQR Method)
    col = 'Traffic Volume'
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 2.0 * IQR
    upper_bound = Q3 + 2.0 * IQR
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    print(f"Found {len(outliers)} outliers in '{col}'. Expected range: [{lower_bound:.2f}, {upper_bound:.2f}]")
    df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
    print(f"Values in '{col}' clipped smoothly to their respective bounds.\n")

    # Average Speed handling (Manual Cap)
    col = 'Average Speed'
    upper_bound = 110.0
    outliers = df[df[col] > upper_bound]
    print(f"Found {len(outliers)} outliers in '{col}'. Manual cap applied at: {upper_bound}")
    df[col] = df[col].clip(upper=upper_bound)
    print(f"Values in '{col}' over {upper_bound} clipped smoothly to {upper_bound}.\n")

    print(f"--- Saving Cleaned Dataset ---")
    df.to_csv(output_csv, index=False)
    print(f"Dataset successfully saved to '{output_csv}'!")

if __name__ == "__main__":
    INPUT_FILE = "Banglore_traffic_Dataset.csv"
    OUTPUT_FILE = "Banglore_traffic_Cleaned.csv"
    clean_bengaluru_traffic_data(INPUT_FILE, OUTPUT_FILE)
