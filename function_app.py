import logging
import requests
from bs4 import BeautifulSoup
import datetime
import azure.functions as func

def check_flag_status():
    # URLs of the flag images
    website_url = "https://www.visitpanamacitybeach.com/plan-your-trip/stay-pcb-current/"
    purple_flag_url = "https://assets.simpleviewinc.com/simpleview/image/upload/c_fill,h_44,q_75,w_58/v1/clients/panamacitybeach/purple_7003bf68-3a99-4a25-9042-5468e3490d60.png"
    yellow_flag_url = "https://assets.simpleviewinc.com/simpleview/image/upload/c_fill,h_80,q_75,w_110/v1/clients/panamacitybeach-redesign/yellow_weather_flag_2x_45dc6242-7cec-4a76-b6f4-ddfea9df95f6.png"
    red_flag_url = "https://assets.simpleviewinc.com/sv-panamacitybeach/image/upload/c_fill,h_80,q_75,w_110/v1/cms_resources/clients/panamacitybeach-redesign/red_weather_flag_2x_35a37199-20cc-45fa-850e-e0d0737973ba.png"
    double_red_flag_url = "https://assets.simpleviewinc.com/sv-panamacitybeach/image/upload/c_limit,h_80,q_75,w_110/v1/cms_resources/clients/panamacitybeach-redesign/double_flag_fd285f87-e94a-4497-9b0e-8150f138daf2.png"

    # Send a request to the website
    response = requests.get(website_url)

    # If the request is successful (status code 200), parse the HTML
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the img tags on the page
        img_tags = soup.find_all('img')

        # Loop through each img tag to check for the image URL
        for img in img_tags:
            img_url = img.get('src')

            # Resolve relative URLs to full URLs if necessary
            if not img_url.startswith(('http://', 'https://')):
                img_url = requests.compat.urljoin(website_url, img_url)

            # Check if the current img tag matches given flag types
            if double_red_flag_url in img_url:
                print(f"Double Red Flag detected at {datetime.datetime.now().strftime('%A, %B %d, %Y at %I:%M:%S %p')}")
                return "Double Red Flag"
            elif red_flag_url in img_url:
                print(f"Red Flag detected at {datetime.datetime.now().strftime('%A, %B %d, %Y at %I:%M:%S %p')}")
                return "Red Flag"
            elif yellow_flag_url in img_url:
                print(f"Yellow Flag detected at {datetime.datetime.now().strftime('%A, %B %d, %Y at %I:%M:%S %p')}")
                return "Yellow Flag"
        
        print("No relevant flag found.")
        return "No Flag"
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
        return "Error"

# Main function for Azure Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
@app.route(route="flag_status")
def flag_status(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function processed a request.')

    # Call the web scraper function
    flag_status = check_flag_status()

    # Return the response as plain text
    return func.HttpResponse(f"Current flag status: {flag_status}", status_code=200)