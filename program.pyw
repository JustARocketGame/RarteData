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
        Label(self.controls_frame, text="Use Arrow Keys to Rotate").pack()
        
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

class Character3D:
    def __init__(self, root):
        self.root = root
        
        # Canvas setup
        self.canvas = Canvas(root, width=400, height=400, bg='grey')
        self.canvas.pack(pady=20)
        
        # Character part sizes
        self.head_size = 0.2
        self.body_height = 0.6
        self.body_width = 0.3
        self.arm_length = 0.4
        self.arm_width = 0.1
        self.leg_length = 0.4
        self.leg_width = 0.1
        
        # Head (cube)
        self.head_vertices = [
            [-self.head_size, -self.head_size, -self.head_size], [self.head_size, -self.head_size, -self.head_size],
            [self.head_size, self.head_size, -self.head_size], [-self.head_size, self.head_size, -self.head_size],
            [-self.head_size, -self.head_size, self.head_size], [self.head_size, -self.head_size, self.head_size],
            [self.head_size, self.head_size, self.head_size], [-self.head_size, self.head_size, self.head_size]
        ]
        # Body (taller cuboid)
        self.body_vertices = [
            [-self.body_width, -self.body_height, -self.body_width], [self.body_width, -self.body_height, -self.body_width],
            [self.body_width, self.body_height, -self.body_width], [-self.body_width, self.body_height, -self.body_width],
            [-self.body_width, -self.body_height, self.body_width], [self.body_width, -self.body_height, self.body_width],
            [self.body_width, self.body_height, self.body_width], [-self.body_width, self.body_height, self.body_width]
        ]
        # Left Arm (cuboid)
        self.left_arm_vertices = [
            [-self.body_width - self.arm_width, -self.arm_length, -self.arm_width], [-self.body_width, -self.arm_length, -self.arm_width],
            [-self.body_width, self.arm_length, -self.arm_width], [-self.body_width - self.arm_width, self.arm_length, -self.arm_width],
            [-self.body_width - self.arm_width, -self.arm_length, self.arm_width], [-self.body_width, -self.arm_length, self.arm_width],
            [-self.body_width, self.arm_length, self.arm_width], [-self.body_width - self.arm_width, self.arm_length, self.arm_width]
        ]
        # Right Arm (symmetric to left)
        self.right_arm_vertices = [
            [self.body_width, -self.arm_length, -self.arm_width], [self.body_width + self.arm_width, -self.arm_length, -self.arm_width],
            [self.body_width + self.arm_width, self.arm_length, -self.arm_width], [self.body_width, self.arm_length, -self.arm_width],
            [self.body_width, -self.arm_length, self.arm_width], [self.body_width + self.arm_width, -self.arm_length, self.arm_width],
            [self.body_width + self.arm_width, self.arm_length, self.arm_width], [self.body_width, self.arm_length, self.arm_width]
        ]
        # Left Leg (cuboid)
        self.left_leg_vertices = [
            [-self.body_width, -self.body_height, -self.leg_width], [-self.body_width + self.leg_width, -self.body_height, -self.leg_width],
            [-self.body_width + self.leg_width, -self.body_height - self.leg_length, -self.leg_width], [-self.body_width, -self.body_height - self.leg_length, -self.leg_width],
            [-self.body_width, -self.body_height, self.leg_width], [-self.body_width + self.leg_width, -self.body_height, self.leg_width],
            [-self.body_width + self.leg_width, -self.body_height - self.leg_length, self.leg_width], [-self.body_width, -self.body_height - self.leg_length, self.leg_width]
        ]
        # Right Leg (symmetric to left)
        self.right_leg_vertices = [
            [self.body_width - self.leg_width, -self.body_height, -self.leg_width], [self.body_width, -self.body_height, -self.leg_width],
            [self.body_width, -self.body_height - self.leg_length, -self.leg_width], [self.body_width - self.leg_width, -self.body_height - self.leg_length, -self.leg_width],
            [self.body_width - self.leg_width, -self.body_height, self.leg_width], [self.body_width, -self.body_height, self.leg_width],
            [self.body_width, -self.body_height - self.leg_length, self.leg_width], [self.body_width - self.leg_width, -self.body_height - self.leg_length, self.leg_width]
        ]
        
        # Edges for each part (same for all cuboids)
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
            (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
        ]
        
        # Faces for each part (define all six faces of a cube)
        self.faces = [
            (0, 1, 2, 3),  # Back face
            (4, 5, 6, 7),  # Front face
            (0, 1, 5, 4),  # Left face
            (1, 2, 6, 5),  # Right face
            (2, 3, 7, 6),  # Top face
            (0, 3, 7, 4)   # Bottom face
        ]
        
        # Projection parameters
        self.scale = 100
        self.distance = 4
        self.angle_x = math.pi  # Rotate 180 degrees around x-axis to fix upside-down view
        self.angle_y = 0
        self.position = [0, 0, 0]  # Character position (x, y, z)
        
        # Controls
        self.controls_frame = Frame(root)
        self.controls_frame.pack()
        Label(self.controls_frame, text="Arrow Keys: Rotate, WASD: Move").pack()
        
        # Bind keys
        self.root.bind('<Left>', lambda event: self.rotate('y', -0.1))
        self.root.bind('<Right>', lambda event: self.rotate('y', 0.1))
        self.root.bind('<Up>', lambda event: self.rotate('x', -0.1))
        self.root.bind('<Down>', lambda event: self.rotate('x', 0.1))
        self.root.bind('<w>', lambda event: self.move(0, 0, -0.1))  # Forward
        self.root.bind('<s>', lambda event: self.move(0, 0, 0.1))   # Backward
        self.root.bind('<a>', lambda event: self.move(-0.1, 0, 0))  # Left
        self.root.bind('<d>', lambda event: self.move(0.1, 0, 0))   # Right
        
        # Start animation
        self.animate()
        threading.Thread(target=self.step_1, daemon=True).start()
    
    def step_1(self):
        global respawn
        while True:
            time.sleep(0.1)
            if not in_game:
                self.canvas.pack_forget()
                self.controls_frame.pack_forget()
                game1_label.place(x=20, y=10)
                game1_play_button.place(x=20, y=45)
                break  # Exit thread to avoid restarting
            else:
                if respawn:
                    self.scale = 100
                    self.distance = 4
                    self.angle_x = math.pi  # Reset to 180 degrees
                    self.angle_y = 0
                    self.position = [0, 0, 0]  # Reset position
                    respawn = False
                    self.draw()
    
    def project(self, vertex):
        """Project 3D point to 2D using perspective projection with stabilization."""
        x, y, z = vertex
        epsilon = 0.01
        factor = self.distance / (self.distance + z + epsilon)
        x = x * factor * self.scale + 200
        y = y * factor * self.scale + 200
        return x, y
    
    def rotate_point(self, x, y, z, angle_x, angle_y):
        """Rotate point around x and y axes."""
        cos_x = math.cos(angle_x)
        sin_x = math.sin(angle_x)
        y_new = y * cos_x - z * sin_x
        z_new = y * sin_x + z * cos_x
        y = y_new
        z = z_new
        
        cos_y = math.cos(angle_y)
        sin_y = math.sin(angle_y)
        x_new = x * cos_y + z * sin_y
        z_new = -x * sin_y + z * cos_y
        x = x_new
        z = z_new
        
        return x, y, z
    
    def move(self, dx, dy, dz):
        """Move character in 3D space."""
        self.position[0] += dx
        self.position[1] += dy
        self.position[2] += dz
        self.draw()
    
    def rotate(self, axis, angle):
        """Update rotation angles."""
        if axis == 'x':
            self.angle_x += angle
        elif axis == 'y':
            self.angle_y += angle
        self.draw()
    
    def draw(self):
        """Draw the character using fresh transformations each frame."""
        self.canvas.delete("all")
        
        # List of parts and their offsets
        parts = [
            (self.head_vertices, [0, self.body_height + self.head_size, 0]),  # Head above body
            (self.body_vertices, [0, 0, 0]),                          # Body at origin
            (self.left_arm_vertices, [0, self.body_height - self.arm_length, 0]),  # Left arm
            (self.right_arm_vertices, [0, self.body_height - self.arm_length, 0]), # Right arm
            (self.left_leg_vertices, [0, -self.body_height / 5, 0]),  # Left leg higher up
            (self.right_leg_vertices, [0, -self.body_height / 5, 0])  # Right leg higher up
        ]
        
        for vertices, offset in parts:
            transformed_vertices = []
            for vertex in vertices:
                # Apply part offset
                x, y, z = vertex[0] + offset[0], vertex[1] + offset[1], vertex[2] + offset[2]
                # Apply character position
                x += self.position[0]
                y += self.position[1]
                z += self.position[2]
                # Rotate
                x, y, z = self.rotate_point(x, y, z, self.angle_x, self.angle_y)
                # Project
                x, y = self.project([x, y, z])
                transformed_vertices.append((x, y))
            
            # Draw filled faces instead of edges
            for face in self.faces:
                points = [transformed_vertices[i] for i in face]
                self.canvas.create_polygon(points, fill='white', outline='black')
    
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

    Character3D(root)

game1_label = Label(text="Игра 1", font='"Comic Sans MS" 15 bold', background="grey")
game1_label.place(x=20, y=10)

game1_play_button = Button(text="   Играть   ", command=Play)
game1_play_button.place(x=20, y=45)

root.config(background="grey")
root.mainloop()
