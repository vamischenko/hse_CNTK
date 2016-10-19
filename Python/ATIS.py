import os
import sys
import re
import string
import subprocess

os.chdir("c:/Users/user/CNTK-1-7-2-Windows-64bit-CPU-Only/cntk/Examples/CNTK_HandsOn_KDD2016/SLUHandsOn")

vocabulary = {}
types = {}

for file_name in ["./atis.train.ctf", "./atis.test.ctf"]:
    with open(file_name) as file:
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



tmp = ""
sentence = sys.stdin.readline()
for char in sentence:
    if char.isalnum() or char in string.whitespace or char in "'":
        tmp += char
sentence = tmp.lower().split()

with open("./pyInput.ctf", "w") as file:
    file.write("0	|S0 178:1 |# BOS\n")
    for word in sentence:
        if word in vocabulary.keys():
            file.write("0	|S0 " + str(vocabulary[word]) + ":1 |# " + word + "\n")
    file.write("0	|S0 179:1 |# EOS\n")

subprocess.run("c:/Users/user/CNTK-1-7-2-Windows-64bit-CPU-Only/cntk/cntk/CNTK.exe"
               " configFile=./pyConfig.cntk")

with open("pyOutput.ctf.outputs") as file:
    line = file.readline()

line = [int(float(x)) for x in line.split()]
type_index = line.index(1)
print("This sentence is about " + types[str(type_index)] + ".")