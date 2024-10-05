import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.cluster import MiniBatchKMeans

# Returns five RGB lists in a list
def generate_color_palette(image_path, num_colors=5):
    # Load the image
    image = Image.open(image_path)
    
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

    # Convert rgb to hex

    
    # Display the palette
    # plt.figure(figsize=(8, 2))
    # plt.title(f'Color Palette ({num_colors} colors)')
    # for i, color in enumerate(colors):
    #     plt.subplot(1, num_colors, i + 1)
    #     plt.axis('off')

    #     plt.imshow([[color]])  # Display each color
    #     plt.text(0, 0.5, f'#{color[0]:02X}{color[1]:02X}{color[2]:02X}', va='center', ha='center', fontsize=10)
    # plt.show()

    return colors


# Path to your local image
image_path = 'clothing-images\sample_image_shirt.jpg'

# Generate and display the color palette
generate_color_palette(image_path, num_colors=5)

