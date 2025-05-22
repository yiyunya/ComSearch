import json


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
            if "\\" in data_d["original_text"]:
                data_d["original_text"] = data_d["original_text"].replace('\\', '/')
                data_d["segmented_text"] = data_d["segmented_text"].replace('\\', '/')
            data.append(data_d)
            js = ""

    return data

def write_data(data, fp):
    for d in data:
        fp.write(
            '{{\n    "id":"{}",\n    "original_text":"{}",\n    "segmented_text":"{}",\n    "equation":"{}",\n    "ans":"{}"\n}}\n'.format(
                d['id'], d["original_text"], d["segmented_text"], d["equation"], d["ans"]))


data = load_raw_data('./Math_23K.json')
new_data = load_raw_data('./Math_23K_new.json')

test = json.load(open('./test23k_processed.json'))
valid = json.load(open('./valid23k_processed.json'))

test_ids = [d['id'] for d in test]
valid_ids = [d['id'] for d in valid]

test_data = list(filter(lambda x: x['id'] in test_ids, data))
unsup_train_data = list(filter(lambda x: x['id'] not in test_ids + valid_ids, new_data))
unsup_valid_data = list(filter(lambda x: x['id'] in valid_ids, new_data))
valid_data = list(filter(lambda x: x['id'] in valid_ids, data))
train_data = list(filter(lambda x: x['id'] not in test_ids + valid_ids, data))

write_data(train_data, open('./Math_23K_train.json', 'w'))
write_data(unsup_train_data, open('./Math_23K_new_train.json', 'w'))
write_data(unsup_valid_data, open('./Math_23K_new_valid.json', 'w'))
write_data(valid_data, open('./Math_23K_valid.json', 'w'))
write_data(test_data, open('./Math_23K_test.json', 'w'))
write_data(unsup_train_data+unsup_valid_data, open('./Math_23K_new_train_valid.json', 'w'))
write_data(train_data+valid_data, open('./Math_23K_train_valid.json', 'w'))







