# Vigenère Cipher
With Python 2.7

### Summary
The Vigenère Cipher was developed by mathematician Blaise de Vigenère in the 16th century. The Vigenère Cipher was adapted as a twist on the standard Caesar cipher to reduce the effectiveness of performing frequency analysis on the ciphertext. The cipher accomplishes this using uses a text string (for example, a word) as a key, which is then used for doing a number of alphabet shifts on the plaintext. Similar to the Caesar Cipher, but instead of performing a single alphabet shift across the entire plaintext, the Vigenère cipher uses a key to determine several different shift amounts across the entirety of the message. [Reference](https://learncryptography.com/classical-encryption/vigenere-cipher)  

### Contents
 - [Encryption](https://github.com/gravity226/Cryptography/tree/master/Vigenère_Cipher#encryption)
 - [Letter Frequency](https://github.com/gravity226/Cryptography/tree/master/Vigenère_Cipher#letter-frequency)
 - [Find the Key Length](https://github.com/gravity226/Cryptography/tree/master/Vigenère_Cipher#find-the-key-length)

##### Encryption
``` python
import string

letters = string.uppercase[:26] + "!@#$%^&*()_+-=,./<>?'1234567890"
# letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=,./<>?'1234567890"

def encrypt(text, key='TOMMY'):
    encrypted_text = ''
    for n in xrange(len(text)):
        en = letters.index(text[n])
        adding = n % len(key)

        new_letter = en + adding

        if new_letter > len(letters):
            encrypted_text += letters[new_letter - len(letters)]
        else:
            encrypted_text += letters[new_letter]

    return encrypted_text
```

##### Letter Frequency
Lets take a look at the letter frequency again like we did with the Caesar Cipher.

``` python
import matplotlib.pyplot as plt
import numpy as np

def letter_frequency(sup, s):
    f = np.array( sorted([[s.count(l), l] for l in set(s)], key=lambda z: z[1]) )
    # f = np.array(sorted(f, key=lambda z: z[1]))
    # return f
    plt.bar(np.arange(len(f))[1:], map(int, f[:,0].tolist())[1:], .4)
    plt.xticks(np.arange(len(f))[1:], f[:,1].tolist()[1:])
    plt.suptitle(sup)
    # plt.title(s)
    plt.savefig('original_message.png')
    plt.show()
```

Original Text Letter Frequency<br />

<img src="https://github.com/gravity226/Cryptography/blob/master/Vigenère_Cipher/imgs/original_message.png" height="400" />

Encrypted Text Letter Frequency<br />

<img src="https://github.com/gravity226/Cryptography/blob/master/Vigenère_Cipher/imgs/encrypted_message.png" height="400" />

<i>Results</i><br />
So this is nice but it's a lot harder to interpret when compared to the Caesar Cipher letter frequency.

##### Find the Key Length
In order to find our key length we need to find coincidences in our encrypted text. [Reference](https://www.youtube.com/watch?v=LaWp_Kq0cKs)

Finding coincidences is the process of shifting letters over by one space, counting the number of letters that are the same, and then repeating the process until the end.  See the reference for a better explanation.  :)

```python
def coincidences(encrypted_text):
    pattern = []
    for a in xrange(1, len(encrypted_text)):
        count = 0
        for b, c in zip(encrypted_text[a:], encrypted_text[:-a]):
            if b == c:
                count += 1
        pattern.append(count)

    plt.plot(pattern[:40])
    plt.savefig('key_length_pattern.png')
    plt.show()
```

<img src="https://github.com/gravity226/Cryptography/blob/master/Vigenère_Cipher/imgs/key_length_pattern.png" height="400" />

Looking at this we can already start to see a pattern from just the first 40 characters in the encrypted text.  The idea here is to look at the distance between the spikes and that should also be the length of the key that is being used.

```python
def find_key_length(encrypted_text):
    pattern = coincidences(encrypted_text)

    distances = []
    last = 0
    for x in xrange(1, len(pattern)-1):
        if pattern[x] > pattern[x-1] and pattern[x] > pattern[x+1]:
            distances.append(x - last)
            last = x

    plt.plot(distances)
    plt.savefig('key_length.png')
    plt.show()

    print Counter(distances).most_common(5)
```
```output
[(5, 54), (3, 27), (2, 26), (4, 11), (6, 5)]
```

Thanks to this nifty little library called Counter we can see what the most common numbers are and how often they appear.  At the top is the number 5 with 54 total peaks in our encrypted message.  So from here we can assume that the length of the key is 5.  Now we need to figure out the key itself.  

Here is a quick visual of the height of all of the peaks in our data.

<img src="https://github.com/gravity226/Cryptography/blob/master/Vigenère_Cipher/imgs/key_length.png" height="400" />
