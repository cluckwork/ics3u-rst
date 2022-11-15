# Pellet Game - ICS3UC RST
A game about avoiding pellets, made with Pygame by Roman Daher.

## Concept
The object of this game is to avoid the projectiles for as long as possible. More projectiles spawn as time progresses, and touching a projectile will cause you to lose one of your 3 lives. The game ends once you lose all of your lives. 

Points begin at zero and increment by one every second. Points have no applications in the game but they serve as a metric for your achievement while playing.

## Controls
- Arrow Keys - Move Player
- Spacebar (Hold) - Dash
  
## Player
### Human
`entities.Human` is a class that is responsible for representing the player visually. The `Human` constructor requires 3 parameters, being `colour`, `xywh`, and `velocity`. `colour` is a tuple with (R,G,B) values, `xywh`is a tuple with (x,y,width,height) that indicates the coordinates and size of the `Human`, and `velocity` is an integer that indicates speed. 

### Movement
The `Human` object has two methods that let the user control its movement. Firstly, it has `Human.walk()`. This function has a parameter, `keys`, which is the dictionary returned by `pygame.key.get_pressed()` repeatedly called each frame. `walk()` will check the dictionary keys based on the arrow keys, which are `pygame.K_UP`, `pygame.K_RIGHT`, etc. `pygame.key.get_pressed()` assigns boolean values to each key that is pressed, so `walk()` will check each key and if their value is true, it will add or subtract `Human.velocity` from the appropriate coordinate (up/down affects y coordinate, right/left affects x coordinate). This makes velocity easy to adjust as a smaller velocity will make the key affect the character less every frame and vice versa. Movement also considers the boundaries of the screen. The `walk()` function will not let the `Human` object surpass `0`-`cf.SCREEN_WIDTH` on the x-axis, and `0`-`cf.SCREEN_HEIGHT` on the y-axis. After the `Human` object's coordinates are adjusted, it is redrawn in the main loop with `Human.draw()` every frame, which is a function that curries `pygame.draw.rect()` by supplying properties of the `Human` object.
  
### Movement - Dashing
`Human.walk()` also checks if the player is holding down the spacebar. While the player is holding down the spacebar, the player expends "boost". Boost is stored in the `Human` object as `self.boost`, which is initialized to `cf.PLAYER_BOOST`. `self.boost` does not fall below 0 or go above `cf.PLAYER_BOOST`, and when the player isn't holding down the spacebar `self.boost` increments by `cf.PLAYER_BOOST_REGEN`. While spacebar is being held, `self.boost` decrements by `cf.PLAYER_BOOST_DECAY`. While the player is dashing, the player's velocity is doubled and the player is invincible to projectiles. The `Human`'s `self.colour` also changes to blue, to provide a visual representation of dashing. 

## Projectiles
### CircleProjectile
`entities.CircleProjectile` is a class that is responsible for representing projectiles visually. The `CircleProjectile` constructor requires 4 parameters, being `colour`, `radius`, `velocity`, and `dir`. `colour` is a tuple with (R,G,B) values, `radius` is the radius of the projectile, `velocity` is an integer that gives the speed of the projectile, and `dir` is an integer that denotes the direction of the projectile.

### Projectile Spawning
Projectile spawning is handled by the function `game_events.spawn_pellet()`. This function has one parameter, `delta`, which is a float that represents time elapsed in seconds. This function uses the mathematical function `S(t) = math.e ** (t * math.log(3) * (1/70))` which is an exponential function that gives a real non-negative number. `random.uniform()` is then used to get a random real number from 0 to `S(t)`. This number is then compared against `cf.SPAWN_RATE`, and if the random number is greater than that value then a pellet will spawn. Since `S(t)` continuously gets larger with `t`, the pellets are more likely to spawn in an exponential fashion as `t` becomes larger. `cf.SPAWN_RATE` can also be easily adjusted to  increase the probability that a projectile spawns, since it increases the margin of numbers that will trigger a projectile spawning. If the function spawns a projectile, it returns a new `entities.CircleProjectile` object that is appended to a global list in `main.py`.

### Projectile Movement - Generating Values
Projectiles have a 50/50 chance to spawn from either the left or right side of the screen. From here, the projectiles will move either right or left at a constant speed so they cross the screen. This constant speed is determined by generating a random real number between `3` and `cf.PELLET_VELOCITY`. Projectiles also have an angle at which they move determined by generating a random real number between `-3` and `3`.  These are passed into the `entities.CircleProjectile` constructor that is returned in `game_events.spawn_projectile()`.

### Projectile Movement - Moving the Projectiles
_`entities.CircleProjectile` is abbreviated as `CP` in this article_

Projectile movement is created by adjusting the spawn position of the projectiles and redrawing them every frame. This is accomplished using two methods of `CP`, `CP.move()`, and `CP.draw()`. `CP.move()` is responsible for adjusting `CP.y` and `CP.x` (the 2D coordinates of the projectile). By adding the velocity of the projectile to `CP.x`, and adding the angle of the projectile to `CP.y`, it adjusts the projectile's position according to its velocity and angle accordingly. This is done every frame, by iterating over the list of all projectiles in the game loop and calling `CP.move()` on every object. In the same loop, `CP.draw()` is called on these objects which creates the circle on the screen. Similarly to `Human.draw()`, `CP.draw()` is merely a curried `pygame.draw.circle()` that supplies properties of `CP`.

### Projectile Collision
Projectile collision occurs when a projectile overlaps the character. Every frame, after the `CircleProjectile`s have moved, the `game_events.collision()` function is called. This function takes two parameters, a `Human` object, and a list of `CircleProjectile` objects. It first calculates the center coordinate of the player, then it iterates through the list of projectiles with a `for` loop. If a projectile is sufficiently close to the player, the `remove()` method is called on the list of projectiles. Since lists are passed as references, the `remove()` method affects the global variable that was passed in, which successfully deletes the projectile from the screen. The function then checks if the player is invincible, and if they aren't, it subtracts one from the player's lives. This function returns -1 if no collision occurred, and `player.lives` if a collision did occur. Events based on collisions are handled in the main loop. The game ends if `collision()` returns 0, since the player no longer has lives.

## Problems that Occurred
- There was an issue in the spawning of projectiles, where they would not appear. This was because the projectiles were being drawn before the background, which would cover the projectiles. This was resolved by drawing the background after the projectiles.

- There was an issue regarding the player's hitbox where it was not in the correct place. This was because `game_events.collision()` was subtracting `player.y` from `proj.x` and `player.x` from `proj.y` while calculating the  distance between them. This was resolved by correctly subtracting `player.y` from `proj.y` and `player.x` from `proj.x`.

- There was an issue regarding lag due to the amount of objects being drawn and adjusted, and the limited processing power of the host. This was partly resolved by implementing `entities.CircleProjectile.on_screen()` which checks if the projectile is on the screen. In the game loop, projectiles were deleted if they were off the screen.

- There was an issue regarding the dashing feature where holding spacebar when you're out of boost still makes you invincible. This was resolved by adding an `else` statement to the dash function that sets the player's colour back to red and removes invincibility if `self.boost` is 0.

- There was an issue where time was stuck and would not progress forward. This was causing issues with the spawning algorithm and score. This was resolved by getting the time every frame rather than just at the start. 