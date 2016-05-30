import pandas as pd
import string


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
    def dist(w):
        letters = dict(zip(string.uppercase[:26], range(1,27)) +
                       zip(string.lowercase[:26], range(1,27)) + [["'", 27], ['-', 28], ['/', 29]])

        if len(w) == 1:
            return letters[w]
        else:
            count = 0
            for x in xrange(len(w) - 1):
                if x == "'":
                    count += 0
                elif letters[w[x]] > letters[w[x+1]]:
                    count += (26 - letters[w[x]]) + letters[w[x+1]]
                else:
                    count +=  abs(letters[w[x]] - letters[w[x+1]])
            return count

    df['Distance'] = df.Word.map(dist)

    # This is a very naive approach becuase I am assuming that only letters
    # will be used with no characters like ' " , . ? !
