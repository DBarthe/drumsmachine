from . import state


def _validate_track_name(track_name: str):
    if track_name not in track_name:
        raise Exception("track {} does not exists".format(track_name))


def _validate_cursor(cursor: int):
    if cursor < 0 or cursor >= state.cycle_size:
        raise Exception("cursor {} is out of bound".format(cursor))


def get_track(track_name: str):
    _validate_track_name(track_name)
    return state.tracks[track_name]


def list_tracks():
    return state.tracks_order


def set_note(track_name: str, cursor: int, value: bool):
    _validate_track_name(track_name)
    _validate_cursor(cursor)
    state.tracks[track_name][cursor] = value


def toogle_note(track_name: str, cursor: int):
    _validate_track_name(track_name)
    _validate_cursor(cursor)
    state.tracks[track_name][cursor] = not state.tracks[track_name][cursor]


def set_tempo(tempo: int):
    state.tempo = tempo


def increase_tempo(gap: int):
    state.tempo = state.tempo + gap
