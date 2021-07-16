#!/usr/bin/env python
import pytest
import museoptimize
import callchannel
import util_funcs


empty_score_asm = ('Music_GBTemplate:\n',
                   '\tmusicheader 4, 1, Music_GBTemplate_Ch1\n',
                   '\tmusicheader 1, 2, Music_GBTemplate_Ch2\n',
                   '\tmusicheader 1, 3, Music_GBTemplate_Ch3\n',
                   '\tmusicheader 1, 4, Music_GBTemplate_Ch4\n',
                   '\n',
                   '\n',
                   'Music_GBTemplate_Ch1:\n',
                   '\ttempo 640\n',
                   '\tvolume $77\n',
                   '\tnotetype $c, $95\n',
                   '\tdutycycle $2\n',
                   'Music_GBTemplate_Ch1_Loop:\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tjumpchannel Music_GBTemplate_Ch1_Loop\n',
                   '\n',
                   '\n',
                   'Music_GBTemplate_Ch2:\n',
                   '\tnotetype $c, $95\n',
                   '\tdutycycle $2\n',
                   'Music_GBTemplate_Ch2_Loop:\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tjumpchannel Music_GBTemplate_Ch2_Loop\n',
                   '\n',
                   '\n',
                   'Music_GBTemplate_Ch3:\n',
                   '\tnotetype $c, $15\n',
                   'Music_GBTemplate_Ch3_Loop:\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tjumpchannel Music_GBTemplate_Ch3_Loop\n',
                   '\n',
                   '\n',
                   'Music_GBTemplate_Ch4:\n',
                   '\tnotetype $c\n',
                   '\ttogglenoise 1\n',
                   'Music_GBTemplate_Ch4_Loop:\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tnote __, 4\n',
                   '\tjumpchannel Music_GBTemplate_Ch4_Loop\n',
                   '\n',
                   '\n')

empty_score_asm_scrubbed = ('Music_GBTemplate:\n',
                            '\tmusicheader 4, 1, Music_GBTemplate_Ch1\n',
                            '\tmusicheader 1, 2, Music_GBTemplate_Ch2\n',
                            '\tmusicheader 1, 3, Music_GBTemplate_Ch3\n',
                            '\tmusicheader 1, 4, Music_GBTemplate_Ch4\n',
                            'Music_GBTemplate_Ch1:\n',
                            '\ttempo 640\n',
                            '\tvolume $77\n',
                            '\tnotetype $c, $95\n',
                            '\tdutycycle $2\n',
                            'Music_GBTemplate_Ch1_Loop:\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tjumpchannel Music_GBTemplate_Ch1_Loop\n',
                            'Music_GBTemplate_Ch2:\n',
                            '\tnotetype $c, $95\n',
                            '\tdutycycle $2\n',
                            'Music_GBTemplate_Ch2_Loop:\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tjumpchannel Music_GBTemplate_Ch2_Loop\n',
                            'Music_GBTemplate_Ch3:\n',
                            '\tnotetype $c, $15\n',
                            'Music_GBTemplate_Ch3_Loop:\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tjumpchannel Music_GBTemplate_Ch3_Loop\n',
                            'Music_GBTemplate_Ch4:\n',
                            '\tnotetype $c\n',
                            '\ttogglenoise 1\n',
                            'Music_GBTemplate_Ch4_Loop:\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tnote __, 4\n',
                            '\tjumpchannel Music_GBTemplate_Ch4_Loop\n')

