# Caesar Cipher

### Summary
This is a simple encryption technique where you shift every letter in a document by n spaces.  

### Contents
 - [Encryption](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#encryption)
 - [Letter Frequency](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#letter-frequency)
 - [Word Frequency](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#word-frequency)
 - [Letter Distance](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#letter-distance)
 - [Check Distance](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#check-distance)
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
Top ten words on my list of ranked words.
Original:
['the', 'be', 'and', 'of', 'a', 'in', 'to', 'have', 'to', 'it']
[37, 3, 29, 17, 1, 5, 21, 49, 21, 11]

Encrypted:
['WKH', 'EH', 'DQG', 'RI', 'D', 'LQ', 'WR', 'KDYH', 'WR', 'LW']
[37, 3, 29, 17, 4, 5, 21, 49, 21, 11]
```

<i>Results</i><br />
As expected the distance algorithm works really well except when we look at one letter words.
##### Decryption
