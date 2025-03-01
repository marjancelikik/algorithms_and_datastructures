def one_edit(s1: str, s2: str) -> bool:
    return is_replace_char(s1, s2) or is_delete_char(s1, s2) or is_delete_char(s2, s1)


def is_replace_char(s1, s2):
    for i in range(len(s1)):
        for c in range(ord('a'), ord('z') + 1):
            rep = replace_char(s1, i, chr(c))
            if rep == s2:
                return True
    return False


def is_delete_char(s1, s2):
    for i in range(len(s1)):
        if delete_char(s1, i) == s2:
            return True
    return False


def replace_char(s: str, i, c):
    s_new = list(s)
    s_new[i] = c
    return ''.join(s_new)


def delete_char(s: str, i):
    return s[0:i] + s[i+1:]


print(one_edit("pale", "ple"))
print(one_edit("pales", "pale"))
print(one_edit("pale", "bale"))
print(one_edit("pale", "bake"))

