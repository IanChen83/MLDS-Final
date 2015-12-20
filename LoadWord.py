############## LoadWord.py ############
# Usage:
#   Read all dictionary files and blacklist files and patch file
#   and write the dictionary to output for further word selection
#
# Data Format:
#   # dictionary file and dictionary file 2:
#       Open those file for more information
#
#   # blacklist file:
#       In the file are multiple ilne, each line being a word that
#       shouldn't be writed to output dictionary.
#   # Patch file:
#       Example shown below:
#       #######################
#       #the 4
#       #a 4
#       #an 4
#       #######################
#
#   If we want to change the class of some words, we should
#       1. Add these words into blacklist files
#       2. Add these words into patch file with correct class

adj_file = "dataset/dictionary/adj.exc"
adj2_file = "dataset/dictionary/data.adj"

adv_file = "dataset/dictionary/adv.exc"
adv2_file = "dataset/dictionary/data.adv"

verb_file = "dataset/dictionary/verb.exc"
verb2_file = "dataset/dictionary/data.verb"

noun_file = "dataset/dictionary/noun.exc"
noun2_file = "dataset/dictionary/data.noun"

blacklist_file = "dataset/dictionary/blacklist.exc"
patch_add_file = "dataset/dictionary/patch.exc"

dic_file = "dataset/word_dictionary.txt"
try:
    adj = open(adj_file, 'r')
    adj2 = open(adj2_file, 'r')

    adv = open(adv_file, 'r')
    adv2 = open(adv2_file, 'r')

    verb = open(verb_file, 'r')
    verb2 = open(verb2_file, 'r')

    noun = open(noun_file, 'r')
    noun2 = open(noun2_file, 'r')

    _blacklist = open(blacklist_file, 'r')

    patch_add = open(patch_add_file, 'r')

    out = open(dic_file, 'w');
except IOError as e:
    print(e)
    exit()
dic = dict()

# adj:  0
# adv:  1
# verb: 2
# noun: 3

blacklist = []
patch = []

def add_blacklist(l, f):
    for line in f:
        l.append(line.rstrip())
    print("Block {0} words".format(len(l)))

def output(f, f2, name, out_file, num):
    dic = dict()
    counter = 0
    for line in f:
        a = [x.lower() for x in line.split()]
        if a[0] not in dic:
            counter += 1
            dic[a[0]] = num
        if a[1] not in dic:
            counter += 1
            dic[a[1]] = num
    print("{0}: {1}".format(name, counter))
    counter = 0
    for line in f2:
        a = [x.lower() for x in line.split()]
        if a[4] not in dic:
            counter += 1
            dic[a[4]] = num
    print("{0}2: {1}".format(name, counter))
    for i in blacklist:
        if i in dic:
            del dic[i]
    for i in dic:
        out_file.write("{0} {1}\n".format(i, dic[i]))
add_blacklist(blacklist, _blacklist)
output(adj, adj2, "adj", out, 0)
output(noun, noun2, "noun", out, 3)
output(adv, adv2, "adv", out, 1)
output(verb, verb2, "verb", out, 2)

# Patching
patch = [line.rsplit() for line in patch_add]
for a in patch:
    out.write("{0} {1}\n".format(a[0], a[1]))
print("Patch {0} words".format(len(patch)))
# In out_file:
#   <word> <label> in each line
# label:
#
# adj:  0
# adv:  1
# verb: 2
# noun: 3
#

