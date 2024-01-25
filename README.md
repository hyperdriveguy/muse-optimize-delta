# Muse-optimize delta
A program for optimizing assembly macros for music output by [Muse2pokecrystal](https://github.com/nephitejnf/muse2pokecrystal).
All optimizations are for code size, not speed. The algorithms take a while, but multiple optimization strategies are executed in parallel.

## Usage
* `--mono` strips all panning and makes it so the song is mono only.
* `--agressive` is intended to make the look-ahead algorithm more strict, thus potentially getting better optimizations.
  * TODO: fix spelling in code and documentation
