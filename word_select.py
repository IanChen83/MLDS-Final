import pdb
import sys
from random import randrange
# adj:  0
# adv:  1
# verb: 2
# noun: 3
# the : 4
# be-V: 5
# other:6

dic_file = open("./dataset/word_dictionary.txt")
dic_array = [l.split() for l in dic_file]
# dic_array data structure
# [
#   ['word', '0']
# ]
class smart_dict(dict):
    def __missing__(self, key):
        if key[0:-1] in self:
            return self[key[0:-1]]
        elif key[0:-2] in self:
            return self[key[0:-2]]
        return [6]
    def hasClass(self, key, cla):
        for x in self[key]:
            if x == cla:
                return True
        return False

dic = smart_dict()    # Look-up convenience
for x in dic_array:
    if x[0] not in dic:
        dic[x[0]] = [int(x[1])]
    else:
        dic[x[0]].append(int(x[1]))

def isArt(x):
    return (4 in dic[x])

def getNoun(sen, loc):
    ##### The grammar of N
    # N ->  N + n
    #   |   the/a + N
    #   |   N + of + N
    #   |   adj + N
    #   |   n
    if len(sen) <= loc:
        return None
    if dic.hasClass(sen[loc], 3):
        if len(sen) > loc + 1:
            if sen[loc + 1] == 'of' and len(sen) > loc + 2: # N of n
                return getNoun(sen, loc + 2)
            elif dic.hasClass(sen[loc + 1], 3):             # N n
                return getNoun(sen, loc+1)
            else:
                return sen[loc]                             # N x
        else:
            return sen[loc]                                 # N
    elif dic.hasClass(sen[loc], 4):                         # the/a N
        if len(sen) < loc + 1:
            return sen[loc]
        else:
            return getNoun(sen, loc + 1)
    elif dic.hasClass(sen[loc], 0):
        if len(sen) >= loc + 1:
            return getNoun(sen, loc + 1)
    else:
        return None

def getAnotherNoun(sen, avoid, r):
    candidate = []
    for w in sen:
        if dic.hasClass(w, 3) == False:
            continue
        a = getNoun(sen, sen.index(w))
        if a in candidate or a == None:
            continue
        else:
            candidate.append(a)
    less_noun_count = 8
    less_noun = None
    for w in candidate:
        if len(dic[w]) < less_noun_count and less_noun != avoid:
            less_noun = w
            less_noun_count = len(dic[w])
    if less_noun != None:
        r.append(less_noun)
    elif avoid != None:
        r.append(avoid)

def getLessVerb(sen, r):
    less_verb_count = 8
    less_verb = None
    for w in reversed(sen):
        if dic.hasClass(w, 2) and len(dic[w]) < less_verb_count:
            less_verb = w
            less_verb_count = len(dic[w])
    if less_verb != None:
        r.append(less_verb)
    

def rule1(sen, r):
    # 1. <Which | What | How many | How much> + <N | N of N>
    if (sen[0] == 'Which' or sen[0] == 'What') and dic.hasClass(sen[1], 3):
        r.append(sen[0])
        r.append(getNoun(sen, 1))
        getAnotherNoun(sen, r[1], r)

    elif (sen[0] == 'How' and sen[1] == 'many') or (sen[0] == 'How' and sen[1] == 'much'):
        if len(sen) < 4:
            r.append(sen[0])
            r.append(sen[2])
            getAnotherNoun(sen, r[1], r)
        else:
            if sen[3] == 'of':
                r.append(sen[0])
                r.append(sen[5] if isArt(sen[4]) else sen[4])
                getAnotherNoun(sen, r[1], r)
            else:
                r.append(sen[0])
                r.append(sen[2])
                getAnotherNoun(sen, r[1], r)
    if len(r) == 3:
        getLessVerb(sen ,r)
#    pdb.set_trace()

def rule2(sen, r):
    # 2. <5W1H> + <be-V> + <N>
    if (sen[0] == 'Which' or sen[0] == 'What' or sen[0] == 'Who' or sen[0] == 'Where' or sen[0] == 'Why' or sen[0] == 'How') and dic.hasClass(sen[1], 5) and getNoun(sen, 2) != None:
        r.append(sen[0])
        r.append(getNoun(sen, 2))
        getAnotherNoun(sen, r[1], r)
        getLessVerb(sen, r)
