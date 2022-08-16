import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class visualiser:
    def __init__(self) -> None:
        self.job_df = pd.read_json("processed_naukri_job_data.json")
        
    def visual(self):
        sns.set_style('darkgrid')
        
        "=================================================================================================================="
        "experiance vs average salary"
        sns.barplot(x ='experience', y ='average_salary', data = self.job_df)
        plt.xticks(rotation=90)
        plt.show()
        "=================================================================================================================="
        
        "====================================================================================================================="
        "location vs average "
        metro_cities_df=["Mumbai","Pune","Bangalore","Noida","Hyderabad","Chennai","Thane","Ahmedabad","Kolkata","Gurgaon"]
        job_metro_cities=self.job_df[self.job_df["location"].isin(metro_cities_df)]
        sns.barplot(x ='location', y ='average_salary', data = job_metro_cities)
        plt.xticks(rotation=90)
        plt.show()
        "======================================================================================================================="

        "========================================================================================================================="
        "job title vs average salary"
        jd_list=["Senior Machine Learning Engineer","Sr. Project Engineer - AI /ML","Ai Ml Engineer","R Programmer/ R Developer","Software Developer","Machine Learning Developer",
         "Python Developer","Data Analyst","Business Analyst RPA","Business analyst","Cloud Solution Architect","IoT Solution Architect","AWS Cloud Engineer",
         "Data Scientist Lead"]
        job_title_df=self.job_df[self.job_df["job_title"].isin(jd_list)]
        sns.barplot(x ='job_title', y ='average_salary', data = job_title_df)
        plt.xticks(rotation=90)
        plt.show()
        "==========================================================================================================================="
        
visualiser_object=visualiser()
visualiser_object.visual()