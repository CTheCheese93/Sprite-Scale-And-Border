from xml.dom.minidom import parse
from PIL import Image, ImageDraw, ImageFont
import os

from magnified_px import MagnifiedPx as x6px
from sprite_image import SpriteImage

parent_directory = os.getcwd()

# Getting List of Assets from AssetStudio XML Export
def get_assets():
    document = parse("assets.xml")
    assets = document.getElementsByTagName("Asset")
    return assets

# Extracting Creatures from Asset List
def load_creatures():
    creatures_dict = {}

    assets = get_assets()

    for a in assets:
        container_path = a.getElementsByTagName("Container")[0].firstChild.nodeValue.split("/")
        creature = container_path[len(container_path)-1]
        
        if creature not in creatures_dict and creature.find("_glow") == -1:
            creatures_dict[creature] = []

        if creature.find("_glow") == -1:
            creatures_dict[creature].append(a.getElementsByTagName("Name")[0].firstChild.nodeValue.replace(" ", "_"))

    return creatures_dict

# Not actually used beyond seeing an indexed list to cross reference while processing
def output_to_file():
    with open('creatures', "w", encoding="utf-8") as f:
        i = 0
        for creature in creatures_dict:
            i += 1
            creature_string = '{}: {}\n'.format(i, creatures_dict[creature], )
            print(creature_string)
            f.write(creature_string)

# Create folders for items in the list
def create_folders(src_list, target_dir):
    target_directory = os.path.join(parent_directory, target_dir)

    print(target_directory)

    if not os.path.exists(target_directory):
        os.mkdir(target_directory)

    for item in src_list:
        new_directory = os.path.join(target_directory, item)
        if not os.path.exists(new_directory):
            print('Creating directory for {}'.format(item))
            os.mkdir(new_directory)
        else:
            print('Directory for {} already exists'.format(item))
    
    return target_directory

def remove_spaces_from_files(target_dir):
    images_with_spaces_found = False
    for root, dirs, files in os.walk(target_dir):
        for name in files:
            if name.find(" ") != -1:
                images_with_spaces_found = True
                print(name)
                new_name = name.replace(" ", "_")
                os.rename(os.path.join(root, name), os.path.join(root, new_name))
    if not images_with_spaces_found:
        print("No files found with spaces")

def get_image_size(filep):
    img = Image.open(filep)
    w = img.width
    h = img.height
    return {"width":w,"height":h}

def debug_pixel(si, x, y):
    print('({},{}) - {} - {}'.format(x, y, si.get_pixel_color(x, y), si.pixel_is_transparent(x, y)))

def debug_x6p(si, x6p):
    print(x6p.cursor())
    print(are_all_pixels_transparent(si, x6p))

def is_valid_position(cursor, img_width, img_height):
    x6p_tl, x6p_br = cursor
    if x6p_tl[0] < 0 or x6p_tl[0] >= img_width:
        return False
    
    if x6p_tl[1] < 0 or x6p_tl[1] >= img_height:
        return False

    return True

def are_all_pixels_transparent(si, x6p):
    for px in x6p.get_cursor_pixel_list():
        if not si.pixel_is_transparent(px[0],px[1]):
            return False
    return True

def get_cursor_list(width, height):
    x6p = x6px()
    x6p_count_x = width/6
    x6p_count_y = height/6

    r = []

    y = 0
    x = 0
    while(y < x6p_count_y):
        r.append(x6p.cursor())
        x = 1
        while(x < x6p_count_x):
            x6p.move_right()
            r.append(x6p.cursor())
            x += 1
        x6p.move_down()
        x6p.align_left()
        y += 1

    return r

def cursor_transparency_quick_scan(cursor, si):
    tl, br = cursor
    tlx, tly = tl
    brx, bry = br

    return si.pixel_is_transparent(tlx, tly) and si.pixel_is_transparent(brx, bry)

def get_border_scores(si, x6p_list):
    def calculate_neighbor_transparencies(cursor, si):
        tl, br = cursor
        tlx, tly = tl
        brx, bry = br
        
        ref_x6px = x6px()
        ref_x6px.set_location(tlx, tly)

        nesw = [
            ref_x6px.get_move_up(),
            ref_x6px.get_move_right(),
            ref_x6px.get_move_down(),
            ref_x6px.get_move_left()
        ]

        valid_nesw = {}

        for neighbor in nesw:
            if is_valid_position(neighbor, si.width, si.height):
                if cursor_transparency_quick_scan(neighbor, si):
                    valid_nesw[neighbor[0]] = 0
                else:
                    valid_nesw[neighbor[0]] = 1
        
        return valid_nesw
    
    border_scores = {}

    for cursor in x6p_list:
        tl, br = cursor
        tlx, tly = tl
        brx, bry = br

        current_x6px_transparency_score = 0
        current_x6p_is_transparent = True

        # Get Current x6pixel transparency score
        if not cursor_transparency_quick_scan(cursor, si):
            current_x6px_transparency_score += 1
            current_x6p_is_transparent = False

        # Check if NWSE are transparent
        neighbor_values_to_add = calculate_neighbor_transparencies(cursor, si)

        # Add 0 if not transparent, 1 if it is
        for neighbor in neighbor_values_to_add:
            current_x6px_transparency_score += neighbor_values_to_add[neighbor]
        
        border_scores[tl] = {
            "transparency_score": current_x6px_transparency_score,
            "is_transparent": current_x6p_is_transparent
        }
    
    return border_scores

