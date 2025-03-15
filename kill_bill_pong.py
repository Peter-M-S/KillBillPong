# based on code by Graviatr64 YouTube video
# https://www.youtube.com/watch?v=UsUOYnp3zBU

import pygame as pg


class Ball:
  def __init__(self, farbe, pos, richtung):
    self.farbe = farbe
    self.pos = pg.Vector2(pos)
    self.richtung = pg.Vector2(richtung)
    self.rect = pg.Rect(self.pos, (BALL_RADIUS * 2, BALL_RADIUS * 2))
    self.rect.center = pos
    self.rect_alt = self.rect.copy()

  def update(self):
    self.rect_alt = self.rect.copy()
    self.pos += self.richtung
    self.rect.center = self.pos

    if self.pos.x < 0:
      self.pos.x = breite
    if self.pos.x > breite:
      self.pos.x = 0
    if self.rect.top < 0 or self.rect.bottom > höhe:
      self.richtung.y *= -1

    for block in blöcke:
      if block.farbe != self.farbe: continue
      if not self.rect.colliderect(block.rect): continue
      if self.rect_alt.right <= block.rect.left or self.rect_alt.left >= block.rect.right:
        self.richtung.x *= -1
      if self.rect_alt.top >= block.rect.bottom or self.rect_alt.bottom <= block.rect.top:
        self.richtung.y *= -1
      block.tausche_farbe()
      break

    if self.rect.colliderect(schläger_l.rect):
      self.pos -= self.richtung
      normal_vektor = self.pos - pg.Vector2(-70, schläger_l.rect.centery)
      self.richtung.reflect_ip(normal_vektor)
    if self.rect.colliderect(schläger_r.rect):
      self.pos -= self.richtung
      normal_vektor = self.pos - pg.Vector2(70, schläger_r.rect.centery)
      self.richtung.reflect_ip(normal_vektor)

    pg.draw.circle(fenster, self.farbe, self.pos, BALL_RADIUS)


class Block:
  def __init__(self, farbe, pos):
    self.farbe = farbe
    self.pos = pg.Vector2(pos)
    self.rect = pg.Rect(*pos, BLOCK_GROESSE, BLOCK_GROESSE)

  def update(self):
    pg.draw.rect(fenster, self.farbe, self.rect)

  def tausche_farbe(self):
    self.farbe = 'yellow' if self.farbe == 'black' else 'black'


class Schläger:
  def __init__(self, farbe, rechts):
    self.farbe = farbe
    self.rechts = rechts
    if self.rechts:
      self.pos = pg.Vector2(breite - SCHLÄGER_OFFSET, höhe // 2)
    else:
      self.pos = pg.Vector2(SCHLÄGER_OFFSET, höhe // 2)
    self.rect = pg.Rect(*self.pos, 20, 100, center=self.pos)

  def update(self):
    keys = pg.key.get_pressed()
    dy = 0
    if self.rechts:
      if keys[pg.K_p]:
        dy = -1
      elif keys[pg.K_l]:
        dy = +1
    else:
      if keys[pg.K_w]:
        dy = -1
      elif keys[pg.K_s]:
        dy = +1
    self.rect.y += 15 * dy
    self.rect.y = int(pg.math.clamp(self.rect.y, 0, höhe - 100))
    pg.draw.rect(fenster, self.farbe, self.rect)
    pg.draw.rect(fenster, "red", self.rect, 5)


print("Kill-Bill Pong für 2 Spieler.\n"
      "Spieler rechts  = gelber Ball\n"
      "   hoch = p\n"
      "   runter = l\n"
      "Spieler links = schwarzer Ball\n"
      "   hoch  = w\n"
      "   runter = s\n"
      )

pg.init()
größe = breite, höhe = 1600, 800
fenster = pg.display.set_mode(größe)

clock = pg.time.Clock()
FPS = 40
pg.mouse.set_visible(False)

BALL_RADIUS = 20
BLOCK_GROESSE = 40
BALL_SPEED = 5
SCHLÄGER_OFFSET = breite // 4
bälle = [Ball('black', (103, 87), (BALL_SPEED, BALL_SPEED)),
         Ball('yellow', (1087, 420), (-BALL_SPEED, -BALL_SPEED))]
schläger_r = Schläger('yellow', True)
schläger_l = Schläger("black", False)

blöcke = []
for y in range(0, höhe, BLOCK_GROESSE):
  for x in range(0, breite, BLOCK_GROESSE):
    farbe = 'yellow' if x < breite / 2 else 'black'
    blöcke.append(Block(farbe, (x, y)))

while True:
  clock.tick(FPS)

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  for block in blöcke: block.update()
  for ball in bälle: ball.update()
  schläger_l.update()
  schläger_r.update()

  anz_gelbe_blöcke = sum(b.farbe == 'yellow' for b in blöcke)
  pg.display.set_caption(f'Kill-Bill PONG, SCORE = {anz_gelbe_blöcke:>3} : {len(blöcke) - anz_gelbe_blöcke:>3}')

  pg.display.flip()
