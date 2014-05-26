import pygame
import random

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 550
WHITE = (255, 255, 255)
RED = (255, 0 , 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 255)
PAD_AREA = 100

PUNCH_SCORE = 5
ARROW_HEART_SCORE = -15
HEART_SCORE = 5
ALIEN_HIT_SCORE = 20
STUN_HUGO = 2000
STUN_HA = 5000

class Hugo(pygame.sprite.Sprite):
	
	left_boundary = PAD_AREA
	right_boundary = SCREEN_WIDTH
	change_x = 1
	shoot_speed = 1000
	speed_left = 3
	speed_right = 5
	diff = 0	
	constant_heart = None
	constant_bad_heart = None
	constant_good_heart = None
	speed_diff = 0
	hit_time = 0
	previous_hit_time = 0
	main_pic = None
	stunned_pic = None
	won_pic = None
	
	def __init__(self, filename):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(filename).convert()
		self.rect = self.image.get_rect()
		self.rect.midtop = (SCREEN_WIDTH / 2, 0)
		self.diff = (self.rect.right - self.rect.left) / 2
		self.main_pic = pygame.image.load("hugo.png").convert()
		self.stunned_pic = pygame.image.load("stunned_hugo.png").convert()
		self.won_pic = pygame.image.load("won_hugo.png").convert()
		self.constant_heart = pygame.image.load("heart.png").convert()
		self.constant_bad_heart = pygame.image.load("alien.png").convert()
		self.constant_good_heart = pygame.image.load("big_heart.png").convert()
		
	def update(self):
		if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
			self.change_x *= -1
			self.rect.x += self.change_x * random.randrange(1, 2)
		self.rect.x += self.change_x * random.randrange(self.speed_left, self.speed_right) 
	
	def shoot(self):
		if random.randrange(0, 9) < 3:
			heart = Heart(self.constant_good_heart, True, "good")
		else: 
			heart = Heart(self.constant_heart, False, "bad")
			
		heart.rect.midtop = self.rect.midbottom
		heart.left_boundary = self.diff + PAD_AREA
		heart.right_boundary = SCREEN_WIDTH - self.diff
		return heart
	
	def shoot_alien(self):
		heart = Heart(self.constant_bad_heart, False, "alien")
		heart.rect.midtop = self.rect.midbottom
		heart.left_boundary = self.diff + PAD_AREA
		heart.right_boundary = SCREEN_WIDTH - self.diff
		return heart

class Ha(pygame.sprite.Sprite):
	left_boundary = PAD_AREA
	right_boundary = SCREEN_WIDTH
	direction = 1
	speed = 0
	const_speed = 15
	constant_glove = None
	main_pic = None
	dead_pic = None
	stunned_pic = None
	hit_time = 0
	previous_hit_time = 0
	
	def __init__(self, filename):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(filename).convert()
		self.rect = self.image.get_rect()
		self.rect.midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT)
		self.main_pic = pygame.image.load("ha.png").convert()
		self.dead_pic = pygame.image.load("dead_ha.png").convert()
		self.stunned_pic = pygame.image.load("stunned_ha.png").convert()
		self.constant_glove = pygame.image.load("glove.png").convert()
	
	def update(self):
		if self.rect.right >= self.right_boundary:
			self.rect.right = SCREEN_WIDTH - 1
		elif self.rect.left <= self.left_boundary:
			self.rect.x = 1+ PAD_AREA
		else: 
			self.rect.x += self.speed
			
	def shoot(self):
		arrow = Arrow(self.constant_glove)
		arrow.rect.midtop = self.rect.midtop
		return arrow		
		

class Heart(pygame.sprite.Sprite):
	left_boundary = 0
	right_boundary = SCREEN_WIDTH
	speed = 0
	speed_y = 0
	ind = False
	type = ""
	
	def __init__(self, file, ind, type):
		pygame.sprite.Sprite.__init__(self)
		self.image = file
		self.rect = self.image.get_rect()
		
		self.speed = random.randrange(-5, 5)
		self.speed_y = 3
		
		self.ind = ind
		self.type = type
		
	def update(self):
		if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
			self.speed *= -1
		self.rect.y += self.speed_y
		self.rect.x += self.speed
	
class Arrow(pygame.sprite.Sprite):
	
	speed = 10
	def __init__(self, glove):
		pygame.sprite.Sprite.__init__(self)
		self.image = glove
		self.rect = self.image.get_rect()
		
	def update(self):
		self.rect.y -= self.speed
