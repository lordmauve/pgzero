import pygame
from pgzero.actor import Actor
from pgzero import loaders
import time
from typing import List, Sequence, Callable
from ._common import _CanBeRect
from .rect import ZRect
from .clock import each_tick, unschedule


class FramesList:

    def __init__(self, **kwargs):
        self._imgs: List[pygame.Surface] = []
        self._rects: List[ZRect] = []
        pass

    def addFromSheet(self, sheet_name: str, cols: int, rows: int, cnt: int = 0,
                     subrect: _CanBeRect = None):
        sheet: pygame.Surface = loaders.images.load(sheet_name)
        if subrect is not None:
            sheet = sheet.subsurface(subrect)
        i = 0
        for row in range(0, rows):
            for col in range(0, cols):
                if cnt != 0 and i == cnt:
                    return
                width = sheet.get_width()/cols
                height = sheet.get_height()/rows
                self._rects.append((int(col*width), int(row*height),
                                   int(width), int(height)))
                self._imgs.append(sheet_name)
                i += 1

    def addFromList(self, frame_images: Sequence[str]):
        for imgName in frame_images:
            self._rects.append(None)
            self._imgs.append(imgName)

    def add(self, image: str, subrect: _CanBeRect = None):
        self.frames_rects.append(subrect)
        self.frames_imgs.append(image)

    def __len__(self) -> int:
        return len(self._imgs)


class FrameBasicAnimation:
    def __init__(self, actor: Actor, frames: FramesList):
        self._idx: int = 0
        self._actor = actor
        self._actor_subrect = None
        self._actor_image = None
        self._actor = actor
        self._frames = frames

    def store_actor_image(self):
        self._actor_subrect = self._actor.subrect
        self._actor_image = self._actor.image

    def restore_actor_image(self):
        self._actor.image = self._actor_image
        self._actor.subrect = self._actor_subrect

    def sel_frame(self, idx):
        idx = idx % len(self._frames)
        if (self._idx != idx):
            self._idx = idx
            self._actor.image = self._frames._imgs[self._idx]
            self._actor.subrect = self._frames._rects[self._idx]

    def next_frame(self) -> int:
        self._idx = (self._idx+1) % len(self._frames)
        self.sel_frame(self._idx)
        return self._idx

    def prev_frame(self) -> int:
        self._idx = (self._idx-1) % len(self._frames)
        self.sel_frame(self._idx)
        return self._idx


class FrameAnimation(FrameBasicAnimation):
    def __init__(self, actor: Actor, frames: FramesList, fps: int,
                 restore_image_at_stop: bool = True):
        self._time_start = 0
        self._time = 0
        self._restore_image_at_stop = restore_image_at_stop
        self.fps = fps
        self._stop_at_loop = -1
        self._stop_at_index = -1
        self._duration = 0
        self._running = False
        self._finished = False
        super().__init__(actor, frames)

    def animate(self, dt=-1) -> (int, int):
        # calculate elapsed time
        if dt == -1:
            now = time.time()
            if self._time_start == 0:
                self._time_start = now
            self._time = now - self._time_start
        else:
            self._time = self._time + dt

        # go to next frame base on elapsed time
        frame_idx = int(self._time * self.fps) % len(self._frames)
        loop = int(self._time * self.fps) // len(self._frames)
        self.sel_frame(frame_idx)

        # check stop condition
        if self._duration != 0:
            if self._time > self._duration:
                self.stop(True)
        else:
            if (self._stop_at_loop != -1
                    and loop >= self._stop_at_loop and frame_idx >= self._stop_at_idx):
                self.stop(True)

        return (loop, frame_idx)

    def play(self, stop_at_loop: int = -1, stop_at_idx: int = -1, duration: float = 0,
             on_finished: Callable = None) -> bool:
        if self._running:
            return False
        self._duration = duration
        self._running = True
        self._finished = False
        self.on_finished = on_finished
        self._stop_at_loop = stop_at_loop
        self._stop_at_idx = stop_at_idx
        self.store_actor_image()
        each_tick(self.animate)
        return True

    def play_once(self, on_finished: Callable = None):
        self.play(0, len(self._frames)-1, on_finished=on_finished)

    def play_several(self, nbr_of_loops: int, on_finished: Callable = None):
        self.play(nbr_of_loops-1, len(self._frames)-1, on_finished=on_finished)

    def play_during(self, duration: int, on_finished: Callable = None):
        self.play(duration=duration, on_finished=on_finished)
        
    def play_infinite(self):
        self.play()

    def pause(self):
        if not self._paused:
            unschedule(self.animate)
            self._paused = True

    def unpause(self):
        if self._paused:
            each_tick(self.animate)
            self._paused = False

    def stop(self, call_on_finished: bool = False):
        unschedule(self.animate)
        self._running = False
        self._finished = True
        self._paused = False
        if self._restore_image_at_stop:
            self.restore_actor_image()
        if call_on_finished and self.on_finished:
            argcount = self.on_finished.__code__.co_argcount
            if argcount == 0:
                self.on_finished()
            elif argcount == 1:
                self.on_finished(self._actor)
