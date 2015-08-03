import random, math

"""
Pi Lander
 * A basic Lunar Lander style game in Pygame Zero
 * Run with 'pgzrun pi_lander.py', control with the LEFT, RIGHT and UP arrow keys
 * Author Tim Martin: www.Tim-Martin.co.uk
 * Licence: Creative Commons Attribution-ShareAlike 4.0 International
 * http://creativecommons.org/licenses/by-sa/4.0/
"""

WIDTH = 800 # Screen width
HEIGHT = 600 # Screen height

class LandingSpotClass:
    """ Each instance defines a landing spot by where it starts, how big it is and how many points it's worth """
    landing_spot_sizes = ["small", "medium", "large"]
    def __init__(self, starting_step):
        self.starting = starting_step
        random_size = random.choice(LandingSpotClass.landing_spot_sizes) # And randomly choose size
        if random_size == "small":
            self.size = 4
            self.bonus = 8
        elif random_size == "medium":
            self.size = 10
            self.bonus = 4
        else: # Large
            self.size = 20
            self.bonus = 2
    def get_within_landing_spot(self, step):
        if (step >= self.starting) and (step < self.starting + self.size):
            return True
        return False

class LandscapeClass:
    """ Stores and generates the landscape, landing spots and star field """
    step_size = 3 # Landscape is broken down into steps. Define number of pixels on the x axis per step.
    world_steps = int(WIDTH/step_size) # How many steps can we fit horizontally on the screen
    small_height_change = 3 # Controls how bumpy the landscape is
    large_height_change = 10 # Controls how steep the landscape is
    features = ["mountain","valley","field"] # What features to generate
    n_stars = 30 # How many stars to put in the background
    n_spots = 4 # Max number of landing spots to generate
    def __init__(self):
        self.world_height = [] # Holds the height of the landscape at each step
        self.star_locations = [] # Holds the x and y location of the stars
        self.landing_spots = [] # Holds the landing spots
    def get_within_landing_spot(self, step):
        """ Calculate if a given step is within any of the landing spots """
        for spot in self.landing_spots:
            if spot.get_within_landing_spot(step) == True:
                return True
        return False
    def get_landing_spot_bonus(self, step):
        for spot in self.landing_spots:
            if spot.get_within_landing_spot(step) == True:
                return spot.bonus
        return 0
    def reset(self):
        """ Generates a new landscape """
        # First: Choose which steps of the landscape will be landing spots
        del self.landing_spots[:] # Delete any previous LandingSpotClass objects
        next_spot_start = 0
        # Move from left to right adding new landing spots until either
        # n_spots spots have been placed or we run out of space in the world
        while len(self.landing_spots) < LandscapeClass.n_spots and next_spot_start < LandscapeClass.world_steps:
            next_spot_start += random.randint(10, 50) # Randomly choose location to start landing spot
            new_landing_spot = LandingSpotClass(next_spot_start) # Make a new landing object at this spot
            self.landing_spots.append( new_landing_spot ) # And store it in our list
            next_spot_start += new_landing_spot.size # Then take into account its size before choosing the next
        # Second: Randomise the world map
        del self.world_height[:] # Clear any previous world height data
        feature_steps = 0 # Keep track of how many steps we are into a feature
        self.world_height.append(random.randint(300, 500)) # Start the landscape between 300 and 500 pixels down
        for step in range(1, LandscapeClass.world_steps):
            # If feature_step is zero, we need to choose a new feature and how long it goes on for
            if feature_steps == 0:
                feature_steps = random.randint(25, 75)
                current_feature = random.choice(LandscapeClass.features)
            # Generate the world by setting the range of random numbers, must be flat if in a landing spot
            if self.get_within_landing_spot(step) == True:
                max_up = 0 # Flat
                max_down = 0 # Flat
            elif current_feature == "mountain":
                max_up = LandscapeClass.small_height_change
                max_down = -LandscapeClass.large_height_change
            elif current_feature == "valley":
                max_up = LandscapeClass.large_height_change
                max_down = -LandscapeClass.small_height_change
            elif current_feature == "field":
                max_up = LandscapeClass.small_height_change
                max_down = -LandscapeClass.small_height_change
            # Generate the next piece of the landscape
            current_height = self.world_height[step-1]
            next_height = current_height + random.randint(max_down, max_up)
            self.world_height.append(next_height)
            feature_steps -= 1
            # Stop mountains getting too high, or valleys too low
            if next_height > 570:
                current_feature = "mountain" # Too low! Force a mountain
            elif next_height < 200:
                current_feature = "valley" # Too high! Force a valley
        # Third: Randomise the star field
        del self.star_locations[:]
        for star in range(0, LandscapeClass.n_stars):
            star_step = random.randint(0, LandscapeClass.world_steps-1)
            star_x = star_step * LandscapeClass.step_size
            star_y = random.randint( 0, self.world_height[star_step] ) # Keep the stars above the landscape
            self.star_locations.append( (star_x, star_y) )

