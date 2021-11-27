"""Pi Lander.

 * A basic Lunar Lander style game in Pygame Zero
 * Run with 'pgzrun pi_lander.py', control with the LEFT, RIGHT and UP arrow keys
 * Author Tim Martin: www.Tim-Martin.co.uk
 * Licence: Creative Commons Attribution-ShareAlike 4.0 International
 * http://creativecommons.org/licenses/by-sa/4.0/
"""
import random
import math

WIDTH = 800  # Screen width
HEIGHT = 600  # Screen height


def rotated(x, y, angle):
    """Return the vector (x, y) rotated by the given angle (in degrees)."""
    angle = -math.radians(angle)
    sina = math.sin(angle)
    cosa = math.cos(angle)
    return (x * cosa - y * sina, x * sina + y * cosa)


class LandingSpot:
    """A landing pad.

    Each instance defines a landing spot by where it starts, how big it is and
    how many points it's worth.
    """

    # The sizes of landing spots, as a tuple (width, bonus)
    LANDING_SPOT_SIZES = [
        (4, 8),  # small, high bonus
        (10, 4),  # medium, medium bonus
        (20, 2),  # large, low bonus
    ]

    def __init__(self, starting_step):
        self.starting = starting_step
        self.size, self.bonus = random.choice(self.LANDING_SPOT_SIZES)

    def get_within_landing_spot(self, step):
        return self.starting <= step < self.starting + self.size


class Landscape:
    """Stores and generates the landscape, landing spots and star field."""

    # Landscape is broken down into steps.
    # Define number of pixels on the x axis per step.
    step_size = 3

    # How many steps can we fit horizontally on the screen
    world_steps = int(WIDTH/step_size)

    # Controls how bumpy the landscape is
    small_height_change = 3
    # Controls how steep the landscape is
    large_height_change = 10

    # What features to generate
    features = ["mountain", "valley", "field"]

    # How many stars to put in the background
    n_stars = 30

    # Max number of landing spots to generate
    n_spots = 4

    def __init__(self):
        self.world_height = []  # The height of the landscape at each step
        self.star_locations = []  # The x and y location of the stars
        self.landing_spots = []  # The landing spots

    def get_within_landing_spot(self, step):
        """Return True if a given step is within any of the landing spots."""
        return any(
            spot.get_within_landing_spot(step)
            for spot in self.landing_spots
        )

    def get_landing_spot_bonus(self, step):
        for spot in self.landing_spots:
            if spot.get_within_landing_spot(step):
                return spot.bonus
        return 0

    def reset(self):
        """ Generates a new landscape """
        # First: Choose which steps of the landscape will be landing spots
        self.landing_spots.clear()  # Delete any previous LandingSpotClass objects
        next_spot_start = 0

        # Move from left to right adding new landing spots
        for i in range(Landscape.n_spots):
            # Randomly choose location to start landing spot
            next_spot_start += random.randint(10, 50)

            # If we've run out of space, stop
            if next_spot_start >= Landscape.world_steps:
                break

            # Make a new landing object at this spot
            new_landing_spot = LandingSpot(next_spot_start)
            # And store it in our list
            self.landing_spots.append(new_landing_spot)
            # Then take into account its size before choosing the next
            next_spot_start += new_landing_spot.size

        # Second: Randomise the world map
        self.world_height = []
        feature_steps = 0  # Keep track of how many steps we are into a feature

        # Start the landscape between 300 and 500 pixels down
        self.world_height.append(random.randint(300, 500))
        for step in range(1, Landscape.world_steps):
            # If feature_step is zero, we need to choose a new feature
            # and how long it goes on for
            if feature_steps == 0:
                feature_steps = random.randint(25, 75)
                current_feature = random.choice(Landscape.features)

            # Generate the world by setting the range of random numbers.
            # Must be flat if in a landing spot
            if self.get_within_landing_spot(step):
                max_up = 0  # Flat
                max_down = 0  # Flat
            elif current_feature == "mountain":
                max_up = Landscape.small_height_change
                max_down = -Landscape.large_height_change
            elif current_feature == "valley":
                max_up = Landscape.large_height_change
                max_down = -Landscape.small_height_change
            elif current_feature == "field":
                max_up = Landscape.small_height_change
                max_down = -Landscape.small_height_change

            # Generate the next piece of the landscape
            current_height = self.world_height[step - 1]
            next_height = current_height + random.randint(max_down, max_up)
            self.world_height.append(next_height)
            feature_steps -= 1
            # Stop mountains getting too high, or valleys too low
            if next_height > 570:
                current_feature = "mountain"  # Too low! Force a mountain
            elif next_height < 200:
                current_feature = "valley"  # Too high! Force a valley

        # Third: Randomise the star field
        self.star_locations = []
        for i in range(0, self.n_stars):
            star_step = random.randint(0, self.world_steps-1)
            star_x = star_step * self.step_size

            # To keep the stars above the landscape, we only generate them
            # in the sky part of the column
            star_y = random.randint(0, self.world_height[star_step])
            self.star_locations.append((star_x, star_y))


