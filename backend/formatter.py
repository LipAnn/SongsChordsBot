from dataclasses import dataclass, asdict
import enum
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
        chord_events: list[Event] = []
        text_events: list[Event] = []

        for chord in chords:
            content = chord[2]
            if ":" in chord[2]:
                content = chord[2][:-4]
            if chord[2].endswith("min"):
                content += "m"
            chord_events.append(Event(start=chord[0], end=chord[1], type=EventType.chord, content=content))

        for seg in list(text):
            if seg.words is None:
                text_events.append(Event(start=seg.start, end=seg.end, type=EventType.phrase, content=seg.text))
            else:
                text_events.append(Event(start=seg.end, end=seg.end, type=EventType.newline, content=""))

            for word in (seg.words or []):
                text_events.append(Event(start=word.start, end=word.end, type=EventType.phrase, content=word.word))
                    
        text_events.sort(key=lambda x: (x.start, x.end))
        current_len = len(text_events)
        for i in range(current_len):
            if i == 0:
                # Add empty word before beginning text
                if text_events[i].start > 0:
                    text_events.append(Event(start=0, end=text_events[i].start, type=EventType.newline, content=""))
            elif i == current_len - 1:
                # Add empty word after text
                text_events.append(Event(start=text_events[i].end, end=100500, type=EventType.newline, content=""))
            else:
                if abs(text_events[i + 1].start - text_events[i].end) > 1e-3:
                    text_events.append(Event(start=text_events[i].end, end=text_events[i + 1].start, type=EventType.newline, content=""))
            
        events = chord_events + text_events
        events.sort(key=lambda x: (x.start, x.end))

        return events

    def make_bold(self, s):
        return s

    def events_to_str(self, events: list[Event]) -> str:
        UNDEF = 10000
        result = ''
        chords = ''
        text = ''
        last_phrase = Event(
            start=0,
            end=UNDEF,
            type=EventType.phrase, 
            content=''
        )

        events = list(sorted(events, key=lambda x: (x.start if x.type != EventType.newline else x.end - 1e-7, x.type, x.start)))

        for event in events:
            if event.type == EventType.newline:
                result += self.make_bold(chords) + '\n' + text + '\n'
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
                text = text.ljust(len(chords))
                chords = chords.ljust(len(text) + 1)
                text += event.content
                last_phrase = event
             
        return result

    def format(self, chords, text, use_word_timestamps: bool) -> str:
        events = self.parse_raw(chords, text)
        # if use_word_timestamps:
        #     return json.dumps(events, ensure_ascii=False, indent=4, default=lambda o: asdict(o))
        return self.events_to_str(events)
