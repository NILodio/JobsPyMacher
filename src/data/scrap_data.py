# from jobscrapper import scrape_jobs
import sys
import os
# setting path
sys.path.insert(0, '..')
# importing
from jobscrapper import scrape_jobs
import pandas as pd
from IPython.display import display, HTML

# print("Insert resume data source directory for search term extraction:")
# job_titles = os.listdir(input()) # extracted from resume data source folders
job_titles = ['ACCOUNTANT', 'ADVOCATE', 'AGRICULTURE', 'APPAREL', 'ARTS', 'AUTOMOBILE', 'AVIATION', 'BANKING', 'BPO', 'BUSINESS-DEVELOPMENT', 'CHEF', 'CONSTRUCTION', 'CONSULTANT', 'DESIGNER', 'DIGITAL-MEDIA', 'ENGINEERING', 'FINANCE', 'FITNESS', 'HEALTHCARE', 'HR', 'INFORMATION-TECHNOLOGY', 'PUBLIC-RELATIONS', 'SALES', 'TEACHER']
job_titles = list(map(str.lower, job_titles))
job_titles = [w.replace('-', ' ') for w in job_titles]
job_titles += ['software engineer', 'software developer', 'data scientist', 'data analyst'] # adding extra terms
num_titles = len(job_titles)

jobs_total = None
for i, job in enumerate(job_titles):
	print("===== Scrapping Job (" + str(i+1) + "/" + str(num_titles) + "):", job, "=====")
	jobs_remote = scrape_jobs(
	    site_name=["indeed"],
	    search_term=job,
	    country_indeed="CANADA",
	    hyperlinks=False,
	    is_remote=True,
	    results_wanted=250, 
	)
	jobs_onsite = scrape_jobs(
	    site_name=["indeed"],
	    search_term=job,
	    country_indeed="CANADA",
	    hyperlinks=False,
	    is_remote=False,
	    results_wanted=250, 
	)
	jobs = pd.concat([jobs_remote, jobs_onsite], ignore_index=True)
	if jobs_total is not None:
		jobs_total = pd.concat([jobs_total, jobs], ignore_index=True)
	else:
		jobs_total = jobs.copy()

	# save CSV file checkpoint
	jobs_total.to_csv(f'jobs_{jobs_total.shape[0]}.csv', index=False)
	print(f"Checkpoint saved as CSV file:'jobs_{jobs_total.shape[0]}.csv'")
