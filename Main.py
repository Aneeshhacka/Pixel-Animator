import pygame
from pathlib import Path
import os
from sys import exit
pygame.font.init()
import tkinter.messagebox as MB
import tkinter.simpledialog as SD
font = pygame.font.SysFont("consolas",24)

if not Path("Media").is_dir():
    os.makedirs("Media")

onion_skinning = True
onion_skin_image = None
color_rect = pygame.Rect(500,0,30,30)
size = 1
fps = 10
animating = False
animation_index = 0
sample_surf = pygame.Surface((50,50))

class pixel:
    def __init__(self,pos,color):
        self.color = color
        self.rect = pygame.Rect(pos[0],pos[1],10,10)
    def draw_pixel(self,wnd):
        pygame.draw.rect(wnd,self.color,self.rect)
        
def change_color():
    global current_color
    while True:
        color = SD.askstring("Color","Type color name or (R,G,B) ")
        if color == None:
            return
        try:
            sample_surf.fill(color)
            current_color = color
            return
        except:
            try:
                color = color.strip("(")
                color = color.strip(")")
                color = color.split(",")
                sample_surf.fill((int(color[0]),int(color[1]),int(color[2])))
                current_color = (int(color[0]),int(color[1]),int(color[2]))
                return
            except:
                pass
def draw_color_rect():
    pygame.draw.rect(screen,current_color,color_rect)
    
def doublicate_frame(frame):
    new_frame = []
    for pix in frame:
        new_frame.append(pixel(pix.rect.topleft,pix.color))

    return new_frame

def show_brush_preview():
    global size
    brush_preview = []
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (mouse_pos[0] - (mouse_pos[0] % 10), mouse_pos[1] - (mouse_pos[1] % 10))
    if size == 1:
        if 50 <= mouse_pos[0] <= 540 and 50 <= mouse_pos[1] <= 540:
            brush_preview.append(pixel(mouse_pos,current_color))
    elif size == 2:
        if 50 <= mouse_pos[0] <= 530 and 50 <= mouse_pos[1] <= 530:
            brush_preview.append(pixel(mouse_pos,current_color))
            brush_preview.append(pixel((mouse_pos[0] + 10,mouse_pos[1]),current_color))
            brush_preview.append(pixel((mouse_pos[0],mouse_pos[1] + 10),current_color))
            brush_preview.append(pixel((mouse_pos[0] + 10,mouse_pos[1] + 10),current_color))
    
    elif size == 3:
        if 60 <= mouse_pos[0] <= 530 and 60 <= mouse_pos[1] <= 530:
            brush_preview.append(pixel((mouse_pos[0] -10 ,mouse_pos[1] - 10),current_color),)
            brush_preview.append(pixel((mouse_pos[0],mouse_pos[1] - 10),current_color))
            brush_preview.append(pixel((mouse_pos[0] + 10,mouse_pos[1]-10),current_color))
            brush_preview.append(pixel((mouse_pos[0] - 10,mouse_pos[1]),current_color))
            brush_preview.append(pixel(mouse_pos,current_color))
            brush_preview.append(pixel((mouse_pos[0] + 10,mouse_pos[1]),current_color))
            brush_preview.append(pixel((mouse_pos[0] -10 ,mouse_pos[1] + 10),current_color))
            brush_preview.append(pixel((mouse_pos[0],mouse_pos[1] + 10),current_color))
            brush_preview.append(pixel((mouse_pos[0] + 10,mouse_pos[1]+10),current_color))

    for x in brush_preview:
        x.draw_pixel(screen)

help_box = """Controls:\n
a = play animation

esc = stop playing animation

d = dublicate frame

c = change color

s = sample color

p = pencil

e = eraser

1,2,3 = change size 

d = doublicate frame

delete = delete frame

o = toggle onion skinning

enter = save work

f = change fps
"""