class Ship:
    """Holds the state of the player's ship and handles movement."""

    max_fuel = 1000  # How much fuel the player starts with
    booster_power = 0.05  # Power of the ship's thrusters
    rotate_speed = 10  # How fast the ship rotates in degrees per frame
    gravity = [0., 0.01]  # Strength of gravity in the x and y directions
    leg_length = Landscape.step_size * 3  # Length of the ship's legs

    def __init__(self):
        """Create the variables which will describe the players ship."""
        self.angle = 0  # The angle the ship is facing 0 - 360 degrees
        self.altitude = 0  # The number of pixels the ship is above the ground
        self.booster = False  # True if the player is firing their booster
        self.fuel = 0  # Amount of fuel remaining
        self.position = [0, 0]  # The x and y coordinates of the ship
        self.velocity = [0, 0]  # The x and y velocity of the ship
        self.acceleration = [0, 0]  # The x and y acceleration of the ship

    def reset(self):
        """Set the ships position, velocity and angle to their new-game values."""
        self.position = [750., 100.]  # Always start at the same spot
        self.velocity = [  # But with some initial speed
            -random.random(),
            random.random()
        ]
        self.acceleration = (0, 0)   # No initial thrust
        self.angle = random.randint(0, 360)  # And pointing in a random direction
        self.fuel = Ship.max_fuel  # Fill up fuel tanks

    def rotate_left(self):
        """Rotate the ship to the left."""
        self.angle = (self.angle - self.rotate_speed) % 360

    def rotate_right(self):
        """Rotate the ship to the right."""
        self.angle = (self.angle + self.rotate_speed) % 360

    def booster_on(self):
        """Apply booster accceleration for this frame.

        When booster is firing we accelerate in the opposite direction,
        80 degrees, from the way the ship is facing.
        """
        self.booster = True
        self.acceleration = rotated(0, -Ship.booster_power, self.angle)
        self.fuel -= 2

    def booster_off(self):
        """When the booster is not firing we do not accelerate."""
        self.booster = False
        self.acceleration = (0, 0)

    def update_physics(self):
        """Update the ship.

        Apply acceleration and gravity to the velocity, and velocity to
        the position.
        """
        for axis in (0, 1):
            self.velocity[axis] += Ship.gravity[axis]
            self.velocity[axis] += self.acceleration[axis]
            self.position[axis] += self.velocity[axis]

        # Update player altitude.
        # Note that (LanscapeClass.step_size * 3) is the length of the ship's legs
        x, y = self.position
        ship_step = int(x / Landscape.step_size)
        if ship_step < Landscape.world_steps:
            self.altitude = game.landscape.world_height[ship_step] - y - self.leg_length

    def get_out_of_bounds(self):
        """Check if the player has hit the ground or gone off the sides."""
        return self.altitude <= 0 or not (0 < self.position[0] < WIDTH)

    def draw(self):
        size = Landscape.step_size
        screen.draw.circle(self.position, size * 2, "yellow")  # Draw the player

        x, y = self.position
        # Legs are drawn 45 degrees either side of the ship's angle
        legs = [
            rotated(0, self.leg_length, self.angle - 45),
            rotated(0, self.leg_length, self.angle + 45)
        ]
        for lx, ly in legs:
            screen.draw.line(
                (x, y),
                (x + lx, y + ly),
                color="yellow"
            )
        if self.booster:
            # Booster is drawn under the ship
            flame_x, flame_y = rotated(0, size * 3, self.angle)
            screen.draw.filled_circle((x + flame_x, y + flame_y), size, "orange")


