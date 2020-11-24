import requests
from bs4 import BeautifulSoup
import requests_cache
import pandas as pd
requests_cache.install_cache("bases_scraping", expire_after=10e5)

#Param
url = "https://www.leboncoin.fr/recherche?category=2&text=205 gti"
page = "&page="
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#get all_ads
def getting_add(all_ads):
    list_all_ads = []

    for ads in all_ads:
        infos = ads.find(class_="_2pXp-")
        title = infos.find(class_="_1MlU1").text.strip()
        image = infos.find(class_="_1cnjm")

        try:
            price = infos.find(class_="_1C-CB").text.strip()
        except:
            price = None

        #get the location of the ad
        locals = infos.findAll(class_="_1UzWr")
        location = ""
        for local in locals:
            location = location + local.text.strip()
            location = location + ","
            pass

        list_all_ads.append({"title":title, "price":price, "location":location,"image":image['src']})

    return list_all_ads

#display in panda DataFrame
def display_pandas(list_all_ads):
    df_leboncoin = pd.DataFrame(list_all_ads)
    df_leboncoin.head()
    pass


def main():
    #execute la requête
    response = requests.get(url, headers=headers)

    if response == "<Response [200]>":
        #beautiful soup parsing
        soup = BeautifulSoup(response.text, "lxml")
        div_annonce = soup.find(class_="styles_classifiedColumn__LeJpD")
        all_ads = div_annonce.findAll(class_="styles_adListItem__3Z_IE")

        list_all_ads = getting_add(all_ads)

        display_pandas(list_all_ads)

    else:
        print("Error having a bad status code:")
        print(response)


    pass

main()
