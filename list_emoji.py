import json

with open("emojidata.json", "r") as file:
    d = json.load(file)

names = set()
surrogates = set()

for c in d:
    for i in d[c]:
        if i["names"][0].startswith("regional_indicator_"):
            continue
        names.update(i["names"])
        surrogates.add(i["surrogates"])
        if "diversityChildren" in i:
            for j in i["diversityChildren"]:
                names.update(j["names"])
                surrogates.add(j["surrogates"])

# ugghhhh, i'll just hardcode this since discord is weird about it
# add lone skintone modifiers
surrogates.update([chr(i) for i in range(127995, 128000)])

names = list(names)
surrogates = list(surrogates)
names.sort()
surrogates.sort()

with open("emoji_names.txt", "w") as file:
    file.write("\n".join(names))
with open("emoji_surrogates.txt", "w") as file:
    file.write("\n".join(surrogates))
