import math
import random
import config as cf
import entities

def spawn_pellet(delta):
  spawn_slope = math.e ** (delta * math.log(3) * (1/70))
  spawn_freq = random.uniform(0,spawn_slope)
  if spawn_freq > cf.SPAWN_RATE:
    pellet_y = random.randint(1,cf.SCREEN_HEIGHT)
    pellet_speed = random.uniform(3,cf.PELLET_VELOCITY)
    pellet_angle = random.uniform(-3,3)
    spawn_dir = random.randint(0,1)
    if spawn_dir:
      pellet_x = 30
    else:
      pellet_x = cf.SCREEN_WIDTH - 30
      pellet_speed = -1 * pellet_speed
    return entities.CircleProjectile(
      (0,255,0),
      (pellet_x,pellet_y),
      cf.PELLET_SIZE,
      pellet_speed,
      pellet_angle
    )
  return

def collision(player, projectiles):
  center_x = player.x + (cf.PLAYER_WIDTH / 2)
  center_y = player.y + (cf.PLAYER_HEIGHT / 2)

  for proj in projectiles:
    if abs(proj.x - center_x) <= cf.PLAYER_WIDTH and abs(proj.y - center_y) <= cf.PLAYER_HEIGHT:
      projectiles.remove(proj)
      if player.invincible == False:
        player.lives -= 1
        return player.lives
  return -1