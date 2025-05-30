#import necessary packages needed for this project
from bs4 import BeautifulSoup
import requests, pandas

#get the request to the website to parse
SCRAPE = "https://www.audible.com/search?keywords=book&node=18573211011"

response = requests.get(SCRAPE)
website = response.text

#use BeautifulSoup to get the data that we need from the website
soup = BeautifulSoup(website, "html.parser")

#take the title of the books
book_title = soup.find_all(name="h3", class_="bc-heading bc-color-link bc-pub-break-word bc-size-medium")
titles =[]
for title in book_title:
    title_trim = title.text.strip()
    titles.append(title_trim)

#take the author of the books
book_author = soup.find_all(name="li", class_="bc-list-item authorLabel")
authors = []
for author in book_author:
    author_trim = author.text.strip().replace("By:", "").strip()
    authors.append(author_trim)

#take the narrators of the books
book_narrator = soup.find_all(name="li", class_="bc-list-item narratorLabel")
narrators = []
for narrator in book_narrator:
    narrator_trim = narrator.text.strip().replace("Narrated by:", "").strip()
    narrators.append(narrator_trim)

#take the length of the audio
book_runtime = soup.find_all(name="li", class_="bc-list-item runtimeLabel")
length = []
for runtime in book_runtime:
    runtime_trim = runtime.text.strip().replace("Length: ", "")
    length.append(runtime_trim)

#take the release date of the books
book_date = soup.find_all(name="li", class_="bc-list-item releaseDateLabel")
dates = []
for date in book_date:
    date_trim = date.text.strip().replace("Release date:", "").strip()
    dates.append(date_trim)

#take the languages of the books
book_lang = soup.find_all(name="li", class_="bc-list-item languageLabel")
languages = []
for lang in book_lang:
    lang_trim = lang.text.strip().replace("Language:", "").strip()
    languages.append(lang_trim)

#take the star ratings of the book
book_rating = soup.find_all(name="li", class_="bc-list-item ratingsLabel")
rates = []
for rating in book_rating:
    rating_trim = rating.text.strip()
    rates.append(rating_trim.split("\n"))
#separate the star rating from the total ratings
stars = [rates[i][0] for i in range(len(rates))]
total_rates = []
not_rated = "Not rated yet"
for i in range(len(rates)):
    try:
        total_rates.append(rates[i][1])
    except IndexError:
        total_rates.append(not_rated)

#create the dictionary to prepare the csv
data = {
    "Title": titles,
    "Author": authors,
    "Narrator": narrators,
    "Release Date": dates,
    "Language": languages,
    "Star Rating": stars,
    "Total Rating": total_rates
}

#create the csv file using pandas dataframe
file = pandas.DataFrame(data)
file.to_csv("data.csv", index=False)