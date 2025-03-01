# PCB Flag Status Scraper - Azure Python Function App

This Azure Function App scrapes the [Visit Panama City Beach website](https://www.visitpanamacitybeach.com/plan-your-trip/stay-pcb-current/) to check and return the current beach flag status. The app is triggered every 4 hours, automatically recording the flag type, date, and time in a SQL database. The recorded data is then displayed on a Flask Web App hosted on Azure ([see PCB Flag Data Viewer](https://github.com/gsquared11/pcb-flag-viewer)).

![beachflags-100x100](https://github.com/user-attachments/assets/0ca109e4-1c53-40e6-9913-75414c9e284d)

## Features

### 1. Flag Status Scraping

- **Function Name**: `check_flag_status()`
- **Purpose**: Scrapes the [VisitPCB webpage](https://www.visitpanamacitybeach.com/plan-your-trip/stay-pcb-current/) to identify the current beach flag status.
- **Approach**:
  - Sends an HTTP request to the webpage.
  - Parses the HTML using `BeautifulSoup`.
  - Loops through `<img>` tags to find image URLs corresponding to known flag types:
    - **Yellow Flag**
    - **Red Flag**
    - **Double Red Flag**
  - Returns the corresponding flag status:
    - `"Double Red Flag"`, `"Red Flag"`, or `"Yellow Flag"` if a known flag is detected.
    - `"No Flag"` if no matching flag image is found.
    - `"Error"` if the website is inaccessible.

### 2. Scheduled Timer Trigger Function

- **Function Name**: `flag_status_function_timer()`
- **Purpose**: Triggers every 4 hours using Azure's Timer Trigger.
- **Schedule**: Executes at the start of every 4th hour (e.g., 12:00, 04:00, 08:00, ...).
- **Functionality**:
  - Logs the execution time.
  - Calls `check_flag_status()` to get the current flag status.
  - If no error occurs, inserts the flag status and the current timestamp into the SQL database using Azure’s SQL binding.
  - Logs the detected flag status or any errors encountered during the scraping process.


## Technology Stack

- **Backend**:
  - **Azure Functions**:
    - `Timer Trigger`: Schedules the scraping every 4 hours.
    - `SQL Output Binding`: Stores flag status and timestamp.
  - **Web Scraping**:
    - `requests`: Sends HTTP requests to the target webpage.
    - `BeautifulSoup`: Parses HTML to extract image URLs.
- **Database**:
  - **Azure SQL Database**: Stores flag status and timestamps.
- **Web Display**:
  - **Flask Web App**: Displays the recorded data on a frontend hosted on Azure.

## Prerequisites

- **Python**: 3.8 or higher
- **Azure Functions Core Tools**: Installed and configured
- **Azure SQL Database**: Connection string configured as `SqlConnectionString` in Azure Function App settings.

