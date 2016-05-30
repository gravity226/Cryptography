# Caesar Cipher

### Summary
This is a simple encryption technique where you shift every letter in a document by n spaces.  

### Contents
 - [Encryption](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#encryption)
 - [Frequency](https://github.com/gravity226/Cryptography/tree/master/Caesar_Cipher_Encryption#frequency)
 - Decryption

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

##### Frequency
One technique for decrypting a document is to look at the frequency of the letters used.
```python
import matplotlib.pyplot as plt
import numpy as np

def frequency(s):
    f = np.array( [[s.count(l), l] for l in set(s)] )
    plt.bar(np.arange(len(f))[1:], map(int, f[:,0].tolist())[1:], .4)
    plt.xticks(np.arange(len(f))[1:], f[:,1].tolist()[1:])
    plt.show()
```
<br />
<img src="https://github.com/gravity226/Cryptography/blob/master/Caesar_Cipher_Encryption/imgs/original_message.png" height="200" />
<br />
<br />
<img src="https://github.com/gravity226/Cryptography/blob/master/Caesar_Cipher_Encryption/imgs/encrypted_message.png" height="200" />