def make_new_onion_skin():
    global onion_skin_image
    onion_skin_image = pygame.Surface((600,600))
    onion_skin_image.fill(BG_COLOR)
    onion_skin_image.set_alpha(75)
    for pixel in frames[current_frame - 1]:
        pixel.draw_pixel(onion_skin_image)

def save(frames):
    name = SD.askstring("Save","What would you like to save this as ?")
    if name != None:
        frames2 = []
        for frame in frames:
            f = pygame.Surface((600,600), pygame.SRCALPHA, 32)
            for pixel in frame:
                pixel.draw_pixel(f)
            frames2.append(f)

        if MB.askyesno("Transparent background","Would you like to save this with a transparent background?"):
            sprite_sheet = pygame.Surface((len(frames2)*500,500), pygame.SRCALPHA, 32)
        else:
            sprite_sheet = pygame.Surface((len(frames2)*500,500), pygame.SRCALPHA, 32)
            sprite_sheet.fill("white")
        
        for x in range(0,len(frames2)):
            sprite_sheet.blit(frames2[x],((x*500) - 50,-50))

        pygame.image.save(sprite_sheet,f"Media/{name}.png")

width = height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Animate")
BG_COLOR = "white"
INFO_COLOR = (128,128,128)
GRID = True
c = pygame.time.Clock()

hold = False
occupied_pixels = [[]]
frames = [[]]
current_frame = 0
current_color = "black"
mode = "P"

def make_new_pixel(pos):
    pos = (pos[0] - (pos[0] % 10), pos[1] - (pos[1] % 10))
    if not pos in occupied_pixels[current_frame] and 50 <= pos[0] <= 540 and 50 <= pos[1] <= 540:
        occupied_pixels[current_frame].append(pos)
        frames[current_frame].append(pixel(pos,current_color))

def use_pencil():
    mouse_pos = pygame.mouse.get_pos()
    if size == 1:
        make_new_pixel(mouse_pos)
    elif size == 2:
        make_new_pixel(mouse_pos)
        make_new_pixel((mouse_pos[0] + 10,mouse_pos[1]))
        make_new_pixel((mouse_pos[0],mouse_pos[1] + 10))
        make_new_pixel((mouse_pos[0] + 10,mouse_pos[1] + 10))
    elif size == 3:
        make_new_pixel((mouse_pos[0] -10 ,mouse_pos[1] - 10))
        make_new_pixel((mouse_pos[0],mouse_pos[1] - 10))
        make_new_pixel((mouse_pos[0] + 10,mouse_pos[1]-10))
        make_new_pixel((mouse_pos[0] - 10,mouse_pos[1]))
        make_new_pixel(mouse_pos)
        make_new_pixel((mouse_pos[0] + 10,mouse_pos[1]))
        make_new_pixel((mouse_pos[0] -10 ,mouse_pos[1] + 10))
        make_new_pixel((mouse_pos[0],mouse_pos[1] + 10))
        make_new_pixel((mouse_pos[0] + 10,mouse_pos[1]+10))

    

def display_info():
    info_surf = font.render(f"Frame {current_frame + 1}",True,INFO_COLOR)
    info_rect = info_surf.get_rect(midtop = (100,10))
    screen.blit(info_surf,info_rect)
    info_surf = font.render('To view controls, press "h"',True,INFO_COLOR)
    info_rect = info_surf.get_rect(midbottom = (300,590))
    screen.blit(info_surf,info_rect)
    

def draw_grid():
    if GRID:
        for i in range(50,551,10):
            pygame.draw.line(screen,INFO_COLOR,(i,50),(i,550))
            pygame.draw.line(screen,INFO_COLOR,(50,i),(550,i))


