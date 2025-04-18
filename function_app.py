import azure.functions as func
import logging
from azure.functions.decorators.core import DataType
import requests
from bs4 import BeautifulSoup
import datetime

# Declare function app instance
app = func.FunctionApp()

# Function to check the flag status by scraping the website
def check_flag_status():
    # URLs of the flag images
    website_url = "https://www.visitpanamacitybeach.com/plan-your-trip/stay-pcb-current/"
    yellow_flag_url = "https://assets.simpleviewinc.com/sv-panamacitybeach/image/upload/c_fill,h_80,q_75,w_110/v1/cms_resources/clients/panamacitybeach-redesign/yellow_weather_flag_2x_45dc6242-7cec-4a76-b6f4-ddfea9df95f6.png"
    red_flag_url = "https://assets.simpleviewinc.com/sv-panamacitybeach/image/upload/c_fill,h_80,q_75,w_110/v1/cms_resources/clients/panamacitybeach-redesign/red_weather_flag_2x_35a37199-20cc-45fa-850e-e0d0737973ba.png"
    double_red_flag_url = "https://assets.simpleviewinc.com/sv-panamacitybeach/image/upload/c_limit,h_80,q_75,w_110/v1/cms_resources/clients/panamacitybeach-redesign/double_flag_fd285f87-e94a-4497-9b0e-8150f138daf2.png"
    red_purple_flag_url = "https://assets.simpleviewinc.com/sv-panamacitybeach/image/upload/c_limit,h_80,q_75,w_110/v1/cms_resources/clients/panamacitybeach/Red_and_Purple2_bffd8d4c-2bc1-4ad1-910f-90d9f11611f6.png"
    yellow_purple_flag_url = "https://assets.simpleviewinc.com/sv-panamacitybeach/image/upload/c_limit,h_80,q_75,w_110/v1/cms_resources/clients/panamacitybeach/Yellow_and_Purple2_ae8edbde-66fa-4815-86ed-a1b72f519004.png"

    # Send a request to the website
    response = requests.get(website_url)

    # If the request is successful (status code 200), parse the HTML
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tags = soup.find_all('img')

        # Loop through each img tag to check for the image URL
        for img in img_tags:
            img_url = img.get('src')
            # Resolve relative URLs to full URLs if necessary
            if not img_url.startswith(('http://', 'https://')):
                img_url = requests.compat.urljoin(website_url, img_url)

            # Check which flag is detected
            if double_red_flag_url in img_url:
                return "Double Red Flag"
            elif red_flag_url in img_url:
                return "Red Flag"
            elif yellow_flag_url in img_url:
                return "Yellow Flag"
            elif red_purple_flag_url in img_url:
                return "Red Over Purple Flag"
            elif yellow_purple_flag_url in img_url:
                return "Yellow Over Purple Flag"
        
        # If no flag is detected
        return "No Flag"
    else:
        # Return an error status if the website could not be reached
        return "Error"

@app.function_name(name="flag_status_timer")
@app.schedule(schedule="0 0 */4 * * *", arg_name="timer", run_on_startup=False, use_monitor=True)
@app.generic_output_binding(
    arg_name="flagData", 
    type="sql", 
    CommandText="dbo.flag_data", 
    ConnectionStringSetting="SqlConnectionString", 
    data_type=DataType.STRING
)
def flag_status_function_timer(timer: func.TimerRequest, flagData: func.Out[func.SqlRow]) -> None:
    logging.info('Timer trigger function executed at: %s', datetime.datetime.now())

    # Scrape the current flag status
    current_flag_status = check_flag_status()

    # Get the current time and date in UTC
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # If the flag status is not an error, prepare the SQL output
    if current_flag_status != "Error":
        # Use SQL binding to insert the data into the database
        flagData.set(func.SqlRow({
            "flag_type": current_flag_status,
            "date_time": current_time
        }))
        
        logging.info(f"Flag status: {current_flag_status} detected at {current_time}")
    else:
        # Log the error in fetching the flag status
        logging.error("Error fetching the flag status.")