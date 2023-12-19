class Formatter:
    def __init__(self) -> None:
        ...

    def format(self, chords) -> str:
        for i in range(len(chords)):
            chords[i] = list(chords[i])
            chords[i][-1] = chords[i][-1][:-4] + ('m' if chords[i][-1][-3:] == 'min' else '')
        return ...
