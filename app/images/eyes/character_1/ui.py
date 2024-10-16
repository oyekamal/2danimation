import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Initialize the window
root = tk.Tk()
root.title("Streaming Platform Image Overlay")

# Variables to track position, size, and flipped state
x_offset = 0
y_offset = 0
scale_factor = 1
flipped = False

# Frame for left-side controls (buttons, sliders, and size/position display)
control_frame = tk.Frame(root)
control_frame.pack(side=tk.LEFT, fill=tk.Y)

# Canvas for image display
canvas = tk.Canvas(root)
canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

# Labels to show the current image width, height, x, and y position
width_label = tk.Label(control_frame, text="Width: 0")
height_label = tk.Label(control_frame, text="Height: 0")
x_label = tk.Label(control_frame, text="X Position: 0")
y_label = tk.Label(control_frame, text="Y Position: 0")

# Display the labels
width_label.pack(pady=5, fill=tk.X)
height_label.pack(pady=5, fill=tk.X)
x_label.pack(pady=5, fill=tk.X)
y_label.pack(pady=5, fill=tk.X)

# Copy x, y to clipboard
def copy_xy_to_clipboard():
    xy_position = f"{x_offset},{y_offset}"
    root.clipboard_clear()
    root.clipboard_append(xy_position)
    root.update()  # Keeps the clipboard updated

# Copy width, height to clipboard
def copy_wh_to_clipboard():
    wh_size = f"{int(overlay_img.width * scale_factor)},{int(overlay_img.height * scale_factor)}"
    root.clipboard_clear()
    root.clipboard_append(wh_size)
    root.update()  # Keeps the clipboard updated

# Load background image function
def load_background():
    global bg_img, bg_tk, canvas, x_slider, y_slider
    file_path = filedialog.askopenfilename()
    if file_path:
        bg_img = Image.open(file_path)
        bg_tk = ImageTk.PhotoImage(bg_img)

        # Resize window and canvas to match the background image
        root.geometry(f"{bg_img.width+200}x{bg_img.height+100}")  # Extra width for control panel
        canvas.config(width=bg_img.width, height=bg_img.height)

        canvas.create_image(0, 0, anchor=tk.NW, image=bg_tk)

        # Dynamically adjust slider ranges based on the background image size
        x_slider.config(from_=-bg_img.width, to=bg_img.width)
        y_slider.config(from_=-bg_img.height, to=bg_img.height)

# Load transparent image and overlay function
def load_transparent_image():
    global overlay_img, overlay_tk, overlay_canvas_id
    file_path = filedialog.askopenfilename()
    if file_path:
        overlay_img = Image.open(file_path).convert("RGBA")
        update_overlay()

# Update image position, size, and the displayed values
def update_overlay():
    global overlay_tk, overlay_canvas_id, flipped
    # Rescale the image
    resized_img = overlay_img.resize((int(overlay_img.width * scale_factor), int(overlay_img.height * scale_factor)))

    # Flip the image if required
    if flipped:
        resized_img = resized_img.transpose(Image.FLIP_LEFT_RIGHT)

    overlay_tk = ImageTk.PhotoImage(resized_img)

    # If image already exists, update it, otherwise create a new one
    if "overlay_canvas_id" in globals():
        canvas.coords(overlay_canvas_id, x_offset, y_offset)
        canvas.itemconfig(overlay_canvas_id, image=overlay_tk)
    else:
        overlay_canvas_id = canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=overlay_tk)

    # Update the labels with the current size and position
    width_label.config(text=f"Width: {int(overlay_img.width * scale_factor)}")
    height_label.config(text=f"Height: {int(overlay_img.height * scale_factor)}")
    x_label.config(text=f"X Position: {x_offset}")
    y_label.config(text=f"Y Position: {y_offset}")

# Remove overlay image function
def remove_overlay_image():
    global overlay_canvas_id
    if "overlay_canvas_id" in globals():
        canvas.delete(overlay_canvas_id)
        del overlay_canvas_id

# Slider functions
def change_size(val):
    global scale_factor
    scale_factor = float(val)
    update_overlay()

def move_x(val):
    global x_offset
    x_offset = int(val)
    update_overlay()

def move_y(val):
    global y_offset
    y_offset = int(val)
    update_overlay()

# Function to flip image horizontally
def flip_image():
    global flipped
    flipped = not flipped
    update_overlay()

# Buttons to load images
btn_bg = tk.Button(control_frame, text="Open Background", command=load_background)
btn_bg.pack(pady=5, fill=tk.X)

btn_overlay = tk.Button(control_frame, text="Open Transparent Image", command=load_transparent_image)
btn_overlay.pack(pady=5, fill=tk.X)

# Button to flip the image horizontally
btn_flip = tk.Button(control_frame, text="Flip Image Horizontally", command=flip_image)
btn_flip.pack(pady=5, fill=tk.X)

# Button to remove the transparent image
btn_remove_overlay = tk.Button(control_frame, text="Remove Transparent Image", command=remove_overlay_image)
btn_remove_overlay.pack(pady=5, fill=tk.X)

# Sliders for scaling and positioning in control frame
size_slider = tk.Scale(control_frame, from_=0.1, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, label="Resize", command=change_size)
size_slider.pack(pady=5, fill=tk.X)

x_slider = tk.Scale(control_frame, from_=-400, to=400, orient=tk.HORIZONTAL, label="Move Left/Right", command=move_x)
x_slider.pack(pady=5, fill=tk.X)

y_slider = tk.Scale(control_frame, from_=-400, to=400, orient=tk.HORIZONTAL, label="Move Up/Down", command=move_y)
y_slider.pack(pady=5, fill=tk.X)

# Buttons to copy x, y and width, height to clipboard
btn_copy_xy = tk.Button(control_frame, text="Copy X,Y", command=copy_xy_to_clipboard)
btn_copy_xy.pack(pady=5, fill=tk.X)

btn_copy_wh = tk.Button(control_frame, text="Copy Width,Height", command=copy_wh_to_clipboard)
btn_copy_wh.pack(pady=5, fill=tk.X)

# Start the application
root.mainloop()
