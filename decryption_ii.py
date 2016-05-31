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
        return [letters[w]]
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

def shape_data(w):
    a = dist_breakdown(w)
    l = [len(w)]
    needed = [ 0 for zero in xrange(16 - len(a)) ]

    return l + a + needed


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
    X = df.Word.map(shape_data).values
    model.fit_transform(list(X))
    joblib.dump(model, 'kmeans_16d_model.pkl')

def naive_predictions(df):
    from Caesar_Cipher_Encryption.c_cipher import encrypt

    # get model
    model = joblib.load('kmeans_16d_model.pkl')
    labels = list(model.labels_)

    # to encrypt
    s = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG'
    encrypted_s = encrypt(s, 3)

    words = [ shape_data(word) for word in encrypted_s.split() ]
    preds = model.predict(words)

    predicted_sentence = [ df.Word.ix[labels.index(n)] for n in preds ]

    print "Original Sentence"
    print s.split()
    print
    print "Decrypted sentence with KMeans"
    print predicted_sentence


def key_predictions(df):
    from Caesar_Cipher_Encryption.c_cipher import encrypt

    # get model
    model = joblib.load('kmeans_16d_model.pkl')
    labels = list(model.labels_)

    # to encrypt
    s = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG'
    encrypted_s = encrypt(s, 3)

    # get words frequencies
    words = encrypted_s.split()
    frequencies = np.array( sorted([[words.count(w), w] for w in set(words)], key=lambda w: w[1], reverse=True) )

    # predict the word with the highest frequency
    count = 0
    for word in words:
        pred = model.predict([shape_data(word)])
        predicted_word = df.Word.ix[labels.index(pred)]
        if dist_breakdown(word) == dist_breakdown(predicted_word):
            key = dist(word[0]+predicted_word[0])
            break
        else:
            count += 1

    if count < len(words):
        print encrypt(encrypted_s, key)
    else:
        print "No guess here..."



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
