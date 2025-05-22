import json

path = 'Math_23K.json'
alpha_dic = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13, 'o':14, 'p':15, 'q':16, 'r':17}
# f_data = open(path)

# data = json.load(f_data)

def load_raw_data(filename):  # load the json data to list(dict()) for MATH 23K
    print("Reading lines...")
    f = open(filename, encoding="utf-8")
    js = ""
    data = []
    for i, s in enumerate(f):
        js += s
        i += 1
        if i % 7 == 0:  # every 7 line is a json
            data_d = json.loads(js)
            if "千米/小时" in data_d["equation"]:
                data_d["equation"] = data_d["equation"][:-5]
            data.append(data_d)
            js = ""

    return data


examples = json.load(open('./rule_data.json'))
examples_dict = {d['id']:d for d in examples}

data = load_raw_data(path)
unsup_data = []

# count = 0

for d in data:
    example = examples_dict[d['id']]
    if 'rule_equation' in example.keys():
        unsup_data.append({"id":d['id'],
                           "original_text":d['original_text'],
                           "segmented_text":d["segmented_text"],
                           "equation":'x='+example['rule_equation'],
                           "ans":d['ans']})
    elif 'tmp_equation' in example.keys():
        if len(set(example['tmp_equation'])) == 1:
            tmp_equation = example['tmp_equation'][0]
            reformed_eq = 'x=' + ''.join(tmp_equation.split(' '))
            # reformed_text = example
            tokens = example['text'].split(' ')
            for i, tok in enumerate(tokens):
                if 'temp' in tok:
                    tokens[i] = str(example['num_list'][alpha_dic[tok[-1]]])
                elif tok == '\\':
                    tokens[i] = '\\\\'
            reformed_origin = ''.join(tokens)
            reformed_seg = ' '.join(tokens)
            unsup_data.append({"id": d['id'],
                               "original_text": reformed_origin,
                               "segmented_text": reformed_seg,
                               "equation": reformed_eq,
                               "ans": example["answer"]})

print(len(unsup_data))

f_out = open('./Math_23K_new.json', 'w')

for d in unsup_data:
    f_out.write(
        '{{\n    "id":"{}",\n    "original_text":"{}",\n    "segmented_text":"{}",\n    "equation":"{}",\n    "ans":"{}"\n}}\n'.format(
            d['id'], d["original_text"], d["segmented_text"], d["equation"], d["ans"]))
