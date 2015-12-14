#ifndef DATA_HEADER
#define DATA_HEADER

#include "dataset.h"
#define <bitset>

#define word_noun 0
#define word_verb 1
#define word_adjective 2
#define word_adverb 3
#define word_ques_word 4

class question{
public:
    string subject;
    string subject2;
    bitset<5> ans_type;
};

#endif
