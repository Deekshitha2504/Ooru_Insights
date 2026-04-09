import sys
import pandas as pd
import numpy as np

def clean_bengaluru_traffic_data(input_csv, output_csv):#taking Banglore_traffic_Dataset as input CSV and creating Banglore_traffic_Cleaned as output CSV
    
    print(f"Loading '{input_csv}'...")
    df = pd.read_csv(input_csv)# to access the data in the CSV we have read it

    print("\n--- 1. Datetime Conversion ---")
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')#converting the date column's datatype from string to datetime for easier use in the dashboard
    print("Datatype of 'Date' changed to:", df['Date'].dtype)

    print("\n--- 2. Boolean Mapping ---")
    YtoT = {"Roadwork and Construction Activity": {"Yes": True, "No": False}}#converting the Yes to True and No to False in the Roadwork and Construction Activity column for easier recognition 
    df = df.replace(YtoT)
    df['Roadwork and Construction Activity'] = df['Roadwork and Construction Activity'].astype(bool)
    print("Unique values in 'Roadwork and Construction Activity':", df['Roadwork and Construction Activity'].unique())

    print("\n--- 3. Categorical Variables Optimization ---")
    categorical_cols = ['Area Name', 'Road/Intersection Name', 'Weather Conditions']#Since there are repeated area names, if each area name has a value mapped to it instead of the whole name for memory optimization
    for col in categorical_cols:
        df[col] = df[col].astype('category')#coversion from string type to categorical type
        print(f"Converted '{col}' to category. Memory optimized.")

    print("\n--- 4. Adding Latitude and Longitude Columns ---")
    road_coords = {
    '100 Feet Road': [12.9626, 77.6381],
    'CMH Road': [12.9784, 77.6385],
    'Anil Kumble Circle': [12.9757, 77.5992],
    'Trinity Circle': [12.9730, 77.6171],
    'Sony World Junction': [12.9365, 77.6252],
    'Sarjapur Road': [12.9248, 77.6534],
    'South End Circle': [12.9385, 77.5801],
    'Jayanagar 4th Block': [12.9285, 77.5830],
    'Marathahalli Bridge': [12.9561, 77.6991],
    'Ballari Road': [13.0184, 77.5891],
    'Hebbal Flyover': [13.0354, 77.5913],
    'ITPL Main Road': [12.9863, 77.7337],
    'Yeshwanthpur Circle': [13.0232, 77.5501],
    'Tumkur Road': [13.0333, 77.5333],
    'Hosur Road': [12.9100, 77.6250],
    'Silk Board Junction': [12.9176, 77.6226]}
    #adding a latitude and longitude columns for mapping
    df['latitude'] = df['Road/Intersection Name'].map(lambda x: road_coords.get(x, [12.9716, 77.5946])[0])
    df['longitude'] = df['Road/Intersection Name'].map(lambda x: road_coords.get(x, [12.9716, 77.5946])[1])

    print("\n--- 5. Adding Time Features ---")
    df['Day_of_Week'] = df['Date'].dt.dayofweek
    df['Day_Name'] = df['Date'].dt.day_name()
    df['Is_Weekend'] = df['Day_of_Week'] >= 5
    df['Month'] = df['Date'].dt.month

    print("\n--- 6. Adding Stress Score ---")                        
    df['Stress Score']=(df['Traffic Volume']/df['Average Speed'])
    
    print(f"\n--- Saving Cleaned Dataset ---")
    df.to_csv(output_csv, index=False)
    print(f"\nDataset successfully saved to '{output_csv}'!")

if __name__ == "__main__":
    INPUT_FILE = "Banglore_traffic_Dataset.csv"
    OUTPUT_FILE = "Banglore_traffic_Cleaned.csv"
    LOG_FILE = "clean_data_output.txt"
    
    with open(LOG_FILE, 'w') as f:
        sys.stdout = f #logging everything into the text file which is been printed into the terminal for record 
        clean_bengaluru_traffic_data(INPUT_FILE, OUTPUT_FILE)
        sys.stdout = sys.__stdout__ #setting the terminal output to normal mode
