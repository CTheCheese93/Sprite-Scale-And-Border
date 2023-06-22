from xml.dom.minidom import parse
from PIL import Image, ImageDraw, ImageFont
import os

from magnified_px import MagnifiedPx as x6px
from sprite_image import SpriteImage
import mpx_img_interface
import debugging

parent_directory = os.getcwd()

def full_process():
    # Loads creatures from Assets file
    creatures = load_creatures()
    # Creates folders to extract files into
    creatures_dir = create_folders(creatures, "creatures")
    # # TODO: Automate extracting files from Assets.xml, currently you must export manually
    # remove_spaces_from_files(os.path.join(parent_directory, "creatures"))

    # creatures_dir = os.path.join(parent_directory, "testing")

    # target_dir = os.path.join(parent_directory, "x6")
    # bordered_images = add_border_to_all_images(creatures_dir, target_dir)

    # for bi in bordered_images:
    #     move_file(bi, target_dir)

full_process()