import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")


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


def send_email(message):
    """Sends an email"""
    host = "smtp.gmail.com"
    port = 465
    username = "Dannybui5155@gmail.com"
    with open(".env", 'r') as file:
        password = file.read().split("=")[1]
        # print(password)
    receiver = "Dannybui5155@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host=host, port=port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


def store(extracted):
    """Stores the event in a SQLite Database"""
    row = extracted.split(",")
    row = [item.strip() for item in row]  # remove leading spaces
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()

def read(extracted):
    """Reads extracted content """
    row = extracted.split(",")
    row = [item.strip() for item in row] # remove leading spaces

    band, city, date = row # assigns each index with a name
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        # If event exists and not a duplicate, send the email and store in txt
        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row: # If read function returns an empty list
                store(extracted)
                send_email(message="Hey, a new event was found!")
                print("Email was sent!")
        time.sleep(2) # Checks for events every 5 minutes