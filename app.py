import tkinter as tk

class GridGUI:
    def __init__(self, master, grid_size, proximity_threshold=10):
        self.master = master
        self.grid_size = grid_size
        self.proximity_threshold = proximity_threshold
        self.points = []

        self.canvas = tk.Canvas(master, width=grid_size, height=grid_size)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.mode = "point" 
        self.selected_point = None
        self.lines = []

        self.btn_point = tk.Button(master, text="Point Mode", command=self.set_point_mode)
        self.btn_point.pack(side=tk.LEFT)
        self.btn_line = tk.Button(master, text="Line Mode", command=self.set_line_mode)
        self.btn_line.pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.handle_click)

    def set_point_mode(self):
        self.mode = "point"
        self.selected_point = None
        self.draw_grid()
        self.btn_point.config(fg='green')
        self.btn_line.config(fg='blue')

    def set_line_mode(self):
        self.mode = "line"
        self.selected_point = None
        self.draw_grid()
        self.btn_line.config(fg='green')
        self.btn_point.config(fg='blue')        

    def handle_click(self, event):
        x, y = event.x, event.y

        if self.mode == "point":
            # Point mode handling (same as before)
            for i, (px, py) in enumerate(self.points):
                if abs(x - px) <= self.proximity_threshold and abs(y - py) <= self.proximity_threshold:
                    del self.points[i]
                    self.draw_grid()
                    print("Points:", self.points)
                    return
            self.points.append((x, y))
            self.draw_grid()
            print("Points:", self.points)

        elif self.mode == "line":
            for i, (px, py) in enumerate(self.points):
                if abs(x - px) <= self.proximity_threshold and abs(y - py) <= self.proximity_threshold:
                    if self.selected_point == (px, py): # Deselect if clicked again
                        self.selected_point = None
                    elif self.selected_point: # Second point clicked, draw line
                        if (self.selected_point, (px, py)) in self.lines:
                            # Remove the line
                            self.lines.remove((self.selected_point, (px, py)))
                        elif ((px, py), self.selected_point) in self.lines:
                            # Remove the line
                            self.lines.remove(((px, py), self.selected_point))
                        else:
                            # Add line
                            self.lines.append((self.selected_point, (px, py)))
                        self.selected_point = None
                        print("Lines:", self.lines)
                    else:  # First point clicked, select it
                        self.selected_point = (px, py)
                    self.draw_grid()
                    return

    def draw_grid(self):
        self.canvas.delete("all")
        for x, y in self.points:
            color = "red" if (x, y) == self.selected_point else "blue"
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color)
        for (x1, y1), (x2, y2) in self.lines:
            self.canvas.create_line(x1, y1, x2, y2, width=2)

root = tk.Tk()
app = GridGUI(root, 400)
root.mainloop()
