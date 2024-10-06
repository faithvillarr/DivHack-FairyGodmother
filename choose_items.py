# 1. create separate lists of types from the database
# 2. iterate through each clothing_type, finding the item that most closely matches the palette
# 3. return the chosen set of items

# NOTE: two functions left to implement: reading items and palette from database, and (DONE)comparing hex vals <3
from db_management import get_clothing_info

def compare_hex(hex1, hex2):
    # Get red/green/blue int values of hex1
    r1 = int(hex1[0:2], 16)
    g1 = int(hex1[2:4], 16)
    b1 = int(hex1[4:6], 16)
    
    # Get red/green/blue int values of hex2
    r2 = int(hex2[0:2], 16)
    g2 = int(hex2[2:4], 16)
    b2 = int(hex2[4:6], 16)
    
    # Calculate differences between reds, greens, and blues
    r = 255 - abs(r1 - r2)
    g = 255 - abs(g1 - g2)
    b = 255 - abs(b1 - b2)
    
    # Limit differences between 0 and 1
    r /= 255
    g /= 255
    b /= 255
    
    return (r + g + b) / 3

def pull_from_database(username):
    # Get hex values of each clothing belonging to user for each clothing clothing_type
    clothing_types = ['top', 'bottoms', 'dress', 'shoes', 'outerwear', 'accessories']
    clothing_items = {clothing_type: [] for clothing_type in clothing_types}
    
    # Query the database for clothing items associated with the user
    items = get_clothing_info(username)
    
    for item in items:
        clothing_type = item['clothing_type']
        clothing_items[clothing_type].append([item['image_name'], item['rgb_colors']])

    # hex_list = hex_colors.strip().split()
    
    return clothing_items



def find_closest_matches(palette):
    lists = pull_from_database() # tops {item: hex}, bottoms, dresses, shoes, outerwear, accessories

    similarities = {}

    for i in range(3):
        clothing_type = lists[i] # Chooses shirt, then botooms, dress, etc.
        max_similarity = 0
        max_item = None
        for item in clothing_type:
            hex = compare_hex(item, palette, clothing_type)
            if hex > max_similarity:
                max_similarity = hex
                max_item = item
        similarities[clothing_type] = (max_item, max_similarity)

        # choose dress or top/bottom
        if max(similarities["top"][1], similarities["bottom"][1]) < similarities["dress"][1]:
            items = ["dress", "shoes", "outerwear", "accessories", "accessories"]
        else:
            items = ["top", "bottom", "shoes", "outerwear", "accessories"]

    for clothing_type in items:
        final_items = []
        if not similarities[clothing_type] or (similarities[clothing_type] and clothing_type == "accessories"):
            if similarities[clothing_type]: # account for the second accessories item
                clothing_type.remove(similarities[clothing_type][0]) # remove the max item
            max_similarity = 0
            max_item = None
            for item in clothing_type:
                hex = compare_hex(item, palette, clothing_type)
                if hex > max_similarity:
                    max_similarity = hex
                    max_item = item
            final_items.append(max_item)
    
    return final_items

if __name__ == "__main__":
    print(pull_from_database('janedoe'))