# -*- coding: utf-8 -*-
"""

"""

# Exclude those weeks when an exhibition opens because it opens on Saturday
# while the special exhibition is closed on the preceding Thursday & Friday.
# The dates shown are the Monday of a week to skip.
#
# SKIPWEEKS is a list of strings each in the format: yyyy-mm-dd
# SKIPLIST is used to build SKIPWEEKS and contains sub-lists where the first
# entry is the year and the 2nd through nth entries are 2-lists of the month
# and day of the affected weeks.
SKIPLIST = [[2017, [1, 9], [3, 27], [6, 12], [11, 27]],
             [2018, [2, 17], [5, 21], [8,20], [11,19]],
             [2019, [2, 18], [5, 20], [8, 26], [11,17]]
            ]
SKIPWEEKS = []

for yl in SKIPLIST:
    SKIPWEEKS += [f'{yl[0]}-{m[0]:02d}-{m[1]:02d}' for m in yl[1:]]

ADMISSION_TYPES = [
    "Adult",
    "Adult with Gift Aid",
    "Child with Gift Aid",
    "Child, 5 - 18",
    "Concession",
    "Concession with Gift Aid",
    "Family",
    "Family with Gift Aid",
    "Free",
    "Group",
    "Over 65 with Gift Aid",
    "Over 65s",
]

