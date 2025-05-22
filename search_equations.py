from fractions import Fraction
import json

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

class Node:
    def __init__(self, ch=None, left=None, right=None, polar=0, id=0):
        self.ch = ch                                    # 变量或运算符
        self.left = left                                # 左孩子
        self.right = right                              # 右孩子
        self.polar = polar                              # 极性，可取 0, 1, -1
        self.id = id                                    # 结点编号

    def __str__(self):                                  # 把树转换成算式
        if self.ch not in '+-*/':
            return self.ch                              # 单变量不加括号
        left = str(self.left)                           # 左子树转字符串
        right = str(self.right)                         # 右子树转字符串
        if self.ch in '*/' and self.left.ch in '+-':
            left = '(' + left + ')'                     # 左子树加括号
        if self.ch == '/' and self.right.ch in '+-*/' or self.ch in '*-' and self.right.ch in '+-':
            right = '(' + right + ')'                   # 右子树加括号
        return left + ' ' + self.ch + ' ' + right       # 用根结点的运算符相连

# 下面是几种 actions 函数，它们接收两个结点，返回它们的各种运算结果
# 「去重」者可以避免交换律、结合律、去括号、反转减号四种原因造成的重复

# 仅考虑加法与乘法，不去重


def naive2(left, right):
    for op in '+*':
        yield Node(op, left, right)
        yield Node(op, right, left)

# 仅考虑加法与乘法，去重


def smart2(left, right):
    for op in '+*':
        if op != left.ch and (op != right.ch or left.id < right.left.id):
            yield Node(op, left, right)

# 考虑加减乘除，不去重


def naive4(left, right):
    for op in '+-*/':
        yield Node(op, left, right)
        yield Node(op, right, left)

# 考虑加减乘除，去重


def smart4(left, right):
    # 加法：两个孩子都不能是减号；左孩子还不能是加号；
    #       若右孩子是加号，则左孩子和右孩子的左孩子要满足单调性
    if left.ch not in '+-' and right.ch != '-' and (right.ch != '+' or left.id < right.left.id):
        if left.polar == 0 or right.polar == 0:
            # 无极性 + 无极性 = 无极性
            yield Node('+', left, right, left.polar + right.polar)
            # 有极性 + 无极性 = 有极性者的极性
        else:
            # 有极性 + 有极性 = 右子树极性
            yield Node('+', left, right, right.polar)
    # 减法：两个孩子都不能是减号
    if left.ch != '-' and right.ch != '-':
        if left.polar == 0 and right.polar == 0:                    # 无极性 - 无极性：
            yield Node('-', left, right, 1)                         # 正过来减是正极性
            yield Node('-', right, left, -1)                        # 反过来减是负极性
        else:
            if left.polar == 0:
                # 有极性 - 无极性 = 有极性者的极性
                yield Node('-', right, left, right.polar)
                # （无极性 - 有极性 = 舍弃）
                # （有极性 - 有极性 = 舍弃）
            if right.polar == 0:
                yield Node('-', left, right, left.polar)            # 同上
    # 乘法：两个孩子都不能是除号；左孩子还不能是乘号；
    #       若右孩子是乘号，则左孩子和右孩子的左孩子要满足单调性
    if left.ch not in '*/' and right.ch != '/' and (right.ch != '*' or left.id < right.left.id):
        if left.polar == 0 or right.polar == 0:
            # 无极性 * 无极性 = 无极性
            yield Node('*', left, right, left.polar + right.polar)
            # 有极性 * 无极性 = 有极性者的极性
        elif left.polar > 0:
            # 正极性 * 有极性 = 右子树极性
            yield Node('*', left, right, right.polar)
            # （负极性 * 有极性 = 舍弃）
    # 除法：两个孩子都不能是除号
    if left.ch != '/' and right.ch != '/':
        if left.polar == 0 or right.polar == 0:
            # 无极性 / 无极性 = 无极性
            yield Node('/', left, right, left.polar + right.polar)
            # 有极性 / 无极性 = 有极性者的极性
            # 无极性 / 有极性 = 有极性者的极性
            yield Node('/', right, left, left.polar + right.polar)  # 同上
        else:
            if left.polar > 0:
                # 正极性 / 有极性 = 右子树极性
                yield Node('/', left, right, right.polar)
                # （负极性 / 有极性 = 舍弃）
            if right.polar > 0:
                yield Node('/', right, left, left.polar)            # 同上

# 枚举由 n 个变量组成的算式


def enum(n, actions):
    def DFS(trees, minj):                                           # trees 为当前算式列表，minj 为第二棵子树的最小下标
        if len(trees) == 1:
            yield str(trees[0])                                     # 只剩一个算式，输出
            return
        for j in range(minj, len(trees)):                           # 枚举第二棵子树
            for i in range(j):                                      # 枚举第一棵子树
                for node in actions(trees[i], trees[j]):            # 枚举运算符
                    node.id = trees[-1].id + 1                      # 为新结点赋予 id
                    new_trees = [treesk for k, treesk in enumerate(
                        trees) if k != i and k != j] + [node]
                    # 从列表中去掉两棵子树，并加入运算结果
                    new_minj = j - 1 if actions in (smart2, smart4) else 1
                    # 若 actions 函数去重，则此处也避免「独立运算顺序不唯一」造成的重复
                    for expression in DFS(new_trees, new_minj):     # 递归下去
                        yield expression

    trees = [Node(chr(ord('a') + i), id=i)
             for i in range(n)]           # 初始时有 n 个由单变量组成的算式
    return DFS(trees, 1)




