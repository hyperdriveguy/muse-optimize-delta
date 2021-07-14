import concurrent.futures

from util_funcs import calc_song_size
from callchannel import optimize_callchannel
from loopchannel import optimize_loopchannel
from other_compression import convert_loopchannel, remove_stereopanning


def call_then_loop_optimize(song):
    call_optimize = optimize_callchannel(song)
    loop_optimize = optimize_loopchannel(call_optimize)
    return loop_optimize


def loop_then_call_optimize(song):
    loop_optimize = optimize_loopchannel(song)
    call_optimize = optimize_callchannel(loop_optimize)
    return call_optimize


def run_optimization_passes(song, no_panning=False):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_og_song_size = executor.submit(calc_song_size, song)
        song_cleaned = convert_loopchannel(song)
        if no_panning:
            song_cleaned = remove_stereopanning(song_cleaned)
        future_call_first = executor.submit(call_then_loop_optimize, song_cleaned)
        future_loop_first = executor.submit(loop_then_call_optimize, song_cleaned)
        song_call_first = future_call_first.result()
        song_loop_first = future_loop_first.result()
        future_call_first_size = executor.submit(calc_song_size, song_call_first)
        future_loop_first_size = executor.submit(calc_song_size, song_loop_first)
        og_song_size = future_og_song_size.result()
        song_call_first_size = future_call_first_size.result()
        song_loop_first_size = future_loop_first_size.result()
        if song_call_first_size < song_loop_first_size:
            return (song_call_first, og_song_size, song_call_first_size)
        return (song_loop_first, og_song_size, song_loop_first_size)
        
