import pygame
from win32api import GetSystemMetrics
import os
import math
def matrix_multiplication(a, b):
    columns_a = len(a[0])
    rows_a = len(a)
    columns_b = len(b[0])
    rows_b = len(b)

    result_matrix = [[j for j in range(columns_b)] for i in range(rows_a)]
    if columns_a == rows_b:
        for x in range(rows_a):
            for y in range(columns_b):
                sum = 0
                for k in range(columns_a):
                    sum += a[x][k] * b[k][y]
                result_matrix[x][y] = sum

        return result_matrix

    else:
        print("columns of the first matrix must be equal to the rows of the second matrix")
        return None
scale = 0.75
strength = int(scale*3)
print(strength)
os.environ["SDL_VIDEO_CENTERED"]= '1'

black, white, blue  = (5, 6, 6), (230, 230, 230), (0, 154, 255)

width , height = [int(GetSystemMetrics(i)*scale) for i in range(2)]

pygame.init()
pygame.display.set_caption("4D cube Projection")
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60

angle = 0
cube_position = [width//2, height//2]
scale = 4000*scale
speed = 0.01
points = [n for n in range(16)]

points[0] = [[-1], [-1], [1], [1]]
points[1] = [[1], [-1], [1], [1]]
points[2] = [[1], [1], [1], [1]]
points[3] = [[-1], [1], [1], [1]]
points[4] = [[-1], [-1], [-1], [1]]
points[5] = [[1], [-1], [-1], [1]]
points[6] = [[1], [1], [-1], [1]]
points[7] = [[-1], [1], [-1], [1]]
points[8] = [[-1], [-1], [1], [-1]]
points[9] = [[1], [-1], [1], [-1]]
points[10] = [[1], [1], [1], [-1]]
points[11] = [[-1], [1], [1], [-1]]
points[12] = [[-1], [-1], [-1], [-1]]
points[13] = [[1], [-1], [-1], [-1]]
points[14] = [[1], [1], [-1], [-1]]
points[15] = [[-1], [1], [-1], [-1]]


def connect_point(i, j, k, offset):
    a = k[i + offset]
    b = k[j + offset]
    pygame.draw.line(screen, white, (a[0], a[1]), (b[0], b[1]), strength)


run = True
while run:
    clock.tick(fps)
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                run = False

    index = 0
    projected_points = [j for j in range(len(points))]

    #3d matrix rotations
    rotation_x = [[1, 0, 0],
                  [0, math.cos(angle), -math.sin(angle)],
                  [0, math.sin(angle), math.cos(angle)]]

    rotation_y = [[math.cos(angle), 0, -math.sin(angle)],
                  [0, 1, 0],
                  [math.sin(angle), 0, math.cos(angle)]]

    rotation_z = [[math.cos(angle), -math.sin(angle), 0],
                  [math.sin(angle), math.cos(angle), 0],
                  [0, 0 ,1]]
    tesseract_rotation = [[1, 0, 0],
                          [0, math.cos(-math.pi/2), -math.sin(-math.pi/2)],
                          [0, math.sin(-math.pi/2), math.cos(-math.pi/2)]]
    #4d matrix rotations

    rotation4d_xy= [[math.cos(angle), -math.sin(angle), 0, 0],
                  [math.sin(angle), math.cos(angle), 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]]
    rotation4d_xz = [[math.cos(angle), 0, -math.sin(angle), 0],
                     [0, 1, 0, 0],
                     [math.sin(angle), 0, math.cos(angle), 0],
                     [0, 0, 0, 1]]
    rotation4d_xw = [[math.cos(angle), 0, 0, -math.sin(angle)],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [math.sin(angle), 0, 0, math.cos(angle)]]
    rotation4d_yz = [[1, 0, 0, 0],
                     [0, math.cos(angle), -math.sin(angle), 0],
                     [0, math.sin(angle), math.cos(angle), 0],
                     [0, 0, 0, 1]]
    rotation4d_yw = [[1, 0, 0, 0],
                     [0, math.cos(angle), 0, -math.sin(angle)],
                     [0, 0, 1, 0],
                     [0, math.sin(angle), 0, math.cos(angle)]]
    rotation4d_zw = [[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, math.cos(angle), -math.sin(angle)],
                     [0, 0, math.sin(angle), math.cos(angle)]]

    for point in points:

        rotated_3d = matrix_multiplication(rotation4d_xy, point)
        rotated_3d = matrix_multiplication(rotation4d_zw, rotated_3d)

        distance = 5
        w = 1/(distance - rotated_3d[3][0])
        projection_matrix4 = [
                            [w, 0, 0, 0],
                            [0, w, 0, 0],
                            [0, 0, w, 0],]

        projected_3d = matrix_multiplication(projection_matrix4, rotated_3d)
        rotated_2d = matrix_multiplication(tesseract_rotation, projected_3d)
        z = 1/(distance - (rotated_2d[2][0] + rotated_3d[3][0]))
        projection_matrix = [[z, 0, 0],
                            [0, z, 0 ]
                            ]

        rotated_2d = matrix_multiplication(rotation_x, projected_3d)
        projected_2d = matrix_multiplication(projection_matrix, rotated_2d)
        x = int(projected_2d[0][0] * scale) + cube_position[0]
        y = int(projected_2d[1][0] * scale) + cube_position[1]

        projected_points[index] = [x, y]
        pygame.draw.circle(screen, blue, (x, y), 10)
        index += 1
    #draw edges
    for m in range(4):
        connect_point(m, (m+1)%4, projected_points, 8)
        connect_point(m+4, (m+1)%4 + 4, projected_points, 8)
        connect_point(m, m+4, projected_points, 8)

    for m in range(4):
        connect_point(m, (m+1)%4, projected_points, 0)
        connect_point(m+4, (m+1)%4 + 4, projected_points, 0)
        connect_point(m, m+4, projected_points, 0)

    for m in range(8):
        connect_point(m,  m+8, projected_points, 0)

    angle += speed
    pygame.display.update()

pygame.quit()