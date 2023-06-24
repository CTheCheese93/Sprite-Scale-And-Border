import os
import sys

parent_directory = os.getcwd()

sys.path.insert(0, os.path.join(parent_directory, "core"))

from file_handling import get_assets, get_container, get_sprite_name

def get_container_idx(assets):
    sample_container = get_container(assets[0])
    container_idx_options = sample_container.split("/")

    print("Choose which value best represents the name of your object:")

    cidx = 0
    for cidxo in container_idx_options:
        print('{}: {}'.format(cidx, cidxo))
        cidx += 1

    cidx = int(input('Choose an option: '))

    return cidx

def get_option_choice(options):
    i = 1
    for o in options:
        print('{}: {}'.format(i,o))
        i += 1
    
    print("--------------------")
    print("[b]ack | [r]un\n")
    return input('Choose an Option: ').lower()[0]

def default_option_chosen(chosen_option):
    match chosen_option:
        case "r":
            print("Run Chosen")
        case "b":
            print("Back Chosen")
        case _:
            print("No Option Chosen")

def main_menu():
    options = [
        "Extraction Settings",
        "Editing Settings",
        "Preview Results"
    ]
    
    chosen_option = get_option_choice(options)

    match chosen_option:
        case "1":
            print("Extraction Settings Chosen")
        case "2":
            print("Editing Settings Chosen")
        case "3":
            print("Preview Results Chosen")
        case _:
            default_option_chosen(chosen_option)

def main_loop():
    settings = {
        "asset_file": os.path.join(parent_directory, "assets.xml"),
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
    # Get Asset File Path

    # Find Asset Name Index
    assets = get_assets(settings["asset_file"])
    cidx = get_container_idx(assets)

    for a in assets:
        container = get_container(a)
        sprite_name = get_sprite_name(a)
        creature = container.split("/")
        print('{}: {}'.format(creature[cidx],sprite_name))

    # Set Asset Output Dir

main_menu()