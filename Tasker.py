import tkinter as tk
from tkinter import messagebox, scrolledtext
from Delete_Reports import delete_reports
from Combine_Reports import combine_reports
from idlelib.tooltip import Hovertip
from SUB_index import SUBindex
# Constants
FOLDER_PATH = r"\\uluroweb\submit\rpt"

# Initialization
root = tk.Tk()
root.geometry("525x500")
root.maxsize(515,500)
root.title("FI Tasker")

# Status dialogue messagebox
def update_status(message, is_error=False):
    status_box.config(state=tk.NORMAL)
    tag = "error" if is_error else "info"
    status_box.insert(tk.END, f"- {message}\n", tag)
    status_box.see(tk.END)
    status_box.config(state=tk.DISABLED)

# Function to delete files, take in ID and jobID, default rpt folder
def run_delete_reports():
    ID, jobID = entry_id.get(), entry_jobid.get()
    if not validate_inputs(ID, jobID):
        return
    
    result = delete_reports(int(ID), int(jobID), FOLDER_PATH)
    update_status(result, is_error="Error" in result)

# Function to combine files with ID and jobID, saved in rpt folder
def run_combine_reports():
    ID, jobID = entry_id.get(), entry_jobid.get()
    if not validate_inputs(ID, jobID):
        return
    
    result = combine_reports(int(ID), int(jobID), FOLDER_PATH)
    update_status(result, is_error="Error" in result)

# Validate input fields
def validate_inputs(ID, jobID):
    if not ID or not jobID:
        update_status("Error: Both ID and Job ID must be provided", is_error=True)
        return False
    try:
        int(ID)
        int(jobID)
        return True
    except ValueError:
        update_status("Error: ID and Job ID must be integers", is_error=True)
        return False

# Clear input fields and status box
def clear_inputs():
    status_box.config(state=tk.NORMAL)
    status_box.delete(1.0, tk.END)
    status_box.config(state=tk.DISABLED)
# Sub_index function call
def run_SUBindex():
    ID = entry_id.get()
    # if not validate_inputs(ID):
    #     return
    
    result = SUBindex(ID, FOLDER_PATH)
    update_status(result, is_error="Error" in result)



#Pressing Enter will run Combine Reports
def bind_Enter(event):
    run_combine_reports()
# User input for ID and jobID initialization
tk.Label(root, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

tk.Label(root, text="Job ID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
entry_jobid = tk.Entry(root)
entry_jobid.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
entry_jobid.bind('<Return>', bind_Enter)

# Clear inputs button
clear_button = tk.Button(root, text="Clear", command=clear_inputs)
clear_button.grid(row=4, column=0,sticky="W"+"E"+"N"+"S")

# Status box initialization
status_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=60, height=20)
status_box.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
status_box.tag_config("error", foreground="red")
status_box.tag_config("info", foreground="black")

# Delete files action button
delete_button = tk.Button(root, text="Delete Files", command=run_delete_reports, fg="red", font="bold")
deleteTip = Hovertip(delete_button, "Deletes the report files associated with the job ID")
delete_button.grid(row=2, column=0,  pady=5, sticky ="W")

# Combine reports button to call function
combine_button = tk.Button(root, text="Combine Files", command=run_combine_reports, fg="green", font="bold")
combineTip = Hovertip(combine_button, "Creates paperwork for job ID. Recommended to wait >10 min to ensure all files are generated")
combine_button.grid(row=2, column=1, sticky = "W" ,pady=5)

# Add Edit CSV Button
sub_index_button = tk.Button(root, text="SUB Index", command=run_SUBindex, fg="blue", font="bold")
Hovertip(sub_index_button, "make the index file for Sylacuaga")
sub_index_button.grid(row=2, column=2, padx=5, pady=5)


root.mainloop()