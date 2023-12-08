import numpy as np
from PIL import Image

def calculate_score(image_location):
    location_normalized = image_location * 2.0 - 1.0  # -1 to 1
    location_normalized = 1.0 - np.abs(location_normalized)  # 0.01s on border, 1s in centers

    if np.min(location_normalized) < 0.0:
        return 0.0

    score = np.clip(location_normalized[0] * location_normalized[1], 0.001, 1.0)  # Clamping between 0.001 and 1
    return score ** 10.0  # blendingPower is 10

def calculate_image_location(xyz, camera_mvp):
    print("Shape of MVP matrix:", camera_mvp.shape)  # Debug: Print shape of camera_mvp
    print("Shape of xyz vector:", xyz.shape)  # Debug: Print shape of xyz

    # Apply MVP transformation
    projected_xyz = camera_mvp @ xyz
    if projected_xyz[2] <= 0:
        return (0.0, 0.0), 0.0
    else:
        # Convert from homogeneous to 2D coordinates
        location = projected_xyz[:2] / projected_xyz[2]
        weight = calculate_score(location)
        return location, weight

# Clamping function to keep values within the image size
clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

def blend_images(image1, image2, camera1_mvp, camera2_mvp, back_color):
    # Assume images are the same size and have mode 'RGBA'
    width, height = image1.size

    output_image = Image.new('RGBA', (width, height), back_color)

    for y in range(height):
        for x in range(width):
            # Normalized pixel coordinates, assuming top-left is (0,0) and bottom-right is (1,1)
            px = (x + 0.5) / width  # Add 0.5 to target pixel center
            py = (y + 0.5) / height  # Add 0.5 to target pixel center
            position = np.array([px, py, 1.0, 1.0])  # Assume we're working with 2D images, Z=1 for simplicity

            # Calculate weights
            image1_location, image1_weight = calculate_image_location(position, camera1_mvp)
            image2_location, image2_weight = calculate_image_location(position, camera2_mvp)

            total_weight = image1_weight + image2_weight

            if total_weight == 0:
                continue  # If no weights, background is already set

            # Sampling colors from images using nearest neighbor and clamping to ensure within bounds
            image1_color = image1.getpixel((clamp(int(image1_location[0] * width), 0, width - 1), clamp(int(image1_location[1] * height), 0, height - 1)))
            image2_color = image2.getpixel((clamp(int(image2_location[0] * width), 0, width - 1), clamp(int(image2_location[1] * height), 0, height - 1)))

            # Normalize weights
            image1_weight /= total_weight
            image2_weight /= total_weight

            # Blend colors
            blended_color = [0, 0, 0, 0]
            for i in range(4):  # RGBA channels
                blended_color[i] = int(image1_color[i] * image1_weight + image2_color[i] * image2_weight)

            output_image.putpixel((x, y), tuple(blended_color))

    return output_image

# Example usage:

# Load images
image1 = Image.open('cat1.jpg').convert('RGBA')
image2 = Image.open('cat2.jpg').convert('RGBA')

camera1_mvp = np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0]
])

camera2_mvp = np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0]
])

# Define background color (as an RGBA tuple)
back_color = (255, 255, 255, 255)  # White background

# Blend images
blended_image = blend_images(image1, image2, camera1_mvp, camera2_mvp, back_color)

# Save or show the result
blended_image.save('blended_output.png')
blended_image.show()
