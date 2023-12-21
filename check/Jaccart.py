import Levenshtein
from backend import EventType, Event

def By_bar(elem):
    return elem[1]

def Jaccart(true_event, predict_event):
    chords_true = []
    num_of_chord = []
    for i in range(0, len(true_event)):
        v = true_event[i]
        if v.content == "N":
            continue
        chords_true.append(v)
        key = 1
        for i in num_of_chord:
            if i == v.content:
                key = 0
                break
        if key:
            num_of_chord.append(v.content)
    chords_predict = []
    for i in range(0, len(predict_event)):
        v = predict_event[i]
        if v.content == "N":
            continue
        chords_predict.append(v)
        key = 1
        for i in num_of_chord:
            if i == v.content:
                key = 0
                break
        if key:
            num_of_chord.append(v.content)
    num_of_chord.append("N")
    list_of_point = []
    pr_finish = 0
    for chord in chords_true:
        list_of_point.append([1, pr_finish, len(num_of_chord) - 1])
        list_of_point.append([0, chord.start, len(num_of_chord) - 1])
        left_bar = chord.start
        right_bar = chord.end
        num = 0
        for i in range(0, len(num_of_chord)):
            if num_of_chord[i] == chord.content:
                num = i
                break
        list_of_point.append([1, left_bar, num])
        list_of_point.append([0, right_bar, num])
        pr_finish = chord.end
    pr_finish = 0
    for chord in chords_predict :
        list_of_point.append([1, pr_finish, len(num_of_chord) - 1])
        list_of_point.append([0, chord.start, len(num_of_chord) - 1])
        left_bar = chord.start
        right_bar = chord.end
        num = 0
        for i in range(0, len(num_of_chord)):
            if num_of_chord[i] == chord.content:
                num = i
                break
        list_of_point.append([1, left_bar, num])
        list_of_point.append([0, right_bar, num])
        pr_finish = chord.end
    cnt = 0
    last_left = []
    cnt_of_left = []
    list_of_point.sort(key=By_bar)
    for i in range(1, len(list_of_point)):
        if list_of_point[i - 1][1] == list_of_point[i][1] and list_of_point[i][0] == 1:
            list_of_point[i], list_of_point[i - 1] = list_of_point[i - 1], list_of_point[i]
    # for i in list_of_point :
    #     print(i[0], i[1], i[2])
    # print()
    for i in range(0, len(num_of_chord)):
        last_left.append(0)
        cnt_of_left.append(0)
    maximum = 0
    result = 0
    for i in range(0, len(list_of_point)):
        if cnt >= 1 :
            maximum += list_of_point[i][1] - list_of_point[i - 1][1]
        if list_of_point[i][0] == 1:
            cnt += 1
            last_left[list_of_point[i][2]] = list_of_point[i][1]
            cnt_of_left[list_of_point[i][2]] += 1
        else :
            cnt -= 1
            if cnt_of_left[list_of_point[i][2]] > 1:
                # print(list_of_point[i][1], last_left[list_of_point[i][2]])
                result += list_of_point[i][1] - last_left[list_of_point[i][2]]
            cnt_of_left[list_of_point[i][2]] -= 1
    # print(result, maximum)
    return result / maximum

# size_of_true = int(input())
# chords_true = []
# for i in range(0, size_of_true) :
#     info = input().split()
#     v = Event(0, 0, EventType(1), "")
#     v.start = float(info[0])
#     v.end = float(info[1])
#     v.type = int(info[2])
#     v.content = info[3]
#     chords_true.append(v)
# size_of_predict = int(input())
# chords_predict = []
# for i in range(0, size_of_predict) :
#     info = input().split()
#     v = Event(0, 0, EventType(1), "")
#     v.start = float(info[0])
#     v.end = float(info[1])
#     v.type = int(info[2])
#     v.content = info[3]
#     chords_predict.append(v)
# # print(chords_true[0].start, chords_true[0].end, chords_true[0].type, chords_true[0].content)
# # print(chords_predict[0].start, chords_predict[0].end, chords_predict[0].type, chords_predict[0].content)
# print(Jaccart(chords_true, chords_predict))
