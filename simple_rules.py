import json

nums = ['0','1','2','3','4','5','6','7','8','9']
ops = ['+', '-', '*', '/', '^']


def check_overlap(tmp_str, tmp_list):
    for tmp in tmp_list:
        if tmp in tmp_str:
            return True
    return False

def main():
    templates = {}
    # train = json.load(open('./train23k_processed.json'))
    # valid = json.load(open('./valid23k_processed.json'))
    # test = json.load(open('./test23k_processed.json'))
    #
    # data = train + valid + test
    data = json.load(open('./matching_data.json'))
    # data = json.load(open('./oracle_matching_data.json'))

    count = 0

    for d in data:
        text = d["original_text"]
        seg = d["segmented_text"]
        if check_overlap(text, ops):
            toks = seg.split(' ')
            start = len(toks)-1
            end = 0
            for i, tok in enumerate(toks):
                if check_overlap(tok, nums):
                    start = i
                    break
            for j, inv_tok in enumerate(toks[::-1]):
                if check_overlap(inv_tok, nums):
                    end = len(toks) - j
                    break
            if start <= end:
                eq_list = toks[start:end]
                # for i, tok in enumerate(eq_list):
                #     if tok not in ops:
                #         eq_list[i] = str(eval(tok))
                eq = ''.join(eq_list)
                # print(eq)
                try:
                    ans = eval(eq)
                    if abs(ans - d['answer'])<0.01:
                        d['rule_equation'] = eq
                        count += 1
                        print(eq)
                except:
                    pass
    print(count)
    f = open('./rule_data.json', 'w')
    # f = open('./oracle_rule_data.json', 'w')
    json.dump(data, f)





if __name__ == '__main__':
    main()