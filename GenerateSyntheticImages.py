from PIL import Image, ImageDraw
import numpy as np
import os
import sys

# Load the reference images
viable_image_path = 'ExampleData/viable.png'  # Update with correct path if necessary
non_viable_image_path = 'ExampleData/non-viable.png'  # Update with correct path if necessary

viable_image = Image.open(viable_image_path)
non_viable_image = Image.open(non_viable_image_path)

def is_overlapping(x, y, existing_positions, radius):
    for (ex, ey) in existing_positions:
        if np.sqrt((x - ex)**2 + (y - ey)**2) < 2 * radius:
            return True
    return False

def is_within_circle(x, y, center, radius):
    return np.sqrt((x - center[0])**2 + (y - center[1])**2) <= radius

# Function to create synthetic frog egg images
def create_synthetic_frog_egg_image(viable_img, non_viable_img, num_viable=50, num_non_viable=50, image_size=(1000, 1000)):
    synthetic_image = Image.new('RGBA', image_size, (160, 172, 185, 255))  # light grey.     (119, 117, 104, 255).  (90, 80, 68, 255)
    egg_radius = 20  # radius for synthetic eggs
    viable_img_resized = viable_img.resize((egg_radius * 2, egg_radius * 2))
    non_viable_img_resized = non_viable_img.resize((egg_radius * 2, egg_radius * 2))

    positions = []
    center = (image_size[0] // 2, image_size[1] // 2)
    circle_radius = 500  # radius 500 for a diameter of 1000
    margin = egg_radius + 4  # margin from the perimeter

    # Place viable eggs
    for _ in range(num_viable):
        while True:
            x = np.random.randint(margin, image_size[0] - margin)
            y = np.random.randint(margin, image_size[1] - margin)
            if not is_overlapping(x, y, positions, egg_radius) and is_within_circle(x, y, center, circle_radius - margin):
                positions.append((x, y))
                synthetic_image.paste(viable_img_resized, (x - egg_radius, y - egg_radius), viable_img_resized)
                break

    # Place non-viable eggs
    for _ in range(num_non_viable):
        while True:
            x = np.random.randint(margin, image_size[0] - margin)
            y = np.random.randint(margin, image_size[1] - margin)
            if not is_overlapping(x, y, positions, egg_radius) and is_within_circle(x, y, center, circle_radius - margin):
                positions.append((x, y))
                synthetic_image.paste(non_viable_img_resized, (x - egg_radius, y - egg_radius), non_viable_img_resized)
                break

    # Create a circular mask with a grey circle and a black rim
    grey_circle = Image.new('RGBA', image_size, (0, 0, 0, 255))  # black
    grey_circle_mask = Image.new('L', image_size, 0)
    draw = ImageDraw.Draw(grey_circle_mask)
    draw.ellipse((center[0] - circle_radius, center[1] - circle_radius,
                  center[0] + circle_radius, center[1] + circle_radius), fill=255)
    grey_circle.paste(synthetic_image, (0, 0), grey_circle_mask)

    # Create the black rim
    draw = ImageDraw.Draw(grey_circle)
    draw.ellipse((center[0] - circle_radius, center[1] - circle_radius,
                  center[0] + circle_radius, center[1] + circle_radius), outline=(211, 211, 211, 255)) # light grey

    return grey_circle

# Create directories for synthetic dataset
os.makedirs('synthetic_frog_eggs/mixture', exist_ok=True)

# Generate synthetic images
num_images = 2
for i in range(num_images):
    # Create image with both viable and non-viable eggs
    synthetic_image = create_synthetic_frog_egg_image(viable_image, non_viable_image, num_viable=int(sys.argv[1]), num_non_viable=int(sys.argv[2]))
    synthetic_image.save(f'synthetic_frog_eggs/mixture/synthetic_frog_egg_{i}.png')

print('Synthetic frog egg images generated successfully.')