class ShipClass:
    """ Holds the state of the player's ship and handles movement """
    max_fuel = 1000 # How much fuel the player starts with
    booster_power = 0.05 # Power of the ship's thrusters
    rotate_speed = 10 # How fast the ship rotates in degrees per frame
    gravity = [0., 0.01] # Strength of gravity in the x and y directions
    def __init__(self):
        """ Create the variables which will describe the players ship """
        self.angle = 0 # The angle the ship is facing 0 - 360 degrees
        self.altitude = 0 # The number of pixels the ship is above the ground
        self.booster = False # True if the player is firing their booster
        self.fuel = 0 # Amount of fuel remaining
        self.position = [0,0] # The x and y coordinates of the players ship
        self.velocity = [0,0] # The x and y velocity of the players ship
        self.acceleration = [0,0] # The x and y acceleration of the players ship
    def reset(self):
        """ Set the ships position, velocity and angle to their new-game values """
        self.position = [750., 100.] # Always start at the same spot
        self.velocity = [ -random.random(), random.random() ] # But with some initial speed
        self.acceleration = [0., 0.] # No initial acceleration (except gravity of course)
        self.angle = random.randint(0, 360) # And pointing in a random direction
        self.fuel = ShipClass.max_fuel # Fill up fuel tanks
    def rotate(self, direction):
        """ Rotate the players ship and keep the angle within the range 0 - 360 degrees """
        if direction == "left":
            self.angle -= ShipClass.rotate_speed
        elif direction == "right":
            self.angle += ShipClass.rotate_speed
        if self.angle > 360: # Remember than adding or subtracting 360 degrees does not change the angle
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
    def booster_on(self):
        """ When booster is firing we accelerate in the opposite direction, 180 degrees, from the way the ship is facing """
        self.booster = True
        self.acceleration[0] = ShipClass.booster_power * math.sin( math.radians(self.angle + 180) )
        self.acceleration[1] = ShipClass.booster_power * math.cos( math.radians(self.angle + 180) )
        self.fuel -= 2;
    def booster_off(self):
        """ When the booster is not firing we do not accelerate """
        self.booster = False
        self.acceleration[0] = 0.
        self.acceleration[1] = 0.
    def update_physics(self):
        """ Update ship physics in X and Y, apply acceleration (and gravity) to the velocity and velocity to the position """
        for axis in range(0,2):
            self.velocity[axis] += ShipClass.gravity[axis]
            self.velocity[axis] += self.acceleration[axis]
            self.position[axis] += self.velocity[axis]
        # Update player altitude. Note that (LanscapeClass.step_size * 3) is the length of the ship's legs
        ship_step = int(self.position[0]/LandscapeClass.step_size)
        if ship_step < LandscapeClass.world_steps:
            self.altitude = game.landscape.world_height[ship_step] - self.position[1] - (LandscapeClass.step_size * 3)
    def get_out_of_bounds(self):
        """ Check if the player has hit the ground or gone off the sides """
        if self.altitude <= 0 or self.position[0] <= 0 or self.position[0] >= WIDTH:
            return True
        return False

class GameClass:
    """ Holds main game data, including the ship and landscape objects. Checks for game-over """
    def __init__(self):
        self.time = 0. # Time spent playing in seconds
        self.score = 0 # Player's score
        self.game_speed = 30 # How fast the game should run in frames per second
        self.time_elapsed = 0. # Time since the last frame was changed
        self.blink = True # True if blinking text is to be shown
        self.n_frames = 0 # Number of frames processed
        self.game_on = False # True if the game is being played
        self.game_message = "PI   LANDER\nPRESS SPACE TO START" # Start of game message
        self.ship = ShipClass() # Make a object of the ShipClass type
        self.landscape = LandscapeClass()
        self.reset() # Start the game with a fresh landscape and ship
    def reset(self):
        self.time = 0.
        self.ship.reset()
        self.landscape.reset()
    def check_game_over(self):
        """ Check if the game is over and update the game state if so """
        if self.ship.get_out_of_bounds() == False:
            return # Game is not over
        self.game_on = False # Game has finished. But did we win or loose?
        # Check if the player looses. This is if the ship's angle is > 20 degrees
        # the ship is not over a landing site, is moving too fast or is off the side of the screen
        ship_step = int(self.ship.position[0]/LandscapeClass.step_size)
        if self.ship.position[0] <= 0 \
           or self.ship.position[0] >= WIDTH \
           or self.landscape.get_within_landing_spot(ship_step) == False \
           or abs(self.ship.velocity[0]) > .5 \
           or abs(self.ship.velocity[1]) > .5 \
           or (self.ship.angle > 20 and self.ship.angle < 340):
            self.game_message = "YOU JUST DESTROYED A 100 MEGABUCK LANDER\n\nLOOSE 250 POINTS\n\nPRESS SPACE TO RESTART"
            self.score -= 250
        else: # If the player has won! Update their score based on the amount of remaining fuel and the landing bonus
            points = self.ship.fuel / 10
            points *= self.landscape.get_landing_spot_bonus(ship_step)
            self.score += points
            self.game_message = "CONGRATULATIONS\nTHAT WAS A GREAT LANDING!\n\n" + str(round(points)) + " POINTS\n\nPRESS SPACE TO RESTART"

