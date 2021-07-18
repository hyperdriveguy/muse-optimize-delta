from functools import reduce


# Functions for working with tuples

def multi_map(iterable, *functions):
    mapped = iterable
    for function in functions:
        mapped = tuple(map(function, mapped))
    return mapped


def multi_filter(iterable, *filters):
    mapped = iterable
    for function in filters:
        mapped = tuple(filter(function, mapped))
    return mapped


def tuple_append(base, to_add, *additional):
    if type(base) != tuple or type(to_add) != tuple:
        raise ValueError('Arguments must be tuples')

    base += to_add

    check_nested_tuples(additional)
    for tup in additional:
        base += tup
    return base


def check_nested_tuples(iterable):

    def filter_no_tuple(line):
        if type(line) != tuple:
            return True
        return False

    def filter_only_tuple(line):
        if type(line) == tuple:
            return True
        return False

    no_tuples = tuple(filter(filter_no_tuple, iterable))
    only_tuples = tuple(filter(filter_only_tuple, iterable))
    if len(iterable) > len(no_tuples) and len(iterable) > len(only_tuples):
        raise ValueError('Arguments must be tuples')


def flatten_tuple(nested_tuple):
    """
    Make a 2D tuple one dimensional.
    The given tuple must only contain tuples.
    """
    base = ()
    for tup in nested_tuple:
        base = tuple_append(base, tup)
    return base


def remove_dup(iterable):
    """
    WARNING: Sets do not preserve order
    Do not use on tuples that are index sensitive.
    """
    return tuple(set(iterable))


# Filter functions


def filter_out_label(line):
    clean_line = line.strip()
    try:
        # Check for labels
        if clean_line[-1] == ':':
            return False
        # Check for labels with inline comments
        elif ';' in clean_line and clean_line.split(';')[0].strip()[-1] == ':':
            return False
    except IndexError:
        # Found a blank line, fallthrough below
        pass

    return True


def filter_labels(line):
    return not filter_out_label(line)


def filter_comments_space(line):
    clean_line = line.strip()
    # Check if line is blank
    if clean_line == '':
        return False
    # Skip commented out lines
    # Inline comments still work for non-labels
    elif clean_line[0] == ';':
        return False

    return True


# Command processing


def remove_inline_comment(line):
    if ';' in line:
        return line.split(';')[0].strip(' ') + '\n'

    return line


def get_root_command(raw_command):
    command = raw_command.split(' ')[0].strip()
    if command == 'notetype':
        if len(raw_command.split(' ')) > 2:
            return 'notetype_1'
        else:
            return 'notetype_2'

    return command


# Song attributes


def get_song_name(song):
    song_labels = tuple(filter(filter_labels, song))
    # Base the song name off the first label found
    return song_labels[0][:-2]


def scrub_song(song):
    scrubbed_song = tuple(filter(filter_comments_space, song))
    scrubbed_song = tuple(map(remove_inline_comment, scrubbed_song))
    return scrubbed_song


def calc_song_size(song):
    scrubbed_song = multi_filter(song, filter_out_label, filter_comments_space)
    command_bytes = multi_map(scrubbed_song,
                              get_root_command,
                              get_command_size)
    accumulator = lambda a, b: a + b
    try:
        song_size = reduce(accumulator, command_bytes)
    except TypeError:
        # We got here by trying to only calculate lines that take no space
        song_size = 0
    return song_size


def get_command_size(root_command):
    """
    Get a byte size (int) for an associated music command.
    Size map is ordered by most to least common commands.
    """
    # notetype can vary in size
    size_map_names = ('note', 'octave', 'notetype_1', 'notetype_2',
                      'dutycycle', 'intensity', 'tempo', 'tone',
                      'stereopanning', 'vibrato', 'slidepitchto', 'transpose',
                      'jumpchannel', 'callchannel', 'loopchannel',
                      'endchannel', 'jumpif', 'setcondition', 'togglenoise',
                      'volume', 'musicheader')
    size_map_bytes = (1, 1, 2, 3,
                      2, 2, 3, 2,
                      2, 3, 3, 2,
                      3, 3, 4,
                      1, 4, 2, 2,
                      2, 3)
    try:
        bytesize = size_map_bytes[size_map_names.index(root_command)]
    except IndexError:
        print(f'Unknown music command {root_command}, assuming size 1')
        bytesize = 1

    return bytesize


# Blacklists


