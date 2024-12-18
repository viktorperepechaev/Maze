import pygame
import sys

class ComplexityManager:
	def __init__(self, width, height):
		self.width = width
		self.height = height
	def toMenu(self):
		pygame.init()
		pygame.display.set_caption("SetComplexity")
		font = pygame.font.Font(None, 32)
		f = 1
		screen = pygame.display.set_mode((self.width, self.height))
		while f:
			screen.fill((0, 0, 0))
			discription_text = font.render(f'Выберите уровень сложности:', True, (255, 255, 255))
			F_text = font.render(f'F - стандартный лабиринт, время не ограничено', True, (255, 255, 255))
			G_text = font.render(f'G - Меняющаяяся скорость игрока, 45 секунд на прохождение', True, (255, 255, 255))
			H_text = font.render(f'H - Меняющаяяся скорость игрока, 35 секунд на прохождение,', True, (255, 255, 255))
			H2_text = font.render(f'перестраивающийся лабиринт', True, (255, 255, 255))
			# Размещение текстов на экране
			screen.blit(discription_text, (self.width // 2 - discription_text.get_width() // 2, 100))
			screen.blit(F_text, (50, 200))
			screen.blit(G_text, (50, 300))
			screen.blit(H_text, (50, 400))
			screen.blit(H2_text, (80, 420))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					# Выходим из игры при закрытии окна
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_f:
						complexity = 'F'
						f = 0
					elif event.key == pygame.K_g:
						complexity = 'G'
						f = 0
					elif event.key == pygame.K_h:
						complexity = 'H'
						f = 0
		pygame.mixer.music.play(-1)
		return complexity