empty_score_asm_optimized = ('Music_GBTemplate:\n',
                             '\tmusicheader 4, 1, Music_GBTemplate_Ch1\n',
                             '\tmusicheader 1, 2, Music_GBTemplate_Ch2\n',
                             '\tmusicheader 1, 3, Music_GBTemplate_Ch3\n',
                             '\tmusicheader 1, 4, Music_GBTemplate_Ch4\n',
                             'Music_GBTemplate_Ch1:\n',
                             '\ttempo 640\n',
                             '\tvolume $77\n',
                             '\tnotetype $c, $95\n',
                             '\tdutycycle $2\n',
                             'Music_GBTemplate_Ch1_Loop:\n',
                             '\tcallchannel Music_GBTemplate_Branch1\n',
                             '\tjumpchannel Music_GBTemplate_Ch1_Loop\n',
                             'Music_GBTemplate_Ch2:\n',
                             '\tnotetype $c, $95\n',
                             '\tdutycycle $2\n',
                             'Music_GBTemplate_Ch2_Loop:\n',
                             '\tcallchannel Music_GBTemplate_Branch1\n',
                             '\tjumpchannel Music_GBTemplate_Ch2_Loop\n',
                             'Music_GBTemplate_Ch3:\n',
                             '\tnotetype $c, $15\n',
                             'Music_GBTemplate_Ch3_Loop:\n',
                             '\tcallchannel Music_GBTemplate_Branch1\n',
                             '\tjumpchannel Music_GBTemplate_Ch3_Loop\n',
                             'Music_GBTemplate_Ch4:\n',
                             '\tnotetype $c\n',
                             '\ttogglenoise 1\n',
                             'Music_GBTemplate_Ch4_Loop:\n',
                             '\tcallchannel Music_GBTemplate_Branch1\n',
                             '\tjumpchannel Music_GBTemplate_Ch4_Loop\n',
                             'Music_GBTemplate_Branch1:\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tnote __, 4\n',
                             '\tendchannel\n')

empty_score_asm_optimized_looped = ('Music_GBTemplate:\n',
                                    '\tmusicheader 4, 1, Music_GBTemplate_Ch1\n',
                                    '\tmusicheader 1, 2, Music_GBTemplate_Ch2\n',
                                    '\tmusicheader 1, 3, Music_GBTemplate_Ch3\n',
                                    '\tmusicheader 1, 4, Music_GBTemplate_Ch4\n',
                                    'Music_GBTemplate_Ch1:\n',
                                    '\ttempo 640\n',
                                    '\tvolume $77\n',
                                    '\tnotetype $c, $95\n',
                                    '\tdutycycle $2\n',
                                    'Music_GBTemplate_Ch1_Loop:\n',
                                    '\tcallchannel Music_GBTemplate_Branch1\n',
                                    '\tjumpchannel Music_GBTemplate_Ch1_Loop\n',
                                    'Music_GBTemplate_Ch2:\n',
                                    '\tnotetype $c, $95\n',
                                    '\tdutycycle $2\n',
                                    'Music_GBTemplate_Ch2_Loop:\n',
                                    '\tcallchannel Music_GBTemplate_Branch1\n',
                                    '\tjumpchannel Music_GBTemplate_Ch2_Loop\n',
                                    'Music_GBTemplate_Ch3:\n',
                                    '\tnotetype $c, $15\n',
                                    'Music_GBTemplate_Ch3_Loop:\n',
                                    '\tcallchannel Music_GBTemplate_Branch1\n',
                                    '\tjumpchannel Music_GBTemplate_Ch3_Loop\n',
                                    'Music_GBTemplate_Ch4:\n',
                                    '\tnotetype $c\n',
                                    '\ttogglenoise 1\n',
                                    'Music_GBTemplate_Ch4_Loop:\n',
                                    '\tcallchannel Music_GBTemplate_Branch1\n',
                                    '\tjumpchannel Music_GBTemplate_Ch4_Loop\n',
                                    'Music_GBTemplate_Branch1:\n',
                                    'Music_GBTemplate_loop1:\n',
                                    '\tnote __, 4\n',
                                    '\tloopchannel 16, Music_GBTemplate_loop1',
                                    '\tendchannel\n')

