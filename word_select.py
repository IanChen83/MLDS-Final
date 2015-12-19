import pdb

que_file = open("./dataset/pack/question.train")
miss_file = open("miss.txt", 'w')
next(que_file)

que = [l.split('\t')[2].split('"')[1].rsplit('?')[0].split() for l in que_file]
# que data structure
# [
#   ['what', 'is', ...],
#   ['how', 'many', ...],
#   ...]
# ]

dic_file = open("./dataset/word_dictionary.txt")
dic_array = [l.split() for l in dic_file]
# dic_array data structure
# [
#   ['word', '0']
# ]
class smart_dict(dict):
    def __missing__(self, key):
        return [6]
    def hasClass(self, key, cla):
        for x in self[key]:
            if x == cla:
                return true
        return false

dic = smart_dict()    # Look-up convenience
for x in dic_array:
    if x[0] not in dic:
        dic[x[0]] = [int(x[1])]
    else:
        dic[x[0]].append(int(x[1]))

def isArt(x):
    return dic[x][0] == 4

def getNoun(sen, loc):
    if dic.hasClass(sen[loc], 3):
        return getNoun(sen, loc + 1)
    if len(sen) > loc + 1:
        if dic.hasKey(sen[loc + 1], 3):
            if sen[loc + 1] != 'of':
                return sen[loc]
            else:
                if len(sen) > loc + 2:
                    return getNoun(sen, loc + 2)
                else:
                    return getNoun(sen,loc)
        else:
            return getNoun(sen, loc + 1)
    else:
        return sen[loc]


#qtag = []
#for m in que:
    #i = []
    #for n in m:
        #i.append([dic[n]])
    #qtag.append(i)

ret = []
miss = 0
for i in range(len(que)):
    #########
    # 1. Answer type
    #########
    count = 0
    r = []
    # Define rules
    sen = que[i]

    # 1. <Which | What | How many | How much> + <N | N of N>
    if (sen[0] == 'Which' or sen[0] == 'What') and dic[sen[1]] == '3':
        if sen[2] == 'of':
            r.append(sen[0])
            r.append(sen[4] if isArt(sen[3]) else sen[3])
        else:
            r.append(sen[0])
            r.append(sen[1])
        count += 2
    elif (sen[0] == 'How' and sen[1] == 'many') or (sen[0] == 'How' and sen[1] == 'much'):
        if len(sen) < 4:
            r.append(sen[0])
            r.append(sen[2])
        else:
            if sen[3] == 'of':
                r.append(sen[0])
                r.append(sen[5] if isArt(sen[4]) else sen[4])
            else:
                r.append(sen[0])
                r.append(sen[2])
        count += 2

    # 2. <5W1H> + <be-V> + <N | N of N >
    if (sen[0] == 'Which' or sen[0] == 'What' or sen[0] == 'Who' or sen[0] == 'Where' or sen[0] == 'Why' or sen[0] == 'How') and dic[sen[1]] == '5':
        r.append(sen[0])
        if isArt(sen[2]):
            if len(sen) < 5:
                if len(sen) < 4:
                    r.append(sen[2])
                else:
                    r.append(sen[3])
            else:
                if sen[4] == 'of':
                    if len(sen) < 5:
                        r.append(sen [6] if isArt(sen[5]) else sen[5])
                    else:
                        r.append(sen[3])
                else:
                    r.append(sen[3])
        else:
            r.append(sen[2])
        count += 2
    # 3. <How> + <adj> + <be-V> + <N>
    if (sen[0] == 'How') and (dic[sen[1]] == '0') and (dic[sen[2]] == '5'):
        r.append(sen[0])
        r.append(sen[3])
        count += 2

    if len(r) != 2:
        #pdb.set_trace()
        miss += 1
        miss_file.write(' '.join(sen))
        miss_file.write('\n')

# To get the missing count
print(miss)
