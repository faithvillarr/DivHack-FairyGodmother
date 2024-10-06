from pymongo import MongoClient, ASCENDING
import bcrypt
from palette_generator import generate_color_palette

from accessing_s3 import upload_file_to_s3
from accessing_s3 import download_image_from_s3
from PIL import Image


# Replace with your actual MongoDB connection string
connection_string = "mongodb+srv://faithmvillarreal:Z0jvySKubC8uShGx@fairycluster.0fyob.mongodb.net/y"
client = MongoClient(connection_string)

# Access the databases
user_db = client['UserData']
user_collection = user_db['Users']
image_db = client['Clothing']
image_collection = image_db['Closet'] 

# Set username as the primary key
user_collection.create_index("username", unique=True)

# Function to create a user
def create_user(first_name, last_name, username, email, password):
    # Check if already exist in db
    if user_collection.find_one({"username": username}):
        print("User already exists!")
        return False
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    user_document = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "password": hashed_password
    }
    
    user_collection.insert_one(user_document)
    print(f"User '{username}' created successfully!")
    return True

# Function to upload an image
def upload_clothing_image(image_path, username):
    # Check if the user exists
    if not user_collection.find_one({"username": username}):
        print("User does not exist!")
        return False

    obj_name = upload_file_to_s3(image_path)
    if obj_name is None:
        return False
    image = Image.open(image_path)
    colors = generate_color_palette(image)
    
    # Create a clothing image document
    image_document = {
        "image-name": obj_name,
        "username": username,
        "rgb_colors": colors
    }
    
    image_collection.insert_one(image_document)
    print(f"Image uploaded successfully for user '{username}'!")
    return True

# Return names of all 
def get_clothing_names(username):
    # Query the database for images associated with the given username
    images = image_collection.find({"username": username})

    # Extract the "image-name" field from each document and return a list of those names
    image_names = [image.get("image-name") for image in images]
    return image_names


# Function to get clothing instances for a specific user
def get_user_clothing_instances(username):
    # Find the user
    user = user_collection.find_one({"username": username})
    if not user:
        print("User not found!")
        return []

    # Find clothing images associated with the user
    images = get_clothing_names(username)
    print(f'We grabbed {len(images)} images from {username}')

    for i in images:
        download_image_from_s3(i)

        
    return images

def close_connection():
    client.close()

def grab_closet_urls(username):
    # Query the database for images associated with the given username
    images = get_clothing_names(username)  # Use the helper function to get image names
    
    # Base URL for S3 bucket (replace with your bucket's actual base URL)
    s3_base_url = "https://fairyclothing.s3.us-east-2.amazonaws.com/"
    
    # Create full URLs by appending image names to the base URL
    image_urls = [f"{s3_base_url}{image_name}" for image_name in images]
    
    # Return the list of URLs
    return image_urls

# Example usage
if __name__ == "__main__":
    print(grab_closet_urls('janedoe'))
    
    # # Create a new user
    # create_user("Jane", "Doe", "janedoe", "jane@example.com", "mypassword")

    # # Upload a clothing image
    # image_path = 'clothing-images/sample_image_shirt.jpg'
    # upload_clothing_image(image_path, "janedoe")  # Example RGB colors

    # # Retrieve clothing instances for a user
    # clothing_instances = get_user_clothing_instances("janedoe")
    # for i in clothing_instances:
    #     print(i)
    
    # print(clothing_instances)
    # for image in clothing_instances:
    #     print(image)

    # Close the connection
    close_connection()
    

