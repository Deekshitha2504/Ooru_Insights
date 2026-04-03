import pandas as pd
import sys


with open('eda_results.txt', 'w') as f:              # to write into a text file
    df = pd.read_csv('Banglore_traffic_Dataset.csv') # to read the CSV file

    f.write("=== DATA INFO ===\n")
    import io                   # to hold the text into a virtual file instead of printing it into the screen
    buffer = io.StringIO()      # creating the variable for the virtual file
    df.info(buf=buffer)         # to get info about the dataset and hold it in the virtual file
    f.write(buffer.getvalue())  # writing the info held in the virtual file into the text file 

    f.write("\n=== MISSING VALUES ===\n")   
    f.write(str(df.isnull().sum()) + "\n")  #to get the sum of the missing values in each column, converting it into string because it is in series type

    f.write("\n=== DUPLICATES ===\n")
    f.write("Total duplicates: " + str(df.duplicated().sum()) + "\n")   # incrementing the sum if an entire row is duplicate of any of the previous rows

    f.write("\n=== FIRST 5 ROWS ===\n")
    f.write(str(df.head()) + "\n")     # getting the first 5 rows
    
    f.write("\n=== UNIQUE VALUES IN CAT COLUMNS ===\n")
    for col in df.select_dtypes(include=['object']).columns:    # to select certain columns according to the data type by including or excluding, selecting columns with string(object) values
        f.write(f"\n--- Column: {col} ---\n")   # writing the column names from the above selection
        f.write(str(df[col].value_counts(dropna=False).head(15)) + "\n")    # count number of occurences of each unique value in each column, include missing values and display only the first 15 values
    
    f.write("\n=== NUMERIC STATISTICS ===\n")
    f.write(str(df.describe()) + "\n")  # to  write mean, median, max etc of the dataset
