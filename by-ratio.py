import re


capitals = re.compile('.*[A-Z]')

def parse_line(line):
    if line[0] == "#":
        return {
            "is_comment": True
        }
    chunks, first, second = line.split()
    return {
        "chunks": int(chunks),
        "length": len(first),
        "ratio": int(chunks)/len(first),
        "words": [first, second]
    }

def is_boring(pair):
    if pair.get("is_comment", False):
        return True
    if capitals.match(" ".join(pair["words"])):
        return True
    if pair["ratio"] == 1:
        return True
    return False

def print_pairs(pairs):
    print("# these are sorted by ratio of minimum anagram chunks to length, highest ratio first\n"
          "# ratios are given as integer percentages, for more precise numbers see rescore-difference.txt")
    for pair in pairs:
        print(pair["chunks"], int(pair["ratio"]*100), pair["words"][0], pair["words"][1])

def print_rescore_difference(pairs):
    ratios_by_score = {}
    for pair in pairs:
        key = pair["chunks"]
        ratio = pair["ratio"]
        if key not in ratios_by_score:
            ratios_by_score[key] = {}
        ratios_by_score[key][ratio] = ratios_by_score[key].get(ratio, 0) + 1
    print("# this is the amount of variation in chunks:length ratio for each chunk count (original score)\n"
          "# each group lists a count for each ratio among anagrams with that chunk score")
    for chunks, ratios in {k:v for k, v in ratios_by_score.items() if len(v) > 1}.items():
        print(chunks, "chunks")
        for ratio, count in ratios.items():
            print(f"  {count}: {ratio}")

def main():
    with open('anagrams-scored.txt') as f:
        lines = f.readlines()
    pairs = [pair for pair in map(lambda line: parse_line(line), lines) if not is_boring(pair)]
    pairs.sort(key=lambda pair: pair["ratio"], reverse=True)
    print_pairs(pairs)
    # print_rescore_difference(pairs)

if __name__ == "__main__":
    main()