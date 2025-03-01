# convert int to string
def int_to_str(n: int) -> str:

    s = []
    while n > 0:
        s.append(str(n % 10))
        n = n // 10

    return ''.join(reversed(s))


def str_to_int(s: str) -> int:

    n = 0
    for c in s:
        n = 10 * n + int(c)

    return n


def reverse_str(s: str) -> str:
    s_l = list(s)
    for i in range(len(s_l) // 2):
        tmp = s_l[i]
        s_l[i] = s[len(s_l) - 1 - i]
        s_l[len(s_l) - 1 - i] = tmp

    return ''.join(s_l)


class Track:
    def __init__(self, name: str, tags: set, disk_location: str):
        self.name = name
        self.tags = tags
        self.disk_location = disk_location


def filter_tracks_by_tag(filter_tags: set, tracks: list) -> list:
    return [track for track in tracks if len(track.tags.intersection(filter_tags)) > 0]


# track1 = Track("1", {"jazz"}, disk_location="")
#
# ft = filter_tracks_by_tag({"jazz1"}, [track1])
# print(len(ft))

from numpy import random

x = random.normal(loc=0, scale=1, size=(1, 128))

print(x)