no_nesting = ('Yeet:\n',
              '\tnote A_, 2\n',
              '\tcallchannel yote\n',
              '\tnote A_, 2\n',
              '\tcallchannel yote\n',
              '\tnote A_, 2\n',
              '\tcallchannel yote\n',
              '\tnote A_, 2\n',
              '\tcallchannel yote\n',
              '\tnote A_, 2\n',
              '\tcallchannel yote\n',
              '\tjumpchannel Yeet\n',
              'yote:\n',
              '\tnote A_, 2\n',
              '\tnote B_, 2\n',
              '\tnote C_, 2\n',
              '\tnote D_, 2\n',
              '\tendchannel\n')

looped_cal = ('Yeet:\n',
              'Yeet_loop1:\n',
              '\tnote A_, 2\n',
              '\tcallchannel yote\n',
              '\tloopchannel 5, Yeet_loop1',
              '\tjumpchannel Yeet\n',
              'yote:\n',
              '\tnote A_, 2\n',
              '\tnote B_, 2\n',
              '\tnote C_, 2\n',
              '\tnote D_, 2\n',
              '\tendchannel\n')


no_nesting_blacklist = (0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16, 17)
empty_score_blacklist = (0, 1, 2, 3, 4, 5, 7, 10, 28, 31, 49, 51, 69, 71, 72)


def test_read_file():
    assert museoptimize.read_file('empty_score.asm') == empty_score_asm


def test_format_size_diff():
    assert museoptimize.format_size_diff(100, 100) == 'Before optimization: 100\nAfter optimization: 100\n100.00% of original size'


def test_song_scrub():
    assert museoptimize.scrub_song(empty_score_asm) == empty_score_asm_scrubbed


def test_multi_map():

    def make_string(item):
        if type(item) != str:
            return str(item)
        return item

    def make_int(item):
        if type(item) != int:
            return int(item)
        return item

    def add_a(item):
        return item + 'a'

    def add_one(item):
        return item + 1

    iterable_1 = (1, 2, 3, 4, 'a', 5, 6, 7, 'x')
    iterable_2 = ('a', 'b', 'c', 1, 3, '3', '23')
    iterable_3 = (454, '99', '33', 1, 3, '3', '23')
    assert util_funcs.multi_map(iterable_1, make_string, add_a) == \
        ('1a', '2a', '3a', '4a', 'aa', '5a', '6a', '7a', 'xa')
    assert util_funcs.multi_map(iterable_2, make_string, add_a) == \
        ('aa', 'ba', 'ca', '1a', '3a', '3a', '23a')
    assert util_funcs.multi_map(iterable_3, make_int, add_one) == \
        (455, 100, 34, 2, 4, 4, 24)


def test_multi_filter():

    def filter_string(item):
        if type(item) == str:
            return True
        return False

    def filter_int(item):
        if type(item) == int:
            return True
        return False

    def filter_lt_four(item):
        if item < 4:
            return True
        return False

    def filter_a(item):
        if item == 'a':
            return True
        return False

    iterable_1 = (1, 2, 3, 4, 'a', 5, 6, 7, 'x')
    iterable_2 = ('a', 'b', 'c', 1, 3, '3', '23')
    iterable_3 = (454, '99', '33', 1, 3, '3', '23')
    assert util_funcs.multi_filter(iterable_1, filter_string, filter_a) == \
        ('a',)
    assert util_funcs.multi_filter(iterable_1, filter_int, filter_lt_four) == \
        (1, 2, 3)
    assert util_funcs.multi_filter(iterable_2, filter_string, filter_a) == \
        ('a',)
    assert util_funcs.multi_filter(iterable_2, filter_int, filter_lt_four) == \
        (1, 3)
    assert util_funcs.multi_filter(iterable_3, filter_string, filter_a) == \
        ()
    assert util_funcs.multi_filter(iterable_3, filter_int, filter_lt_four) == \
        (1, 3)


