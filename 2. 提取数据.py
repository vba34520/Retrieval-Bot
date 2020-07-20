import os
import json
from collections import defaultdict

result = defaultdict(dict)  # 最终数据结果

# 构建所有JSON文件路径
dir = './WebQA.v1.0'
json_list = []
for file_path in os.listdir(dir):
    if file_path.endswith(".json"):
        file_path = os.path.join(dir, file_path)
        json_list.append(file_path)

id = 0  # 存在问题编号相同但内容完全不同的情况
for file_path in json_list:
    with open(file_path) as f:
        data = f.read()
        data = json.loads(data)

    for _, v in data.items():
        question = v['question']
        evidences = v['evidences']
        for _k, _v in evidences.items():
            answer = _v['answer'][0]
            evidence = _v['evidence']
            # print(question, answer, evidence)
            if id not in result:  # 该问题还没答案
                if answer != 'no_answer':  # 当前答案不为空
                    result[id]['question'] = question
                    result[id]['answer'] = answer
                    result[id]['evidence'] = evidence
            else:  # 该问题已有答案
                old_answer_list = []  # 已有的答案
                old_answer_index_list = []  # 已有的答案编号
                for __k in result[id]:
                    if 'answer' in __k:
                        old_answer_list.append(result[id][__k])
                        old_answer_index_list.append(__k)
                if answer != 'no_answer' and answer not in old_answer_list:  # 当前答案不为空且与已有答案不同
                    index = 0
                    for i in old_answer_index_list:
                        temp = [int(j) if j else 0 for j in i.split('answer')]
                        temp.append(index)
                        index = max(temp)  # 计算当前最大的答案编号
                    result[id]['answer{}'.format(index + 1)] = answer  # 添加新答案
                    result[id]['evidence{}'.format(index + 1)] = evidence  # 添加新证据
        id = id + 1  # 更新id

# 保存数据
with open('WebQA.v1.0.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False, indent=2))

print('数据共 {} 条'.format(len(result)))
