import requests
import selectorlib

URL = "http://programmer100.pythonanywhere.com/tours/"

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    """Extract the selector"""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email():
    """Sends the event as an email"""
    print("Email was sent!")


def store(extracted):
    """Stores the event in a txt file"""
    with open("data.txt", "w") as file:
        file.write(extracted + "\n")


def read(extracted):
    """Reads a txt file"""
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)

    content = read(extracted)
    # If event exists and not a duplicate, send the email and store in txt
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email()