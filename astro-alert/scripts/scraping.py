import requests
import csv
import html5lib
from bs4 import BeautifulSoup


def scrape():
    # Send a request to the webpage
    url = "https://github.com/cjwinchester/earth-impact-data/blob/main/earth-impact-craters.csv"
    r = requests.get(url)

    # Extract the HTML content
    html_content = r.content

    # Create a BeautifulSoup object and parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the table element that contains the data
    table = soup.find("table")

    # Extract the data from the table
    data = []
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [col.text.strip() for col in cols]
        data.append(cols)

    D1_file = "C:/Users/hp/Desktop/uni/sem4/ds_proj/excel_files/raw_D1.csv"

    with open(D1_file, "w", newline="") as file:
        writer = csv.writer(file)
        headers = [
            "Empty",
            "Crater Name",
            "State",
            "Country",
            "Rock",
            "Diameter (km)",
            "Age (Ma)",
            "Exposed",
            "Drilled",
            "Bolide Type",
            "Latitude",
            "Longitude",
            "URL",
            "Notes",
        ]
        writer.writerow(headers)
        writer.writerows(data)
