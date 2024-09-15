# PCB Flag Status Tracker - Azure Python Function App

This Python-based Azure Function App scrapes the Visit Panama City Beach website (https://www.visitpanamacitybeach.com/plan-your-trip/stay-pcb-current/) to check and return the current beach flag status. It is now on a four hour timer (changed from a simple http trigger) that automatically records the flag type, date, and time in a SQL database. This data will soon be displayed on a web app to examine historical data patterns to see if there are any interesting trends regarding safety, surf, hurricane season, etc.!

![beachflags-100x100](https://github.com/user-attachments/assets/0ca109e4-1c53-40e6-9913-75414c9e284d)

# Imports and Libraries
  - Uses `azure.functions`, `logging`, `requests`, `BeautifulSoup`, and `datetime` libraries.
 
# Flag Status Scraping
  - Defines a function `check_flag_status()` that scrapes a website for beach safety flag status based on image URLs of flags (yellow, red, double red).
  - Sends an HTTP request to VisitPCB webpage.
  - Parses the page’s HTML with `BeautifulSoup`.
  - Loops through `<img>` tags to identify and return the corresponding flag (yellow, red, double red).
  - Returns "No Flag" if no flag is found, and "Error" if the website is inaccessible.
  
# Scheduled Timer Trigger Function
  - A function `flag_status_function_timer()` triggers every 4 hours using Azure's schedule decorator.
  - Logs the execution time.
  - Calls the `check_flag_status()` function to get the current flag status.
  - Inserts the flag status and the current timestamp into a SQL database using Azure’s SQL binding if no error occurs.
  - Logs the flag status or any errors in scraping.




## Requirements

- Python 3.8+
- Azure Functions Core Tools
- Required dependencies listed in requirements.txt
