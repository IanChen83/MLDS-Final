adj_file = "dataset/dictionary/adj.exc"
adj2_file = "dataset/dictionary/data.adj"

adv_file = "dataset/dictionary/adv.exc"
adv2_file = "dataset/dictionary/data.adv"

verb_file = "dataset/dictionary/verb.exc"
verb2_file = "dataset/dictionary/data.verb"

noun_file = "dataset/dictionary/noun.exc"
noun2_file = "dataset/dictionary/data.noun"

dic_file = "output.dict"
try:
    adj = open(adj_file, 'r')
    adj2 = open(adj2_file, 'r')

    adv = open(adv_file, 'r')
    adv2 = open(adv2_file, 'r')

    verb = open(verb_file, 'r')
    verb2 = open(verb2_file, 'r')

    noun = open(noun_file, 'r')
    noun2 = open(noun2_file, 'r')

    out = open(dic_file, 'w');
except IOError as e:
    print(e)
    exit()
dic = dict()

# adj:  0
# adv:  1
# verb: 2
# noun: 3

def output(f, f2, name, out_file):
    dic = dict()
    counter = 0
    for line in f:
        a = line.split()
        if a[0] not in dic:
            counter += 1
            dic[a[0]] = 0
        if a[1] not in dic:
            counter += 1
            dic[a[1]] = 0
    print("{0}2: {1}\n".format(name, counter))
    counter = 0
    for line in f2:
        a = line.split()
        if a[4] not in dic:
            counter += 1
            dic[a[4]] = 0
    print("{0}: {1}\n".format(name, counter))
    for i in dic:
        out_file.write("{0} {1}\n".format(i, dic[i]))

output(adj, adj2, "adj", out)
output(noun, noun2, "noun", out)
output(adv, adv2, "adv", out)
output(verb, verb2, "verb", out)

# In out_file:
#   <word> <label> in each line
# label:
#
# adj:  0
# adv:  1
# verb: 2
# noun: 3
#

