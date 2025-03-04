import numpy as np
import pygame

k = complex(0.35, 0.5)
def mandelbrot(c, max_iter, k):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + k
    return max_iter

def controls():
    global zoom_factor, offset_x, offset_y, dragging, drag_start_x, drag_start_y, running, k
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                dragging = True
                drag_start_x, drag_start_y = event.pos

            mouse_x, mouse_y = event.pos
            width, height = pygame.display.get_surface().get_size()
            center_x, center_y = width / 2, height / 2

            if event.button == 4: 
                zoom_factor *= 1.1
                offset_x += (425 - center_x) / width / zoom_factor

            elif event.button == 5:
                zoom_factor /= 1.1
                offset_x -= (432 - center_x) / width / zoom_factor

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                dx, dy = event.pos[0] - drag_start_x, event.pos[1] - drag_start_y
                width, height = 1000, 1000
                offset_x -=  ((xmax-xmin) * (dx))/width
                offset_y -=   ((ymax-ymin)* (dy))/height
                drag_start_x, drag_start_y = event.pos

def render_mandelbrot(screen, width, height):
    global zoom_factor, offset_x, offset_y, running, ymax, xmax, ymin, xmin, k
    xmin = -2.0 / zoom_factor + offset_x
    xmax = 2.0 / zoom_factor + offset_x
    ymin = -2.0 / zoom_factor + offset_y
    ymax = 2.0 / zoom_factor + offset_y

    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    dk = 0

    for i in range(height):
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            k += complex(0.01, 0)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            k -= complex(0.01, 0)

        if pygame.key.get_pressed()[pygame.K_UP]:
            k -= complex(0.0, 0.01)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            k += complex(0.0, 0.01)
        print(k)

        for j in range(width):
            c = complex(x[j], y[i])
            mset = mandelbrot(c, max_iter, k)
            color = ((mset*10) % 255, (10*mset) % 255, (10*mset) % 255)
            screen.set_at((j, i), color)
    
        pygame.draw.line(screen, (255, 0, 0), (width//2, 0), (width//2, height), 1)
        pygame.draw.line(screen, (255, 0, 0), (0, height//2), (width, height//2), 1)
        pygame.draw.circle(screen, (255,0,0), (width//2,height//2), 200, 1)
        pygame.draw.circle(screen, (255,0,0), (width//2 + k.real *100, height//2 + k.imag *100), 2)
        pygame.display.flip()
        
        controls()
        xmin = -2.0 / zoom_factor + offset_x
        xmax = 2.0 / zoom_factor + offset_x
        ymin = -2.0 / zoom_factor + offset_y
        ymax = 2.0 / zoom_factor + offset_y
        x = np.linspace(xmin, xmax, width)
        y = np.linspace(ymin, ymax, height)

def main():          
    global running, dragging, drag_start_x, drag_start_y, zoom_factor, offset_x, offset_y, max_iter
    pygame.init()
    width, height = 1000, 1000
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Mandelbrot Set')

    running = True
    zoom_factor = 1.0
    offset_x, offset_y = 0, 0
    dragging = False
    drag_start_x, drag_start_y = 0, 0
    max_iter = 200

    while running:
        render_mandelbrot(screen, width, height)

    pygame.quit()

if __name__ == "__main__":
    main()
