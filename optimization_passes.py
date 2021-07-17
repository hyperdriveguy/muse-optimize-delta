import concurrent.futures

from util_funcs import calc_song_size
from callchannel import optimize_callchannel
from loopchannel import optimize_loopchannel
from other_compression import convert_loopchannel, remove_stereopanning


def reused_call_optimize(song):
    print('Doing callchannel optimizations [Type 1 & 2]...')
    call_optimize = optimize_callchannel(song)
    print('Completed callchannel optimizations [Type 1 & 2]!')
    return call_optimize


def loop_outside_call_optimize(call_optimize, agressive):
    print('Doing loopchannel optimizations [Type 1]...')
    loop_optimize = optimize_loopchannel(call_optimize, agress=agressive)
    print('Completed loopchannel optimizations [Type 1]!')
    print('Completed optimization type 1')
    return loop_optimize


def loop_optimize_inside_call(call_optimize, agressive):
    print('Doing inside call loopchannel optimizations [Type 2]...')
    loop_optimize = optimize_loopchannel(call_optimize, inside_called=True, agress=agressive)
    print('Completed inside call loopchannel optimizations [Type 2]!')
    print('Completed optimization type 2')
    return loop_optimize


def loop_then_call_optimize(song, agressive):
    print('Doing loopchannel optimizations [Type 3]...')
    loop_optimize = optimize_loopchannel(song, agress=agressive)
    print('Completed loopchannel optimaztions [Type 3]!')
    print('Doing callchannel optimizations [Type 3]...')
    call_optimize = optimize_callchannel(loop_optimize)
    print('Completed callchannel optimizations [Type 3]!')
    print('Completed optimization type 3')
    return call_optimize


def run_optimization_passes(song, no_panning=False, agress=False):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_og_song_size = executor.submit(calc_song_size, song)
        song_cleaned = convert_loopchannel(song)
        if no_panning:
            song_cleaned = remove_stereopanning(song_cleaned)
        future_reused_call = executor.submit(reused_call_optimize, song_cleaned)
        future_loop_first = executor.submit(loop_then_call_optimize, song_cleaned, agress)
        # The results of this partial optimization method are reusable
        song_reused_call = future_reused_call.result()
        future_loop_outside_call = executor.submit(loop_outside_call_optimize, song_reused_call, agress)
        future_loop_inside_call = executor.submit(loop_optimize_inside_call, song_reused_call, agress)
        # Get all final results
        song_loop_first = future_loop_first.result()
        song_loop_outside_call = future_loop_outside_call.result()
        song_loop_inside_call = future_loop_inside_call.result()
        # Get sizes of each used method
        future_loop_first_size = executor.submit(calc_song_size, song_loop_first)
        future_outside_call_size = executor.submit(calc_song_size, song_loop_outside_call)
        future_inside_call_size = executor.submit(calc_song_size, song_loop_inside_call)
        og_song_size = future_og_song_size.result()
        song_loop_first_size = future_loop_first_size.result()
        song_outside_call_size = future_outside_call_size.result()
        song_inside_call_size = future_inside_call_size.result()
        # Return smallest size
        if song_outside_call_size < song_loop_first_size and song_outside_call_size < song_inside_call_size:
            print('Using optimization type 1')
            return (song_loop_outside_call, og_song_size, song_outside_call_size)
        elif song_inside_call_size < song_outside_call_size and song_inside_call_size < song_loop_first_size:
            print('Using optimization type 2')
            return (song_loop_inside_call, og_song_size, song_inside_call_size)
        print('Using optimization type 3')
        return (song_loop_first, og_song_size, song_loop_first_size)
