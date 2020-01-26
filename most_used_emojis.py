# Import necessary libraries
import pandas as pd
from functools import reduce
from collections import Counter
from tabulate import tabulate
from PIL import Image, ImageDraw, ImageFont
import regex, operator, sys

# Data path
args = sys.argv
if len(args) == 1:
    print("Specify the path to CSV file")
    exit(1)

file_path = args[1]

# Load data and show first five rows
data = pd.read_csv(file_path)

# Most used emojis

def most_used_emojis(member):
    emojis_list_of_list = data.loc[
        (data["sender"] == member) & (data["is_forwarded"] == 0)
    ]["text_emojis"].dropna().apply(lambda x: regex.findall(r"\X", x)).tolist()

    if(len(emojis_list_of_list) > 0):
        emojis_list = reduce(operator.concat, emojis_list_of_list)
        emojis_count = len(emojis_list)
        most_common = Counter(emojis_list).most_common(10)
        emojis = ''.join(list(zip(*most_common))[0])
        return [emojis_count, member, emojis]
    else:
        return [0, ""]

members = list(pd.unique(data["sender"].ravel("K")))

emojis = []
for member in members:
    emojis.append(most_used_emojis(member))

reports = [x for x in sorted(emojis, key=lambda x: x[0], reverse=True) if x[0] > 0]
mcl = len(str(reports[0][0])) # most count length
emoji_members = (list(list(zip(*reports))[1]))
lnl = len(max(emoji_members, key=len)) # longest name length

print(tabulate(reports, headers=["count", "name", "most used emojis"]))
