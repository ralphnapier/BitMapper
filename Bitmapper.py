import tkinter as tk
from tkinter import filedialog
from PIL import Image

class PixelGrid(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BitMapper")
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.threshold = 128  # Initial threshold value
        self.image_path = None  # Variable to store the path of the imported image
        self.pixel_size = 10  # Size of each pixel
        self.rectangles = []  # Store rectangle IDs
        self.image = None
        self.drawing = False  # State to track if the mouse is drawing
        self.brush_size = 1  # Initial brush size
        self.draw_color = "black"  # Initial drawing color
        self.pixel_state = [["white" for _ in range(128)] for _ in range(64)]  # Store the current state of each pixel

        # Create menu
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import Image", command=self.import_image)
        filemenu.add_command(label="Import Text File", command=self.import_text_file)  # Add import text file option
        filemenu.add_command(label="Export Bitmap Text File", command=self.export_binary_bitmap)  # Add export option
        menubar.add_cascade(label="File", menu=filemenu)

        threshold_menu = tk.Menu(menubar, tearoff=0)
        threshold_menu.add_command(label="Increase Threshold, [", command=self.increase_threshold)
        threshold_menu.add_command(label="Decrease Threshold, ]", command=self.decrease_threshold)
        menubar.add_cascade(label="Adjust Threshold", menu=threshold_menu)

        # Add plus and minus buttons to adjust the brush size
        brush_menu = tk.Menu(menubar, tearoff=0)
        brush_menu.add_command(label="Increase Brush Size, +", command=self.increase_brush_size)
        brush_menu.add_command(label="Decrease Brush Size, -", command=self.decrease_brush_size)
        menubar.add_cascade(label="Adjust Brush Size", menu=brush_menu)

        # Add shift left, right, up, and down buttons
        shift_menu = tk.Menu(menubar, tearoff=0)
        shift_menu.add_command(label="Shift Left", command=self.shift_left)
        shift_menu.add_command(label="Shift Right", command=self.shift_right)
        shift_menu.add_command(label="Shift Up", command=self.shift_up)
        shift_menu.add_command(label="Shift Down", command=self.shift_down)
        menubar.add_cascade(label="Shift Pixels", menu=shift_menu)

        self.config(menu=menubar)

        # Bind keys to their functions
        self.bind("<KeyPress-bracketleft>", self.decrease_threshold)  # "["
        self.bind("<KeyPress-bracketright>", self.increase_threshold)  # "]"
        self.bind("<KeyPress-braceleft>", self.decrease_threshold_by_one)  # "{"
        self.bind("<KeyPress-braceright>", self.increase_threshold_by_one)  # "}"
        self.bind("<KeyPress-minus>", self.decrease_brush_size)  # "-"
        self.bind("<KeyPress-plus>", self.increase_brush_size)  # "+"
        self.bind("<KeyPress-equal>", self.increase_brush_size)  # "=" (usually used for "+" without shift)
        self.bind("<Configure>", self.on_resize)

        # Bind arrow keys to shift functions
        self.bind("<Left>", self.shift_left)
        self.bind("<Right>", self.shift_right)
        self.bind("<Up>", self.shift_up)
        self.bind("<Down>", self.shift_down)

        # Bind mouse events for drawing and zooming
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonPress-3>", self.toggle_draw_color)  # Right click to toggle color
        self.canvas.bind("<MouseWheel>", self.zoom)

    def draw_grid(self):
        self.canvas.delete("all")
        self.rectangles = []
        for i in range(64):
            row = []
            for j in range(128):
                x1, y1 = j * self.pixel_size, i * self.pixel_size
                x2, y2 = x1 + self.pixel_size, y1 + self.pixel_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.pixel_state[i][j], outline="")
                row.append(rect)
            self.rectangles.append(row)

    def import_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.process_image(file_path)

    def process_image(self, file_path):
        image = Image.open(file_path).convert("L")  # Convert to grayscale
        aspect_ratio = image.width / image.height

        # Calculate new size while maintaining aspect ratio
        if aspect_ratio > 128 / 64:
            new_width = 128
            new_height = int(128 / aspect_ratio)
        else:
            new_height = 64
            new_width = int(64 * aspect_ratio)

        self.image = image.resize((new_width, new_height), Image.LANCZOS)
        self.offset_x = (128 - new_width) // 2
        self.offset_y = (64 - new_height) // 2
        self.update_canvas()

    def update_canvas(self):
        if not self.image:
            return
        for i in range(64):
            for j in range(128):
                color = self.pixel_state[i][j]
                self.canvas.itemconfig(self.rectangles[i][j], fill=color)

    def increase_threshold(self, event=None):
        self.threshold = min(self.threshold + 10, 255)  # Increase threshold, max 255
        self.update_image_pixels()

    def decrease_threshold(self, event=None):
        self.threshold = max(self.threshold - 10, 0)  # Decrease threshold, min 0
        self.update_image_pixels()

    def increase_threshold_by_one(self, event=None):
        self.threshold = min(self.threshold + 1, 255)  # Increase threshold by 1, max 255
        self.update_image_pixels()

    def decrease_threshold_by_one(self, event=None):
        self.threshold = max(self.threshold - 1, 0)  # Decrease threshold by 1, min 0
        self.update_image_pixels()

    def update_image_pixels(self):
        if not self.image:
            return
        for i in range(64):
            for j in range(128):
                if self.offset_y <= i < self.offset_y + self.image.height and self.offset_x <= j < self.offset_x + self.image.width:
                    pixel_value = self.image.getpixel((j - self.offset_x, i - self.offset_y))
                    color = "black" if pixel_value < self.threshold else "white"
                    self.pixel_state[i][j] = color
        self.update_canvas()

    def on_resize(self, event):
        self.draw_grid()

    def start_drawing(self, event):
        self.drawing = True
        self.draw(event)

    def stop_drawing(self, event):
        self.drawing = False

    def draw(self, event):
        if not self.drawing:
            return
        x, y = event.x, event.y
        j = x // self.pixel_size
        i = y // self.pixel_size
        for di in range(-self.brush_size + 1, self.brush_size):
            for dj in range(-self.brush_size + 1, self.brush_size):
                ni, nj = i + di, j + dj
                if 0 <= ni < 64 and 0 <= nj < 128:
                    self.canvas.itemconfig(self.rectangles[ni][nj], fill=self.draw_color)
                    self.pixel_state[ni][nj] = self.draw_color

    def toggle_draw_color(self, event):
        self.draw_color = "white" if self.draw_color == "black" else "black"

    def zoom(self, event):
        if event.delta > 0:
            self.pixel_size = min(self.pixel_size + 1, 50)  # Zoom in
        else:
            self.pixel_size = max(self.pixel_size - 1, 1)  # Zoom out
        self.draw_grid()

    def increase_brush_size(self, event=None):
        self.brush_size = min(self.brush_size + 1, 10)  # Max brush size 10

    def decrease_brush_size(self, event=None):
        self.brush_size = max(self.brush_size - 1, 1)  # Min brush size 1

    def export_binary_bitmap(self):
        binary_bitmap = []
        for i in range(64):
            line = []
            byte = 0
            for j in range(128):
                if j % 8 == 0 and j != 0:
                    line.append(f"0b{format(byte, '08b')},")
                    byte = 0
                color = self.canvas.itemcget(self.rectangles[i][j], "fill")
                if color == "white":  # Inverted condition
                    byte |= (1 << (7 - (j % 8)))
            line.append(f"0b{format(byte, '08b')},")
            binary_bitmap.append(' '.join(line))

        # Save the binary bitmap to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for line in binary_bitmap:
                    file.write(line + "\n")

    def import_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                lines = file.readlines()
            
            # Reset the canvas
            self.draw_grid()
            
            for i in range(64):
                line = lines[i].strip().split(',')
                for j in range(128 // 8):
                    byte = int(line[j], 2)
                    for bit in range(8):
                        if byte & (1 << (7 - bit)):
                            self.pixel_state[i][j * 8 + bit] = "white"
                            self.canvas.itemconfig(self.rectangles[i][j * 8 + bit], fill="white")
                        else:
                            self.pixel_state[i][j * 8 + bit] = "black"
                            self.canvas.itemconfig(self.rectangles[i][j * 8 + bit], fill="black")

    def shift_left(self, event=None):
        new_pixel_state = [["white" for _ in range(128)] for _ in range(64)]
        for i in range(64):
            for j in range(1, 128):
                new_pixel_state[i][j-1] = self.pixel_state[i][j]
        self.pixel_state = new_pixel_state
        self.update_canvas()

    def shift_right(self, event=None):
        new_pixel_state = [["white" for _ in range(128)] for _ in range(64)]
        for i in range(64):
            for j in range(127):
                new_pixel_state[i][j+1] = self.pixel_state[i][j]
        self.pixel_state = new_pixel_state
        self.update_canvas()

    def shift_up(self, event=None):
        new_pixel_state = [["white" for _ in range(128)] for _ in range(64)]
        for i in range(1, 64):
            for j in range(128):
                new_pixel_state[i-1][j] = self.pixel_state[i][j]
        self.pixel_state = new_pixel_state
        self.update_canvas()

    def shift_down(self, event=None):
        new_pixel_state = [["white" for _ in range(128)] for _ in range(64)]
        for i in range(63):
            for j in range(128):
                new_pixel_state[i+1][j] = self.pixel_state[i][j]
        self.pixel_state = new_pixel_state
        self.update_canvas()

if __name__ == "__main__":
    app = PixelGrid()
    app.draw_grid()
    app.mainloop()
