import os
import glob

def delete_reports(ID,jobID,folder_path):
    def get_files_with_identifiers(path,ID,jobID):
        patterns = [
            f"RPT0000000{ID}.isr.pdf",
            f"RPT00000000{jobID}.ps.pdf",
            f"RPT00000000{jobID}.3600.pdf",
            f"RPT00000000{jobID}.qual.pdf",
            f"RPT0000000{ID}.3553.pdf",
            f"RPT0000000{ID}.bad.pdf",
            f"RPT0000000{ID}.mov.pdf",
            f"RPT00000000{jobID}.cont.pdf",
            f"RPT00000000{jobID}.mani.pdf",
            f"RPT00000000{jobID}.jman.pdf",
            f"RPT00000000{jobID}.msl.txt",
            f"RPT0000000{ID}.dtl.pdf",
            f"RPT0000000{ID}.big.pdf",
            f"RPT0000000{ID}.rtnrpt.pdf",
            f"RPT0000000{ID}.pd.csv",
            f"RPT0000000{ID}.fc.pdf",
            f"RPT0000000{ID}.car.csv",
            f"RPT0000000{ID}.bad.csv",
            f"RPT00000000{jobID}.jss.pdf",
            f"RPT00000000{jobID}.jpd.csv",
            f"RPT00000000{jobID}.acct.csv",
        ]

        files = []
        for pattern in patterns:
            files.extend(glob.glob(os.path.join(path,pattern)))
        return files
    

    def delete_pdfs(input_files):
        for file in input_files:
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except FileNotFoundError:
                print(f"File not found: {file}")

    files_with_identifiers = get_files_with_identifiers(folder_path, ID, jobID)
    if files_with_identifiers:
        delete_pdfs(files_with_identifiers)
        return f"Deleted {len(files_with_identifiers)} files."
    else:
        return "No matching files found with the specified identifiers."