class Game:
    """Hold main game data, including the ship and landscape objects.

    Check for game-over.
    """

    def __init__(self):
        self.time = 0.  # Time spent playing in seconds
        self.score = 0  # Player's score
        self.game_speed = 30  # How fast the game should run in frames per second
        self.time_elapsed = 0.  # Time since the last frame was changed
        self.blink = True  # True if blinking text is to be shown
        self.game_on = False  # True if the game is being played
        self.game_message = "PI   LANDER\nPRESS SPACE TO START"  # Start of game message
        self.ship = Ship()  # Make a object of the ShipClass type
        self.landscape = Landscape()
        self.reset()  # Start the game with a fresh landscape and ship

    def reset(self):
        self.time = 0.
        self.ship.reset()
        self.landscape.reset()

    def check_game_over(self):
        """ Check if the game is over and update the game state if so """
        if not self.ship.get_out_of_bounds():
            return  # Game is not over
        self.game_on = False  # Game has finished. But did we win or lose?
        # Check if the player looses. This is if the ship's angle is > 20 degrees
        # the ship is not over a landing site, is moving too fast or is off the
        # side of the screen
        ship_step = int(self.ship.position[0]/Landscape.step_size)
        if self.ship.position[0] <= 0 \
           or self.ship.position[0] >= WIDTH \
           or not self.landscape.get_within_landing_spot(ship_step) \
           or abs(self.ship.velocity[0]) > .5 \
           or abs(self.ship.velocity[1]) > .5 \
           or (self.ship.angle > 20 and self.ship.angle < 340):
            self.game_message = (
                "YOU JUST DESTROYED A 100 MEGABUCK LANDER\n\n"
                + "LOSE 250 POINTS\n\n"
                + "PRESS SPACE TO RESTART"
            )
            self.score -= 250
        else:
            # The player has won! Update their score based on the amount of
            # remaining fuel and the landing bonus.
            points = self.ship.fuel / 10
            points *= self.landscape.get_landing_spot_bonus(ship_step)
            self.score += points
            self.game_message = (
                "CONGRATULATIONS\n"
                + "THAT WAS A GREAT LANDING!\n\n"
                + "{} POINTS\n\n"
                + "PRESS SPACE TO RESTART"
            ).format(round(points))


# Create the game object
game = Game()


def draw():
    """
    Draw the game window on the screen in the following order:
    start message, mountain range, bonus points, stars, statistics, player's ship
    """
    screen.fill("black")
    size = Landscape.step_size

    if not game.game_on:
        screen.draw.text(game.game_message, center=(WIDTH/2, HEIGHT/5), align="center")

    # Get the x and y coordinates of each step of the landscape and draw it as a
    # straight line
    for step in range(0, game.landscape.world_steps - 1):
        x_start = size * step
        x_end = size * (step + 1)
        y_start = game.landscape.world_height[step]
        y_end = game.landscape.world_height[step + 1]
        screen.draw.line((x_start, y_start), (x_end, y_end), "white")
        # Every second we flash the landing spots with a thicker line by drawing
        # a narrow rectangle
        if (game.blink or not game.game_on) \
                and game.landscape.get_within_landing_spot(step):
            screen.draw.filled_rect(
                Rect(x_start - size, y_start-1, size, 3),
                "white"
            )

    # Draw the bonus point notifier
    if game.blink or not game.game_on:
        for spot in game.landscape.landing_spots:
            x_text = spot.starting * size
            y_text = game.landscape.world_height[spot.starting]
            y_text += 10  # Add 10 pixels to put the text below the landscape
            screen.draw.text(str(spot.bonus) + "x", (x_text, y_text), color="white")

    # Draw the stars
    for star in game.landscape.star_locations:
        screen.draw.line(star, star, "white")

    # Draw the stats
    stats_left = [
        f"SCORE: {round(game.score)}",
        f"TIME: {round(game.time)}",
        f"FUEL: {game.ship.fuel}",
    ]
    vx, vy = game.ship.velocity
    stats_right = [
        f"ALTITUDE: {round(game.ship.altitude)}",
        f"HORIZONTAL SPEED: {vx:.2f}",
        f"VERTICAL SPEED: {-vy:.2f}",
    ]
    y = 10
    for left, right in zip(stats_left, stats_right):
        screen.draw.text(
            left,
            (10, y),
            color="white",
            background="black"
        )
        screen.draw.text(
            right,
            (WIDTH - 230, y),
            color="white",
            background="black"
        )
        y += 15

    game.ship.draw()


def blink():
    game.blink = not game.blink


clock.schedule_interval(blink, 1)


def update(deltatime):
    """ Updates the game physics 30 times every second  """
    game.time_elapsed += deltatime
    if game.time_elapsed < 1./game.game_speed:
        return  # A 30th of a second has not passed yet
    game.time_elapsed -= 1./game.game_speed

    # Start the game if the player presses space when the game is not on
    if keyboard.space and not game.game_on:
        game.game_on = True
        game.reset()
    elif not game.game_on:
        return

    # If the game is on, update the movement and the physics
    if keyboard.left:  # Change space ship rotation
        game.ship.rotate_left()
    elif keyboard.right:
        game.ship.rotate_right()

    if keyboard.up and game.ship.fuel > 0:
        # Fire boosters if the player has enough fuel
        game.ship.booster_on()
    else:
        game.ship.booster_off()

    game.time += deltatime
    game.ship.update_physics()
    game.check_game_over()
