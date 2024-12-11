import pandas as pd
from tkinter import filedialog
import tkinter as tk
import datetime

def select_file():
    root = tk.Tk()
    root.withdraw()
    # file_path = filedialog.askopenfilename()
    file_path = filedialog.askopenfilename(initialdir = r'\\uluroweb\d\Submit\rpt')
    return file_path

# Step 1: Prompt the user to select the CSV file
print("Please select the CSV file to edit.")
file_path = select_file()

# Step 2: Read the CSV file into a DataFrame
# df = pd.read_csv(file_path)
df = pd.read_csv(file_path, header=None)

# Step 4: Drop columns F-AD and columns C and D
columns_to_drop = df.columns[2:4].append(df.columns[5:30])
df = df.drop(columns=columns_to_drop)

# copy values from column C to column A
df.iloc[:, 0] = df.iloc[:, 2]

# add .pdf to the end of every value in column C
df.iloc[:, 2] = df.iloc[:, 2].astype(str) + ".pdf"

# delete the top row that is not needed
df = df.iloc[1:]

# Format the date column to have consistent format
df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1]).dt.strftime('%m/%d/%Y')

# Get the current date
current_date = datetime.datetime.now().strftime("%m%d%y")

# Define the prefix and suffix for the filename
prefix = "SUB_Index_"
suffix = ".csv"

# Step 7: Save the DataFrame back to a CSV file
edited_file_path = file_path.replace(
    file_path.split('/')[-1], f"{prefix}{current_date}{suffix}"
)
# edited_file_path = f"{prefix}{current_date}{suffix}"
df.to_csv(edited_file_path, index=False, header=None)

print(f"The edited file has been saved as '{edited_file_path}'.")