def test_tuple_append():
    tuple_1 = ('a', 'b', 'c')
    tuple_2 = ('d', 'e', 'f')
    tuple_3 = (1, 2, 3)
    tuple_4 = (4, 5, 6)

    assert util_funcs.tuple_append(tuple_1, tuple_2) == \
        ('a', 'b', 'c', 'd', 'e', 'f')
    assert util_funcs.tuple_append(tuple_2, tuple_1) == \
        ('d', 'e', 'f', 'a', 'b', 'c')
    assert util_funcs.tuple_append(tuple_3, tuple_4) == (1, 2, 3, 4, 5, 6)
    assert util_funcs.tuple_append(tuple_4, tuple_3) == (4, 5, 6, 1, 2, 3)

    assert util_funcs.tuple_append(tuple_1, tuple_2, tuple_3) == \
        ('a', 'b', 'c', 'd', 'e', 'f', 1, 2, 3)
    assert util_funcs.tuple_append(tuple_1, tuple_2, tuple_3, tuple_4) == \
        ('a', 'b', 'c', 'd', 'e', 'f', 1, 2, 3, 4, 5, 6)
    assert util_funcs.tuple_append(
        tuple_1, tuple_2, tuple_3, tuple_4, tuple_4) == \
        ('a', 'b', 'c', 'd', 'e', 'f', 1, 2, 3, 4, 5, 6, 4, 5, 6)


def test_nested_tuples():
    good_tuple = (3, 4, 5, 6)
    bad_tuple_1 = ((1, 2, 3), 4)
    bad_tuple_2 = (1, (2, 3, 4))

    try:
        util_funcs.check_nested_tuples(good_tuple)
    except ValueError:
        assert False

    try:
        util_funcs.check_nested_tuples(bad_tuple_1)
    except ValueError:
        assert True

    try:
        util_funcs.check_nested_tuples(bad_tuple_2)
    except ValueError:
        assert True


def test_flatten_tuple():
    tup1 = ((1, 2, 3), (1, 2, 3))
    tup2 = (('a', 'b', 'c'), ('d', 'e', 'f'))
    assert util_funcs.flatten_tuple(tup1) == (1, 2, 3, 1, 2, 3)
    assert util_funcs.flatten_tuple(tup2) == ('a', 'b', 'c', 'd', 'e', 'f')


def test_remove_dup():
    dups1 = (1, 1, 1, 2, 2, 4, 3)
    dups2 = ('a', 'a', 'b', 'a', 'c')
    dups3 = ((1, 2, 3), (4, 5, 6), (1, 2, 3))
    assert util_funcs.remove_dup(dups1) == (1, 2, 3, 4)
    assert tuple(sorted(util_funcs.remove_dup(dups2))) == ('a', 'b', 'c')
    assert util_funcs.remove_dup(dups3) == ((1, 2, 3), (4, 5, 6))


def test_filter_non_command_whitespace():
    assert util_funcs.filter_comments_space('\n') is False
    assert util_funcs.filter_comments_space('\t\n') is False
    assert util_funcs.filter_comments_space('\t \n') is False
    assert util_funcs.filter_comments_space('\t\t    \n') is False


def test_filter_non_command_labels():
    assert util_funcs.filter_out_label('Yeet:\n') is False
    assert util_funcs.filter_out_label('Yeetasdf:\n\n') is False
    assert util_funcs.filter_out_label('\tYeeter:\n') is False
    assert util_funcs.filter_labels('Yeet:\n') is True
    assert util_funcs.filter_labels('Yeetasdf:\n\n') is True
    assert util_funcs.filter_labels('\tYeeter:\n') is True


def test_filter_non_command_comments():
    assert util_funcs.filter_comments_space('; This is a comment\n') is False
    assert util_funcs.filter_comments_space('\t; measure 14\n') is False
    assert util_funcs.filter_comments_space('; yeet') is False
    assert util_funcs.filter_comments_space(';norp') is False


