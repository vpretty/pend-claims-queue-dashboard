import pandas as pd
import numpy as np
import os
from autocorrect import Speller
import regex as re
from datetime import datetime

#GLOBAL VARIABLES
#Directory containing source data.
sourcedir = r""
#Directory to save results to.
destpath = r""

#FUNCTIONS

#load_source
#Loads data from csv file and uses it to create a dataframe.
def load_source(sourcedir):
    for f in os.listdir(sourcedir):
        if f.endswith(".csv"):
            filepath = sourcedir + "\\" + f
            df = pd.read_csv(filepath)

    return df

#prepare
#Takes text and applies a series of transformations to it.
#Used to normalize text data for analysis.
def prepare(text,pipeline):
    for transform in pipeline:
        text = transform(text)
    return text

#spell_correct
#Corrects spelling mistakes in text.
def spell_correct(text):
    spell = Speller("en")
    return spell(text)

#remove_whitespace
#Replaces multiple spaces with single spaces.
def remove_whitespace(text):
    return re.sub("\s{2,}"," ",text)

#remove_slashes
#Removes slashes from text.
def remove_slashes(text):
    return text.replace("\\","")

#save_results
#Saves a dataframe as a csv.
def save_results(df,destpath,filename):
    df_dest_path = destpath + "//" + filename
    df.to_csv(df_dest_path,sep = ",",index = False)

#claims_cleared
#Gathers claim information for claims with a clear date.
def claims_cleared(df):
    claims_cleared_df = df[~df["clear_date"].isnull()]
    claims_cleared_df = claims_cleared_df[["ClaimID","clear_date","ReceiptDate","Most recent note"]]

    return claims_cleared_df

#calc_total_claims
#Calculates total pending claims.
def calc_total_claims(df):
    total_claims_temp = df[df["clear_date"].isnull()]
    total_claims_df = total_claims_temp.groupby("report_date")["ClaimID"].nunique()
    total_claims_df = total_claims_df.to_frame().reset_index()
    total_claims_df.columns = ["report_date","total"]

    return total_claims_df

#calc_total_dollars
#Calculates total dollar amount of pended claims.
def calc_total_dollars(df):
    temp_dol = df[df["clear_date"].isnull()]
    temp_dol = temp_dol[["report_date","TotalCharge"]]
    total_dol_df = temp_dol.groupby("report_date")["TotalCharge"].sum()
    total_dol_df = total_dol_df.to_frame().reset_index()
    total_dol_df.columns = ["report_date","total"]

    return total_dol_df

#calc_total_prac
#Calculates total practitioners associated with pended claims.
def calc_total_prac(df):
    total_prac_temp = df[df["clear_date"].isnull()]
    total_prac_df = total_prac_temp.groupby("report_date")["NPI"].nunique()
    total_prac_df = total_prac_df.to_frame().reset_index()
    total_prac_df.columns = ["report_date","total"]

    return total_prac_df

#calc_total_groups
#Calculates total provider groups.
def calc_total_groups(df):
    total_group_temp = df[df["clear_date"].isnull()]
    total_groups_df = total_group_temp.groupby("report_date")["Provider_Group"].nunique()
    total_groups_df = total_groups_df.to_frame().reset_index()
    total_groups_df.columns = ["report_date","total"]

    return total_groups_df

#calc_total_facilities
#Calculates total facilities from unique addresses.
def calc_total_facilities(df):
    total_fac_temp = df[df["clear_date"].isnull()]
    total_fac_temp["ADDR_concat"] = total_fac_temp["ADDR_1"] + total_fac_temp["ADDR_2"] + total_fac_temp["CITY"] + total_fac_temp["STATE"]
    total_fac_df = total_fac_temp.groupby("report_date")["ADDR_concat"].nunique()
    total_fac_df = total_fac_df.to_frame().reset_index()
    total_fac_df.columns = ["report_date","total"]

    return total_fac_df

#calc_total_claims_left
#Calculates total unique claims per clear date to determine how many claims "left the queue" on that day.
def calc_total_claims_left(df):
    clear_temp = df[~df["clear_date"].isnull()]
    total_claims_left_df = clear_temp.groupby("clear_date")["ClaimID"].nunique()
    total_claims_left_df = total_claims_left_df.to_frame().reset_index()
    total_claims_left_df.columns = ["clear_date","total"]

    return total_claims_left_df

#top_aging_claims
#Gathers top claims without a clear_date by age.
def top_aging_claims(df):
    top_day = [10,20,30]

    aging_claims = df.sort_values(by=["Age"],ascending=False)
    for t in top_day:
        top_temp = aging_claims.head(t)
        top_temp["top_num"] = t
            
        if t == 10:
            top_10_20_30 = top_temp
        else:
            top_10_20_30 = pd.concat([top_10_20_30,top_temp],ignore_index=True)

    return top_10_20_30

#aging_claims_30_60_90
#Totals unique claims without a clear_date by age category.
def aging_claims_30_60_90(df):
    aging_dict = {
        "0-9 days":"0 <= Age <= 9",
        "10-20 days":"10 <= Age <= 20",
        "21-25 days":"21 <= Age <= 25",
        "26-30 days":"26 <= Age <= 30",
        "<=30 days":"Age <= 30",
        "31-44 days":"31 <= Age <= 44",
        "45-60 days":"45 <= Age <= 60",
        "61-90 days":"61 <= Age <= 90",
        ">90 days":"91 <= Age",
        ">30 days":"30 < Age"
        }

    temp_no_clear_df = df[df["clear_date"].isnull()]

    age_total_dict_list = []
    for l,q in aging_dict.items():
        aging_temp = temp_no_clear_df.query(q)
        aging_temp["age_group"] = l
        aging_total_temp = aging_temp.groupby("age_group")["ClaimID"].nunique()
        aging_total_temp = aging_total_temp.to_frame().reset_index()
        aging_total_temp.columns = ["age_group","total"]
        age_total_dict_list.append(aging_total_temp)

    age_total_df = pd.concat(age_total_dict_list,ignore_index=True)
    age_total_df["report_date"] = datetime.today().strftime("%m-%d-%Y")

    return age_total_df

