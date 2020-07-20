import json


def parse_structure(d, n=None, n_tab=-1):
    '''解析数据结构'''
    if isinstance(d, list):
        for i in d:
            parse_structure(i, n, n_tab)
    elif isinstance(d, dict):
        n_tab += 1
        if n == n_tab:
            return
        for key, value in d.items():
            print("{}{}".format("\t" * n_tab, key))
            parse_structure(value, n, n_tab)
    else:
        pass


# with open('./WebQA.v1.0/me_test.ann.json') as f:
with open('./WebQA.v1.0/me_test.ir.json') as f:
# with open('./WebQA.v1.0/me_train.json') as f:
# with open('./WebQA.v1.0/me_validation.ann.json') as f:
# with open('./WebQA.v1.0/me_validation.ir.json') as f:
    data = f.read()
    data = json.loads(data)

# 观察结构
# parse_structure(data)

# 完整输出
for id, value in data.items():
    if id == 'Q_IR_VAL_001029':
        print(value)
    question = value['question']
    evidences = value['evidences']
    for _, v in evidences.items():
        answer = v['answer'][0]
        evidence = v['evidence']
        print(question, answer, evidence)

print('数据共 {} 条'.format(len(data)))
