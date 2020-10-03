import json
import requests
import nltk
from pprint import pprint
from PIL import Image
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd

st.title("Project 1 by Samantha Fernandez")

st.header("Part A - The Top Stories API")

st.subheader("I. Topic Selection")

name = st.text_input("What's your name?", " ")

option = st.selectbox(
    "Choose a Top NYT Story topic:",
    ["arts", "automobiles", "books", "business", "fashion", "food", "health", "home", "insider", "magazine", "movies",
     "nyregion", "obituaries", "opinion", "politics", "realestate", "science", "sports", "sundayreview", "technology",
     "theater", "t-magazine", "travel", "upshot", "US", "world"]
)
'Hello', name, 'the topic you chose is ', option, "."

### Start of data retrieval
api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_key"]
url = "https://api.nytimes.com/svc/topstories/v2/" + option + ".json?api-key=" + api_key
response = requests.get(url).json()

main_functions.save_to_file(response, "JSON_Files/response.json")

my_articles = main_functions.read_from_file("JSON_Files/response.json")
### End of data retrieval

str1 = ""
for i in my_articles["results"]:
    str1 = str1 + i["abstract"]

sentences = sent_tokenize(str1)

words = word_tokenize(str1)

fdist = FreqDist(words)

words_no_punc = []

for w in words:
    if w.isalpha():
        words_no_punc.append(w.lower())

fdist = FreqDist(words_no_punc)

pprint(fdist.most_common(10))

stopwords = stopwords.words("english")

clean_words = []

for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)

# print(len(clean_words))

fdist3 = FreqDist(clean_words)

#pprint(fdist3.most_common(10))

wordcloud = WordCloud().generate(str1)

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud)

plt.axis("off")
plt.show()

wordcloud.to_file("img/wordcloud.png")

### II. Frequency Distribution
st.subheader("II. Frequency Distribution")
st.write("By checking below you'll get to generate a fancy frequency distribution chart displaying the most "
             "popular words across all NYT articles about " + option)

# create a dictionary with the frequency distribution
dataset = {'list': fdist3.most_common(10)}

position_x = [x[0] for x in dataset['list']]
position_y = [x[1] for x in dataset['list']]

freq_chart = pd.DataFrame({
    'Words': position_x,
    'Count': position_y
})

freq_chart = freq_chart.rename(columns={'Words': 'Index'}).set_index('Index')

if st.checkbox("Check here " + name):
    st.line_chart(freq_chart)

### III. WordCloud Visualization
st.subheader("III. WordCloud Visualization")
image = Image.open("img/wordcloud.png")
st.image(image, "Here is a perfect visual summary of the most popular words across NYT articles", use_column_width=True)

#Part B
st.header("Part B - Most Popular Articles")
st.subheader("I. Choose Sharing and Frequency")
option2 = st.selectbox(
    "Here, choose your preferred way of sharing NYT articles: ",
    ["emailed", "shared", "viewed"]
)
name,'chose', option2,"!"

option3 = st.selectbox(
    "How often do you engage with " + option2 + " NYT articles?",
    ["1", "7", "30"]
)
name,'chose every', option3," days! Good choice."

### Start of data retrieval
url2 = "https://api.nytimes.com/svc/mostpopular/v2/" + option2 + "/" + option3 + ".json?api-key=" + api_key
response2 = requests.get(url2).json()

main_functions.save_to_file(response2, "JSON_Files/response2.json")

my_popular_articles = main_functions.read_from_file("JSON_Files/response2.json")
### End of data retrieval

str2 = " "
for i in my_popular_articles["results"]:
    str2 = str2 + i["abstract"]

### WordCloud Visualization
wordcloud2 = WordCloud().generate(str2)

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud2)

plt.axis("off")
plt.show()

wordcloud2.to_file("img/wordcloud2.png")

st.subheader("II. WordCloud Visualization")
image = Image.open("img/wordcloud2.png")
st.image(image, "", use_column_width=True)

st.write(name + " you have reached the end of my project, thank you for testing it out!")