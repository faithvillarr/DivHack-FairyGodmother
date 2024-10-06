# 1. create separate lists of types from the database
# 2. iterate through each clothing_type, finding the item that most closely matches the palette
# 3. return the chosen set of items

# NOTE: two functions left to implement: reading items and palette from database, and (DONE)comparing hex vals <3
from db_management import get_clothing_info
from choose_pin_from_board import choose_pin
from palette_generator import generate_color_palette

def compare_five_hex (hex_l1, hex_l2):
    print('+++++++++++++++++', hex_l1, hex_l2)
    similarity_sum = 0 # higher == less similar
    for i in hex_l1:
        for j in hex_l2:
            similarity_sum = compare_hex(i, j)
    return similarity_sum

def compare_hex(hex1, hex2):
    # Get red/green/blue int values of hex1
    hex1 = hex1[1:]
    hex2 = hex2[1:]

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



def find_closest_matches(username, palette):
    lists = pull_from_database(username) # tops {item: hex}, bottoms, dresses, shoes, outerwear, accessories
    palette = palette.split()
    print(f'The palette now contains {palette}')

    similarities = {}
    items = []

    for i in ['top', 'bottoms', 'dress']: # Looking at shirt, bottoms and dresses.
        clothing_type = lists[i] # Returns list of lists. Inner list holds [name, hex_string]
        max_similarity = 0
        max_item = None
        for item in clothing_type:
            item_hex = item[1].strip().split()
            # print(f'The item_hex now contains {item_hex}.')
            # print(f'Palette: {palette} {type(palette)}{type(palette[0])}\nItem Hex: {item_hex}{type(item_hex)}{type(item_hex[0])}')
            curr_similarity_score = compare_five_hex(palette, item_hex)
            if curr_similarity_score > max_similarity:
                max_similarity = curr_similarity_score
                max_item = item
        
        similarities[i] = (max_item, max_similarity)
        print(f'Similarities: {similarities}')

        # choose dress or top/bottom
        if max(similarities["top"][1], similarities["bottoms"][1]) < similarities["dress"][1]:
            items = ["dress", "shoes", "outerwear", "accessories", "accessories"]
        else:
            items = ["top", "bottoms", "shoes", "outerwear", "accessories"]

    for clothing_type in items: # literally the clothing_type
        found_clothing = lists[clothing_type]
        final_items = [] # Store object names to retrieve later from database

        for item in found_clothing:
            if not similarities[clothing_type] or (similarities[clothing_type] and clothing_type == "accessories"):
                if similarities[clothing_type]: # account for the second accessories item
                    clothing_type.remove(similarities[clothing_type][0]) # remove the max item
                max_similarity = 0
                max_item = None
                for obj_name, hex_vals in item:
                    hex_values = item[1].strip().split()
                    curr_hex_val = compare_five_hex(palette, hex_vals)
                    if curr_hex_val > max_similarity:
                        max_similarity = curr_hex_val
                        max_item = item
                final_items.append(max_item)
    
    return final_items

if __name__ == "__main__":
    # board_url = "https://www.pinterest.com/bookeater999/fall-2024/"  # Replace with actual Pinterest board URL
    # MAX_PINS = 20  # Set the maximum number of pins you want to download
    # CHROMEDRIVER_PATH = "C:\Program Files\Google\Chrome"
    palette = '#EBEBEA #3C405A #AF7E4B #0D0D1E #C8BEB3'

    res = find_closest_matches('janedoe', palette)
    print(res)

    # a = ['#303837', '#FCFCFB', '#CEC7B6', '#7C8175', '#4B5652']
    # b = ['#596164', '#FEFEFE', '#929899', '#717A7C', '#BBBFBF']
    # res = compare_five_hex(a, b)
    # print(res)
