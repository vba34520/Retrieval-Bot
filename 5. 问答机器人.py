import os
import time
import json
import jieba
import gensim
import argparse


def split_word(sentence, stoplist=[]):
    '''分词+删除停用词，返回列表'''
    words = jieba.cut(sentence)
    result = [i for i in words if i not in stoplist]
    return result


# 解析参数
parser = argparse.ArgumentParser(description='问答机器人参数')
parser.add_argument('--data_filepath', default='./data/WebQA.v1.0.json')  # 语料路径
parser.add_argument('--stopwords_filepath', default='./data/stopwords.txt')  # 停用词路径
parser.add_argument('--splitdata_filepath', default='./data/splitdata.json')  # 分词结果路径
parser.add_argument('--dictionary_filepath', default='./data/dictionary')  # gensim字典路径
parser.add_argument('--model_filepath', default='./data/tfidf.model')  # tfidf模型路径
parser.add_argument('--index_filepath', default='./data/tfidf.index')  # 相似度比较序列路径
args = parser.parse_args()

# 语料库
with open(args.data_filepath, encoding='utf-8') as f:
    data = json.load(f)

# 停用词
with open(args.stopwords_filepath, encoding='utf-8') as f:
    stoplist = f.read().splitlines()

beg = time.time()
print('分词中...')
# 加载分词结果，若无则生成
splitdata_filepath = args.splitdata_filepath
if os.path.exists(splitdata_filepath):
    with open(splitdata_filepath, encoding='utf-8') as f:
        content = json.load(f)
else:
    content = []  # 已分词且去停用词的问题
    for key, value in data.items():
        question = value['question']
        content.append(split_word(question, stoplist))
    with open(splitdata_filepath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False))
print('分词耗时 {:.2f}s'.format(time.time() - beg))

beg = time.time()
# 加载gensim字典，若无则生成
dictionary_filepath = args.dictionary_filepath
if os.path.exists(dictionary_filepath):
    dictionary = gensim.corpora.Dictionary.load(dictionary_filepath)
else:
    dictionary = gensim.corpora.Dictionary(content)
    dictionary.save(dictionary_filepath)
print('gensim字典耗时 {:.2f}s'.format(time.time() - beg))

beg = time.time()
num_features = len(dictionary)  # 特征数

# 加载tfidf模型，若无则生成
model_filepath = args.model_filepath
if os.path.exists(model_filepath):
    tfidf = gensim.models.TfidfModel.load(model_filepath)
else:
    corpus = [dictionary.doc2bow(line) for line in content]  # 语料转词袋表示
    tfidf = gensim.models.TfidfModel(corpus)  # 构建tfidf模型
    tfidf.save(args.model_filepath)  # 保存tfidf模型

# 加载tfidf相似度比较序列，若无则生成
index_filepath = args.index_filepath
if os.path.exists(index_filepath):
    index = gensim.similarities.Similarity.load(index_filepath)
else:
    index = gensim.similarities.Similarity(args.index_filepath, tfidf[corpus], num_features)  # 文本相似度序列
    index.save(index_filepath)
print('语料转词袋耗时 {:.2f}s'.format(time.time() - beg))

sentences = '郑州在哪个省份？'
while True:
    sentences = split_word(sentences, stoplist)  # 分词
    vec = dictionary.doc2bow(sentences)  # 转词袋表示
    sims = index[tfidf[vec]]  # 相似度比较
    sorted_sims = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)  # 逆序

    print('分词结果 ->  ', sentences)
    print("相似度比较 ->  ", sorted_sims[:5])
    for i, similarity in sorted_sims[:5]:
        print(similarity, data[str(i)])

    sentences = input('Your input ->  ')
