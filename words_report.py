import threading
import os
import time

import requests as req
from bs4 import BeautifulSoup as BS
import pickle as pkl
from tqdm import tqdm

trans=True
multi_size=200

trans_url='http://www.youdao.com/w/%s/'

word_freq=pkl.load(open('data/word_freq.pkl', 'rb'))
word_list=pkl.load(open('data/wordlist.pkl', 'rb'))
word_filter=set(pkl.load(open('data/middle_school_words.pkl', 'rb'))+[''])
word_info=pkl.load(open('data/info.pkl', 'rb'))

# word_set=set(x if x not in word_filter else None for x in set(word_list.keys()))
word_set=set()
for w in word_list.keys():
    if word_list[w] not in word_filter:
        word_set.add(w)

def get_wordlist_form_text(text: str, trans: bool, multi: int) -> dict:
    wlis=[]
    def _get_words(text: str, trans: bool) -> dict:
        # character in text must be lower
        words = {}
        for x in word_set:
            count=text.count(x)
            if count==0: continue

            origin_word=word_list[x]
            if origin_word not in words:
                words[origin_word] = [0, word_freq[origin_word]/word_info['total_word_count']]
                if trans:
                    words[origin_word].append(translate(origin_word))
            words[origin_word][0]+=count

        wlis.append(words)
        return words

    text_split=text.lower().split(' ')
    length=int(len(text_split)/multi)+1
    threads=[]
    for i in range(multi):
        ts=text_split[i*length:(i+1)*length]
        threads.append(
            threading.Thread(target=_get_words, args=(ts, trans))
        )

    for t in threads: t.start()
    for t in threads: t.join()

    words={}
    for w in wlis:
        words=dict(words, **w)

    return words

def translate(word: str) -> str:
    html=req.get(trans_url%word)
    soup=BS(html.content, 'lxml')
    res=''
    try:
        for x in soup.find_all('div', class_='trans-container')[0].find_all('li'):
            res+=x.text+'\n'
    except:
        return 'None\n'
    return res

def get_report(filename: str) -> str:
    text=open(filename, 'r').read()
    report=get_wordlist_form_text(text, trans=trans, multi=multi_size)

    report_text=""
    for key in report.keys():
        value=report[key]

        report_text+="%s [%d, %f%%]\n"%(key, value[0], value[1]*100)
        if trans: report_text+=value[2]+'\n'
    return report_text

start_time=time.time()
for novel_name in os.listdir('novel'):
    novel_path=os.path.join('novel', novel_name)
    report_dir = os.path.join('report', novel_name)
    try:
        os.mkdir(report_dir)
    except:
        pass

    for filename in os.listdir(novel_path):
        file_path=os.path.join(novel_path, filename)
        print(file_path)
        report=get_report(file_path)
        open(os.path.join(report_dir, 'report_'+filename), 'w').write(report)
print('done, cost', time.time()-start_time)