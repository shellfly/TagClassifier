from collections import Counter

import random
import nltk
import jieba

jieba.add_word("村上春树")
jieba.add_word("夏目漱石")
jieba.add_word("细思极恐")
stopwords = set([l.strip() for l in open('stopwords.txt')])

topics = {
    19551556:"旅行",
    19789286: "日语学习",
    19562563: "日剧",
    19860581: "JLPT",
    19622153: "留学日本",
    19550994: "游戏",
    19597091: "日本文学",
    19591985: "动漫"
}
def tokensize(content):
    content = content.replace(' ', '').replace('\n', '');
    return [w for w in jieba.cut(content) if len(w) > 1 and w not in stopwords]

def build_dictionary(num):
    dictionary = set()
    for name in topics.values():
        words = [w for l in open(name+".txt") for w in tokensize(l)]
        words = Counter(words)
        dictionary |= set(w[0] for w in words.most_common(num))
    return dictionary

dictionary = build_dictionary(100)
print('dictionary length: ', len(dictionary))

def gen_features(content):
    words = list(tokensize(content))
    return {w: words.count(w) for w in dictionary}

original_featuresets = []
for name in topics.values():
    content = open(name+".txt").read()
    items = [i for i in content.split('\n\n') if i]
    original_featuresets.extend([(gen_features(item), name, item) for item in items])

random.shuffle(original_featuresets)
featuresets = [of[:2] for of in original_featuresets]
print('all feature sets: ', len(featuresets))
train_set, devtest_set, test_set = featuresets[200:], featuresets[100:200], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, devtest_set))


errors = []
for (features, name, item) in original_featuresets[500:1000]:
    guess = classifier.classify(features)
    if guess != name:
        print( 'name: ', name, 'guess: ', guess)
        print([(f,count) for f,count in features.items() if count])