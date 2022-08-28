import requests, bs4, re, urllib

alt_cover = ["", "B", "C"]

# alcuni albi hanno una o più copertine alternative, contrassegnate da una B o una C alla fine del numero dell'albo

res = requests.get("https://inducks.org/country.php?c=it")
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, features="lxml")

testate = soup.select('li a')

link_testate = []
nomi_testate = []

for i in testate:
    link_testate.append("https://inducks.org/" + i.attrs["href"])
    nomi_testate.append(i.getText())

for i in link_testate:
    res = requests.get(i)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features="lxml")

    codice_testata = re.sub(re.compile(r".*?2F"), "", i)
    issues = soup.findAll("a", {"href": re.compile(r"issue.php.*?")})  # trova tutti i tag che contengono gli albi

    last_issue_number = re.sub("[^0-9]", "", issues[-1].getText())
    last_issue_number_digits = len(str(last_issue_number))

    for j in range(1, int(last_issue_number) + 1):
        for k in alt_cover:
            issue_url = "https://inducks.org/issue.php?c=it%2F" + codice_testata + \
                        str(j).rjust(7-len(codice_testata), "+") + k  # left padding
                        # ipotesi che totale caratteri URL sia 7, non sempre verificata
            res = requests.get(issue_url)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, features="lxml")
            cover_elem = soup.select("figcaption a")
            if cover_elem:
                cover_url = "https://inducks.org/" + cover_elem[0].attrs["href"]
                urllib.request.urlretrieve(cover_url, "copertine/" + str(j) + k + ".jpg")