def test_filter_non_command_inline_comments():
    assert util_funcs.filter_out_label('Bork: ; norp\n') is False
    assert util_funcs.filter_out_label('\tRee:;norp\n') is False
    assert util_funcs.filter_comments_space('\tBork: ; norp\n') is True
    assert util_funcs.filter_comments_space('\tRee:;norp\n') is True
    assert util_funcs.filter_comments_space('\tnote A_, 13 ;m 23') is True
    assert util_funcs.filter_comments_space('\toctave 3 ;asdf\n') is True


def test_get_song_name():
    test_song_1 = ('Music_Yeet:\n',)
    test_song_2 = ('Yeet:\n', '\tnote A_, 4')

    assert util_funcs.get_song_name(empty_score_asm) == 'Music_GBTemplate'
    assert util_funcs.get_song_name(empty_score_asm_scrubbed) == \
        'Music_GBTemplate'
    assert util_funcs.get_song_name(test_song_1) == 'Music_Yeet'
    assert util_funcs.get_song_name(test_song_2) == 'Yeet'


def test_remove_inline_comment():
    assert util_funcs.remove_inline_comment('Bork: ; norp\n') == \
        'Bork:\n'
    assert util_funcs.remove_inline_comment('\tRee:;norp\n') == \
        '\tRee:\n'
    assert util_funcs.remove_inline_comment('\tBork: ; norp\n') == \
        '\tBork:\n'
    assert util_funcs.remove_inline_comment('\tRee:;norp\n') == \
        '\tRee:\n'
    assert util_funcs.remove_inline_comment('\tnote A_, 13 ;m 23') == \
        '\tnote A_, 13\n'
    assert util_funcs.remove_inline_comment('\toctave 3 ;asdf\n') == \
        '\toctave 3\n'


def test_get_root_command():
    assert util_funcs.get_root_command('\tnote A_, 13 ;m 23') == \
        'note'
    assert util_funcs.get_root_command('\tnote A_, 13\n') == \
        'note'
    musicheader = '\tmusicheader 1, 4, Music_GBTemplate_Ch4\n'
    assert util_funcs.get_root_command(musicheader) == \
        'musicheader'
    del musicheader
    assert util_funcs.get_root_command('\ttempo 640\n') == \
        'tempo'
    assert util_funcs.get_root_command('\tdutycycle $2\n') == \
        'dutycycle'
    assert util_funcs.get_root_command('Music_GBTemplate_Ch1_Loop:\n') == \
        'Music_GBTemplate_Ch1_Loop:'


def test_calc_song_size():
    test_window = ('\tcallchannel yeet\n', '\tnote __, 1\n', 'endchannel')
    test_unscrubbed_window = ('\tcallchannel yeet\n', '\n', 'endchannel')

    assert util_funcs.calc_song_size(empty_score_asm) == 108
    assert util_funcs.calc_song_size(empty_score_asm_scrubbed) == 108
    assert util_funcs.calc_song_size(test_window) == 5
    assert util_funcs.calc_song_size(test_unscrubbed_window) == 4


def test_get_command_size():
    assert util_funcs.get_command_size('note') == 1
    assert util_funcs.get_command_size('octave') == 1
    assert util_funcs.get_command_size('notetype_1') == 2
    assert util_funcs.get_command_size('notetype_2') == 3
    assert util_funcs.get_command_size('dutycycle') == 2
    assert util_funcs.get_command_size('intensity') == 2
    assert util_funcs.get_command_size('tempo') == 3
    assert util_funcs.get_command_size('tone') == 2
    assert util_funcs.get_command_size('stereopanning') == 2
    assert util_funcs.get_command_size('vibrato') == 3
    assert util_funcs.get_command_size('slidepitchto') == 3
    assert util_funcs.get_command_size('transpose') == 2
    assert util_funcs.get_command_size('jumpchannel') == 3
    assert util_funcs.get_command_size('callchannel') == 3
    assert util_funcs.get_command_size('loopchannel') == 4
    assert util_funcs.get_command_size('endchannel') == 1
    assert util_funcs.get_command_size('jumpif') == 4
    assert util_funcs.get_command_size('setcondition') == 2
    assert util_funcs.get_command_size('togglenoise') == 2
    assert util_funcs.get_command_size('volume') == 2
    assert util_funcs.get_command_size('musicheader') == 3