# Create the game object
game = GameClass()

def draw():
    """
    Draw the game window on the screen in the following order:
    start message, mountain range, bonus points, stars, statistics, player's ship
    """
    screen.fill("black")
    size = LandscapeClass.step_size

    if game.game_on == False:
        screen.draw.text(game.game_message, center=(WIDTH/2, HEIGHT/5), align="center")

    # Get the x and y coordinates of each step of the landscape and draw it as a straight line
    for step in range(0, game.landscape.world_steps - 1):
        x_start = size * step
        x_end   = size * (step + 1)
        y_start = game.landscape.world_height[step]
        y_end   = game.landscape.world_height[step + 1]
        screen.draw.line( (x_start, y_start), (x_end, y_end), "white" )
        # Every second we flash the landing spots with a thicker line by drawing a narrow rectangle
        if (game.blink == True or game.game_on == False) and game.landscape.get_within_landing_spot(step) == True:
            screen.draw.filled_rect( Rect(x_start-size, y_start-1, size, 3), "white" )

    # Draw the bonus point notifier
    if game.blink == True or game.game_on == False:
        for spot in game.landscape.landing_spots:
            x_text = spot.starting * size
            y_text = game.landscape.world_height[ spot.starting ] + 10 # The extra 10 pixels puts the text below the landscape
            screen.draw.text(str(spot.bonus) + "x", (x_text,y_text), color="white")

    # Draw the stars
    for star in game.landscape.star_locations:
        screen.draw.line( star, star, "white" )

    # Draw the stats
    screen.draw.text("SCORE: " + str(round(game.score)), (10,10), color="white", background="black")
    screen.draw.text("TIME: " + str(round(game.time)), (10,25), color="white", background="black")
    screen.draw.text("FUEL: " + str(game.ship.fuel), (10,40), color="white", background="black")
    screen.draw.text("ALTITUDE: " + str(round(game.ship.altitude)), (WIDTH-230,10), color="white", background="black")
    screen.draw.text("HORIZONTAL SPEED: {0:.2f}".format(game.ship.velocity[0]), (WIDTH-230,25), color="white", background="black")
    screen.draw.text("VERTICAL SPEED: {0:.2f}".format(-game.ship.velocity[1]), (WIDTH-230,40), color="white", background="black")

    screen.draw.circle( game.ship.position, size*2, "yellow" ) # Draw the player
    # Use sin and cosine functions to draw the ship legs and booster at the correct angle
    # Requires the values in radians (0 to 2*pi) rather than in degrees (0 to 360)
    sin_angle = math.sin( math.radians(game.ship.angle - 45) ) # Legs are drawn 45 degrees either side of the ship's angle
    cos_angle = math.cos( math.radians(game.ship.angle - 45) )
    screen.draw.line( game.ship.position, (game.ship.position[0] + (sin_angle*size*3), game.ship.position[1] + (cos_angle*size*3)), "yellow" )
    sin_angle = math.sin( math.radians(game.ship.angle + 45) )
    cos_angle = math.cos( math.radians(game.ship.angle + 45) )
    screen.draw.line( game.ship.position, (game.ship.position[0] + (sin_angle*size*3), game.ship.position[1] + (cos_angle*size*3)), "yellow" )
    if game.ship.booster == True:
        sin_angle = math.sin( math.radians(game.ship.angle) ) # Booster is drawn at the same angle as the ship, just under it
        cos_angle = math.cos( math.radians(game.ship.angle) )
        screen.draw.filled_circle( (game.ship.position[0] + (sin_angle*size*3), game.ship.position[1] + (cos_angle*size*3)), size, "orange" )

def update(detlatime):
    """ Updates the game physics 30 times every second  """
    game.time_elapsed += detlatime
    if game.time_elapsed < 1./game.game_speed:
        return # A 30th of a second has not passed yet
    game.time_elapsed -= 1./game.game_speed

    # New frame - do all the simulations
    game.n_frames += 1
    if game.n_frames % game.game_speed == 0: # If n_frames is an exact multiple of the game FPS: so once per second
        game.blink = not game.blink # Invert blink so True becomes False or False becomes True

    # Start the game if the player presses space when the game is not on
    if keyboard.SPACE and game.game_on == False:
        game.game_on = True
        game.reset()
    elif game.game_on == False:
        return

    # If the game is on, update the movement and the physics
    if keyboard.LEFT: # Change space ship rotation
        game.ship.rotate("left")
    elif keyboard.RIGHT:
        game.ship.rotate("right")

    if keyboard.UP and game.ship.fuel > 0: # Fire boosters if the player has enough fuel
        game.ship.booster_on()
    else:
        game.ship.booster_off()

    game.time += detlatime
    game.ship.update_physics()
    game.check_game_over()
