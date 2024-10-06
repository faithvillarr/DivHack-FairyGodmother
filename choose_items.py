# 1. create separate lists of types from the database
# 2. iterate through each type, finding the item that most closely matches the palette
# 3. return the chosen set of items

# NOTE: two functions left to implement: reading items and palette from database, and (DONE)comparing hex vals <3

def hex_color_delta(hex1, hex2):
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

def pull_from_database():
    return 1


def find_closest_matches(palette):
    lists = pull_from_database() # tops {item: hex}, bottoms, dresses, shoes, outerwear, accessories

    similarities = {}

    for i in range(3):
        type = lists[i]
        max_similarity = 0
        max_item = None
        for item in type:
            hex = compare_hex(item, palette, type)
            if hex > max_similarity:
                max_similarity = hex
                max_item = item
        similarities[type] = (max_item, max_similarity)

        # choose dress or top/bottom
        if max(similarities["top"][1], similarities["bottom"][1]) < similarities["dress"][1]:
            items = ["dress", "shoes", "outerwear", "accessories", "accessories"]
        else:
            items = ["top", "bottom", "shoes", "outerwear", "accessories"]

    for type in items:
        final_items = []
        if not similarities[type] or (similarities[type] and type == "accessories"):
            if similarities[type]: # account for the second accessories item
                type.remove(similarities[type][0]) # remove the max item
            max_similarity = 0
            max_item = None
            for item in type:
                hex = compare_hex(item, palette, type)
                if hex > max_similarity:
                    max_similarity = hex
                    max_item = item
            final_items.append(max_item)
    
    return final_items

find_closest_matches(palette)