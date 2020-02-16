WIDTH = 200
HEIGHT = 300

INSTRUCTIONS = """\
===================================
Move player left and right with A and D.
Pause and resume the top left explosion with P.
Trigger the bottom left explosion with B.
Move back and forth through the bottom right explosion images
with the left and right arrows.
"""

pauseable = Actor('explosion3', (50, 50))
constant = Actor('explosion3', (150, 50))
temporary = Actor('explosion3', (50, 150))
manual = Actor('explosion3', (150, 150))
player = Actor('girl_walk1_right', midbottom=(WIDTH // 2, HEIGHT))
actors = [pauseable, constant, temporary, manual, player]

images = ['explosion3', 'explosion2', 'explosion1']
walk_right = ['girl_walk1_right', 'girl_walk2_right']
walk_left = ['girl_walk1_left', 'girl_walk2_left']

def remove_boom3():
    actors.remove(temporary)

# An animation that can be paused with the P key (see on_key_down)
pausable_anim = animate.images(pauseable, images, every=0.4, source='clock')
# An animation that will run constantly
animate.images(constant, images, every=0.8, source='clock')
# An animation that is triggered by the B key and runs 3 times
temp_anim = animate.images(temporary, images, every=0.4, source='clock',
        autostart=False, limit=3, on_finished=remove_boom3)
# An animation that only runs based on direct input
manual_anim = animate.images(manual, images)
# An animation with two sets of images (for increasing and decreasing value)
# Used to animate a character walking left and right
animate.images(player, walk_left, walk_right, every=20, source='actor_x')

def draw():
    screen.clear()
    for actor in actors:
        actor.draw()

def update():
    if keyboard.a:
        player.x -= 2
    elif keyboard.d:
        player.x += 2

def on_key_down(key):
    if key == keys.P:
        if pausable_anim.running:
            pausable_anim.stop()
        else:
            pausable_anim.start()
    elif key == keys.B:
        temp_anim.start()
    elif key == keys.LEFT:
        manual_anim.prev()
    elif key == keys.RIGHT:
        manual_anim.next()

print(INSTRUCTIONS)

