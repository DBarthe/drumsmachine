import clockblocks
import time

from pythonosc import udp_client, osc_bundle_builder, osc_message_builder
from . import state

client = udp_client.SimpleUDPClient("127.0.0.1", 57120)


def run_one_iteration(cursor):
    messages = []

    for (name, track) in state.tracks.items():
        if track[cursor]:
            messages.append(osc_message_builder.OscMessageBuilder(address=name).build())

    if len(messages) > 0:
        bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
        for msg in messages:
            bundle.add_content(msg)
        client.send(bundle.build())


def start():
    clock = clockblocks.Clock(initial_tempo=state.tempo)
    start = time.time()
    while True:
        clock.tempo = state.tempo
        cursor = int((clock.beats() * 4) % 16)
        #  print("Current time: {}, breat: {}, tempo: {}, cursor:{}".format(round(time.time() - start, 4),
        # clock.beats(), state.tempo, cursor))
        run_one_iteration(cursor)
        clock.wait(1 / 4)
