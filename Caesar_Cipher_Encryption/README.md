# Caesar Cipher
With Python 2.7

### Summary
This is a simple encryption technique where you shift every letter in a document by n spaces.  

### Contents
 - [Encryption](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#encryption)
 - [Letter Frequency](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#letter-frequency)
 - [Word Frequency](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#word-frequency)
 - [Letter Distance](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#letter-distance)
 - [Check Distance](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#check-distance)
 - [Top 5000 Words](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#top-5000-words)
 - [Modeling](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#modeling)
 - [Decryption](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#decryption)

##### Encryption
``` python
import string

def encrypt(s, key):
    uppers = string.uppercase[:26]
    s1 = ''
    for l in s:
        if l == ' ':
            s1 += ' '
        else:
            new_key = uppers.index(l) + key if uppers.index(l) + key < len(uppers) else uppers.index(l) + key - len(uppers)
            s1 += uppers[new_key]
    return s1
```

##### Letter Frequency
One technique for decrypting a document is to look at the frequency of the letters used.
```python
import matplotlib.pyplot as plt
import numpy as np

def frequency(s):
    f = np.array( sorted([[s.count(l), l] for l in set(s)], key=lambda z: z[1]) )
    plt.bar(np.arange(len(f))[1:], map(int, f[:,0].tolist())[1:], .4)
    plt.xticks(np.arange(len(f))[1:], f[:,1].tolist()[1:])
    plt.show()
```
<br />
<img src="https://github.com/gravity226/Cryptography/blob/master/Caesar_Cipher_Encryption/imgs/original_message.png" height="400" />
<br />
<br />
<img src="https://github.com/gravity226/Cryptography/blob/master/Caesar_Cipher_Encryption/imgs/encrypted_message.png" height="400" />

##### Word Frequency
What about the word frequency?  Some words are naturally used more than others.
``` python
import matplotlib.pyplot as plt
import numpy as np

def word_frequency(s):
    words = s.split()
    f = np.array( sorted([[words.count(w), w] for w in set(words)], key=lambda w: w[1]) )

    plt.bar(np.arange(len(f))[1:], map(int, f[:,0].tolist())[1:], .4, color='y')
    plt.xticks(np.arange(len(f))[1:], f[:,1].tolist()[1:], rotation=45)
    plt.show()
```
<br />
<img src="https://github.com/gravity226/Cryptography/blob/master/Caesar_Cipher_Encryption/imgs/wf_original.png" height="400" />
<br />
<br />
<img src="https://github.com/gravity226/Cryptography/blob/master/Caesar_Cipher_Encryption/imgs/wf_encrypted.png" height="400" />

##### Letter Distance
In order to decrypt this I had the idea to create a distance metric for every word.  This metric would look at the distance between letters in a word.  When you think about it, the distance between letters in a word would be the same whether that word is encrypted or not.  The only exception to this would be one letter words as there is no distance between letters to calculate.

<i>Example:</i><br />
<img src="https://github.com/gravity226/Cryptography/blob/master/Caesar_Cipher_Encryption/imgs/distance_example.jpg" height="200" />

```python
import string

# The input for this method is a word.  ex: w = 'the'
def dist(w):
    # create a list of letters that might be seen in a given word
    letters = dict(zip(string.uppercase[:26], range(1,27)) +
                   zip(string.lowercase[:26], range(1,27)) + [["'", 27], ['-', 28], ['/', 29]])

    # check the length of the word.  one letter words will be calculated differently
    if len(w) == 1:
        return letters[w]
    else:
        count = 0
        for x in xrange(len(w) - 1):
            # check that you're looking at a letter and nothing else
            if x == "'":
                count += 0
            elif letters[w[x]] > letters[w[x+1]]:
                count += (26 - letters[w[x]]) + letters[w[x+1]]
            else:
                count +=  abs(letters[w[x]] - letters[w[x+1]])
        return count
```

##### Check Distance
Let's make sure that the distance lines up with my words and their encrypted versions.

```python
def check_dist():
    # top 10 words used in the English language
    top_10 = ['the', 'be', 'and', 'of', 'a', 'in', 'to', 'have', 'to', 'it']

    sentence = reduce(lambda x, y: x + ' ' + y,top_10) # need to input a sentence to this algorithm

    # Using the encrypt() method we created above
    encrypted_s = encrypt(sentence.upper(), 3)

    print "Top ten words on my list of ranked words."
    print "Original:"
    print top_10
    print map(dist, top_10) # use the dist() method we created above
    print
    print "Encrypted:"
    print encrypted_s.split()
    print map(dist, encrypted_s.split())
```
```output
Top ten words used in the English language.
Original:
['the', 'be', 'and', 'of', 'a', 'in', 'to', 'have', 'to', 'it']
[37, 3, 29, 17, 1, 5, 21, 49, 21, 11]

Encrypted:
['WKH', 'EH', 'DQG', 'RI', 'D', 'LQ', 'WR', 'KDYH', 'WR', 'LW']
[37, 3, 29, 17, 4, 5, 21, 49, 21, 11]
```

<i>Results</i><br />
As expected the distance algorithm works really well except when we look at one letter words.

##### Top 5000 Words
So in order to decrypt a document I need a group of words to build my model on.  I got a copy of the 5000 most used words in the English language from [www.wordfrequency.info](http://www.wordfrequency.info).  Thanks to them I am able to test my ideas on decryption.

```python
import pandas as pd

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
```
```ouput
   Rank  Word Part_of_speech  Frequency  Dispersion  Counts  Distance
0     1   the              a   22038615        0.98       3        37
1     2    be              v   12545825        0.97       2         3
2     3   and              c   10741073        0.99       3        29
3     4    of              i   10343885        0.97       2        17
4     5     a              a   10144200        0.98       1         1
5     6    in              i    6996437        0.98       2         5
6     7    to              t    6332195        0.98       2        21
7     8  have              v    4303955        0.97       4        49
8     9    to              i    3856916        0.99       2        21
9    10    it              p    3872477        0.96       2        11
```

##### Modeling
So we now know a couple important things about a word, whether it's encrypted or not.  First we have a universal distance metric that works for anything except one letter words.  Second we also know how many letters are in each word.  Based on this I had the idea to use a clustering algorithm to group words based on their given distance and number of letters.  A simple clustering algorithm to use and implement is SKLearn's KMeans.

```python
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import pickle

def km_clusters():
    # grab the data
    df = top_5000()
    X = df[['Counts', 'Distance']].values

    # create the model
    # notice that I'm really overfitting the model here
    model = KMeans(n_clusters=5000)
    model.fit_transform(X)

    # save the model so that I only have to run this once
    joblib.dump(model, 'kmeans_model.pkl')
```

##### Decryption
Now it's time to decrypt a message that has been encrypted by a Caesar Cipher.

```python
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.externals import joblib

def naive_predictions(df):
    model = joblib.load('kmeans_model.pkl')
    labels = list(model.labels_)

    # to encrypt
    s = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG'
    encrypted_s = encrypt(s, 3)

    # to decrypt
    words = [ [len(word), dist(word)] for word in encrypted_s.split() ]
    preds = model.predict(words)

    predicted_sentence = [ df.Word.ix[labels.index(n)] for n in preds ]

    print "Original Sentence"
    print s.split()
    print
    print "Decrypted sentence with KMeans"
    print predicted_sentence
```
```output
Original Sentence
['THE', 'QUICK', 'BROWN', 'FOX', 'JUMPS', 'OVER', 'THE', 'LAZY', 'DOG']

Decrypted sentence with KMeans
['the', 'every', 'money', 'who', 'black', 'very', 'the', 'role', 'and']
```

<i>Results</i><br />
So my first attempt wasn't great.  I'm getting about %22 accuracy on this particular sentence.  But I can improve on this.  For my next attempt I will incorporate the word frequency algorithm I made earlier.  Let's try this again.

```python
import numpy as np

def more_naive_predictions(df):
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
    key = dist(word[0]+predicted_word[0])

    # use the same encryption method to decrypt it
    print encrypt(encrypted_s, key)
```

<i>Results</i><br />
So this method decrypts this particular sentence perfectly.  I am still not satisfied though.  This method assumes that the word with the highest frequency will be decrypted correctly.  This would be a problem in real life as not everything is this cut and dry.  So lets try to take this a couple steps further.  
