import json
from glob import glob
import pandas as pd
import os
import re

class DataCleaner:
    def __init__(self) -> None:
        pass
        
    def raw_filter(self,data_path):
        save_path=r"N:\dsda\semester-1\dpdm\naukri_scrapper\Naukri_data_exp"

        file_list = glob(data_path+"/*") #get all json file from the give path
        print("===>>>",len(file_list))
        for f1 in file_list:
            complete_data_dict = {"job_title":[],"company_name":[],"company_rating":[],"company_review_count":[],"experience":[],"salary":[],"location":[],"job_description":[],"job_tags":[]}
            file_name=f1.split(os.sep)[-1]
            with open(f1, 'r') as infile:
                data=json.load(infile)

                for key in data.keys():
                    if key =="experiance":
                        exp_data=data[key]
                        complete_data_dict["experience"]=exp_data
                    else:
                        exp_data=data[key]
                        complete_data_dict[key]=exp_data

            with open(self.save_path+os.sep+file_name, 'w') as output_file:
                json.dump(complete_data_dict, output_file)


    def combine_jsons(self,data_path):
        """combine all the json which is stored as a different file
        Args:
            data_path (str): "Path where all the json file is saved
        """
        file_list = glob(data_path+"/*") #get all json file from the give path
        
        complete_data_dict = {"job_title":[],"company_name":[],"company_rating":[],"company_review_count":[],"experience":[],"salary":[],"location":[],"job_description":[],"job_tags":[]}

        for f1 in file_list:    
            with open(f1, 'r') as infile:
                data=json.load(infile)
                for key in data.keys():
                    for values in data[key]:
                        complete_data_dict[key].append(values)
                    
        with open("combined_job_naukri_data.json", 'w') as output_file:
            json.dump(complete_data_dict, output_file)


    def read_and_filter_json(self,json_path):
        job_df = pd.read_json(json_path)
        print(job_df.head())
        print(job_df.count())

        #remove all not found data from the dataset
        job_df_after_removing_null=job_df.loc[(job_df['job_title'] != "Not Found") & (job_df['company_name'] != "Not Found") & (job_df['company_rating'] != "Not Found") & (job_df['company_review_count'] != "Not Found") & (job_df['experience'] != "Not Found") & (job_df['salary'] != "Not disclosed") & (job_df['location'] != "Not Found") & (job_df['job_description'] != "Not Found")]
        
        # find duplicates
        duplicate = job_df_after_removing_null[job_df_after_removing_null.duplicated(["job_title","company_name","job_description","location"])]
        
        #remove duplicates
        df_after_removing_duplicate=job_df_after_removing_null.drop_duplicates(["job_title","company_name","job_description","location"])

        # print(df_after_removing_duplicate.count())

        review_count_list = df_after_removing_duplicate["company_review_count"] 
        
        updated_review_count=[]
        for reviewcount in review_count_list:
            reviewcount_ = [int(s) for s in re.findall(r'\b\d+\b',reviewcount)][0]
            updated_review_count.append(reviewcount_)
        df_after_removing_duplicate["updated_company_review_count"]=updated_review_count
        # print(df_after_removing_duplicate["updated_company_review_count"])

        company_rating_list = df_after_removing_duplicate["company_rating"] 
        
        updated_rating=[]
        for rating in company_rating_list:
            rating_ = float(rating)
            updated_rating.append(rating_)
        df_after_removing_duplicate["updated_company_rating"]=updated_rating
        print(df_after_removing_duplicate["updated_company_rating"])

        salary_list = df_after_removing_duplicate["salary"] 
        print(salary_list)

        average_asked_salary=[]
        for salary in salary_list:
            bound_salary=salary.split("-")
            print("===>>>",bound_salary)
            if len(bound_salary)==1:
                avg_salary=int(bound_salary[0].strip().split(" ")[0].replace(",",""))
            else:
                low_bound_salary=int(bound_salary[0].strip().replace(",",""))
                print(low_bound_salary)
                # print(bound_salary[1].split(" ")[0].replace(",",""))
                high_bound_salary=float(bound_salary[1].strip().split(" ")[0].replace(",",""))
                avg_salary=(low_bound_salary+high_bound_salary)/2
            average_asked_salary.append(avg_salary)
        
        df_after_removing_duplicate["average_salary"]=average_asked_salary

        
        # print(df_after_removing_duplicate["updated_company_rating"])

        
        df_after_removing_duplicate.to_json('processed_naukri_job_data.json')
        # # print("=--->>",df_after_removing_duplicate.count())



datacleaner_object=DataCleaner()
json_path=r"N:\dsda\semester-1\dpdm\naukri_scrapper\combined_job_naukri_data.json"
datacleaner_object.read_and_filter_json(json_path)   
# datapath=r"N:\dsda\semester-1\dpdm\naukri_scrapper\Naukri_data"

# datacleaner_object.raw_filter(data_path=datapath)
# save_path=r"N:\dsda\semester-1\dpdm\naukri_scrapper\Naukri_data_exp"

# datacleaner_object.combine_jsons(save_path)