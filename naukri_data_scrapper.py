
"""This file will Help you to extract job data from naukri.com"""
#import required libraries
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import json 
import time
import traceback
import os


class Naukri_Scrapper:

    def __init__(self,search_jobtitle,search_experience=0,search_location="Pune",Disable_search_filter=True):
        """init method is used to intialise class attributes 
        Args:
            search_jobtitle (String): Give job title which you want to search on naukri.com
            search_experience (int, optional): Filter for number of years of experience which you want search. Defaults to 0.
            search_location (str, optional): Filter for location of job. Defaults to "Pune".
            Disable_search_filter (Bool, optional): False will enable filter search. Defaults to "True".
        """
        
        # set chrome paramters and initialise url to search for scrapping
        self.set_chrome_parameter()
        self.url="https://www.naukri.com/"
        self.driver.get(self.url)

        #initialise search parameters
        self.searchJobtitle = search_jobtitle
        self.search_exp = search_experience  
        self.searchLocation = search_location
        self.disable_filter_Parameters = Disable_search_filter
        self.file_counter = 0
        
        # initialise raw data dictonary used to store the extracted data from the page
        self.raw_data={"job_title":[],"company_name":[],"company_rating":[],"company_review_count":[],"experience":[],"salary":[],"location":[],"job_description":[],"job_tags":[]}

        print("wait for page to load....")
        time.sleep(5)
        self.search_naukri_data()

    def set_chrome_parameter(self):
        """
        set parameters for chrome like want to run on headless, window size for chrome, certification.....
        """
        chromedriver_autoinstaller.install()  
        """Check if the current version of chromedriver exists
        and if it doesn't exist, download it automatically,
        then add chromedriver to path"""
       
        self.chrome_options = webdriver.ChromeOptions()    
        # Add your options as needed    
        self.options = [
        # Define window size here
        "--window-size=1200,1200",
            "--ignore-certificate-errors"
            "--headless",
            #"--disable-gpu",
            #"--window-size=1920,1200",
            #"--ignore-certificate-errors",
            #"--disable-extensions",
            #"--no-sandbox",
            #"--disable-dev-shm-usage",
            #'--remote-debugging-port=9222'
        ]
        for option in self.options:
            self.chrome_options.add_argument(option)
        
        # driver is used to drive a browser natively
        self.driver = webdriver.Chrome(options = self.chrome_options)

    def search_naukri_data(self):
        """
        Given the filter data search the jobs for the same
        """
        search_bar=self.driver.find_element(By.CLASS_NAME,"qsb") # get search bar field
        search_suggestor=search_bar.find_element(By.CLASS_NAME,"keywordSugg") # get keyword suggestor filed
        suggestor=search_suggestor.find_element(By.CLASS_NAME,"suggestor-wrapper")
        search_keyword=suggestor.find_element(By.CLASS_NAME,"suggestor-input") # filed to input job title to search
        search_keyword.clear()
        search_keyword.send_keys(self.searchJobtitle) # send job title to search bar

        experience_field = search_bar.find_element(By.CLASS_NAME,"qsbExperience")
        """activate experience drop down arrow"""
        experience_field.find_element(By.CLASS_NAME,"dropArrowDD").click() # click on experience to get dropdown active

        exp=experience_field.find_elements(By.CLASS_NAME,"dropdown")
        experience_list=experience_field.find_elements(By.TAG_NAME,"li")
        if not self.disable_filter_Parameters:
            experience_list[self.search_exp].click() # select the experience for which you want to filter your search

        location_bar=search_bar.find_element(By.CLASS_NAME,"locationSugg")
        location_input=location_bar.find_element(By.CLASS_NAME,"suggestor-input")
        if not self.disable_filter_Parameters:
            location_input.send_keys(self.searchLocation) # select location for which you want to filter your search

        search_bar.find_element(By.CLASS_NAME,"qsbSubmit").click() # enter search button to search for the required job posts on naukri.com
        time.sleep(5) # wait for page to load completely
        self.extract_search_result()
    
    def add_and_save_data(self,data):
        """add data to raw dictonary and save after 50 data so that you don't run out of RAM 
        Args:
            data (list): list of scrapped data i.e job_title,company_name,company_rating ....... 
        """
        for i,key in enumerate(list(self.raw_data.keys())):
            self.raw_data[key].append(data[i])

        if len(self.raw_data["job_title"])>50:
            self.save_data()
            self.raw_data={"job_title":[],"company_name":[],"company_rating":[],"company_review_count":[],"experience":[],"salary":[],"location":[],"job_description":[],"job_tags":[]}

    def save_data(self):
        """Save data as json
        """
        with open("Naukri_data"+os.sep+self.searchJobtitle+"_"+str(self.file_counter)+".json", "w") as outfile:
            json.dump(self.raw_data, outfile)
        self.file_counter+=1
    
    def extract_search_result(self):
        """Now we are on the searched page, from this page we will be extracting all details corresponding to the job. i.e. job_title,company_name, company_rating, company_review_count .....
        """
        stop_flag=False
        while not stop_flag:
            search_container=self.driver.find_element(By.CLASS_NAME,"search-result-container") #
            job_container=search_container.find_element(By.CLASS_NAME,"listContainer")
            list_job=job_container.find_element(By.CLASS_NAME,"list")
            jobs=list_job.find_elements(By.CLASS_NAME,"jobTuple")
            
            for job in jobs:

                job_header=job.find_element(By.CLASS_NAME,"jobTupleHeader") 
                try:
                    job_title=job_header.find_element(By.CLASS_NAME,"title").text
                except:
                    job_title="Not Found"
                    # print("job title---",traceback.print_exc())
                try:    
                    company_info=job.find_element(By.CLASS_NAME,"companyInfo")
                    company_name=company_info.find_element(By.TAG_NAME,"a").text
                except:
                    company_name="Not Found"
                    # print("company name----",traceback.print_exc())
                try:
                    company_rating = job_header.find_element(By.CLASS_NAME,"starRating").text
                except:
                    company_rating="Not Found"
                    # print("company rating --- ",traceback.print_exc())
                try:
                    company_review_count=company_info.find_element(By.CLASS_NAME,"reviewsCount").text
                except:
                    company_review_count="Not Found"
                    # print("company review---",traceback.print_exc())
                try:    
                    exp_salary_loc=job_header.find_element(By.TAG_NAME,"ul")
                    requied_experience=exp_salary_loc.find_element(By.CLASS_NAME,"experience").text
                except:
                    requied_experience="Not Found"
                    # print("exp--",traceback.print_exc())
                try:
                    salary=exp_salary_loc.find_element(By.CLASS_NAME,"salary").text
                except:
                    salary="Not Found"
                    # print("salary--",traceback.print_exc())
                try:
                    job_location=exp_salary_loc.find_element(By.CLASS_NAME,"location").text
                except:
                    job_location="Not Found"
                    # print("loc--",traceback.print_exc())
                try:
                    jobdesc=job.find_element(By.CLASS_NAME,"job-description")
                    job_description=jobdesc.text
                except:
                    job_description="Not Found"
                    # print("desc--",traceback.print_exc())
                jobTag=[]
                try:
                    job_tags=job.find_element(By.CLASS_NAME,"tags")
                    tags = job_tags.find_elements(By.CLASS_NAME,"fleft")
                    for tag in tags:
                        jobTag.append(tag.text)
                except:
                    pass
                
                scrapped_data=[]
                scrapped_data.append(job_title)
                scrapped_data.append(company_name)
                scrapped_data.append(company_rating)
                scrapped_data.append(company_review_count)
                scrapped_data.append(requied_experience)
                scrapped_data.append(salary)
                scrapped_data.append(job_location)
                scrapped_data.append(job_description)
                scrapped_data.append(jobTag) 
                self.add_and_save_data(data=scrapped_data)

            page_data=search_container.find_element(By.CLASS_NAME,"pagination")
            next_page=page_data.find_element(By.CLASS_NAME,"fright")
            
            #check if next page is present
            if next_page.get_attribute("disabled"):
                print("stopping....")
                stop_flag=True
                break

            next_page.click() 
            time.sleep(5)
            self.driver.switch_to.window(self.driver.window_handles[-1]) #update driver information for the current 

if __name__=="__main__":
       
    job_titles=["Data Science","Web Designer","UX Designer & UI Developer","Web Developer","DevOps Engineer","Cloud Architect","Artificial Intelligence Engineer" "Information Security Analyst""Business analyst","Data Analyst","HR","system administrator","Network Engineer",]

    for title in job_titles:
        scrapper_object=Naukri_Scrapper(search_jobtitle=title) # scapper object with the given job 
        del scrapper_object #after scrapping delete the object