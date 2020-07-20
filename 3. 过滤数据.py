import json

with open('WebQA.v1.0.json', encoding='utf-8') as f:
    data = json.loads(f.read())

print('数据共 {} 条'.format(len(data)))

# 判断答案是否有3个
hasAnswer2 = False
for _, value in data.items():
    if 'answer2' in value:
        hasAnswer2 = True
if hasAnswer2:
    print('答案有3个的')
else:
    print('答案没有3个的')

# 输出答案
length = 0
for _, value in data.items():
    if 'answer1' in value:
        length += 1
        answer = value['answer']
        answer1 = value['answer1']
        print('|{}|{}|{}|'.format(value['question'], value['answer'], value['answer1']))
print('答案有2个的共 {} 条'.format(length))