def test_make_called_channel_blacklist():
    empty_score_blacklist_called = util_funcs.make_called_channel_blacklist(
        empty_score_asm_scrubbed)
    assert empty_score_blacklist_called == ()

    no_nesting_blacklist_called = util_funcs.make_called_channel_blacklist(
        no_nesting)
    assert no_nesting_blacklist_called == (12, 13, 14, 15, 16, 17)


def test_make_looped_channel_blacklist():
    loop_test = ('Loop:\n', '\tnote A_, 2\n', '\tloopchannel 6, Loop\n')
    assert util_funcs.make_looped_channel_blacklist(loop_test) == (0, 1, 2)
    assert util_funcs.make_looped_channel_blacklist(looped_cal) == (1, 2, 3, 4)


def test_make_unoptimizable_blacklist():
    empty_score_blacklist_called = util_funcs.make_unoptimizable_blacklist(
        empty_score_asm_scrubbed)
    assert empty_score_blacklist_called == (1, 2, 3, 4, 7, 71)

    no_nesting_blacklist_called = util_funcs.make_unoptimizable_blacklist(
        no_nesting)
    assert no_nesting_blacklist_called == (2, 4, 6, 8, 10, 17)


def test_make_label_blacklist():
    empty_score_blacklist_called = util_funcs.make_label_blacklist(
        empty_score_asm_scrubbed)
    assert empty_score_blacklist_called == (0, 5, 10, 28, 31, 49, 51, 69, 72)

    no_nesting_blacklist_called = util_funcs.make_label_blacklist(
        no_nesting)
    assert no_nesting_blacklist_called == (0, 12)


def test_make_callchannel_blacklists():
    gen_empty_song_blacklist = util_funcs.make_callchannel_blacklists(
        empty_score_asm_scrubbed)
    assert gen_empty_song_blacklist == empty_score_blacklist

    gen_no_nest_blacklist = util_funcs.make_callchannel_blacklists(no_nesting)
    assert gen_no_nest_blacklist == no_nesting_blacklist


def test_make_loopchannel_blacklists():
    assert util_funcs.make_loopchannel_blacklists(empty_score_asm_optimized_looped) == (0, 1, 2, 3, 4, 5, 7, 10, 11, 13, 16, 17, 19, 21, 22, 24, 26, 27, 28, 30, 31, 32, 33, 34)
    assert util_funcs.make_loopchannel_blacklists(looped_cal) == (0, 1, 2, 3, 4, 6, 11)


def test_parse_matches_blacklist():
    assert new_blacklist_no_nest == no_nesting_blacklist
    empty_score_expected_blacklist = (
        0, 1, 2, 3, 4, 5, 7, 10, 11, 13, 16, 17, 19, 21, 22, 24, 26, 27, 28)
    assert new_blacklist_empty == empty_score_expected_blacklist


def test_range_in_blacklist():
    assert util_funcs.range_in_blacklist(
        0, 2, no_nesting_blacklist) is True
    assert util_funcs.range_in_blacklist(
        13, 3, no_nesting_blacklist) is True
    assert util_funcs.range_in_blacklist(
        9, 0, no_nesting_blacklist) is False

    assert util_funcs.range_in_blacklist(
        8, 1, empty_score_blacklist) is False
    assert util_funcs.range_in_blacklist(
        11, 16, empty_score_blacklist) is False
    assert util_funcs.range_in_blacklist(
        68, 2, empty_score_blacklist) is True


