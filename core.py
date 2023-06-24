from PIL import Image, ImageDraw, ImageFont
import os
import sys

parent_directory = os.getcwd()

sys.path.insert(0, os.path.join(parent_directory, "core"))

from file_handling import load_creatures, create_folders, remove_spaces_from_files, move_file
from mpx_img_interface import add_border_to_all_images


def full_process():
    # # Loads creatures from Assets file
    # creatures = load_creatures()
    # # Creates folders to extract files into
    # creatures_dir = create_folders(creatures, "creatures")
    # # TODO: Automate extracting files from Assets.xml, currently you must export manually
    # remove_spaces_from_files(os.path.join(parent_directory, "creatures"))

    creatures_dir = os.path.join(parent_directory, "testing", "core", "input")

    target_dir = os.path.join(parent_directory, "testing", "core", "output")
    bordered_images = add_border_to_all_images(creatures_dir, target_dir)

    for bi in bordered_images:
        move_file(bi, target_dir)

settings = {
    "asset_file": "",
    "asset_name_idx": 0,
    "asset_output_dir": "",
    "extraction_name_idx": 0,
    "magnification": 1,
    "bordered_output_dir": "",
    "borderless_output_dir": "",
    "bordered_file_extention": "bordered",
    "borderless_file_extension": "borderless",
    "include_magnification_in_extension": True
}

# full_process()