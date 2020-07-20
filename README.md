# 检索式问答机器人
**基于百度中文问答数据集WebQA构建问答机器人**，共 **45247** 条数据。

属于检索式问答系统，采用倒排索引+TFIDF+余弦相似度。

[语料地址](http://idl.baidu.com/WebQA.html)已失效，已附带在本项目中，43.6Mb，若下载速度较慢可使用[百度网盘](https://pan.baidu.com/s/1TKbyLOj1lRoFUa6mKl5sTw)（frph）

相关论文：[Dataset and Neural Recurrent Sequence Labeling Model for Open-Domain Factoid Question Answering](https://arxiv.org/abs/1607.06275)

![a.gif](https://i.loli.net/2020/07/20/JHS8yLPcGoszjKe.gif)

# 使用方法
1. 安装
```bash
pip install -r requirements.txt
```
2. 解压 WebQA.v1.0.7z
3. 按顺序运行1-4文件
获得过滤好的原始语料 WebQA.v1.0.json，移动到 `./data/`中
4. 启动机器人

# 备注
首次运行会进行分词、转向量任务，需要约25s，将保存多个文件，下一次运行仅需0.2s

|文件名|用途|
|--|--|
|dictionary|语料处理后的gensim字典|
|splitdata.json|原始语料的分词结果|
|tfidf.index|文本相似度序列|
|tfidf.index.0|文本相似度序列缓存文件|
|tfidf.index.1|文本相似度序列缓存文件|
|tfidf.model|TFIDF模型|

# TODO
1. 添加语料接口，更强扩展性



# 1. 观察数据

文件列表

|文件|描述|
|--|--|
|me_test.ann  |一个问题一个证据  |
|me_test.ir  |一个问题多个证据  |
|me_train  |混合训练语料  |
|me_validation.ann  | 一个问题一个证据 |
|me_validation.ir  |一个问题多个证据  |


[解析JSON数据](https://xercis.blog.csdn.net/article/details/107210644)得到构成：

```json
{
  "问题编号": {
    "question": "",
    "evidences": {
      "证据编号1": {
        "answer": "",
        "evidence": ""
      },
      "证据编号n": {
        "answer": "",
        "evidence": ""
      }
    }
  }
}
```

材料中没有答案的话默认为 'no_answer'


存在问题编号相同但内容完全不同的情况



# 2. 提取数据
提取字段有：

|字段|描述|
|--|--|
|question  |问题  |
|answer |答案  |
|evidence  |证据  |
|answer1 | 不同的答案1 |
|answern|不同的答案n  |

提取数据共 **48265** 条，部分结果：

```json
{
  "8284": {
    "question": "世界上最大的岛屿是",
    "answer": "格陵兰岛",
    "evidence": "答：世界上最大的岛屿—格陵兰岛",
    "answer1": "格陵兰",
    "evidence1": "答：世界上最大的岛屿—格陵兰岛"
  },
  "8285": {
    "question": "世界上最大的岛屿在哪里？",
    "answer": "格陵兰岛",
    "evidence": "答：中国最大的岛屿是台湾岛，总陆地面积为35915平方公里，属于台湾省；其次是海南岛，总陆地面积为32198平方公里，属于海南剩世界上最大的岛格陵兰岛（greenland）是世界最大岛，面积2,166,086平方公里(836,330平方哩)。在北美洲东北，北冰洋和大..."
  },
  "8286": {
    "question": "世界上最大的平原是什么",
    "answer": "亚马孙平原",
    "evidence": "亚马孙河是世界流域面积最大的河流,亚马孙河流经的亚马孙平原是世界上面积最大的平原."
  }
}
```


# 3. 过滤数据
观察数据发现：

1. 最多有两个回答，即 'answer' 和 'answer1' 字段
2. 答案有2个的数据共 44 条



# 4. 人工过滤

人工过滤上述数据中有问题的 8 条数据（加粗为正确答案）：

|question|answer|answer1|
|--|--|--|
|第一位任国际足联副主席的华人是|李惠|**李惠堂**|
|世界上最大的金字塔叫什么名字|**胡夫金字塔**|埃及金字塔|
|西游记作者是谁|罗贯中|**吴承恩**|
|西游记的作者是谁|**吴承恩**|罗贯中|
|妙应寺白塔始建于元朝至元八年（公元1271年），由当时哪国的工艺家阿尼哥奉敕主持修建|**尼泊尔**|尼伯尔|
|典故"负荆请罪"中的"负荆"者是向谁请罪的?|蔺相|**蔺相如**|
|《白雪歌送武判官归京》的作者是|岑|**岑参**|
|台湾最大的湖是什么湖？|**日月潭**|澎湖|


# 5. 问答机器人
利用 `gensim` 库构建问答机器人

主要步骤：
1. 读取语料库，分词，去停用词
2. 加载或生成Gensim字典
3. 语料转词袋表示
4. 构建TFIDF模型
5. 比较文本相似度