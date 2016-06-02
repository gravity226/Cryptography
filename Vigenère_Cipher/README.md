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
Like the Caesar Cipher, letter frequency could be a helpful tool in decrypting the message.

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

Looking at this we can already start to see a pattern from just the first 40 characters in the encrypted text.  The idea here is the the distance between the spikes is also the length of the key that is being used.

```python
def find_key_length(encrypted_text):
    pattern = coincidences(encrypted_text)
```
