import pygame
import entities
import config as cf
import game_events

projectiles = []
pygame.init()
FONT = pygame.font.Font(cf.FONT, cf.FONT_SIZE)
win = pygame.display.set_mode((cf.SCREEN_WIDTH,cf.SCREEN_HEIGHT))
x = cf.PLAYER_SPAWN_X
y = cf.PLAYER_SPAWN_Y
width = cf.PLAYER_WIDTH
height = cf.PLAYER_HEIGHT
vel = cf.PLAYER_VELOCITY

c = entities.Human(cf.PLAYER_COLOUR, (x,y,width,height), vel)

running = True
delta = pygame.time.get_ticks()


def spawn():
  p = game_events.spawn_pellet(delta / 1000)
  if p is not None:
    projectiles.append(p)

while running:
  pygame.time.delay(40)
  delta = pygame.time.get_ticks()
  score_text = FONT.render("Score: "+str(delta // 1000), False, (255,255,255))
  boost_text = FONT.render("Boost: " + str(c.boost), False, (255,255,255))
  lives_text = FONT.render("Lives: " + str(c.lives),False,(255,255,255))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  spawn()

  keys = pygame.key.get_pressed()

  c.walk(keys)
  
  win.fill((0,0,0))

  # GUI
  pygame.draw.rect(win,(100,100,0),(10,10,5,c.boost*4))
  
  win.blit(score_text, (25,5))
  win.blit(boost_text, (25,30))
  win.blit(lives_text, (25,55))

  for p in projectiles:
    p.move()
    p.draw(win)
    if not p.on_screen():
      del p

  collision = game_events.collision(c,projectiles)
  if collision == 0:
    print("Game Over!\nYour score was " + str((delta / 1000).__round__()))
    break

  c.draw(win)
 
  pygame.display.update()
pygame.quit()

