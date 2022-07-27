from nltk.corpus import wordnet
import nltk
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
  
  
def get_synonyms_data(word):
    word = 'hello'
    word = word.lower()
    data = pd.read_csv('/content/drive/MyDrive/data/synonyms_data/synonyms.csv')
    data = data.dropna()

    synonyms = data[data['lemma'] == word]['synonyms']
    if len(synonyms.values) == 0:
      synonyms = data[data['lemma'].str.contains(word, case=False)]['synonyms']

    synonyms_list = synonyms.values[0].split(';')
    return synonyms_list
