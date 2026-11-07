from jobspy import scrape_jobs
import os 
# Run the job scraper across multiple boards 
jobs = scrape_jobs( site_name=["linkedin"],
                    search_term="data scientist",
                    location="India",  
                    results_wanted=20, 
                    hours_old= 72, 
                    fetch_description = True
                    )


# Display result summary 
print(f"Found {len(jobs)} jobs") 
jobs_filtered= jobs[["title", "description"]]
print(jobs_filtered.head())
# Export results to a CSV file 
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Data", "test_jobs.csv")
jobs_filtered.to_csv(output_path, index=False)
print(f"Saved to: {output_path}")