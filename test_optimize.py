#!/usr/bin/env python
import pytest
from museoptimize import read_file, filter_non_command, get_root_command, \
    get_command_size


def test_read_file():
    assert read_file('empty_score.asm') == \
        ('Music_GBTemplate:\n',
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


def test_filter_non_command_whitespace():
    assert filter_non_command('\n') is False
    assert filter_non_command('\t\n') is False
    assert filter_non_command('\t \n') is False
    assert filter_non_command('\t\t    \n') is False


def test_filter_non_command_labels():
    assert filter_non_command('Yeet:\n') is False
    assert filter_non_command('Yeetasdf:\n\n') is False
    assert filter_non_command('\tYeeter:\n') is False


def test_filter_non_command_comments():
    assert filter_non_command('; This is a comment\n') is False
    assert filter_non_command('\t; measure 14\n') is False
    assert filter_non_command('; yeet') is False
    assert filter_non_command(';norp') is False


def test_filter_non_command_inline_comments():
    assert filter_non_command('\tBork: ; norp\n') is False
    assert filter_non_command('\tRee:;norp\n') is False
    assert filter_non_command('\tnote A_, 13 ;measure 233') is True
    assert filter_non_command('\toctave 3 ;asdf\n') is True


pytest.main(["-v", "--tb=line", "-rN", "test_optimize.py"])