# function that takes jobid.pd.csv file to modify


import pandas as pd
import datetime
import os

def SUBindex(ID, folder_path):
    # uses ID only to find requried csv file 
    file_path = os.path.join(folder_path, f"RPT0000000{ID}.pd.csv")
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' not found."
    # load csv as a dataframe type
    df = pd.read_csv(file_path, header = None)
    # Deletes columns F- AD & Columns C & D
    columns_to_drop = df.columns[2:4].append(df.columns[5:30])
    df = df.drop(columns=columns_to_drop)

        # Copy values from column C to column A
    df.iloc[:, 0] = df.iloc[:, 2]

        # Append ".pdf" to every value in column C
    df.iloc[:, 2] = df.iloc[:, 2].astype(str) + ".pdf"

        # Delete the top row
    df = df.iloc[1:]

        # Format the date column
    df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1]).dt.strftime('%m/%d/%Y')

    current_date = datetime.datetime.now().strftime("%m%d%y")

    edited_file_path = os.path.join(folder_path, f"{"SUB_Index_"}{current_date}{".csv"}")

    df.to_csv(edited_file_path, index=False, header=None)
    return f"File saved as '{edited_file_path}'."