#calc_aging_claims_30_60_90
#Assigns an age category to claims without a clear date.
def calc_aging_claims_30_60_90(df):
    aging_dict = {
        "0-9 days":"0 <= Age <= 9",
        "10-20 days":"10 <= Age <= 20",
        "21-25 days":"21 <= Age <= 25",
        "26-30 days":"26 <= Age <= 30",
        "<=30 days":"Age <= 30",
        "31-44 days":"31 <= Age <= 44",
        "45-60 days":"45 <= Age <= 60",
        "61-90 days":"61 <= Age <= 90",
        ">90 days":"91 <= Age",
        ">30 days":"30 < Age"
        }
    
    temp_no_clear_df = df[df["clear_date"].isnull()]

    age_dict_list = []
    age_total_dict_list = []
    for l,q in aging_dict.items():
        aging_temp = temp_no_clear_df.query(q)
        aging_temp["age_group"] = l
        age_dict_list.append(aging_temp)
        
    age_30_60_90_full = pd.concat(age_dict_list,ignore_index=True)

    return age_30_60_90_full

#calc_aging_claim_category
#Determines "claim category" by searching for common phrases in claims notes. This category reflects the reason the claim was pended.
def calc_aging_claim_category(df):
    output_list = []
    missing_prac = ["and add practitioner","add practitioner","provider not yet loaded","practitioner not yet loaded","provider id not yet loaded","practitioner not yet loved","provider not available","ni belongs to practitioner",r"add group/practitioner",r"add group / practitioner",r"& practitioner","both practitioner","and practitioner","ni belongs to practitioner","ni is practitioner","pi belongs to practitioner","practitioner does not exist","practitioner not on file","practitioner ni not on file","without rendering","for provider name",r"group/practitioner id not loaded yet","need inn practitioner","ni belongs to rendering","provider ni issue"]
    missing_group = ["review and add facility","group ni not file","group ni not on file","and group","add group","add ancillary group","both group",r"& group","and facility","add grp","add valid tax id","confirm tax id","confirm the tax id","group affiliation does not exist","group ni and","add inn facility","ni belongs to rendering","withoutgroup information","update the inn tax id",r"add inn facility","group id not yet loaded","group pilot on file",r"group/practitioner id not loaded yet","add inn faculty","add faculty","need ancillary group","need stand alone group","without group information","withoutgroup information"]
    missing_agree = ["add valid agreement"]
    ent_cat = ["verify entity category","entity type qualifier","not facility it is a group"]
    dos_prior = ["dos prior"]
    missing_addr = ["review remit address","service address is terminated","provider primary address record not found","provider primary address second not found"]
    search_categories = {
        "missing practitioner":missing_prac,
        "missing group":missing_group,
        "missing agreement":missing_agree,
        "entity category":ent_cat,
        "DOS prior to effective date":dos_prior,
        "address":missing_addr}

    pipeline = [str.lower,str.strip,remove_slashes,remove_whitespace,spell_correct]
    temp = df[df["clear_date"].isnull()]
    temp = temp[["ClaimID","Most recent note"]]
    temp = temp.drop_duplicates()
    temp["spellchecked"] = temp["Most recent note"].apply(prepare,pipeline=pipeline)
    temp["Category"] = np.nan

    for key,value in search_categories.items():
        value_join = "|".join(value)
        temp.loc[(temp["Category"].isnull()) & (temp["spellchecked"].str.contains(value_join,na=False)),"Category"] = key

    temp.loc[temp["Category"].isnull(),"Category"] = "Misc."

    cat_total_df = temp.groupby("Category")["ClaimID"].nunique()
    cat_total_df = cat_total_df.to_frame().reset_index()
    cat_total_df.columns = ["Category","Total"]
    cat_total_df["report_date"] = datetime.today().strftime("%m-%d-%Y")

    return cat_total_df

#calc_pipeline
#Applies functions to source data and saves results.
def calc_pipeline(df,destpath):
    calc_dict = {claims_cleared:"cleared_claims.csv",
                 calc_total_claims:"total_claims.csv",
                 calc_total_dollars:"total_dollars.csv",
                 calc_total_prac:"total_prac.csv",
                 calc_total_groups:"total_groups.csv",
                 calc_total_facilities:"total_facilities.csv",
                 calc_total_claims_left:"total_claims_left.csv",
                 top_aging_claims:"top_aging_claims.csv",
                 aging_claims_30_60_90:"aging_claims_30_60_90.csv",
                 calc_aging_claims_30_60_90:"total_30_60_90.csv",
                 calc_aging_claim_category:"aging_claim_category.csv"}

    df["report_date"] = datetime.today().strftime('%m-%d-%Y')
    
    for calc,filename in calc_dict.items():
        calc_df = calc(df)
        save_results(calc_df,destpath,filename)
        

if __name__ == "__main__":
    df = load_source(sourcedir)
    calc_pipeline(df,destpath)
