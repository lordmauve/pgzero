from pygame.mixer import music as _music
from .loaders import ResourceLoader
from . import constants


__all__ = [
    'rewind', 'stop', 'fadeout', 'set_volume', 'get_volume', 'get_pos',
    'set_pos', 'play', 'queue', 'pause', 'unpause',
]

_music.set_endevent(constants.MUSIC_END)

#뮤직로더 클래스, 음악을 정해진 경로를 확인하여 불러온다.
class _MusicLoader(ResourceLoader):
    """Pygame's music API acts as a singleton with one 'current' track.

    No objects are returned that represent different tracks, so this loader
    can't return anything useful. But it can perform all the path name
    validations and return the validated path, so that's what we do.

    This loader should not be exposed to the user.

    """
    EXTNS = ['mp3', 'ogg', 'oga']
    TYPE = 'music'

    #경로 불러오기.
    def _load(self, path):
        return path

#경로 music의 뮤직로더를 생성
_loader = _MusicLoader('music')


# State of whether we are paused or not
#멈추거나 재생하는 상태를 가진 부울값
_paused = False

#음악 재생하는 내부함수
def _play(name, loop):
    global _paused 
    path = _loader.load(name) #로더의 경로를 가져온다.
    _music.load(path) #경로의 음악을 불러온다.
    _music.play(loop) #음악을 loop수만큼 재생
    _paused = False #상태는 재생

#음악 무한 재생
def play(name):
    """Play a music file from the music/ directory.

    The music will loop when it finishes playing.

    """
    _play(name, -1)

#음악 1회 재생
def play_once(name):
    """Play a music file from the music/ directory."""
    _play(name, 0)

#재생대기열 추가
def queue(name):
    """Queue a music file to follow the current track.

    This will load a music file and queue it. A queued music file will begin as
    soon as the current music naturally ends. If the current music is ever
    stopped or changed, the queued song will be lost.

    """
    path = _loader.load(name)
    _music.queue(path) #뮤직 큐에 경로에 있는거 넣기

#재생중인가?
def is_playing(name):
    """Return True if the music is playing and not paused."""
    return _music.get_busy() and not _paused #재생중이면 True값 리턴

#정지함수
def pause():
    """Temporarily stop playback of the music stream.

    Call `unpause()` to resume.

    """
    global _paused
    _music.pause() #음악을 멈춘다.
    _paused = True #멈춤상태로 변경

#다시재생
def unpause():
    """Resume playback of the music stream after it has been paused."""
    global _paused
    _music.unpause() #다시재생한다
    _paused = False #재생상태로 변경

#페이드아웃
def fadeout(seconds):
    """Fade out and eventually stop the music playback.

    :param seconds: The duration in seconds over which the sound will be faded
                    out. For example, to fade out over half a second, call
                    ``music.fadeout(0.5)``.

    """
    _music.fadeout(int(seconds * 1000)) #입력받은 seconds의 시간만큼 페이드아웃하고 멈춘다.

#다시 재생하기
def rewind():
    _music.rewind()

#완전히 정지
def stop():
    _music.stop()

#볼륨 지정
def set_volume(value):
    volume = _music.get_volume()
    _music.set_volume(volume + value)


get_pos = _music.get_pos
set_pos = _music.set_pos
