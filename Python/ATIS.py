import os
import sys
import re
import string
import subprocess

os.chdir("c:/Users/user/GitHub/hse_CNTK/Python")

vocabulary = {}
tags = {}
types = {}

with open("./atis.all.ctf") as file:
    for line in file:
        index = int(re.search("S0 [0-9]{1,3}:", line).group()[3:-1])
        word = re.search("S0 [0-9]{1,3}:1 \|# [\w']+", line).group()
        word = re.search("# [\w']+", word).group()[2:]
        vocabulary[word] = index

        type_index = re.search("S1 [0-9]{1,2}:", line)
        type_name = re.search("S1 [0-9]{1,2}:1 \|# \w+", line)
        if type_index is not None:
            type_index = type_index.group()[3:-1]
            type_name = re.search("# \w+", type_name.group()).group()[2:]
            types[type_index] = type_name

        tag_index = re.search("S2 [0-9]{1,3}:", line).group()[3:-1]
        tag_name = re.search("S2 [0-9]{1,3}:1 \|# [\w\-\._]+", line)
        tag_name = re.search("# [\w\-\._]+", tag_name.group()).group()[2:]
        tags[tag_index] = tag_name



tmp = ""
sentence = sys.stdin.readline()
for char in sentence:
    if char.isalnum() or char in string.whitespace or char in "'":
        tmp += char
sentence = tmp.lower().split()
unknown_words = []

with open("./pyInput.ctf", "w") as file:
    file.write("0	|S0 178:1 |# BOS\n")
    for word in sentence:
        if word in vocabulary.keys():
            file.write("0	|S0 " + str(vocabulary[word]) + ":1 |# " + word + "\n")
            unknown_words += [False]
        else:
            unknown_words += [True]
    file.write("0	|S0 179:1 |# EOS\n")

subprocess.run("c:/Users/user/CNTK-1-7-2-Windows-64bit-CPU-Only/cntk/cntk/CNTK.exe"
               " configFile=./pyConfig.cntk", stderr=subprocess.DEVNULL)

with open("pyOutputSentenceTags.ctf.outputs") as file:
    line = file.readline()

line = [int(float(x)) for x in line.split()]
type_index = line.index(1)

word_tags = []

with open("pyOutputWordTags.ctf.outputs") as file:
    file.readline()
    for unknown in unknown_words:
        if unknown:
            word_tags += ["O"]
        else:
            line = file.readline()
            line = [int(float(x)) for x in line.split()]
            word_tag_index = line.index(1)
            word_tags += [tags[str(word_tag_index)]]

print("This sentence is about " + types[str(type_index)] + ".")

i = 0
print("{0:<20}{1:<20}".format("Word: ", "Tag:"))
for word in sentence:
    print("{0:<20}{1:<20}".format(word, word_tags[i]))
    i += 1
