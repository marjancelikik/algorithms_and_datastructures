def compress(s: str) -> str:
    uniq = []
    counts = []
    for i in range(len(s)):
        if i == 0 or s[i-1] != s[i]:
            uniq.append(s[i])
            counts.append(1)
        elif s[i-1] == s[i]:
            counts[len(uniq) - 1] += 1

    assert len(counts) == len(uniq)
    compressed = []
    for ch, count in zip(uniq, counts):
        compressed.append(ch)
        compressed.append(str(count))

    return ''.join(compressed)


print(compress("aabcccccaaa"))
