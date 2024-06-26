import re
from collections import Counter

def words(document):
    return re.findall(r'\w+', document.lower())
    
all_words = Counter(words(open('Dictionary.txt').read()))

def edits_one(word):
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    deletes = [left + right[1:] for left, right in splits if right]
    inserts = [left + c + right for left, right in splits for c in alphabets]
    replaces = [left + c + right[1:] for left, right in splits if right for c in alphabets]
    transposes = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right) > 1]
    return set(deletes + inserts + replaces + transposes)

def edits_two(word):
    return (e2 for e1 in edits_one(word) for e2 in edits_one(e1))
        
def known(words):
    return set(word for word in words if word in all_words)
        
def possible_corrections(word):
    return (known([word]) or known(edits_one(word)) or known (edits_two(word)) or [word])

def prob(word, N=sum(all_words.values())):
    return all_words[word] / N
        
def rectify(word):
    correct_word = max(possible_corrections(word), key=prob)
    return correct_word

def suggestion(word):
    return sorted(possible_corrections(word), key=prob, reverse=True)
