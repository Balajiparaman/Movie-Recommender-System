import logging
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

movie_name = []
year = []
time = []
rating = []
metascore = []
director = []
votes = []
# gross = []
description = []
genre = []
cast = []
cas = []
pages = np.arange(1, 1000, 50)

for page in pages:
    page = requests.get(
        "https://www.imdb.com/search/title/?title_type=feature&primary_language=en&start="+str(page)+"&ref_=adv_nxt")

    soup = BeautifulSoup(page.text, "html.parser")
    movie_data = soup.findAll(
        "div", attrs={"class": "lister-item mode-advanced"})

    for store in movie_data:
        name = store.h3.a.text
        movie_name.append(name)

        year_of_release = store.h3.find(
            "span", class_="lister-item-year text-muted unbold").text.replace("(", "")

        year_of_release = year_of_release.replace(")", "")
        year.append(year_of_release)

        runtime = store.p.find("span", class_="runtime").text if store.p.find(
            "span", class_="runtime") else "NA"
        time.append(runtime)

        gen = store.p.find("span", class_="genre").text
        genre.append(gen)

        rate = store.find("div", class_="inline-block ratings-imdb-rating").text.replace(
            "\n", "") if store.find("div", class_="inline-block ratings-imdb-rating") else "NA"
        rating.append(rate)

        meta = store.find("span", class_="metascore").text if store.find(
            "span", class_="metascore") else "NA"
        metascore.append(meta)

        dire = store.find("p", class_="").find_all("a")[0].text
        director.append(dire)

        cast.append([a.text for a in store.find(
            "p", class_="").find_all("a")[1:]])

        value = store.find_all("span", attrs={"name": "nv"}) if store.find_all(
            "span", attrs={"name": "nv"}) else "NA"
        vote = value[0].text if store.find_all(
            "span", attrs={"name": "nv"}) else "NA"
        votes.append(vote)

        describe = store.find_all("p", class_="text-muted")
        description_ = describe[1].text.replace(
            "\n", "") if len(describe) > 1 else "NA"
        description.append(description_)

logging.debug(f"movie_data {movie_data}")

for i in cast:
    c = ",".join(map(str, i))
    cas.append(c)

movie_list = pd.DataFrame({"Title": movie_name,
                           "Year_Of_Release": year,
                           "Runtime": time,
                           "Genre": genre,
                           "Movie_Rating": rating,
                           "Metascore": metascore,
                           "Director": director,
                           "Cast": cas,
                           "Votes": votes,
                           "Description": description})

# logging.debug(f"movie data{movie_list.head(5)}")

# movie_list.to_csv("imdb_scrapped_data.csv")
