from nltk.corpus import wordnet
import nltk
import lemminflect
from collections import Counter
import pandas as pd

nltk.download('omw-1.4')
nltk.download('wordnet')



def get_synonyms(word):
    word = word.lower()
    synonyms_list = []
    synonyms_dict = {}
    synonyms = wordnet.synsets(word)
    for syn in synonyms:
        synonyms_dict[str(syn)] = []
        lemmas = syn.lemma_names()
        for word in lemmas:
            word = word.replace('_', ' ')
            synonyms_list.append(word)
            synonyms_dict[str(syn)].append(word)
    synonyms_list = list(set(synonyms_list))
    return (synonyms_list, synonyms_dict)

def get_synonyms_enhanced(word):
    word = word.lower()
    synonyms_list = []
    synonyms = wordnet.synsets(word)
    for syn in synonyms:
        if word in str(syn):
            lemmas = syn.lemma_names()
            for w in lemmas:
                w = w.replace('_', ' ')
                synonyms_list.append(w)
    synonyms_list = list(set(synonyms_list))
    return synonyms_list




def get_inflections(word):
    word = word.lower()
    all_inf = []
    upos = ['VERB', 'NOUN', 'ADV', 'ADJ']
    for u in upos:
        lemma = lemminflect.getLemma(word, upos=u)[0]
        inf = list(lemminflect.getAllInflections(lemma).values())
        for i in inf:
            for j in i:
                all_inf.append(j)
    return list(set(all_inf))



def process_data(file_name):
    data = pd.read_csv(file_name)
    return data

def get_count(word_l):
    word_count_dict = Counter(word_l)
    return word_count_dict

def get_probs():
    data = process_data(r'D:\Programs\PyCharm\Projects\Saiph\data\unigram_freq.csv')
    full_count = data['count'].sum()
    probs = dict(zip(data['word'], data['count'] / full_count))
    return probs

def delete_letter(word, verbose=False):
    delete_l = []
    split_l = []

    for c in range(len(word)):
        split_l.append((word[:c], word[c:]))
    for a, b in split_l:
        delete_l.append(a + b[1:])

    if verbose: print(f"input word {word}, \nsplit_l = {split_l}, \ndelete_l = {delete_l}")

    return delete_l

def switch_letter(word, verbose=False):
    switch_l = []
    split_l = []

    len_word = len(word)
    for c in range(len_word):
        split_l.append((word[:c], word[c:]))
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_l if len(b) >= 2]

    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nswitch_l = {switch_l}")

    return switch_l

def replace_letter(word, verbose=False):
    letters = 'abcdefghijklmnopqrstuvwxyz\''
    replace_l = []
    split_l = []

    for c in range(len(word)):
        split_l.append((word[0:c], word[c:]))
    replace_l = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_l if b for l in letters]
    replace_set = set(replace_l)
    replace_set.remove(word)

    replace_l = sorted(list(replace_set))

    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nreplace_l {replace_l}")

    return replace_l

def insert_letter(word, verbose=False):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_l = []
    split_l = []

    for c in range(len(word) + 1):
        split_l.append((word[0:c], word[c:]))
    insert_l = [a + l + b for a, b in split_l for l in letters]

    if verbose: print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")

    return insert_l

def edit_one_letter(word, allow_switches=True):
    edit_one_set = set()

    edit_one_set.update(delete_letter(word))
    if allow_switches:
        edit_one_set.update(switch_letter(word))
    edit_one_set.update(replace_letter(word))
    edit_one_set.update(insert_letter(word))

    return edit_one_set

def edit_two_letters(word, allow_switches=True):
    edit_two_set = set()

    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w, allow_switches=allow_switches)
            edit_two_set.update(edit_two)

    return edit_two_set

def get_corrections(word, probs, vocab, n=2, verbose=False):
    suggestions = []
    n_best = []

    suggestions = list(edit_one_letter(word).intersection(vocab))
    suggestions.extend(list(edit_two_letters(word).intersection(vocab)))
    if (word in vocab and word):
        suggestions.append(word)
    n_best = [[s, probs[s]] for s in list(reversed(suggestions))]

    if verbose: print("suggestions = ", suggestions)

    return n_best

def get_correction_suggestions(word):
    word = word.lower()
    word_l = list(process_data(r'D:\Programs\PyCharm\Projects\Saiph\data\unigram_freq.csv')['word'])
    vocab = set(word_l)
    probs = get_probs()
    tmp_corrections = get_corrections(word, probs, vocab, 2, verbose=False)
    tmp_corrections_dict = dict(tmp_corrections)
    tmp_corrections_ordered = {k: v for k, v in
                               reversed(sorted(tmp_corrections_dict.items(), key=lambda item: item[1]))}
    tmp_corrections_ordered_list = tmp_corrections_ordered.keys()

    return list(tmp_corrections_ordered_list)

# my_word = 'laptob'
# tmp_corrections = get_corrections(my_word, probs, vocab, 2, verbose=False)
# tmp_corrections_dict = dict(tmp_corrections)
# tmp_corrections_ordered = {k: v for k, v in reversed(sorted(tmp_corrections_dict.items(), key=lambda item: item[1]))}
# for k, v in tmp_corrections_ordered.items():
#     print(f"word: {k},  prob: {v:.6f}")
# print(tmp_corrections_ordered)
# print(f"data type of corrections {type(tmp_corrections)}")