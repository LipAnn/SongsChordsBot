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

    def format(self, chords, text) -> str:
        events: list[Event] = []
        for chord in chords:
            content = chord[2][:-4]
            if chord[2].endswith("min"):
                content += "m"
            events.append(Event(start=chord[0], end=chord[1], type=EventType.chord, content=content))

        for seg in text["segments"]:
            events.append(Event(start=seg["start"], end=seg["end"], type=EventType.phrase, content=seg["text"]))
                    
        events.sort(key=attrgetter("start"))

        return json.dumps(events, indent=4, default=lambda o: asdict(o))
