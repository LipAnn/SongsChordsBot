import Levenshtein
from backend import EventType, Event

def levenshtein(true_event, predict_event):
    table_of_true = []
    table_of_predict = []
    num_of_chord = []
    mx_bar = 0
    delta = 0.01
    key = 1
    for i in range(0, len(true_event)):
        for j in num_of_chord:
            if j == true_event[i].content:
                key = 0
                break
        if key:
            num_of_chord.append(true_event[i].content)
    for i in range(0, len(predict_event)):
        for j in num_of_chord :
            if j == predict_event[i].content:
                key = 0
                break
        if key:
            num_of_chord.append(predict_event[i].content)
    for chord in true_event:
        left_bar = int(float(chord.start) / delta)
        right_bar = int(float(chord.end) / delta)
        mx_bar = max(mx_bar, right_bar)
        while len(table_of_true) < mx_bar + 1:
            table_of_true.append(' ')
            table_of_predict.append(' ')
        num = 0
        for i in range(0, len(num_of_chord)):
            if num_of_chord[i] == chord.content:
                num = i
                break
        for i in range(left_bar, right_bar + 1):
            table_of_true[i] = num
    for chord in predict_event:
        left_bar = int(float(chord.start) / delta)
        right_bar = int(float(chord.end) / delta)
        mx_bar = max(mx_bar, right_bar)
        while len(table_of_predict) < mx_bar + 1:
            table_of_true.append(' ')
            table_of_predict.append(' ')
        num = 0
        for i in range(0, len(num_of_chord)):
            if num_of_chord[i] == chord.content:
                num = i
                break
        for i in range(left_bar, right_bar + 1):
            table_of_predict[i] = num
    return 1 - Levenshtein.distance(table_of_true, table_of_predict) / 1.0 / mx_bar
