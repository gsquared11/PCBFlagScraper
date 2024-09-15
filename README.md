# PCB Flag Status Tracker - Azure Python Function App

This Python-based Azure Function App scrapes the Visit Panama City Beach website (https://www.visitpanamacitybeach.com/plan-your-trip/stay-pcb-current/) to check and return the current beach flag status. I'm planning to record this data in a SQL database to try and
identify any trends that may be interesting regarding surf, safety, or other marine conditions!

![beachflags-100x100](https://github.com/user-attachments/assets/0ca109e4-1c53-40e6-9913-75414c9e284d)

## Functionality
- Scraping the Website: The function sends an HTTP GET request to the VisitPCB flag status page, parses the returned HTML using BeautifulSoup, and searches for image tags that match specific flag URLs.
- Flag Identification: The function compares the image URLs found on the page to predefined URLs for different flag statuses (e.g., yellow, red, double red). Based on the match, it determines the current flag status.
- HTTP Response: When triggered via an HTTP request, the function returns the detected flag status (e.g., "Yellow Flag", "Red Flag") as a plain text response.
- Error Handling: If the scraping process fails, the function returns an appropriate error message (e.g., "Error" for failed requests).


## Requirements

- Python 3.8+
- Azure Functions Core Tools
- Required dependencies listed in requirements.txt

## Running Locally

1. Install dependencies with pip install -r requirements.txt.
2. Run the function locally using func start.
3. Send an HTTP request to check the flag status.
