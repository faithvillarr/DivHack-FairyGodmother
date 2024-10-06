# install ....????

# 1. create separate lists of types from the database
# 2. iterate through each type, finding the item that most closely matches the palette
# 3. return the chosen set of items

def find_closest_matches(palette):
    lists = pull_items_from_database() # tops {item: hex}, bottoms, dresses, shoes, outerwear, accessories

    similarities = {}

    for i in range(3):
        type = lists[i]
        max_similarity = 0
        for item in type:
            max_similarity = max(max_similarity, compare_hex(item, palette, type))
        similarities[type] = (item, max_similarity)
        if max(similarities["top"][1], similarities["bottom"][1]) < similarities["dress"][1]:
            items = ["dress", "shoes", "outerwear", "accessories", "accessories"]
        else:
            items = ["top", "bottom", "shoes", "outerwear", "accessories"]

    # find similarities for top/bottom and dress and decide between the two
    # find similarities for all other types: if dress chosen, choose accessories twice

    if max(similarities["top"][1], similarities["bottom"][1]) < similarities["dress"][1]:
        items = [similarities["dress"], similarities["shoes"], similarities["outerwear"], similarities["accessories"]]

find_closest_matches(palette)