#    pdb.set_trace()

def rule3(sen, r):
    # 3. <How> + <adj> + <be-V> + <N>
    if sen[0] == 'How' and dic.hasClass(sen[1], 0) and dic.hasClass(sen[2], 5):
        r.append(sen[0])
        r.append(getNoun(sen, 3))
        getAnotherNoun(sen, r[1], r)
        getLessVerb(sen ,r)

def rule4(sen, r):
    # 4. <5W1H> + <aux-V> + <N> + <V>
    if (sen[0] == 'Which' or sen[0] == 'What' or sen[0] == 'Who' or sen[0] == 'Where' or sen[0] == 'Why' or sen[0] == 'How') and dic.hasClass(sen[1], 7) and getNoun(sen, 2) != None:
        r.append(sen[0])
        a = getNoun(sen, 2)
        r.append(a)
        getAnotherNoun(sen, r[1], r)
        idx = sen.index(a)
        if len(sen) > idx + 1:
            r.append(sen[idx+1])
        else:
            getLessVerb(sen, r)

def rule5(sen, r):
    # 5. <5W1H> + <V> + <N>
    if (sen[0] == 'Which' or sen[0] == 'What' or sen[0] == 'Who' or sen[0] == 'Where' or sen[0] == 'Why' or sen[0] == 'How') and dic.hasClass(sen[1], 2) and getNoun(sen, 2) != None:
        r.append(sen[0])
        r.append(getNoun(sen, 2))
        getAnotherNoun(sen, r[1], r)
        r.append(sen[1])

def final_rule(sen, r):
    for w in sen:
        w = w.lower()
        if w == 'which' or w == 'what' or w == 'Who' or w == 'where' or w == 'why' or w == 'how':
            r.append(w)
            break
    less_noun_count = 8
    less_noun = None
    for w in sen:
        if dic.hasClass(w, 3) and len(dic[w]) < less_noun_count:
            less_noun = w
            less_noun_count = len(dic[w])
    if less_noun is not None:
        r.append(less_noun)
        getAnotherNoun(sen, less_noun, r)
    getLessVerb(sen, r)
#for m in que:
    #i = []
    #for n in m:
        #i.append([dic[n]])
    #qtag.append(i)
miss = 0
q_count = 0
def classify(q, write_miss = True, out = None):
    global miss, q_count
    miss_file = None
    if write_miss:
        miss_file = open("miss.txt", 'w')
    for i in range(len(q)):
        q_count += 1
        #########
        # 1. Answer type
        #########
        count = 0
        r = []
        # Define rules
        sen = q[i]

        if len(r) == 0:
            rule1(sen, r)
        if len(r) == 0:
            rule2(sen, r)
        if len(r) == 0:
            rule3(sen, r)
        if len(r) == 0:
            rule4(sen, r)
        if len(r) == 0:
            rule5(sen, r)
        if len(r) == 0:
            final_rule(sen, r)
        for i in range(4-len(r)):
            miss += 1
            r.append(sen[randrange(0, len(sen))].split('\'')[0].lower())
        if len(r) != 4:
            pdb.set_trace()
            if write_miss:
                miss_file.write(' '.join(sen))
                miss_file.write('\n')
        if out is not None:
            out.write("{0} {1} {2} {3}\n".format(r[0], r[1], r[2], r[3]))
if __name__ == '__main__':
    if len(sys.argv) == 1:
        que_file = open("./dataset/pack/question.train")
        next(que_file)

        que = [l.split('\t')[2].split('"')[1].rsplit('?')[0].split() for l in que_file]
        # que data structure
        # [
        #   ['what', 'is', ...],
        #   ['how', 'many', ...],
        #   ...]
        # ]
        
        classify(que)
    else:
        que_file = open("./dataset/pack/question.train")
        next(que_file)

        que = [l.split('\t')[2].split('"')[1].rsplit('?')[0].split() for l in que_file]
        out_file = open(sys.argv[1], 'w')
        classify(que, False, out_file)
# To get the missing count
print("Miss count: {0} questions, miss rate: {1:.10f}".format(miss, float(miss)/float(q_count)))
