import re

def count_word(content, n):
    words = re.findall(r"\w+", content.casefold())
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0)+1

    word_count = sorted(word_count.items(), key= lambda items: items[1], reverse=True)
    # print(f"Top words: {word_count[:n]}")

    return word_count[:n]