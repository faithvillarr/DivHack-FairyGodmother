import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.cluster import MiniBatchKMeans

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2]).upper()

# Returns five RGB lists in a list
# Input: Image type
def generate_color_palette(image, num_colors=5):
    # Convert image to RGB if it has an alpha channel (transparency) or is grayscale
    if image.mode in ('RGBA', 'LA', 'P', 'L'):  # 'P' for paletted images, 'L' for grayscale
        image = image.convert('RGB')

    # Aggressively resize the image to reduce computation
    image = image.resize((50, 50))  # Small size for faster processing

    # Convert image to a 2D array of RGB values
    image_data = np.array(image)
    
    # Check the shape to ensure it's a (50*50, 3) shape
    if image_data.shape[-1] != 3:
        raise ValueError(f"Image data has {image_data.shape[-1]} channels, expected 3 (RGB).")

    # Flatten the image into a 2D array (pixels, RGB values)
    image_data = image_data.reshape((-1, 3))  # Now it should have shape (2500, 3)

    # Subsample the image data for faster processing
    subsample = image_data[np.random.choice(image_data.shape[0], size=1000, replace=False)]

    # Use MiniBatchKMeans for faster clustering with fewer iterations
    kmeans = MiniBatchKMeans(n_clusters=num_colors, max_iter=50)  # Limit iterations for speed
    kmeans.fit(subsample)

    # Stores clusters as five lists of RGB values. 
    colors = kmeans.cluster_centers_.astype(int)

    # Convert RGB to hex format and return as a string
    res = ""
    for i in colors:
        res += rgb_to_hex(i) + " "
        
    return res.strip()  # Trim extra space at the end




