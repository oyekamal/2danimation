import cv2
import numpy as np
from matplotlib import pyplot as plt




def overlay_eyes_on_head(head_img, eyes_img, eye_width_percent, eye_height_percent, x_offset, y_offset, flip_horizontal=False):
    """
    Overlay an eyes image onto a head image at the specified location with given dimensions.

    Parameters:
    - head_img (np.array): Head image array.
    - eyes_img (np.array): Eyes image array.
    - eye_width_percent (float): Width of the eyes image as a percentage of the head image.
    - eye_height_percent (float): Height of the eyes image as a percentage of the head image.
    - x_offset (int): X location on the head image where the eyes should be placed.
    - y_offset (int): Y location on the head image where the eyes should be placed.
    - flip_horizontal (bool): Whether to flip the eyes image horizontally (default is False).
    """
    
    # Check if images are loaded correctly
    if head_img is None or eyes_img is None:
        raise ValueError("Head image or eyes image not loaded properly.")
    
    # Function to resize overlay image based on percentage of the original image
    def resize_image(img, width_percent, height_percent):
        width = int(img.shape[1] * width_percent / 100)
        height = int(img.shape[0] * height_percent / 100)
        return cv2.resize(img, (width, height))

    # Resize the overlay image based on the specified percentage
    eyes_img_resized = resize_image(eyes_img, eye_width_percent, eye_height_percent)

    # Flip the eyes image horizontally if specified
    if flip_horizontal:
        eyes_img_resized = cv2.flip(eyes_img_resized, 1)

    # Get dimensions of the overlay
    overlay_height, overlay_width = eyes_img_resized.shape[:2]
    y1, y2 = y_offset, y_offset + overlay_height
    x1, x2 = x_offset, x_offset + overlay_width

    # Adjust the overlay dimensions if it exceeds the base image's boundaries
    if y2 > head_img.shape[0]:
        y2 = head_img.shape[0]
        eyes_img_resized = eyes_img_resized[:(y2 - y1), :, :]  # Clip the overlay height

    if x2 > head_img.shape[1]:
        x2 = head_img.shape[1]
        eyes_img_resized = eyes_img_resized[:, :(x2 - x1), :]  # Clip the overlay width

    # Extract the alpha channel from the overlay (for PNG with transparency)
    if eyes_img_resized.shape[2] == 4:
        alpha_channel = eyes_img_resized[:, :, 3] / 255.0
        alpha_background = 1.0 - alpha_channel
        eyes_rgb = eyes_img_resized[:, :, :3]  # Get RGB channels
    else:
        eyes_rgb = eyes_img_resized
        alpha_channel = np.ones(eyes_rgb.shape[:2])
        alpha_background = 1.0 - alpha_channel

    # Blend the overlay onto the base image
    for c in range(0, 3):
        head_img[y1:y2, x1:x2, c] = (alpha_channel * eyes_rgb[:, :, c] +
                                     alpha_background * head_img[y1:y2, x1:x2, c])

    # Convert BGR image to RGB for displaying with Matplotlib
    head_img_rgb = cv2.cvtColor(head_img, cv2.COLOR_BGR2RGB)

    # Display the final image in the notebook
    plt.imshow(head_img_rgb)
    plt.axis('off')  # Hide the axes
    plt.show()
