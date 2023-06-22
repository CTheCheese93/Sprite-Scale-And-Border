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

def move_file(target_file, target_dir):
    destination_file = ""
    split_target = target_file.split("\\")
    subfolder = split_target[len(split_target)-3]
    f = split_target[len(split_target)-1]

    destination_folder = os.path.join(target_dir,subfolder)
    destination_file = os.path.join(target_dir,subfolder,f)
   
    if not os.path.exists(destination_folder):
        print(target_file)
        os.makedirs(destination_folder)

    print('Moving {} to {}'.format(f, destination_file))
    os.rename(target_file, destination_file)