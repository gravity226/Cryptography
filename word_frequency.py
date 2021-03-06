import pandas as pd
import string

from sklearn.cluster import KMeans
import pickle
from sklearn.externals import joblib

def dist(w):
    letters = dict(zip(string.uppercase[:26], range(1,27)) +
                   zip(string.lowercase[:26], range(1,27)) + [["'", 27], ['-', 28], ['/', 29]])

    if len(w) == 1:
        return letters[w]
    else:
        count = []
        for x in xrange(len(w) - 1):
            if x == "'":
                count += 0
            elif letters[w[x]] > letters[w[x+1]]:
                count += (26 - letters[w[x]]) + letters[w[x+1]]
            else:
                count +=  abs(letters[w[x]] - letters[w[x+1]])
        return count

def dist_breakdown(w):
    letters = dict(zip(string.uppercase[:26], range(1,27)) +
                   zip(string.lowercase[:26], range(1,27)) + [["'", 27], ['-', 28], ['/', 29]])

    if len(w) == 1:
        return letters[w]
    else:
        count = []
        for x in xrange(len(w) - 1):
            if x == "'":
                count.append(0)
            elif letters[w[x]] > letters[w[x+1]]:
                count.append((26 - letters[w[x]]) + letters[w[x+1]])
            else:
                count.append(abs(letters[w[x]] - letters[w[x+1]]))
        return count

def check_dist():
    # Lets check that this worked...
    from Caesar_Cipher_Encryption.c_cipher import encrypt

    top_10 = df.Word.head(10).values
    sentence = reduce(lambda x, y: x + ' ' + y,top_10) # need to input a sentence to this algorithm

    encrypted_s = encrypt(sentence.upper(), 3)

    print "Top ten words on my list of ranked words."
    print "Original:"
    print map(dist, df.Word.head(10).values)
    print
    print "Encrypted:"
    print map(dist, encrypted_s.split())

    '''
    Results:
    Original ['the', 'be', 'and', 'of', 'a', 'in', 'to', 'have', 'to', 'it']
    dist = [37, 3, 29, 17, 1, 5, 21, 49, 21, 11]

    Encrypted ['WKH', 'EH', 'DQG', 'RI', 'D', 'LQ', 'WR', 'KDYH', 'WR', 'LW']
    dist = [37, 3, 29, 17, 4, 5, 21, 49, 21, 11]

    Almost perfect...  Notice how my algorithm doesn't work on one letter words.
    One way to fix this would be to set the distance equal to zero for one letter
    words.  I don't want to do that though because then all one letter words
    will appear to be the same to the algorithm I'm about to write.
    '''

def top_5000():
    df = pd.read_csv('word_frequency.csv')
    df.columns = [ col.strip().replace(' ', '_') for col in df.columns ]
    # columns = [u'Rank', u'Word', u'Part_of_speech', u'Frequency', u'Dispersion']

    # let's do a little cleaning
    df.Rank = df.Rank.map(int)
    df.Word = df.Word.apply(lambda w: w.strip())
    df.Part_of_speech = df.Part_of_speech.apply(lambda w: w.strip())
    df.Rank = df.Rank.map(int)
    df.Frequency = df.Frequency.map(int)
    df.Frequency = df.Frequency.map(float)

    # and finally a little feature engineering
    df['Counts'] = df.Word.apply(lambda w: len(w))
    df['Distance'] = df.Word.map(dist)

    print df.head(10)

    return df

def km_clusters():
    df = top_5000()
    model = KMeans(n_clusters=5000)
    X = df[['Counts', 'Distance']].values
    model.fit_transform(X)
    return model

def naive_predictions(df):
    from Caesar_Cipher_Encryption.c_cipher import encrypt

    model = joblib.load('kmeans_model.pkl')
    labels = list(model.labels_)

    # to encrypt
    s = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG'
    encrypted_s = encrypt(s, 3)

    words = [ [len(word), dist(word)] for word in encrypted_s.split() ]
    preds = model.predict(words)

    predicted_sentence = [ df.Word.ix[labels.index(n)] for n in preds ]

    print "Original Sentence"
    print s.split()
    print
    print "Decrypted sentence with KMeans"
    print predicted_sentence

def more_naive_predictions(df):
    from Caesar_Cipher_Encryption.c_cipher import encrypt

    # get model
    model = joblib.load('kmeans_model.pkl')
    labels = list(model.labels_)

    # to encrypt
    s = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG'
    encrypted_s = encrypt(s, 3)

    # get words frequencies
    words = encrypted_s.split()
    frequencies = np.array( sorted([[words.count(w), w] for w in set(words)], key=lambda w: w[1], reverse=True) )

    # predict the word with the highest frequency
    word = frequencies[0][1]
    pred = model.predict([[len(word), dist(word)]])
    predicted_word = df.Word.ix[labels.index(pred)]
    # if dist_breakdown(word) == dist_breakdown(predicted_word):
    key = dist(word[0]+predicted_word[0])

    print encrypt(encrypted_s, key)



if __name__ == '__main__':
    # ----  Load and Clean data  ----

    df = pd.read_csv('word_frequency.csv')
    df.columns = [ col.strip().replace(' ', '_') for col in df.columns ]
    # columns = [u'Rank', u'Word', u'Part_of_speech', u'Frequency', u'Dispersion']

    df.Rank = df.Rank.map(int)
    df.Word = df.Word.apply(lambda w: w.strip())
    df.Part_of_speech = df.Part_of_speech.apply(lambda w: w.strip())
    df.Rank = df.Rank.map(int)
    df.Frequency = df.Frequency.map(int)
    df.Frequency = df.Frequency.map(float)

    df['Counts'] = df.Word.apply(lambda w: len(w))

    # need a set of n letter words
    words_counts = set(df.Counts.values)
    # _ = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16}

    # ----  Feature Engineering  ----

    '''
    Lets start with a universal distance metric for our words.
    For this I want to have a distance between letters in a word
    that is the same for any word and its encrypted counterpart.

    So imagine the word "THE" or the letter numbers (20, 8, 5).
    The distance for the word would be:
    |(T - H)| + |(H - E)| or
    abs((20 - 8)) + abs((8 - 5)) = 15

    Now if we encrypt "THE" with a key = 3, we get "WKH" or (23, 11, 8)
    The distance for the word would be:
    |(W - K)| + |(K - H)| or
    abs((23 - 11)) + abs((11 - 8)) = 15

    So now we have the same distance for the word and it's encrypted
    version.  A slight alteration will need to be made for when words
    go over the 26 letter mark.
    '''
    # What I wrote above is wrong.  I'll fix it later...

    df['Distance'] = df.Word.map(dist)

    # This is a very naive approach becuase I am assuming that only letters
    # will be used with no characters like ' " , . ? !

    # check_dist()

    '''
    # Saving the model so I only have to run this once.
    model = km_clusters(df)
    joblib.dump(model, 'kmeans_model.pkl')
    '''
