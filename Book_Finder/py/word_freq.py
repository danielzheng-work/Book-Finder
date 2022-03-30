from json_sampler import load_pkl
from collections import Counter
import operator
from wordcloud import WordCloud, ImageColorGenerator
import nltk
import sys
import pandas as pd
import numpy as np

# must do pip install nltk as well do do nltk.download('punkt')

# this method takes the inputted ASIN and finds the top occuring adjectives
def word_freq(input):
    # import the data
    data = load_pkl("pickles/data.pkl")
    ASIN = input
    # load the data into a panda dataframe
    df = pd.DataFrame(data)
    # get the asins and reviews in a list together
    var = df[(df['asin'] == ASIN) & ('reviewText' in df.keys())]
    var = var[['asin', 'reviewText']]
    train_data = np.array(var)
    asinReview = train_data.tolist()
    counter = Counter()
    # get a count of every word in every review associated with that book
    for i in asinReview:
        # split the review into words and add a token to each 
        splitWord = nltk.word_tokenize(str(i[1]))
        # attach a part of speech tag to each word 
        tokens = nltk.pos_tag(splitWord)
        # create a list with only the adjectives, and convert to lowercase 
        adj = [x.lower() for x, key in tokens if (key == 'JJ')]
        # count the occurences of each word over each iteration 
        counter = counter + Counter(adj)
    # take the words with the top 100 occurences
    topItems = dict(sorted(counter.items(), key = operator.itemgetter(1), reverse = True)[:100])
    return topItems

# this method takes the list of words and frequencies and creates a wordcloud out of it 
def word_cloud(bookName):
    topItems = word_freq(bookName)
    # create the wordcloud 
    # output time is limited by the height and width (resolution of image)
    wordcloud = WordCloud(background_color="white", height=200, width=414).generate_from_frequencies(topItems)
    wordcloud.to_file('word_cloud.png')

# method used to display the output in the gui 
if __name__ == '__main__':
    bookName = sys.argv[1]
    word_cloud(bookName)

# test
# word_freq("Five")
# 0001844423
