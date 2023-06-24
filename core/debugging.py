# Not actually used beyond seeing an indexed list to cross reference while processing
def output_to_file():
    with open('creatures', "w", encoding="utf-8") as f:
        i = 0
        for creature in creatures_dict:
            i += 1
            creature_string = '{}: {}\n'.format(i, creatures_dict[creature], )
            print(creature_string)
            f.write(creature_string)

# Before I added checks for if borderless and bordered images were already created
# I was getting a lot of runs where result images were being reprocessed.
# This just removes all of them in one go.
def remove_reruns(src_path):
    for root, dirs, files in os.walk(src_path):
        for name in files:
            if not name.find("_borderless_x6_bordered") == -1 or not name.find("_borderless_x6_borderless") == -1 or not name.find("_bordered_x6_bordered") == -1 or not name.find("_bordered_x6_borderless") == -1:
                os.remove(os.path.join(root, name))

def debug_pixel(si, x, y):
    print('({},{}) - {} - {}'.format(x, y, si.get_pixel_color(x, y), si.pixel_is_transparent(x, y)))

def debug_x6p(si, x6p):
    print(x6p.cursor())
    print(are_all_pixels_transparent(si, x6p))