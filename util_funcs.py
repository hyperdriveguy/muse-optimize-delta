def multi_map(iterable, *functions, keep_none=True):
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


def get_song_name(song):
    song_labels = tuple(filter(filter_labels, song))
    # Base the song name off the first label found
    return song_labels[0][:-2]


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
