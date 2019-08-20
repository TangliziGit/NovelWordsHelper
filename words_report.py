import threading
import os
import time
import string

import requests as req
from bs4 import BeautifulSoup as BS
from tqdm import tqdm
import nltk

trans = True
multi_size = 50

trans_url = 'http://www.youdao.com/w/%s/'
stopwords=nltk.corpus.stopwords.words('english')
lemmatizer = nltk.stem.WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):
    from nltk.corpus import wordnet
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def get_word_list_form_text(text: str, trans: bool, multi: int) -> dict:
    def check_contain_punctuation(word: str) -> bool:
        for ch in string.punctuation+string.digits:
            if ch in word:
                return True
        return False

    def _get_words(text: str) -> dict:
        # character in text must be lower
        words = {}
        for sent in nltk.sent_tokenize(text):
            for word, pos in nltk.pos_tag(nltk.word_tokenize(sent)):
                if word in stopwords: continue
                if check_contain_punctuation(word): continue

                word=lemmatizer.lemmatize(word, pos=get_wordnet_pos(pos))
                if word not in words:
                    words[word] = [0, 0]
                words[word][0]+=1
        return words

    words=_get_words(text.lower())
    if not trans:
        return words

    trans_list=[]
    lock=threading.Lock()
    def _translate(*keys):
        t={}
        for key in keys:
            t[key]=translate(key)
        lock.acquire()
        trans_list.append(t)
        lock.release()

    length = int(len(words.keys()) / multi) + 1
    threads=[]
    for i in range(multi):
        keys=list(words.keys())[i*length:(i+1)*length]
        threads.append(
            threading.Thread(target=_translate, args=(keys))
        )
    for t in threads: t.start()
    for t in threads: t.join()

    translation={}
    for t in trans_list:
        translation=dict(translation, **t)
    for k in words.keys():
        words[k].append(translation[k])

    return words


def translate(word: str) -> str:
    html = req.get(trans_url % word)
    soup = BS(html.content, 'lxml')
    res = ''
    try:
        for x in soup.find_all('div', class_='trans-container')[0].find_all('li'):
            res += x.text + '\n'
    except:
        return 'None\n'
    return res


def get_report(filename: str) -> str:
    text = open(filename, 'r').read()
    report = get_word_list_form_text(text, trans=trans, multi=multi_size)

    report_text = ""
    for key in tqdm(report.keys()):
        value = report[key]

        report_text += "%s [%d, %f%%]\n" % (key, value[0], value[1] * 100)
        if trans:
            report_text += value[2] + '\n'
    report_text += '-' * 20 + '\n'
    report_text += "Total " + str(len(report.keys())) + ' words.'
    return report_text


start_time = time.time()
for novel_name in os.listdir('novel'):
    novel_path = os.path.join('novel', novel_name)
    report_dir = os.path.join('report', novel_name)
    try:
        os.mkdir(report_dir)
    except:
        pass

    for filename in os.listdir(novel_path):
        file_path = os.path.join(novel_path, filename)
        print(file_path)
        report = get_report(file_path)
        open(os.path.join(report_dir, 'report_' + filename), 'w').write(report)
print('done, cost', time.time() - start_time)