def main():
    templates = {}
    train = json.load(open('./train23k_processed.json'))
    valid = json.load(open('./valid23k_processed.json'))
    test = json.load(open('./test23k_processed.json'))
    for n in range(1, 7):
        smart_exps = list(enum(n, smart4))
        smart_uniq_exps = set(smart_exps)
        templates[n] = smart_uniq_exps

    data = train + valid + test


    # d = data[100]
    # nums = d['num_list']
    # tmp_n = len(nums)
    # print(nums)
    # count_long = 0
    # count_dup = 0
    # count_miss = 0
    # count_const_1 = 0
    # count_const_pi = 0
    # count_pow = 0
    # for d in data:
    #     tmp_n = len(d['num_list'])
    #     if tmp_n == 1:
    #         print(d)
        # equation = d["target_norm_post_template"]
        # if len(d['num_list']) > 5:
        #     count_long += 1
        # used = list(filter(lambda x: 'temp' in x, equation))
        # set_used = set(used)
        # if len(set_used) != len(used):
        #     count_dup += 1
        # if len(set_used) != len(d['num_list']):
        #     count_miss += 1
        # if str(1) in equation:
        #     count_const_1 += 1
        # if 'PI' in equation:
        #     count_const_pi += 1
        #     # print(d["original_text"])
        # if '^' in equation:
    #         count_pow += 1
    # print(len(data))
    # print(count_long)
    # print(count_dup)
    # print(count_miss)
    # print(count_const_1)
    # print(count_const_pi)
    # print(count_pow)




    count_long = 0
    count_dup = 0
    count_miss = 0
    count_const_1 = 0
    count_const_pi = 0
    count_pow = 0


    count = 0
    single_count = 0
    for d in data:
        flag = 0
        tmp_eqs = []
        nums = d['num_list']
        tmp_n = len(nums)
        if tmp_n < 6:
            for ex in templates[tmp_n]:
                tmp_eq = ex
                for i in range(tmp_n):
                    tmp_eq = tmp_eq.replace(alphabet[i], str(nums[i]))
                try:
                    tmp_ans = eval(tmp_eq)
                    if abs(tmp_ans - d['answer']) < 0.01:
                        tmp_eqs.append(tmp_eq)
                        flag = 1
                except:
                    pass
                # if eval(tmp_eq) == d['answer']:
                #     tmp_eqs.append(tmp_eq)
        if not flag:
            if tmp_n > 1 and tmp_n < 6:
                for j in range(len(nums)):
                    new_nums = nums[:j] + nums[j+1:]
                    for ex in templates[tmp_n-1]:
                        tmp_eq = ex
                        for i in range(tmp_n-1):
                            tmp_eq = tmp_eq.replace(alphabet[i], str(new_nums[i]))
                        try:
                            tmp_ans = eval(tmp_eq)
                            if abs(tmp_ans - d['answer']) < 0.01:
                                tmp_eqs.append(tmp_eq)
                                flag = 1
                        except:
                            pass
        if not flag:
            if tmp_n < 5:
                new_nums = [1] + nums
                for ex in templates[tmp_n+1]:
                    tmp_eq = ex
                    for i in range(tmp_n+1):
                        tmp_eq = tmp_eq.replace(alphabet[i], str(new_nums[i]))
                    try:
                        tmp_ans = eval(tmp_eq)
                        if abs(tmp_ans - d['answer']) < 0.01:
                            tmp_eqs.append(tmp_eq)
                            flag = 1
                    except:
                        pass
        if not flag:
            if tmp_n < 5:
                for dup in nums:
                    new_nums = [dup] + nums
                    for ex in templates[tmp_n+1]:
                        tmp_eq = ex
                        for i in range(tmp_n+1):
                            tmp_eq = tmp_eq.replace(alphabet[i], str(new_nums[i]))
                        try:
                            tmp_ans = eval(tmp_eq)
                            if abs(tmp_ans - d['answer']) < 0.01:
                                tmp_eqs.append(tmp_eq)
                                flag = 1
                        except:
                            pass

        d['tmp_equation'] = tmp_eqs
        if len(tmp_eqs) == 1:
            single_count += 1

        if not tmp_eqs:
            equation = d["target_norm_post_template"]
            count += 1
            if tmp_n >= 6:
                count_long += 1
                flag = 1
            used = list(filter(lambda x: 'temp' in x, equation))
            set_used = set(used)
            if len(set_used) != len(used):
                count_dup += 1
                flag = 1
            if len(set_used) != len(d['num_list']):
                count_miss += 1
                flag = 1
            if str(1) in equation:
                count_const_1 += 1
                flag = 1
            if 'PI' in equation:
                count_const_pi += 1
                flag = 1
            if '^' in equation:
                count_pow += 1
                flag = 1
        if not flag:
            print(d['original_text'])
            print(d["target_template"])
            print(d['answer'])

    print(count)
    print(count_long)
    print(count_dup)
    print(count_miss)
    print(count_const_1)
    print(count_const_pi)
    print(count_pow)
    print(len(data))
    print(count/len(data))
    print(single_count)
    print(single_count/len(data))

    json.dump(data, open('./matching_data_new.json', 'w'))

    #     smart_uniq_values = set(eval(ex) for ex in smart_uniq_exps)
    # print(templates[3])
    

if __name__ == '__main__':
    main()
