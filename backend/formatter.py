from dataclasses import dataclass, asdict
import enum
from operator import attrgetter
import json


class EventType(enum.IntEnum):
    chord = 1
    phrase = 2


@dataclass(slots=True)
class Event:
    start: int
    end: int
    type: EventType
    content: str


class Formatter:
    def __init__(self) -> None:
        ...

    def parse_raw(self, chords, text) -> list[Event]:
        events: list[Event] = []
        for chord in chords:
            content = chord[2][:-4]
            if chord[2].endswith("min"):
                content += "m"
            events.append(Event(start=chord[0], end=chord[1], type=EventType.chord, content=content))

        for seg in text["segments"]:
            events.append(Event(start=seg["start"], end=seg["end"], type=EventType.phrase, content=seg["text"]))
                    
        events.sort(key=attrgetter("end"))

        return events

    def events_to_str(self, events: list[Event]) -> str:
        '''
        Аккорды расставляются над соответствующей им строкой.
        Считаем примерное время длительности одного символа текста 
        и этот коэффициент умножаем на длительность каждого аккорда
        '''
        full_time = 0
        sum_symbols = 0
        for el in events:
            if el.type == EventType.phrase:
                sum_symbols += len(el.content)
                full_time += el.end - el.start
        space = max(sum_symbols // full_time, 1)
        queue_chords = []
        result = ""
        last_phrase = None
        events.append(Event(start=events[-1].end + 1, end = start=events[-1].end + 1, type=EventType.chord, content=''))
        for el in events:
            if el.type == EventType.chord:
                if last_phrase:
                    if el.start <= last_phrase.end:
                        result += el.content + '\n' + \
                        last_phrase.content + '\n'
                    else:
                        result += '\n' + last_phrase.content + '\n'
                        queue_chords.append(el)
                    last_phrase = None
                else:
                    queue_chords.append(el)
            else:
                while queue_chords and queue_chords[0].end < el.start:
                    result += queue_chords[0].content + \
                    ' ' * int((queue_chords[0].end - \
                    queue_chords[0].start) * space)
                    queue_chords.pop(0)
                result += '\n'
                while queue_chords:
                    result += queue_chords[0].content + ' ' * int(
                        (queue_chords[0].end - max(queue_chords[0].start, el.start)) * space
                    )
                    queue_chords.pop(0)
                last_phrase = el
        while queue_chords:
            result += queue_chords[0].content + ' '
            queue_chords.pop(0)
        return result

    def format(self, chords, text) -> str:
        events = self.parse_raw(chords, text)
        return self.events_to_str(events) 