def handle_events():
    global hold,current_frame,size,mode,onion_skinning,animating,animation_index
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            hold = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            hold = False

        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_n]:
                frames.append([])
                current_frame = len(frames) - 1
                occupied_pixels.append([])
                make_new_onion_skin()
            elif keys[pygame.K_LEFT]:
                if current_frame - 1 >= 0:
                    current_frame -= 1
                    if current_frame > 0:
                        make_new_onion_skin()
            elif keys[pygame.K_RIGHT]:
                if current_frame + 1 <= len(frames) - 1:
                    current_frame += 1
                    make_new_onion_skin()
            elif keys[pygame.K_h]:
                MB.showinfo("Controls",help_box)
            elif keys[pygame.K_DELETE]:
                if len(frames) > 1:
                    if MB.askokcancel("Warning","Do you want to delete this frame?"):
                        frames.pop(current_frame)
                        occupied_pixels.pop(current_frame)
                        if current_frame == len(frames):
                            current_frame -= 1
            elif keys[pygame.K_d]:
                frames.append(doublicate_frame(frames[current_frame]))
                occupied_pixels.append(occupied_pixels[current_frame])
                current_frame = len(frames) - 1
                make_new_onion_skin()
            elif keys[pygame.K_1]:
                size = 1
            elif keys[pygame.K_2]:
                size = 2
            elif keys[pygame.K_3]:
                size = 3
            elif keys[pygame.K_c]:
                change_color()
            elif keys[pygame.K_e]:
                mode = "E"
            elif keys[pygame.K_p]:
                mode = "P"
            elif keys[pygame.K_s]:
                mode = "S"
            elif keys[pygame.K_o]:
                if onion_skinning:
                    if MB.askokcancel("Toggle onion skin","do you want to turn onion skinning off?"):
                        onion_skinning = False
                else:
                    if MB.askokcancel("Toggle onion skin","do you want to turn on onion skinning?"):
                        onion_skinning = True
            elif keys[pygame.K_RETURN]:
                if MB.askokcancel("Save","Would you like to save your work?"):
                    save(frames)
            elif keys[pygame.K_a]:
                if MB.askokcancel("Animate","would you like to see the preview of the animation?"):
                    animating = True
                    animation_index = 0
def pixel_col():
    global occupied_pixels,current_color,mode
    mouse_pos = pygame.mouse.get_pos()
    for pixel in frames[current_frame]:
        if pixel.rect.collidepoint(mouse_pos):
            if mode == "P":
                if pixel.color != current_color:
                    frames[current_frame] = [x for x in frames[current_frame] if x != pixel]
                    occupied_pixels[current_frame] = [x for x in occupied_pixels if x!= pixel.rect.topleft]
            elif mode == "E":
                occupied_pixels[current_frame] = [x for x in occupied_pixels if x!= pixel.rect.topleft]
                frames[current_frame] = [x for x in frames[current_frame] if x != pixel]
            elif mode == "S":
                current_color = pixel.color
                mode = "P"

def draw_pixels(index = False):
    if type(index) != int :
        for pixel in frames[current_frame]:
            pixel.draw_pixel(screen)
    else:
        for pixel in frames[index]:
            pixel.draw_pixel(screen)

while True:
    if animating:
        k = pygame.key.get_pressed()
        if k[pygame.K_ESCAPE]:
            animating = False
        elif k[pygame.K_f]:
            while True:
                fps = SD.askinteger("frames","type fps (1-30)")
                if type(fps) == int:     
                    if 1 <= fps <= 30:
                        break
        screen.fill(BG_COLOR)
        x = font.render("press esc to exit or f to change fps",True,INFO_COLOR)
        y = x.get_rect(midtop = (300,0))
        screen.blit(x,y)
        draw_pixels(int(animation_index))
        animation_index += .1
        if int(animation_index) >= len(frames):
            animation_index = 0
        pygame.display.update()
        c.tick(fps*10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    else:
        handle_events()
        show_brush_preview()
        screen.fill(BG_COLOR)
        if onion_skinning:
            if current_frame > 0:
                screen.blit(onion_skin_image,(0,0))
        draw_color_rect()
        display_info()
        if hold:
            pixel_col()
            if mode == "P":
                use_pencil()
        
        draw_pixels()
        if mode == "P":
            show_brush_preview()
        draw_grid()
        pygame.display.update()
