from PIL import Image, ImageDraw, ImageFont
from sprite_image import SpriteImage
from magnified_px import MagnifiedPx as x6px
import os

def get_image_size(filep):
    img = Image.open(filep)
    w = img.width
    h = img.height
    return {"width":w,"height":h}

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
    new_image_path = ""
    
    if img_path.find("_x6_borderless.png") >= 0:
        new_image_path = img_path
    else:
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

def add_border_to_all_images(src_directory, target_dir):
    target_images = []

    def is_bordered_image(fyle):
        return fyle.find("_x6_bordered.png") >= 0

    def is_borderless_image(fyle):
        return fyle.find("_x6_borderless.png") >= 0

    for root, dirs, files in os.walk(src_directory):
        if 'Texture2D' in dirs:
            dirs.remove('Texture2D')
        
        for fyle in files:
            target_images.append(os.path.join(root, fyle))

    bordered_files = list(filter(is_bordered_image, target_images))

    for bf in bordered_files:
        borderless = bf.replace("_x6_bordered.png", "_x6_borderless.png")
        original = bf.replace("_x6_bordered.png", ".png")

        target_images.remove(borderless)
        target_images.remove(original)
        target_images.remove(bf)

    borderless_files = list(filter(is_borderless_image, target_images))

    for blf in borderless_files:
        original = blf.replace("_x6_borderless.png", ".png")
        target_images.remove(original)
    
    i = 0

    for ti in target_images:
        bordered_image_path = add_border_to_image(ti)
        bordered_files.append(bordered_image_path)

    return bordered_files