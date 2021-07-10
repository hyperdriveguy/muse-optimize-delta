#!/usr/bin/env python
import pytest
import museoptimize 
import callchannel


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


def test_read_file():
    assert museoptimize.read_file('empty_score.asm') == empty_score_asm


def test_song_scrub():
    assert museoptimize.scrub_song(empty_score_asm) == empty_score_asm_scrubbed



def test_filter_non_command_whitespace():
    assert callchannel.filter_comments_space('\n') is False
    assert callchannel.filter_comments_space('\t\n') is False
    assert callchannel.filter_comments_space('\t \n') is False
    assert callchannel.filter_comments_space('\t\t    \n') is False


def test_filter_non_command_labels():
    assert callchannel.filter_out_label('Yeet:\n') is False
    assert callchannel.filter_out_label('Yeetasdf:\n\n') is False
    assert callchannel.filter_out_label('\tYeeter:\n') is False


def test_filter_non_command_comments():
    assert callchannel.filter_comments_space('; This is a comment\n') is False
    assert callchannel.filter_comments_space('\t; measure 14\n') is False
    assert callchannel.filter_comments_space('; yeet') is False
    assert callchannel.filter_comments_space(';norp') is False


def test_filter_non_command_inline_comments():
    assert callchannel.filter_out_label('\tBork: ; norp\n') is False
    assert callchannel.filter_out_label('\tRee:;norp\n') is False
    assert callchannel.filter_comments_space('\tBork: ; norp\n') is True
    assert callchannel.filter_comments_space('\tRee:;norp\n') is True
    assert callchannel.filter_comments_space('\tnote A_, 13 ;measure 233') is True
    assert callchannel.filter_comments_space('\toctave 3 ;asdf\n') is True


pytest.main(["-v", "--tb=line", "-rN", "test_optimize.py"])