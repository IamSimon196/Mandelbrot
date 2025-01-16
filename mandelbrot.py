import numpy as np
import pygame
import threading
import time

def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def controlls():
    global zoom_factor, offset_x, offset_y, dragging, drag_start_x, drag_start_y, running
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
                offset_x -= (425 - center_x) / width / zoom_factor

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
    global zoom_factor, offset_x, offset_y, running, ymax, xmax, ymin, xmin
    while running:
        xmin = -2.0 / zoom_factor + offset_x
        xmax = 0.5 / zoom_factor + offset_x
        ymin = -1.25 / zoom_factor + offset_y
        ymax = 1.25 / zoom_factor + offset_y

        x = np.linspace(xmin, xmax, width)
        y = np.linspace(ymin, ymax, height)



        for i in range(height):
            for j in range(width):
                c = complex(x[j], y[i])
                mset = mandelbrot(c, max_iter)
                color = ((mset*2) % 1000, (2*mset) % 1000, (2*mset) % 1000)
                screen.set_at((j, i), color)
        
            pygame.display.flip()  
            xmin = -2.0 / zoom_factor + offset_x
            xmax = 0.5 / zoom_factor + offset_x
            ymin = -1.25 / zoom_factor + offset_y
            ymax = 1.25 / zoom_factor + offset_y
            x = np.linspace(xmin, xmax, width)
            y = np.linspace(ymin, ymax, height)


def main():
    global running, dragging, drag_start_x, drag_start_y, zoom_factor, offset_x, offset_y, max_iter
    pygame.init()
    width, height = 1000, 1000
    scale_factor = 1
    small_width, small_height = width // scale_factor, height // scale_factor

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Mandelbrot Set')

    running = True
    zoom_factor = 1.0
    offset_x, offset_y = 0, 0
    dragging = False
    drag_start_x, drag_start_y = 0, 0
    max_iter = 100

    small_surface = pygame.Surface((small_width, small_height))

    render_thread = threading.Thread(target=render_mandelbrot, args=(small_surface, small_width, small_height))
    render_thread.start()

    while running:
        controlls()
        scaled_surface = pygame.transform.scale(small_surface, (width, height))
        screen.blit(scaled_surface, (0, 0))
        pygame.draw.line(screen, (255, 0, 0), (width//2, 0), (width//2, height), 1) 
        pygame.draw.line(screen, (255, 0, 0), (0, height//2), (width, height//2), 1)
        pygame.display.flip()

    render_thread.join()
    pygame.quit()

if __name__ == "__main__":
    main()