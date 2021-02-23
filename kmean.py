import pygame
from random import randint
import math
from sklearn.cluster import KMeans

def distance(p1,p2):
	return math.sqrt((p1[0]-p2[0]) * (p1[0]-p2[0]) + (p1[1]-p2[1]) * (p1[1]-p2[1]))

pygame.init()

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption("Kmean visualization")

running = True

clock = pygame.time.Clock()

BACKGROUND = (214, 214, 214)

BLACK = (0, 0, 0)
WHITE = (255,255,255)
BACKGROUND_PANEL =(249,255,230)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147,153,35)
PURPLE = (0,255,255)
SKY = (255,125,25)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]

font = pygame.font.SysFont('sans', 40)
font_small = pygame.font.SysFont('sans', 20)
text_plus = font.render('+', True, WHITE)
text_minus = font.render('-', True, WHITE)
text_run = font.render('Run', True, WHITE)
text_random = font.render('Random', True, WHITE)
text_algorithm = font.render('Algorithm', True, WHITE)
text_reset = font.render('Reset', True, WHITE)



K = 0
error = 0
points = []
clusters = []
labels = []

while running:
	clock.tick(60)
	screen.fill(BACKGROUND)
	mouse_x, mouse_y = pygame.mouse.get_pos()

	#Draw interface

	#Draw Panel

	pygame.draw.rect(screen, BLACK,(50, 50, 700, 500))
	pygame.draw.rect(screen, BACKGROUND_PANEL,(55, 55, 690, 490))

	#K button +
	pygame.draw.rect(screen, BLACK,(850,50,50,50))
	screen.blit(text_plus,(870,50))

	#K buton -
	pygame.draw.rect(screen, BLACK,(950,50,50,50))
	screen.blit(text_minus,(970,50))

	#K buton Run
	pygame.draw.rect(screen, BLACK,(850,150,150,50))
	screen.blit(text_run,(850,150))

	#K buton Random
	pygame.draw.rect(screen, BLACK,(850,250,150,50))
	screen.blit(text_random,(850,250))

	#K buton Algorithm
	pygame.draw.rect(screen, BLACK,(850,450,150,50))
	screen.blit(text_algorithm,(850,450))

	#K buton Reset
	pygame.draw.rect(screen, BLACK,(850,550,150,50))
	screen.blit(text_reset,(850,550))

	#K value
	text_k = font.render("K = " + str(K), True, BLACK)
	screen.blit(text_k, (1050,50))

	#Error value
	# text_error = font.render("Error = " + str(error), True, BLACK)
	# screen.blit(text_error, (850,350))

	#Draw mouse position when mouse is in panel
	if 50 <mouse_x <750 and 50 < mouse_y < 550:
		text_mouse = font_small.render("("+ str(mouse_x-50)+","+str(mouse_y-50)+ ")", True, BLACK)
		screen.blit(text_mouse, (mouse_x+10,mouse_y))

	#End draw interface

	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			#Create point on panel
			labels = []
			if 50 < mouse_x < 750 and 50 < mouse_y <550:
				point = [mouse_x-50,mouse_y-50]
				points.append(point)
				print(points)


			#change K button +
			if 850 <mouse_x <900 and 50 < mouse_y < 100:
				if K < 8:
					K += 1
				print("Press cong")
			elif 950 <mouse_x <1000 and 50 < mouse_y < 100:
				if K>0:
					K -= 1
				print("Press tru")
			elif 850 <mouse_x <1000 and 150 < mouse_y < 200:
				labels = []
				if clusters == []:
					continue

				#Assign points to closest clusters
				for p in points:
					distances_to_cluster = []
					for c in clusters:
						dis = distance(p,c)
						distances_to_cluster.append(dis)

					min_distance = min(distances_to_cluster)
					label = distances_to_cluster.index(min_distance)
					labels.append(label)

				#Update clusters

				for i in range(K):
					sum_x = 0
					sum_y = 0
					count = 0
					for j in range(len(points)):
						if labels[j] == i:
							sum_x += points[j][0]
							sum_y += points[j][1]
							count += 1
					if count != 0:
						new_cluster_x = sum_x/count
						new_cluster_y = sum_y/count
						clusters[i] = [new_cluster_x,new_cluster_y]
				print("Run")
			elif 850 <mouse_x <1000 and 250 < mouse_y < 300:
				clusters = []
				labels = []
				for i in range(K):
					random_point = [randint(0,700), randint(0,500)]
					clusters.append(random_point)

				print("Random")
			elif 850 <mouse_x <1000 and 450 < mouse_y < 500:
				kmeans = KMeans(n_clusters=K).fit(points)
				print(kmeans.cluster_centers_)
				labels = kmeans.predict(points)
				clusters = kmeans.cluster_centers_
				print("Algorithm")

			elif 850 <mouse_x <1000 and 550 < mouse_y < 600:
				points = []
				labels = []
				error = []
				clusters =[]
				print("Reset")

	#Draw cluster
	for i in range(len(clusters)):
		pygame.draw.circle(screen,COLORS[i], (int(clusters[i][0])+50, int(clusters[i][1])+50),10)

	#Draw point
	for i in range(len(points)):
		pygame.draw.circle(screen, BLACK, (points[i][0]+50, points[i][1]+50),6)

		if labels == []:
			pygame.draw.circle(screen, WHITE, (points[i][0]+50, points[i][1]+50),5)
		else:
			pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0]+50, points[i][1]+50),5)
	
	#Calculate and draw error
	error = 0
	if clusters != [] and labels != []:
		for i in range(len(points)):
			error += distance(points[i], clusters[labels[i]])
	text_error = font.render("Error = " + str(int(error)), True, BLACK)
	screen.blit(text_error,(850,350))

	pygame.display.flip()

pygame.quit()