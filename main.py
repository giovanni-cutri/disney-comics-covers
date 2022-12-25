import argparse
from argparse import RawTextHelpFormatter
import requests
import bs4
import sys
import urllib.request
import os

domain_name = "https://inducks.org/"

res = requests.get("https://inducks.org/legend-country.php")
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, features="lxml")
country_list = soup.select(".countryList a")

countries = []
country_codes = []

try:
    os.makedirs("resources")
except OSError:
    pass

with open("resources/country-codes.txt", "w") as f:
    for i in country_list:
        country = i.getText()
        countries.append(country)
        country_code = i.attrs["href"].split("?c=")[-1]
        country_codes.append(country_code)
        f.write("{:>20}   {:>2}".format(country, country_code) + "\n")

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)  # formatter needed for newline in help message
parser.add_argument("country", help="the country of the publications whose covers you want to download\n" +
                                    "For a list of valid country codes, see resources/country-codes.txt")
args = parser.parse_args()
country = args.country

if country not in country_codes:
    print("Error: could not find any publications\nPlease provide a valid country code")
    sys.exit()

res = requests.get("https://inducks.org/country.php?c=" + country)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, features="lxml")

testate = soup.select('li a')

link_testate = []
nomi_testate = []

for i in testate:
    link_testate.append(domain_name + i.attrs["href"])
    nomi_testate.append(i.getText().replace("?", "").replace("/", "").replace(":", "").replace('"', '')
                        .replace(".", ""))

counter = 0

for i in link_testate:
    res = requests.get(i)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features="lxml")

    print(nomi_testate[counter] + "...")

    tag_albi = soup.select("a[href^='issue.php']")

    for j in tag_albi:
        issue_url = domain_name + j.attrs["href"]
        res = requests.get(issue_url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features="lxml")
        issue_number = issue_url.split("%2F")[-1].replace("+", "")
        cover_elem = soup.select("figcaption a")
        if cover_elem:
            cover_url = domain_name + cover_elem[0].attrs["href"]
            directory = country + "-covers/" + nomi_testate[counter]
            path = country + "-covers/" + nomi_testate[counter] + "/" + issue_number + ".jpg"
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(path):
                urllib.request.urlretrieve(cover_url, path)
    counter = counter + 1
