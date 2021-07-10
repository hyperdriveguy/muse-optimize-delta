import util_funcs


def optimize_callchannel(song):
    """
    Makes different reusable song branches to be called.

    This is the most common and generally most space saving
    optimization in practice. It imitates a dictionary based
    compression algorithm and takes hints from LZ77. The biggest
    drawback is that called channels cannot be nested.
    Since callchannel + endchannel takes 4 bytes, the minimum
    branch size with no space savings is 4 bytes with 2 matches.
    """

    branches = tuple()

    index_blacklist = make_all_blacklists(song)

    file_index = 0
    cur_branch = 1
    # A while loop accounts for a mutating size
    while file_index < len(song):
        lookahead = build_ideal_lookahead(song,
                                          file_index,
                                          index_blacklist)
        if lookahead == 0:
            file_index += 1
            continue

        song, new_branch, index_blacklist = parse_matches(song,
                                                          file_index,
                                                          lookahead,
                                                          index_blacklist,
                                                          cur_branch)
        branches = util_funcs.tuple_append(branches, new_branch)
        cur_branch += 1
    return util_funcs.tuple_append(song, branches)


def build_ideal_lookahead(song, start_index, blacklist):
    lookahead = 0
    found_ideal_lookahead = False
    ideal_lookahead = 0
    prev_size_savings = 0

    def calc_matches_in_window():
        num_matches = 1
        # A while loop is used due to steps needing to vary
        cur_index = start_index + len(window)
        while cur_index < len(song) - lookahead:
            song_subset = song[cur_index:cur_index + lookahead + 1]
            if(window == song_subset and
                    not range_in_blacklist(cur_index,
                                           lookahead,
                                           blacklist)):
                num_matches += 1
                # Increase by window length to avoid conflicts
                cur_index += len(window)
            else:
                cur_index += 1
        return num_matches

    while not found_ideal_lookahead:
        if not range_in_blacklist(start_index, lookahead, blacklist):
            window = song[start_index:start_index + lookahead + 1]
            matches = calc_matches_in_window()
            cur_savings = calc_callchannel_savings(window, matches)
            if cur_savings > prev_size_savings:
                # This ensures minimum savings is zero, preventing regressions
                prev_size_savings = cur_savings
                ideal_lookahead = lookahead
            if matches == 1:
                found_ideal_lookahead = True
            lookahead += 1
        else:
            found_ideal_lookahead = True
    return ideal_lookahead


def calc_callchannel_savings(song_subset, matches):
    matches_size = util_funcs.calc_song_size(song_subset) * (matches - 1)
    callchannel_size = (matches * 3) - 1
    return matches_size - callchannel_size


def parse_matches(song, start_index, lookahead, blacklist, branch):
    window = song[start_index:start_index + lookahead + 1]
    called_branch = make_branch(song, branch, window)
    # A while loop is used due to steps needing to vary
    cur_index = start_index
    while cur_index < len(song) - lookahead:
        song_subset = song[cur_index:cur_index + lookahead + 1]
        if(window == song_subset and
                not range_in_blacklist(cur_index,
                                       lookahead,
                                       blacklist)):
            song = make_new_branch_call(song,
                                        cur_index,
                                        cur_index + lookahead,
                                        branch)
            # Rebuild blacklist
            blacklist = make_all_blacklists(song)
        cur_index += 1
    return (song, called_branch, blacklist)


def make_new_branch_call(song, begin_index, end_index, branch):
    branch_name = f'{util_funcs.get_song_name(song)}_Branch{branch}'
    song_pre = song[:begin_index]
    song_post = song[end_index + 1:]
    callchannel = (f'\tcallchannel {branch_name}\n',)

    return util_funcs.tuple_append(song_pre, callchannel, song_post)


def make_branch(song, branch, contents):
    branch_name = f'{util_funcs.get_song_name(song)}_Branch{branch}'
    label = (branch_name + ':\n',)
    endchannel = ('\tendchannel\n',)
    return util_funcs.tuple_append(label, contents, endchannel)


def range_in_blacklist(start, lookahead, blacklist):
    for index in range(start, start + lookahead + 1):
        if index in blacklist:
            return True
    return False


def make_called_channel_blacklist(song):

    def filter_label_exists(line):
        if line in song:
            return True
        return False

    def filter_callchannel(line):
        if util_funcs.get_root_command(line) == 'callchannel':
            return True
        return False

    format_channel_label = lambda line: line.split(' ')[1].strip() + ':\n'

    called_channels = tuple(filter(filter_callchannel, song))
    called_branch_label = tuple(map(format_channel_label, called_channels))
    existing_labels = util_funcs.remove_dup(
        tuple(filter(filter_label_exists, called_branch_label)))

    return build_callchannel_range(existing_labels, song)


def build_callchannel_range(labels, song):

    def get_range(label):
        start_bad = None
        end_bad = None
        for index in range(len(song)):
            if song[index] == label:
                start_bad = index
            elif start_bad is not None and song[index] == '\tendchannel\n':
                end_bad = index
        if start_bad is None:
            raise IndexError(f'Called branch {label} was not found in song')
        if end_bad is None:
            raise IndexError(f'Called branch {label} '
                                'has no matching endchannel')
        return tuple(range(start_bad, end_bad + 1))

    blacklisted_indexes = tuple(map(get_range, labels))
    return util_funcs.flatten_tuple(blacklisted_indexes)


def make_unoptimizable_blacklist(song):

    def filter_unoptimizable(line):
        unoptimizable = ('callchannel',
                         'musicheader',
                         'endchannel',
                         'volume',
                         'togglenoise')
        if util_funcs.get_root_command(line) in unoptimizable:
            return True
        return False

    def unoptimizable_indexes(line):
        found_indexes = ()
        for index in range(len(song)):
            if song[index] == line:
                found_indexes = util_funcs.tuple_append(found_indexes, (index,))
        return found_indexes

    filtered_unoptimizable = tuple(filter(filter_unoptimizable, song))
    occurences = tuple(map(
        unoptimizable_indexes, filtered_unoptimizable))
    blacklist = util_funcs.remove_dup(util_funcs.flatten_tuple(occurences))

    return blacklist


def make_label_blacklist(song):

    def unoptimizable_indexes(line):
        for index in range(len(song)):
            if song[index] == line:
                return index

    filtered_labels = tuple(filter(util_funcs.filter_labels, song))
    blacklisted_indexes = tuple(map(unoptimizable_indexes, filtered_labels))

    return blacklisted_indexes


def make_all_blacklists(song):
    callchannel_bl = make_called_channel_blacklist(song)
    label_bl = make_label_blacklist(song)
    unoptimizable_bl = make_unoptimizable_blacklist(song)
    full_bl = util_funcs.tuple_append(
        callchannel_bl, label_bl, unoptimizable_bl)
    sorted_bl = tuple(sorted(full_bl))
    return sorted_bl
