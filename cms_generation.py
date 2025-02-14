import pandas as pd
import os
import numpy as np

#GLOBAL VARIABLES
#Path of synthetic Medicare claims data
claimspath = r""

#Path of national downloadable file of clinicians
clinicianpath = r""

#Path of synthetic claims notes.
notespath = r""

#Dir to save completed data to.
destpath = r""

#load_source
#Loads first .csv file in directory. Used to load raw data to transform.
def load_source(sourcedir):
    for f in os.listdir(sourcedir):
        if f.endswith(".csv"):
            filepath = sourcedir + "\\" + f
            df = pd.read_csv(filepath,low_memory=False)

    return df

#format_claims
#Transforms claims data. Renames columns and removes clear_date from all but 15% of claims.
def format_claims(claims_df):
    claims_df = claims_df[["CLM_ID","CLM_FROM_DT","CLM_THRU_DT","CLM_PMT_AMT","AT_PHYSN_NPI"]]

    columns = {"CLM_ID":"ClaimID",
                "CLM_FROM_DT":"ReceiptDate",
		"CLM_THRU_DT":"clear_date",
		"CLM_PMT_AMT":"TotalCharge",
		"AT_PHYSN_NPI":"NPI"
		}
    claims_df = claims_df.rename(columns=columns)
    
    claims_sample = claims_df.sample(frac=0.15)
    claims_sample = claims_sample[["ClaimID","clear_date"]]
    
    claims_df = claims_df.merge(claims_sample, on="ClaimID",how="left")
    claims_df = claims_df.drop(["clear_date_x"],axis=1)
    claims_df = claims_df.rename(columns={"clear_date_y":"clear_date"})

    claims_df = claims_df.drop_duplicates()
    
    return claims_df

#format_clinicians
#Transforms clinician data. Renames columns and drops duplicates on NPI.
def format_clinician(clinician_df):

    clinician_df.columns.values[21] = "ADDR_1"
    clinician_df.columns.values[22] = "ADDR_2" 
    clinician_df.columns.values[24] = "CITY"
    clinician_df.columns.values[25] = "STATE"

    clinician_df = clinician_df.rename(columns={"sec_spec_3":"Provider_Group","Provider Last Name":"Provider_Last_Name","Provider First Name":"Provider_First_Name"})     
    clinician_df = clinician_df[["NPI","Provider_Group","Provider_Last_Name","Provider_First_Name","ADDR_1","ADDR_2","CITY","STATE"]]

    clinician_df = clinician_df.drop_duplicates(subset="NPI",keep="first")
    
    return clinician_df

#join_dfs
#Adds address, provider group, and provider name from clinician data to claims data.
def join_dfs(claims_df,clinician_df):

    clinician_df["NPI"] = clinician_df["NPI"].astype("str")
    claims_df["NPI"] = claims_df["NPI"].astype("str")

    clinician_npi_list = clinician_df["NPI"].tolist()
    clinician_npi_list = list(dict.fromkeys(clinician_npi_list))

    claims_df["temp_NPI"] = np.random.choice(clinician_npi_list,size=len(claims_df))
    
    clinician_df = clinician_df.rename(columns={"NPI":"temp_NPI"})
    data_sans_notes = claims_df.merge(clinician_df, left_on="temp_NPI",right_on="temp_NPI",how="left")
    data_sans_notes = data_sans_notes.drop(["temp_NPI"],axis=1) 

    return data_sans_notes

#add_notes
#Adds synthetic claims notes to claims data.
def add_notes(data_sans_notes,notespath):
    notes_df = pd.read_csv(notespath)
    notes_list = notes_df["Note"].tolist()

    data_sans_notes["Most recent note"] = np.random.choice(notes_list,size=len(data_sans_notes))

    data_sans_age = data_sans_notes
    
    return data_sans_age

#add_age
#Calculates claim's "age" using Receiptdate and max date in clear_date. Age is in days. 
def add_age(data_sans_age):
    data_sans_age["ReceiptDate"] = pd.to_datetime(data_sans_age["ReceiptDate"], format="%Y%m%d")
    data_sans_age["clear_date"] = pd.to_datetime(data_sans_age["clear_date"], format="%Y%m%d")

    max_date = data_sans_age["clear_date"].max()

    print(max_date)

    wo_clear_date = data_sans_age[data_sans_age["clear_date"].isnull()]
    print(wo_clear_date.head())
    
    wo_clear_date = wo_clear_date[["ClaimID","ReceiptDate"]]
    wo_clear_date["Age"] = max_date - wo_clear_date["ReceiptDate"]
    wo_clear_date["Age"] = wo_clear_date["Age"].replace(to_replace=" days")
    wo_clear_date["Age"] = wo_clear_date["Age"].astype("int64")

    wo_clear_date = wo_clear_date[["ClaimID","Age"]]
    data_complete = data_sans_age.merge(wo_clear_date, on="ClaimID",how="left")

    return data_complete

#save_results
#Saves completed data to .csv file.
def save_results(df,destpath,filename):
    df_dest_path = destpath + "//" + filename
    df.to_csv(df_dest_path,sep = ",",index = False)

if __name__ == "__main__":
    claims_df = load_source(claimspath)
    clinician_df = load_source(clinicianpath)
    
    claims_df = format_claims(claims_df)
    clinician_df = format_clinician(clinician_df)

    data_sans_notes = join_dfs(claims_df,clinician_df)
    data_sans_age = add_notes(data_sans_notes,notespath)
    data_complete = add_age(data_sans_age)
    
    save_results(data_complete,destpath,filename="data_complete.csv")
