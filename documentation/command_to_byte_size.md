# Byte sizes

## musicheader
* index + channel count: 1
* address: 2
* total: 3

## note
* pitch + length: 1
* total: 1

## octave
* total: 1

## notetype
* length: 1
* volume + fade: 1
    * not always present
* total: 2 to 3

## transpose
* num octaves + num pitches: 1
* total 2

## tempo
* tempo: 2
* total: 3

## dutycycle
* square type: 1
* total 2

## intensity
* volume + fade: 1
* total: 2

## slidepitchto
* duration: 1
* octave + pitch: 1
* total: 3

## vibrato
* delay: 1
* extent + rate: 1
* total: 3

## togglenoise
* drum kit: 1
* total: 2

## volume
* volume: 2
* total: 3

## tone
* adjust frequency: 1
* total: 2

## stereopanning
* left/right: 1
* total: 2

## tempo_relative
* adjust tempo: 1
* total: 2

## setcondition
* condition: 1
* total: 2

## jumpif
* condition: 1
* address: 2
* total: 4

## jumpchannel
* address: 2
* total: 3

## loopchannel
* loop count: 1
* address: 2
* total: 4

## callchannel
* address: 2
* total: 3

## endchannel
* total: 1