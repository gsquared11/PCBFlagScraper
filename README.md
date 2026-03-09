# PCB Flag Status Scraper

This Azure Python Function App continually monitors the beach flag status from the [Visit Panama City Beach website](https://www.visitpanamacitybeach.com/plan-your-trip/stay-pcb-current/). Running automatically every 4 hours, it scrapes the current flag type and logs the incident alongside a timestamp to an Azure SQL database. The collected data ultimately powers a separate frontend application ([PCB Flag Data Viewer](https://github.com/gsquared11/pcb-flag-viewer)).

![beachflags-100x100](https://github.com/user-attachments/assets/0ca109e4-1c53-40e6-9913-75414c9e284d)

## How It Works

An Azure Timer Trigger schedules the scraper to run at 4-hour intervals. During an execution, the app fetches the PCB website and parses its HTML to locate the active flag indicator.

The app currently recognizes the following flag conditions:
- Yellow Flag
- Red Flag
- Double Red Flag
- Red Over Purple Flag
- Yellow Over Purple Flag

When a recognized flag is found, the data is pushed to the database using an Azure SQL Output Binding. If no valid flag is identified or the site cannot be reached, the function simply logs the event and exits.

## Tech Stack

- **Backend:** Azure Functions (Python 3.8+)
- **Scraping:** `requests`, `BeautifulSoup4`
- **Database:** Azure SQL Database

## Local Development

To run this app locally or deploy it to Azure, you'll need the Azure Functions Core Tools installed.

1. Configure your local environment by adding your Azure SQL connection string to your `local.settings.json` file:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "UseDevelopmentStorage=true",
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "SqlConnectionString": "<YOUR_SQL_CONNECTION_STRING>"
     }
   }
   ```
2. Install the necessary Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the function app locally:
   ```bash
   func start
   ```
