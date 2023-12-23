import os
import sys
from check import jaccart, levenshtein
from backend import Backend, Formatter


def str_to_float(s):
    if s.count('.') == 2:
        a, b, c = map(str, s.split('.'))
        return int(a) * 60 + float(b + '.' + c)
    return float(s)

def get_model_quality():
    directory = "songs/"
    files = os.listdir(directory)
    files.sort()
    chords = []
    songs = []
    texts = []
    res = ''
    for f in files:
        if 'song' in f:
            songs.append(f)
        elif 'text' in f:
            texts.append(f)
        elif 'chord' in f:
            chords.append(f)
    back = Backend()
    formatter = Formatter()
    for i in range(len(chords)):
        lst_chords = []
        for s in open(directory+chords[i]):
            content, start, end = map(str, s.split())
            start = str_to_float(start)
            end = str_to_float(end)
            lst_chords.append((start, end, content))
        #print(*lst_chords, sep = '\n')
        pred = back.query_quality(audio=directory+songs[i])
        #print(*pred, sep = '\n')
        res += songs[i] + "\nОценка по метрике Jaccart: " + str(jaccart(formatter.parse_raw(lst_chords, []), pred)) + \
            "\nОценка по метрике Levenstein: " + str(levenshtein(formatter.parse_raw(lst_chords, []), pred)) + "\n\n"
    #print(songs)
    #print(chords)
    return res