def make_called_channel_blacklist(song):

    def filter_label_exists(line):
        if line in song:
            return True
        return False

    def filter_callchannel(line):
        if get_root_command(line) == 'callchannel':
            return True
        return False

    format_channel_label = lambda line: line.split(' ')[1].strip() + ':\n'

    called_channels = tuple(filter(filter_callchannel, song))
    called_branch_label = tuple(map(format_channel_label, called_channels))
    del called_channels
    existing_labels = remove_dup(
        tuple(filter(filter_label_exists, called_branch_label)))
    del called_branch_label

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
    return flatten_tuple(blacklisted_indexes)


def make_looped_channel_blacklist(song):

    def filter_label_exists(line):
        if line in song:
            return True
        return False

    def filter_loopchannel(line):
        if get_root_command(line) == 'loopchannel':
            return True
        return False
    
    def build_loopchannel_range(label, loop):
        # song.index is used because each label should only have one pair
        begin_index = song.index(label)
        end_index = song.index(loop)
        return tuple(range(begin_index, end_index + 1))

    format_channel_label = lambda line: line.split(' ')[-1].strip() + ':\n'

    loop_channels = tuple(filter(filter_loopchannel, song))
    looped_branch_label = tuple(map(format_channel_label, loop_channels))
    existing_labels = tuple(filter(filter_label_exists, looped_branch_label))
    del looped_branch_label

    blacklisted_indexes = tuple(map(build_loopchannel_range, existing_labels, loop_channels))

    return flatten_tuple(blacklisted_indexes)


def make_unoptimizable_blacklist(song, include_callchannel=True):

    def filter_unoptimizable(line):
        if include_callchannel:
            unoptimizable = ('callchannel',
                            'musicheader',
                            'endchannel',
                            'volume',
                            'togglenoise')
        else:
            unoptimizable = ('musicheader',
                            'endchannel',
                            'volume',
                            'togglenoise')
        if get_root_command(line) in unoptimizable:
            return True
        return False

    def unoptimizable_indexes(line):
        found_indexes = ()
        for index in range(len(song)):
            if song[index] == line:
                found_indexes = tuple_append(found_indexes, (index,))
        return found_indexes

    filtered_unoptimizable = tuple(filter(filter_unoptimizable, song))
    occurences = tuple(map(
        unoptimizable_indexes, filtered_unoptimizable))
    del filtered_unoptimizable
    blacklist = remove_dup(flatten_tuple(occurences))
    del occurences

    return blacklist


def make_label_blacklist(song):

    def unoptimizable_indexes(line):
        for index in range(len(song)):
            if song[index] == line:
                return index

    filtered_labels = tuple(filter(filter_labels, song))
    blacklisted_indexes = tuple(map(unoptimizable_indexes, filtered_labels))
    del filtered_labels

    return blacklisted_indexes


def make_callchannel_blacklists(song):
    loopchannel_whitelist = make_looped_channel_blacklist(song)
    
    def cancel_out_whitelist(line):
        if line in loopchannel_whitelist:
            return False
        return True
        
    callchannel_bl = make_called_channel_blacklist(song)
    label_bl = make_label_blacklist(song)
    clean_label_bl = tuple(filter(cancel_out_whitelist, label_bl))
    unoptimizable_bl = make_unoptimizable_blacklist(song)
    full_bl = tuple_append(
        callchannel_bl, clean_label_bl, unoptimizable_bl)
    del callchannel_bl
    del label_bl
    del unoptimizable_bl
    no_redundant_bl = remove_dup(full_bl)
    del full_bl
    sorted_bl = tuple(sorted(no_redundant_bl))
    del no_redundant_bl
    return sorted_bl


def make_loopchannel_blacklists(song, inside_calls=True):
    loopchannel_bl = make_looped_channel_blacklist(song)
    label_bl = make_label_blacklist(song)
    if not inside_calls:
        unoptimizable_bl = make_unoptimizable_blacklist(song, include_callchannel=False)
        called_channels = make_called_channel_blacklist(song)
        unoptimizable_bl = tuple_append(unoptimizable_bl, called_channels)
    else:
        unoptimizable_bl = make_unoptimizable_blacklist(song)
    full_bl = tuple_append(
        loopchannel_bl, label_bl, unoptimizable_bl)
    del loopchannel_bl
    del label_bl
    del unoptimizable_bl
    del_redundant_bl = remove_dup(full_bl)
    del full_bl
    sorted_bl = tuple(sorted(del_redundant_bl))
    del del_redundant_bl
    return sorted_bl


def range_in_blacklist(start, lookahead, blacklist):
    for index in range(start, start + lookahead + 1):
        if index in blacklist:
            return True
    return False
