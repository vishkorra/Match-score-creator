import pandas as pd
import math
import re
from collections import Counter
from difflib import SequenceMatcher

WORD = re.compile(r"\w+")
file = 'test.csv'


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


df = pd.read_csv(file)


scores = []

final_match = []

for i in range(0, len(df)):
    if not isinstance(df.iloc[i]["OriginalCompany"], str) or not isinstance(df.iloc[i]["MasterCompany"], str):
        score = 0
    else:
        comp1 = text_to_vector(df.iloc[i]["OriginalCompany"])
        comp2 = text_to_vector(df.iloc[i]["MasterCompany"])

        score = similar(df.iloc[i]["OriginalCompany"].lower(), df.iloc[i]["MasterCompany"].lower())

    percent_score = format(score*100, ".2f") + "%"
    scores.append(percent_score)

    if score > 0.98:
        final_match.append(df.iloc[i]["MasterCompany"])
    else:
        final_match.append(df.iloc[i]["OriginalCompany"])


df.insert(4, 'new score', scores)
df.insert(5, 'after auto correct', final_match)

df.to_csv("Final_" + file)
