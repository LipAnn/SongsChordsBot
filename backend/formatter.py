from dataclasses import dataclass, asdict
import enum
from operator import attrgetter
import json


class EventType(enum.IntEnum):
    chord = 1
    phrase = 2
    newline = 3

@dataclass(slots=True)
class Event:
    start: float
    end: float
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

        for seg in text:
            if seg.words is None:
                events.append(Event(start=seg.start, end=seg.end, type=EventType.phrase, content=seg.text))
            else:
                events.append(Event(start=seg.start, end=seg.end, type=EventType.newline, content=""))

            for word in seg.words or []:
                events.append(Event(start=word.start, end=word.end, type=EventType.phrase, content=word.word))
                    
        events.sort(key=attrgetter("start"))

        return events

    def make_bold(s):
        return '\033[1m' + s + '\033[0m'

    def events_to_str(self, events: list[Event]) -> str:
        UNDEF = 10000
        events = [Event(
            start=0,
            end=UNDEF,
            type=EventType.phrase, 
            content=''
            )] + events
        result = ''
        chords = ''
        text = ''
        last_phrase = None
        for event in events:
            if event.type == EventType.newline:
                result += make_bold(chords) + '\n' + text + '\n'
                chords = ''
                text = ''
                last_phrase = Event(
                    start=last_phrase.end,
                    end=UNDEF,
                    type=EventType.phrase, 
                    content=''
                )   
            if event.type == EventType.chord:
                chords += event.content + " "
            if event.type == EventType.phrase:
                text.ljust(len(chords))
                chords.ljust(len(text))
                text += event.content
                last_phrase = event
        return result

    def format(self, chords, text, use_word_timestamps: bool) -> str:
        events = self.parse_raw(chords, text)
        if use_word_timestamps:
            return json.dumps(events, ensure_ascii=False, indent=4, default=lambda o: asdict(o))
        return self.events_to_str(events)
