import concurrent.futures

from util_funcs import calc_song_size
from callchannel import optimize_callchannel
from loopchannel import optimize_loopchannel
from other_compression import convert_loopchannel, remove_stereopanning


def call_then_loop_optimize(song):
    print('Doing callchannel optimizations...')
    call_optimize = optimize_callchannel(song)
    print('Completed callchannel optimizations!')
    print('Doing loopchannel optimizations...')
    loop_optimize = optimize_loopchannel(call_optimize)
    print('Completed loopchannel optimaztions!')
    return loop_optimize


def loop_then_call_optimize(song):
    print('Doing loopchannel optimizations...')
    loop_optimize = optimize_loopchannel(song)
    print('Completed loopchannel optimaztions!')
    print('Doing callchannel optimizations...')
    call_optimize = optimize_callchannel(loop_optimize)
    print('Completed callchannel optimizations!')
    return call_optimize


def call_then_loop_optimize_inside_call(song):
    print('Doing callchannel optimizations...')
    call_optimize = optimize_callchannel(song)
    print('Completed callchannel optimizations!')
    print('Doing inside call loopchannel optimizations...')
    loop_optimize = optimize_loopchannel(call_optimize, inside_called=True)
    print('Completed inside call loopchannel optimaztions!')
    return loop_optimize


def run_optimization_passes(song, no_panning=False):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_og_song_size = executor.submit(calc_song_size, song)
        song_cleaned = convert_loopchannel(song)
        if no_panning:
            song_cleaned = remove_stereopanning(song_cleaned)
        future_call_first = executor.submit(call_then_loop_optimize, song_cleaned)
        future_loop_first = executor.submit(loop_then_call_optimize, song_cleaned)
        future_inside_call = executor.submit(call_then_loop_optimize, song_cleaned)
        song_call_first = future_call_first.result()
        print('Completed optimization type 1...')
        song_loop_first = future_loop_first.result()
        print('Completed optimization type 2...')
        song_inside_call = future_inside_call.result()
        print('Completed optimization type 3...')
        future_call_first_size = executor.submit(calc_song_size, song_call_first)
        future_loop_first_size = executor.submit(calc_song_size, song_loop_first)
        future_inside_call_size = executor.submit(calc_song_size, song_inside_call)
        og_song_size = future_og_song_size.result()
        song_call_first_size = future_call_first_size.result()
        song_loop_first_size = future_loop_first_size.result()
        song_inside_call_size = future_inside_call_size.result()
        if song_call_first_size < song_loop_first_size and song_call_first_size < song_inside_call_size:
            return (song_call_first, og_song_size, song_call_first_size)
        elif song_loop_first_size < song_call_first_size and song_loop_first_size < song_inside_call_size:
            return (song_loop_first, og_song_size, song_loop_first_size)
        return (song_inside_call, og_song_size, song_inside_call_size)
        
