Music_GBTemplate:
	musicheader 4, 1, Music_GBTemplate_Ch1
	musicheader 1, 2, Music_GBTemplate_Ch2
	musicheader 1, 3, Music_GBTemplate_Ch3
	musicheader 1, 4, Music_GBTemplate_Ch4


Music_GBTemplate_Ch1:
	tempo 640
	volume $77
	notetype $c, $95
	dutycycle $2
Music_GBTemplate_Ch1_Loop:
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	jumpchannel Music_GBTemplate_Ch1_Loop


Music_GBTemplate_Ch2:
	notetype $c, $95
	dutycycle $2
Music_GBTemplate_Ch2_Loop:
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	jumpchannel Music_GBTemplate_Ch2_Loop


Music_GBTemplate_Ch3:
	notetype $c, $15
Music_GBTemplate_Ch3_Loop:
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	jumpchannel Music_GBTemplate_Ch3_Loop


Music_GBTemplate_Ch4:
	notetype $c
	togglenoise 1
Music_GBTemplate_Ch4_Loop:
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	note __, 4
	jumpchannel Music_GBTemplate_Ch4_Loop


