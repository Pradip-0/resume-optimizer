import os                                                                                                                                  
import random                                                                                                                              
import time                                                                                                                                
import pandas as pd                                                                                                                        
from jobspy import scrape_jobs                                                                                                             
                                                                                                                                            
search_terms = ["data scientist", "business analyst", "MIS analyst", "ml engineer", "ai engineer"]                                         
proxy_list = [                                                                                                                             
    "socks5://216.105.130.131:4145",                                                                                                       
    "socks5://72.195.114.169:4145",                                                                                                        
    "socks5://184.181.217.210:4145",                                                                                                       
    "socks4://149.248.201.109:9000",                                                                                                       
]                                                                                                                                          
                                                                                                                                            
TARGET_RESULTS_PER_TERM = 80                                                                                                               
all_jobs = []                                                                                                                              
                                                                                                                                            
for term in search_terms:                                                                                                                  
    print(f"\n==========================================")                                                                                 
    print(f"Scraping for: {term}...")                                                                                                      
    print(f"==========================================")                                                                                   
                                                                                                                                            
    term_jobs = []                                                                                                                         
    current_offset = 0                                                                                                                     
                                                                                                                                            
    while current_offset < TARGET_RESULTS_PER_TERM:                                                                                        
        # 1. Random batch size between 5 and 10 entries                                                                                    
        batch_size = random.randint(5, 10)                                                                                                 
                                                                                                                                            
        # Ensure we don't request more than the remaining target                                                                           
        batch_size = min(batch_size, TARGET_RESULTS_PER_TERM - current_offset)                                                             
                                                                                                                                            
        try:                                                                                                                               
            print(f"Fetching batch of {batch_size} jobs (offset: {current_offset})...")                                                    
            jobs_batch = scrape_jobs(                                                                                                      
                site_name=["linkedin", "indeed", "glassdoor", "google", "naukri"],                                                         
                search_term=term,                                                                                                          
                location="India",                                                                                                          
                country_indeed="india",                                                                                                    
                results_wanted=batch_size,                                                                                                 
                offset=current_offset,                                                                                                     
                hours_old=168,                                                                                                             
                fetch_description=True,                                                                                                    
                description_format="plain",                                                                                                
                proxies=proxy_list                                                                                                         
            )                                                                                                                              
                                                                                                                                            
            if jobs_batch.empty:                                                                                                           
                print("No more jobs returned for this search term.")                                                                       
                break                                                                                                                      
                                                                                                                                            
            term_jobs.append(jobs_batch)                                                                                                   
            fetched_count = len(jobs_batch)                                                                                                
            current_offset += fetched_count                                                                                                
            print(f"Successfully retrieved {fetched_count} jobs. Total for '{term}': {current_offset}/{TARGET_RESULTS_PER_TERM}")          
                                                                                                                                            
            # If we still have more jobs to fetch, pause                                                                                   
            if current_offset < TARGET_RESULTS_PER_TERM:                                                                                   
                # 2. Random delay between 5 and 20 seconds                                                                                 
                delay = random.uniform(5, 20)                                                                                              
                print(f"Pausing for {delay:.2f} seconds before the next batch...")                                                         
                time.sleep(delay)                                                                                                          
                                                                                                                                            
        except Exception as e:                                                                                                             
            print(f"Error scraping '{term}' at offset {current_offset}: {e}")                                                              
            break                                                                                                                          
                                                                                                                                            
    if term_jobs:                                                                                                                          
        all_jobs.extend(term_jobs)                                                                                                         
                                                                                                                                            
# Save combined results                                                                                                                    
if all_jobs:                                                                                                                               
    combined_jobs = pd.concat(all_jobs, ignore_index=True)                                                                                 
    combined_jobs.drop_duplicates(subset=["id"], inplace=True, ignore_index=True)                                                          
                                                                                                                                            
    print(f"\nFound {len(combined_jobs)} unique jobs in total.")                                                                           
    jobs_filtered = combined_jobs[["title", "description"]]                                                                                
    print(jobs_filtered.head())                                                                                                            
                                                                                                                                            
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Data")                                                    
    os.makedirs(output_dir, exist_ok=True)                                                                                                 
    output_path = os.path.join(output_dir, "jobs.csv")                                                                                     
                                                                                                                                            
    jobs_filtered.to_csv(output_path, index=False)                                                                                         
    print(f"Saved to: {output_path}")                                                                                                      
else:                                                                                                                                      
    print("No jobs found.")   