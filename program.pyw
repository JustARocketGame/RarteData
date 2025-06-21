import requests
from tkinter import *
from tkinter import messagebox
import time
import threading
import os
import subprocess

messagebox.showinfo("Rarte", "Внимание! Это еще Альфа версия!")

in_game = False
respawn = False

root = Tk()
root = root
root.title("Rarte")

# Задаём размеры окна
window_width = 800
window_height = 600

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Вычисляем координаты для центрирования
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)

# Устанавливаем геометрию окна
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

menubar = Menu(root)

def ExitFromGame():
    global in_game
    if in_game == False:
        messagebox.showinfo("Rarte", "Чтобы выйти из игры, вам нужно быть в игре!")
    else:
        game1_label.place(x=20, y=10)
        game1_play_button.place(x=20, y=45)
        in_game = False

def ResetCharacter():
    global in_game, respawn
    if in_game == False:
        messagebox.showinfo("Rarte", "Чтобы сделать респавн, вам нужно быть в игре!")
    else:
        respawn = True


editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Выход из игры", command=ExitFromGame)
editmenu.add_command(label="Респавн", command=ResetCharacter)
menubar.add_cascade(label="Меню", menu=editmenu)

import math

class Cube3D:
    def __init__(self, root):
        self.root = root
        
        # Canvas setup
        self.canvas = Canvas(root, width=400, height=400, bg='grey')
        self.canvas.pack(pady=20)
        
        # Cube vertices (x, y, z)
        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Back face
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]       # Front face
        ]
        
        # Edges connecting vertices
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
            (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
        ]
        
        # Projection parameters
        self.scale = 100
        self.distance = 4
        self.angle_x = 0
        self.angle_y = 0
        
        # Controls
        self.controls_frame = Frame(root)
        self.controls_frame.pack()
        #Label(self.controls_frame, text="Use Arrow Keys to Rotate").pack()
        
        # Bind keys
        self.root.bind('<Left>', lambda event: self.rotate('y', -0.1))
        self.root.bind('<Right>', lambda event: self.rotate('y', 0.1))
        self.root.bind('<Up>', lambda event: self.rotate('x', -0.1))
        self.root.bind('<Down>', lambda event: self.rotate('x', 0.1))
        
        # Animation
        self.animate()
        threading.Thread(target=self.step_1, daemon=True).start()
    def step_1(self):
        global respawn
        while True:
            time.sleep(0.1)
            if in_game == False:
                subprocess.Popen(["pythonw", "program.pyw"])
                self.root.destroy()
            else:
                if respawn == True:
                    print("Respawning!")
                    self.scale = 100
                    self.distance = 4
                    self.angle_x = 0
                    self.angle_y = 0
                    respawn = False
                    self.draw()
    
    def project(self, vertex):
        """Project 3D point to 2D using perspective projection with stabilization."""
        x, y, z = vertex
        # Prevent division by zero with epsilon
        epsilon = 0.01
        factor = self.distance / (self.distance + z + epsilon)
        x = x * factor * self.scale + 200  # Center at (200, 200)
        y = y * factor * self.scale + 200
        return x, y
    
    def rotate_point(self, x, y, z, angle_x, angle_y):
        """Rotate point around x and y axes using fresh transformations."""
        # Rotate around x-axis
        cos_x = math.cos(angle_x)
        sin_x = math.sin(angle_x)
        y_new = y * cos_x - z * sin_x
        z_new = y * sin_x + z * cos_x
        y = y_new
        z = z_new
        
        # Rotate around y-axis
        cos_y = math.cos(angle_y)
        sin_y = math.sin(angle_y)
        x_new = x * cos_y + z * sin_y
        z_new = -x * sin_y + z * cos_y
        x = x_new
        z = z_new
        
        return x, y, z
    
    def rotate(self, axis, angle):
        """Update rotation angles."""
        if axis == 'x':
            self.angle_x += angle
        elif axis == 'y':
            self.angle_y += angle
        self.draw()
    
    def draw(self):
        """Draw the cube using fresh transformations each frame."""
        self.canvas.delete("all")
        
        # Transform and project vertices
        transformed_vertices = []
        for vertex in self.vertices:
            # Apply full rotation from current angles
            x, y, z = self.rotate_point(*vertex, self.angle_x, self.angle_y)
            x, y = self.project([x, y, z])
            transformed_vertices.append((x, y))
        
        # Draw edges
        for edge in self.edges:
            x1, y1 = transformed_vertices[edge[0]]
            x2, y2 = transformed_vertices[edge[1]]
            self.canvas.create_line(x1, y1, x2, y2, fill='black')
    
    def animate(self):
        """Animation loop."""
        self.draw()
        self.root.after(50, self.animate)


root.config(menu=menubar)

#Cube3D(root)

def Play():

    global in_game
    in_game = True

    game1_label.place_forget()
    game1_play_button.place_forget()

    Cube3D(root)

game1_label = Label(text="Игра 1", font='"Comic Sans MS" 15 bold', background="grey")
game1_label.place(x=20, y=10)

game1_play_button = Button(text="   Играть   ", command=Play)
game1_play_button.place(x=20, y=45)

root.config(background="grey")
root.mainloop()
