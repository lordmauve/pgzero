"""Identify WAV file formats.

This is used only to give better error messages in the event that a sound
file is not loadable by Pygame.

This is based on the 'magic' information for the 'file' command, at

https://github.com/file/file/blob/86e34444a26860f2ad9895a2d77cb16d1ca4c48b/magic/Magdir/riff

"""

from struct import unpack_from


class MagicReader:
    """Interface to reading the magic numbers in a file's header."""
    def __init__(self, path):
        with open(path, 'rb') as f:
            self.bytes = f.read(64 * 1024)

    def read_bytes(self, offset, length=4):
        return self.bytes[offset:offset + length]

    def read_leshort(self, offset):
        """Read an unsigned short at the given offset."""
        return unpack_from('<H', self.bytes, offset)[0]

    def read_lelong(self, offset):
        """Read an unsigned long at the given offset."""
        return unpack_from('<L', self.bytes, offset)[0]


CODECS = {
    1: 'Microsoft PCM',
    2: 'Microsoft ADPCM',
    3: 'PCM (float)',
    6: 'ITU G.711 A-law',
    7: 'ITU G.711 µ-law',
    8: 'Microsoft DTS',
    17: 'IMA ADPCM',
    20: 'ITU G.723 ADPCM (Yamaha)',
    34: 'DSP Group Truespeech',
    49: 'GSM 6.10',
    64: 'ITU G.721 ADPCM',
    80: 'MPEG',
    85: 'MP3',
    112: 'Lernout & Hauspie CELP',
    114: 'Lernout & Hauspie SBC',
    0x2001: 'DTS',
}


def riff_wave(f, offset):
    """Read the WAVE format information."""
    encoding = f.read_leshort(offset)
    yield CODECS.get(encoding, 'unknown encoding %d' % encoding)
    if encoding in (1, 3):
        bitrate = f.read_leshort(offset + 14)
        if 0 < bitrate < 1024:
            yield '%d bit' % bitrate
    channels = f.read_leshort(offset + 2)
    if channels == 1:
        yield 'mono'
    elif channels == 2:
        yield 'stereo'
    elif 2 < channels < 128:
        yield '%d channels' % channels

    hz = f.read_lelong(offset + 4)
    if 0 < hz < 1000000:
        yield '%d Hz' % hz


def riff_walk(f, offset):
    """Search chunks trying to find b'fmt '"""
    chunk = f.read_bytes(offset)
    if chunk == b'fmt ':
        if f.read_lelong(offset + 4) < 0x80:
            return list(riff_wave(f, offset + 8))
    elif chunk[:3] == b'VP8':
        return ['VP8 encoding']
    elif chunk in (b'LIST', b'DISP', b'bext', b'Fake', b'fact'):
        off = f.read_lelong(offset + 4)
        return riff_walk(f, off + 4)
    return ["Unknown WAVE encoding"]


def identify(path):
    f = MagicReader(path)
    if f.read_bytes(0) != b'RIFF':
        return 'Unknown format (not RIFF WAVE)'

    if f.read_bytes(8) != b'WAVE':
        return 'Unknown RIFF format (not WAVE)'

    return 'WAV audio encoded as ' + ', '.join(riff_walk(f, 12))


if __name__ == '__main__':
    import sys
    tabstop = max(len(a) for a in sys.argv[1:]) + 1
    for path in sys.argv[1:]:
        sndfmt = identify(path)
        print(('%s:' % path).ljust(tabstop), sndfmt)
