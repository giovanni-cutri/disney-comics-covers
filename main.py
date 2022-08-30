import requests
import bs4
import urllib.request
import os

domain_name = "https://inducks.org/"

res = requests.get("https://inducks.org/country.php?c=it")
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
            directory = "copertine/" + nomi_testate[counter]
            path = "copertine/" + nomi_testate[counter] + "/" + issue_number + ".jpg"
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(path):
                urllib.request.urlretrieve(cover_url, path)
    counter = counter + 1
