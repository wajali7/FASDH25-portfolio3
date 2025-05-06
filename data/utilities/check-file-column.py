import os
import pandas as pd

base_dir = "../dataframes"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        filename = os.path.join(root, file)
        if filename.split(".")[-1] == "csv":
            print(filename)
            df = pd.read_csv(filename)
            if "file" in df.columns:                
                try:
                    df["file"] = df["file"].str.split(r"\\").str[-1]
                except:                    
                    continue
                df.to_csv(filename, index=False)