def get_border_list(si):
    x6p_cursor_list = get_cursor_list(si.width, si.height)
    all_x6px_border_scores = get_border_scores(si, x6p_cursor_list)

    def transparent_and_gt0(target_px):
        if all_x6px_border_scores[target_px]['is_transparent'] and all_x6px_border_scores[target_px]['transparency_score']:
            return True
        return False

    return filter(transparent_and_gt0, all_x6px_border_scores)

def scale_and_trim_image(filep):
    new_image_path = filep.replace(".png", "_x6_borderless.png")

    if filep.find("borderless") >= 0:
        new_image_path = filep

    if os.path.exists(new_image_path):
        print('Borderless Already Exists: {}'.format(new_image_path))
        return new_image_path

    x1 = get_image_size(filep)["width"]
    x6 = x1*6

    print('Trimming {}'.format(filep))
    os.system('magick {} -scale {} -trim -alpha set -bordercolor none -border 6x12 {}'.format(filep, x6, new_image_path))
    return new_image_path

def add_border_to_image(img_path):
    new_image_path = scale_and_trim_image(img_path)
    bordered_image_path = new_image_path.replace("_x6_borderless.png", "_x6_bordered.png")
    
    if os.path.exists(bordered_image_path):
        print('Bordered Already Exists: {}'.format(bordered_image_path))
        return bordered_image_path
    
    si = SpriteImage(new_image_path)
    border_list = get_border_list(si)

    print('Adding border to {}'.format(new_image_path))
    for x6p in border_list:
        x, y = x6p
        yi = 0

        while yi < 6:
            xi = 0
            while xi < 6:
                si.img[x+xi,y+yi] = (0,0,0,255)
                xi += 1
            yi += 1

    si.save(bordered_image_path)
    return bordered_image_path

def move_file(target_file, target_dir, subfolder = None):
    destination_file = ""
    split_target = target_file.split("\\")
    f = split_target[len(split_target)-1]
    if subfolder:
        destination_folder = os.path.join(target_dir,subfolder)
        destination_file = os.path.join(target_dir,subfolder,f)
        if not os.path.exists(destination_folder):
            print(target_file)
            os.makedirs(destination_folder)
    else:
        destination_file = os.path.join(target_dir, f)

    print('Moving {} to {}'.format(f, destination_file))
    os.rename(target_file, destination_file)

def add_border_to_all_images(src_directory, target_dir):
    bordered_images = []

    for root, dirs, files in os.walk(src_directory):
        for name in files:
            if "Texture2D" not in root:
                print("Working with file: {}".format(os.path.join(root, name)))
                split_root = root.split("\\")
                creature = split_root[len(split_root)-2]

                # Check if file itself is already bordered
                if name.find("_x6_bordered") >= 0:
                    print("Image is already bordered")
                    print("Adding already bordered image to list: {}".format(os.path.join(root, name)))
                    bordered_images.append((os.path.join(root,name), creature))
                # Check if file is borderless
                elif name.find("_x6_borderless") >= 0:
                    bordered_image_path = add_border_to_image(os.path.join(root, name))
                    print("Adding newly bordered image to list: {}".format(bordered_image_path))
                    bordered_images.append((bordered_image_path, creature))
                else:
                    bordered_images.append((add_border_to_image(os.path.join(root, name)), creature))
    
    for bi in bordered_images:
        print("Bordered Image List: {}".format(bi))

    return bordered_images

def full_process():
    # # Loads creatures from Assets file
    # creatures = load_creatures()
    # # Creates folders to extract files into
    # creatures_dir = create_folders(creatures, "creatures")
    # # TODO: Automate extracting files from Assets.xml, currently you must export manually
    # remove_spaces_from_files(os.path.join(parent_directory, "creatures"))

    creatures_dir = os.path.join(parent_directory, "testing")

    target_dir = os.path.join(parent_directory, "x6")
    bordered_images = add_border_to_all_images(creatures_dir, target_dir)

    for bi in bordered_images:
        print("Before Move File: {}".format(bi))
        move_file(bi[0], target_dir, bi[1])

# target_dir = os.path.join(parent_directory, "x6")
# add_border_to_all_images(os.path.join(parent_directory, "test_folder"), target_dir)
# full_process()

# Before I added checks for if borderless and bordered images were already created
# I was getting a lot of runs where result images were being reprocessed.
# This just removes all of them in one go.
def remove_reruns(src_path):
    for root, dirs, files in os.walk(src_path):
        for name in files:
            if not name.find("_borderless_x6_bordered") == -1 or not name.find("_borderless_x6_borderless") == -1 or not name.find("_bordered_x6_bordered") == -1 or not name.find("_bordered_x6_borderless") == -1:
                os.remove(os.path.join(root, name))

# remove_reruns()
full_process()
# print(load_creatures())