def test_optimize_callchannel():
    assert callchannel.optimize_callchannel(empty_score_asm_scrubbed) == \
        empty_score_asm_optimized
    assert callchannel.optimize_callchannel(no_nesting) == no_nesting


def test_build_ideal_lookahead():
    for index in range(len(no_nesting)):
        no_nest_la = callchannel.build_ideal_lookahead(
            no_nesting, index, no_nesting_blacklist)
        assert no_nest_la == 0

    empty_score_la = callchannel.build_ideal_lookahead(
        empty_score_asm_scrubbed, 11, empty_score_blacklist)
    assert empty_score_la == 15


def test_calc_callchannel_savings():
    subset_1 = ('\tnote A_, 2\n',
                '\tnote B_, 2\n',
                '\tnote C_, 2\n',
                '\tnote D_, 2\n')

    subset_2 = ('\tnote A_, 2\n',
                '\tnote B_, 2\n',
                '\tnote C_, 2\n',
                '\tnote B_, 2\n',
                '\tnote C_, 2\n',
                '\tnote D_, 2\n')

    subset_3 = ('\tstereopanning $f0\n',
                '\tnote B_, 2\n',
                '\tnote C_, 2\n',
                '\ttempo 400',
                '\tnote C_, 2\n',
                '\tnote D_, 2\n')

    callchannel.calc_callchannel_savings(subset_2, 8)

    assert callchannel.calc_callchannel_savings(subset_1, 4) == 1
    assert callchannel.calc_callchannel_savings(subset_2, 8) == 19
    assert callchannel.calc_callchannel_savings(subset_3, 12) == 64


def test_parse_matches():
    global new_blacklist_empty
    song_empty, branch_empty, new_blacklist_empty = callchannel.parse_matches(
        empty_score_asm_scrubbed, 11, 15, empty_score_blacklist, 1)
    assert util_funcs.tuple_append(song_empty, branch_empty) == \
        empty_score_asm_optimized

    # We should get none of the matching lines optimized out
    global new_blacklist_no_nest
    song_no_nest, branch_no_nest, new_blacklist_no_nest = \
        callchannel.parse_matches(no_nesting, 1, 1, no_nesting_blacklist, 1)
    assert song_no_nest == no_nesting


def test_make_new_branch_call():
    empty_score_test_1 = callchannel.make_new_branch_call(
        empty_score_asm_scrubbed, 11, 26, 1)
    assert empty_score_test_1[11] == '\tcallchannel Music_GBTemplate_Branch1\n'

    empty_score_test_2 = callchannel.make_new_branch_call(
        empty_score_asm_scrubbed, 32, 47, 1)
    assert empty_score_test_2[32] == '\tcallchannel Music_GBTemplate_Branch1\n'


def test_make_branch():
    branch_1_contents = ('\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n',
                         '\tnote __, 4\n')

    branch_2_contents = ('\tstereopanning $f0\n',
                         '\tnote A_, 4\n',
                         '\tnote __, 4\n',
                         '\tnote B_, 4\n',
                         '\tnote __, 4\n',
                         '\tstereopanning $0f\n')

    formed_branch_1 = callchannel.make_branch(
        empty_score_asm_scrubbed, 1, branch_1_contents)
    assert formed_branch_1[0] == 'Music_GBTemplate_Branch1:\n'
    assert formed_branch_1[-1] == '\tendchannel\n'
    assert formed_branch_1[1:-1] == branch_1_contents

    formed_branch_2 = callchannel.make_branch(
        empty_score_asm_scrubbed, 2, branch_2_contents)
    assert formed_branch_2[0] == 'Music_GBTemplate_Branch2:\n'
    assert formed_branch_2[-1] == '\tendchannel\n'
    assert formed_branch_2[1:-1] == branch_2_contents



pytest.main(["-v", "--tb=line", "-rN", "test_optimize.py"])
