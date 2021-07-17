import util_funcs


def optimize_loopchannel(song, inside_called=True, agress=False):
    """
    Reduces redundant commands that appear all in a row.

    Similar to callchannel optimizations, loopchannels cannot be nested.
    A called branch can have a loop or a loop can have a channel call it it,
    but there can never be a looped channel > called channel > looped channel.
    """
    index_blacklist = util_funcs.make_loopchannel_blacklists(song, inside_calls=inside_called)

    file_index = 0
    cur_loop = 1

    # A while loop accounts for a mutating size
    while file_index < len(song):
        lookahead, redundancy = build_ideal_lookahead(song,
                                                      file_index,
                                                      index_blacklist,
                                                      agressive=agress)
        if redundancy == 1:
            file_index += 1
            continue

        song = insert_loops(song, file_index, lookahead, redundancy, cur_loop)
        index_blacklist = util_funcs.make_loopchannel_blacklists(song, inside_calls=inside_called)
        file_index += 1
        cur_loop += 1
    return song


def build_ideal_lookahead(song, start_index, blacklist, agressive=False):
    """
    Find the ideal number of commands for the loop to contain.

    The main difference between this and the callchannel lookahead is
    that the matches must all be next to each other.
    """
    lookahead = 0
    found_ideal_lookahead = False
    ideal_lookahead = 0
    prev_size_savings = 0
    ideal_matches = 1

    def calc_matches_in_window():
        num_matches = 1
        # A while loop is used due to steps needing to vary
        cur_index = start_index + len(window)
        while(cur_index < len(song) - lookahead and
              not util_funcs.range_in_blacklist(cur_index,
                                                lookahead,
                                                blacklist)):
            song_subset = song[cur_index:cur_index + lookahead + 1]
            if window == song_subset:
                num_matches += 1
                # Increase by window length to avoid conflicts
                cur_index += len(window)
            else:
                # End here because the next match will not be adjacent
                break
        return num_matches

    while not found_ideal_lookahead and start_index + lookahead < len(song) - 1:
        if not util_funcs.range_in_blacklist(start_index, lookahead, blacklist):
            window = song[start_index:start_index + lookahead + 1]
            matches = calc_matches_in_window()
            cur_savings = util_funcs.calc_song_size(window) * (matches - 1) - 4
            if cur_savings > prev_size_savings:
                # This ensures minimum savings is zero, preventing regressions
                prev_size_savings = cur_savings
                ideal_lookahead = lookahead
                ideal_matches = matches
            elif not agressive and matches == 1:
                found_ideal_lookahead = True
            lookahead += 1
        else:
            found_ideal_lookahead = True
    return (ideal_lookahead, ideal_matches)


def insert_loops(song, start_index, lookahead, loop_times, loop_num):
    window = song[start_index:start_index + lookahead + 1]
    gen_loop = format_loop(song, window, loop_times, loop_num)
    begin_song = song[:start_index]
    end_index = (len(window) * loop_times) + start_index
    end_song = song[end_index:]
    return util_funcs.tuple_append(begin_song, gen_loop, end_song)


def format_loop(song, inner_loop, loop_times, loop_num):
    label = f'{util_funcs.get_song_name(song)}_loop{loop_num}:\n'
    looper = f'\tloopchannel {loop_times}, {label[:-2]}\n'
    return util_funcs.tuple_append((label,), inner_loop, (looper,))