#		
# Game object
#
class Game(object):

	all_sprites_list = None
	heart_list = None
	heart_hit_list = None
	arrow_list = None
	arrow_hit_list = None
	alien_list = None
	alien_hit_list = None
	
	ha_list = None
	previous_time = 0
	previous_alien_time = 0
	
	ha = None
	game_over = False
	slaps = 0
	hugs = 0
	score = 0
	bad_hits = 0
	alien_hits = 0
	lives = 3
	ind = ""
	
	def __init__(self):
		self.all_sprites_list = pygame.sprite.Group()	
		self.heart_list = pygame.sprite.Group()
		self.heart_hit_list = pygame.sprite.Group()
		self.arrow_list = pygame.sprite.Group()
		self.arrow_hit_list = pygame.sprite.Group()
		self.ha_list = pygame.sprite.Group()
		self.alien_hit_list = pygame.sprite.Group()
		self.alien_list = pygame.sprite.Group()
		
		self.hugo = Hugo("hugo.png")
		self.ha = Ha("ha.png")
		self.all_sprites_list.add(self.hugo)
		self.all_sprites_list.add(self.ha)
		self.ha_list.add(self.ha)
		previous_time = pygame.time.get_ticks()
		self.previous_alien_time = pygame.time.get_ticks()
		
	def process_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.ha.speed -= self.ha.const_speed
				elif event.key == pygame.K_RIGHT:
					self.ha.speed += self.ha.const_speed
				elif event.key == pygame.K_SPACE:
					arrow = self.ha.shoot()
					self.all_sprites_list.add(arrow)
					self.arrow_list.add(arrow)
				elif event.key == pygame.K_s:
					self.hugo.shoot_speed -= 100
					
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					self.ha.speed += self.ha.const_speed
				elif event.key == pygame.K_RIGHT:
					self.ha.speed -= self.ha.const_speed
			
	def run_logic(self):
		if not self.game_over:
			self.all_sprites_list.update()
		if self.hugs < 5:
			self.hugo.shoot_speed_diff = self.hugs * 5
		elif self.hugs < 10:
			self.hugo.shoot_speed_diff = self.hugs * 9
		elif self.hugs < 20:
			self.hugo.shoot_speed_diff = self.hugs * 12
		else:
			self.hugo.shoot_speed_diff = self.hugs * 14
		
		if self.hugo.shoot_speed_diff > 900:
			self.hugo.shoot_speed_diff = 900
		
		if pygame.time.get_ticks() - self.previous_time >= 2 * (self.hugo.shoot_speed - self.hugo.shoot_speed_diff):
			block = self.hugo.shoot()
			self.heart_list.add(block)
			self.all_sprites_list.add(block)
			self.previous_time = pygame.time.get_ticks()
			
		if pygame.time.get_ticks() - self.hugo.previous_hit_time > self.hugo.hit_time:
			self.hugo.image = self.hugo.main_pic
		
		if pygame.time.get_ticks() - self.ha.previous_hit_time > self.ha.hit_time:
			self.ha.image = self.ha.main_pic
			
		if pygame.time.get_ticks() - self.previous_alien_time >= 5 * (1+ (self.hugs + 1) / 10) * (self.hugo.shoot_speed - self.hugo.shoot_speed_diff):
			block = self.hugo.shoot_alien()
			self.alien_list.add(block)
			self.all_sprites_list.add(block)
			self.previous_alien_time = pygame.time.get_ticks()
		
		# arrow heart collision
		for arrow in self.arrow_list:
			self.heart_hit_list = pygame.sprite.spritecollide(arrow, self.heart_list, True)
			for heart in self.heart_hit_list:
				self.bad_hits += 1
				self.arrow_list.remove(arrow)
				self.all_sprites_list.remove(arrow)
				self.score += ARROW_HEART_SCORE
				
			self.alien_hit_list = pygame.sprite.spritecollide(arrow, self.alien_list, True)
			for alien in self.alien_hit_list:
				self.alien_hits += 1
				self.arrow_list.remove(arrow)
				self.all_sprites_list.remove(arrow)
				self.score += ALIEN_HIT_SCORE
				
			if arrow.rect.y < 0:
				self.arrow_list.remove(arrow)
				self.all_sprites_list.remove(arrow)
		
		# alien ha collision
		self.alien_hit_list = pygame.sprite.spritecollide(self.ha, self.alien_list, True)
		for alien in self.alien_hit_list:
			self.ha.hit_time = STUN_HA
			self.ha.previous_hit_time = pygame.time.get_ticks()
			self.ha.image = self.ha.stunned_pic
			self.lives -= 1
			if self.lives < 0:
				self.game_over = True
				self.ind = "monster" 
		
		# arrow hugo collision
		self.arrow_hit_list = pygame.sprite.spritecollide(self.hugo, self.arrow_list, True)
		for arrow in self.arrow_hit_list:
			self.hugo.hit_time = STUN_HUGO
			self.hugo.previous_hit_time = pygame.time.get_ticks()
			self.hugo.image = self.hugo.stunned_pic
			self.slaps += 1
			self.arrow_list.remove(arrow)
			self.all_sprites_list.remove(arrow)
			self.score += PUNCH_SCORE
		
		# heart ha collision
		self.heart_hit_list = pygame.sprite.spritecollide(self.ha, self.heart_list, False)
		for heart in self.heart_hit_list:
			self.all_sprites_list.remove(heart)
			self.heart_list.remove(heart)
			self.hugs += 1
			self.score += HEART_SCORE
	
		for heart in self.heart_list:
			
			if heart.ind and heart.rect.y > SCREEN_HEIGHT:
				self.game_over = True
				self.ind = "heart_down"
				
			elif not heart.ind and heart.rect.y > SCREEN_HEIGHT:
				self.all_sprites_list.remove(heart)
				self.heart_list.remove(heart)
				
		for heart in self.alien_list:
			if heart.type == "alien" and heart.rect.bottom >= SCREEN_HEIGHT:
				#and heart.rect.bottom >= SCREEN_HEIGHT:	
				heart.speed_y = 0
		
	def display_frame(self, screen):
		screen.fill(BLACK)
		
		pygame.draw.line(screen, GREEN, [self.hugo.diff + PAD_AREA, self.hugo.rect.bottom], [self.hugo.diff + PAD_AREA, SCREEN_HEIGHT], 5)
		pygame.draw.line(screen, GREEN, [SCREEN_WIDTH - self.hugo.diff, self.hugo.rect.bottom], [SCREEN_WIDTH - self.hugo.diff, SCREEN_HEIGHT], 5)
		pygame.draw.line(screen, GREEN, [self.hugo.diff + PAD_AREA, self.hugo.rect.bottom], [SCREEN_WIDTH - self.hugo.diff, self.hugo.rect.bottom], 5)
		pygame.draw.line(screen, GREEN, [self.hugo.diff + PAD_AREA, SCREEN_HEIGHT-2], [SCREEN_WIDTH - self.hugo.diff, SCREEN_HEIGHT-2], 5)
		
		self.all_sprites_list.draw(screen)
		
		font_score = pygame.font.Font(None, 30)
		slap_score = font_score.render("Punches : "+ str(self.slaps), True, RED)
		screen.blit(slap_score, [10, 200])
		hugs_score = font_score.render("Hearts : "+ str(self.hugs), True, RED)
		screen.blit(hugs_score, [10, 250])
		bad = font_score.render("Bad hit : "+ str(self.bad_hits), True, RED)
		screen.blit(bad, [10, 300])
		
		speed_x = int((float(1000000) / (self.hugo.shoot_speed - self.hugo.shoot_speed_diff)))
		speed = font_score.render("Speed : "+ str(speed_x), True, RED)
		screen.blit(speed, [10, 150])
		
		alien_x = font_score.render("Aliens : "+ str(self.alien_hits), True, RED)
		screen.blit(alien_x, [10, 100])
		
		lives_x = font_score.render("Lives : "+ str(self.lives), True, RED)
		screen.blit(lives_x, [10, 350])
		
		score = font_score.render("Score : "+ str(self.score), True, WHITE)
		screen.blit(score, [10, 400])
			
		if self.game_over:	
			font = pygame.font.Font(None, 40)
			message = ""
			if self.ind == "heart_down":
				message = "My heart is broken!"
			else:
				message = "Beware the aliens!"
			
			text = font.render(message, True, RED)
			screen.blit(text, [SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2])
			
			self.ha.image = self.ha.dead_pic
			self.hugo.image = self.hugo.won_pic
			
			ha_s = pygame.sprite.Group()
			ha_s.add(self.hugo)
			ha_s.add(self.ha)
			ha_s.draw(screen)
			
		pygame.display.flip()

def main():
	pygame.init()
	
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("Love me or Punch me")
	pygame.mouse.set_visible(False)
	
	done = False
	clock = pygame.time.Clock()
	
	game = Game()
	
	# Main game loop
	while not done:
	
			done = game.process_events()
		
			game.run_logic()
		
			game.display_frame(screen)
		
			clock.tick(60)
			
	pygame.quit()


# start the game
if __name__ == "__main__":
	main()