import sys
import numpy as np
import math
import re

file = sys.argv[1]
init = 1
utterances = []
utterances.append([])

with open(file, "r") as f:
    for idx, line in enumerate(f.readlines()[1:]):
        stripped = line.replace('\n', '').split('\t')
        #print(stripped)
        try:
            if int(stripped[1]) != init: 
                utterances.append([])
                init = int(stripped[1])
            utterances[init-1].append((stripped[3], stripped[8], stripped[9]))
        except IndexError:
            # this is only here to check the last row which denotes the number of rows
            pass

utterances_length = len(utterances)
summarized = []
cs_total = 0
mult_cs = 0
accounted = False
sum = 0
for idx1, utterance in enumerate(utterances):
    code_switch = False
    lang = "" 
    speaker = utterance[0][1]
    for idx2, word in enumerate(utterance):
        if idx2 == 0:
            lang = word[2]
        else:
            if lang == "eng&spa" and word[2] != "eng&spa" and word[2] != "999":
                lang = word[2]
            if lang != word[2] and word[2] != "eng&spa" and lang != "eng&spa" and word[2] != "999":
                if code_switch and not accounted:
                    mult_cs += 1
                    accounted = True
                else:
                    code_switch = True
                cs_total += 1
    summarized.append((code_switch, lang, speaker, idx1, 0))
    sum += len(utterance) - 1 # accounting for ever-prevalent ending punctuation
avg_utterance_length = sum / utterances_length

#TODO: melting + sentence parsing

# melt it -> melt out z axis, add a new feature which is the index of the z axis
# allows you to check whether if the preceding utterance of a speaker was a code-switch or it
# or if you had a code-switch from the same speaker in the second to last utterance 
# find distance to most recent code-switch to yourself vs not yourself 
# apply cognatal priming to the set of features later as well 

# later on -> maybe also try to find a way to split by sentence using a sentence tokenizer
# ie first collapsing into utterance cluster and then using the sentence tokenizer on it

#collapses summarizes by same person in a row into one list
i = 0
prev = summarized[0][2]
for idx, line in enumerate(summarized[1:]):
    if line[2] != prev:
        prev = line[2]
        i += 1
    list_line = list(line)
    list_line[4] = i
    summarized[idx+1] = tuple(list_line)

# check to see self-priming from close-by utterances 

self_priming = 0
outside_priming = 0

codeswitched = []
cs_in_collapsed = 0

'''
for collapse in collapsed:
    occurences = 0
    for line in collapse:
        if line[0] == True:
            occurences += 1
    if occurences > 1:
        self_priming += 1
    codeswitched.append((occurences > 0))
    if occurences > 0:
        cs_in_collapsed += 1 
'''

print(summarized)

for idx, codeswitch in enumerate(codeswitched[1:]):
    if codeswitched[idx] == True and codeswitch:
        outside_priming += 1

print(cs_in_collapsed)
print(outside_priming)
print(self_priming)
print(cs_total)
print(mult_cs)

'''
print(utterance[0])
print(len(utterances))
print(avg_utterance_length)
'''
