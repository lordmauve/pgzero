def show_keystate():
    print(keyboard._pressed)


clock.schedule_interval(show_keystate, 0.1)
