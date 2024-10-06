import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.cluster import MiniBatchKMeans

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2]).upper()

# Returns five RGB lists in a list
# Input: Image type
def generate_color_palette(image, num_colors=5):
    
    # Aggressively resize the image to reduce computation
    image = image.resize((50, 50))  # Small size for faster processing
    
    # Convert image to a 2D array of RGB values
    image_data = np.array(image)
    image_data = image_data.reshape((-1, 3))  # Flatten the image into a 2D array
    
    # Subsample the image data for faster processing
    subsample = image_data[np.random.choice(image_data.shape[0], size=1000, replace=False)]
    
    # Use MiniBatchKMeans for faster clustering with fewer iterations
    kmeans = MiniBatchKMeans(n_clusters=num_colors, max_iter=50)  # Limit iterations for speed
    kmeans.fit(subsample)
    
    # Stores clusters as five lists of rgb values. 
    colors = kmeans.cluster_centers_.astype(int)

    res = ""
    for i in colors:
        res += rgb_to_hex(i) + " "
        
    # Returns the five HEX values in a string. 
    return res 



