# Sprite Mag and Border

## What brought me here
I tried out [Farworld Pioneers Wiki on Wiki.gg](https://farworldpioneers.wiki.gg/wiki/Farworld_Pioneers_Wiki) and noticed that the wiki was missing a lot of creatures and none of them had their sprites uploaded. So I used AssetStudio to grab the sprites and found the [Image Formatting Guidelines](https://farworldpioneers.wiki.gg/wiki/Meta:_Image_Formatting).

Pretty simple: x6 upscaling, 6px top and bottom transparent padding, and a 6px border around the actual sprite with the sprite centered.

## What I wanted to achieve
Instead of just grabbing one sprite for each creature in the game and manually editing them, I grabbed all of them with intent to automate the Sprite Editing process and keep things nice and tidy.

The full process looks something like this:
1. Export Asset.xml file from AssetStudio
2. Process Asset.xml to get list of creatures
3. Create folders based off list of creatures
4. **Manually** extract Sprites into their designated folders created in Step 3
5. Remove all spaces from files, replacing them with an `_`
6. x6 Upscale, Crop, Center, and create Padding for Sprite, saved as `*_x6_borderless.png`
7. Add 6x6 black border around sprite, saved as `*_x6_bordered.png`
8. Move all `*_x6_bordered.png` images to a `x6` folder, separated into their indvidual creature folders
9. Browse through the results with pride and eventually upload them

All steps have already been completed and my task is already done.

I want to tackle the extraction process of the sprites at some point, but that's bonus content relative to the task at hand.

## What I want to achieve now

 Now I'm pushing the resulting code to GitHub so I can start refactoring it to be more useful outside of this one particular solution as well as show how I solved the problem now and how the problem will be solved when I'm done.

 The steps above will all remain the same, but how we achieve them will change significantly.
 
 There's a lot that can be done, and some that I already did before uploading, here's a likely not complete list:

 * Separate code into a multi-file solution (I already started doing this by the initial commit)
 * Separate certain steps, `add_border_to_all_images()` has major side effects that need to be separated for example
 * Make things more dynamic, the export to an `x6` directory is hardcoded and so is the scaling itself, we can fix that
 * Refactor the interfacing between the actual image and the magnified pixel object

 ## The Full Process (In Depth)

### Export Asset.xml file from AssetStudio

[AssetStudio](https://github.com/Perfare/AssetStudio) is no longer being worked on, but it does still work.

I load in the entire contents of the Pioneers Folder, though you really only need the Resources.Assets file.

<img src=".readme_assets/LoadingFolder.png" alt="Loading Folder" width=75% />

If you go to the Asset List tab and add `sprites/creatures` to the filter, you'll find all the creatures listed.

<img src=".readme_assets/AssetList.png" alt="Asset List" width=75% />

You could sort by Type and not select the Texture2D items, but I chose everything. Now we just extract, simple enough.

<img src=".readme_assets/ExportAssetList.png" alt="Exporting Asset List" width=75% />

### Process Asset.xml to get list of creatures

I looked up how to deal with XML files, assuming it was going to be easy.

Then I found a few articles that talked about how complicated it was going to be.

Turns out, it really depends. For what I'm doing, we can go the DOM route.

```
from xml.dom.minidom import parse

# Getting List of Assets from AssetStudio XML Export
def get_assets():
    document = parse("assets.xml")
    assets = document.getElementsByTagName("Asset")
    return assets
```
Then we take the returned elements from `get_assets()` and consolidate each file by creature.

```
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
```

### Create folders based off list of creatures

Folder creation is simple, using the `os` Python package and iterating through the list created earlier to create the directory structure.

```
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
```

Things like `os.path.join(parent_directory, target_dir)` need to be rewritten to have the path joining be done on the function call and not in the function itself to allow for more explicit control of input and output pathing.

### **Manually** extract Sprites into their designated folders created in Step 3

Here we go back to AssetStudio, now doing the actual extraction for each creature into the newly created folders.

There are roughly 66 creatures, and it took about 30 minutes the last time I did it.

Again, I would like to automate this, but it seems like there are a few handful of hours of work into trying to get the information out of the file by reading and working with the bytes of the file in the same way AssetStudio has.

For the purpose of getting the actual problem solved, I just ate the 30 minutes of manual work.

### Remove all spaces from files, replacing them with an `_`

Again, very simple using standard features found in the `os` package

```
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
```

### x6 Upscale, Crop, Center, and create Padding for Sprite, saved as `*_x6_borderless.png`

<img src=".readme_assets/TrimAndScale.png" alt="Trimmed and Scaled Side-by-Side" />

This was actually the easiest part of it all, we just outsourced all the work to [ImageMagick](https://imagemagick.org/index.php) and we're making an `os.system` call to execute the command.

The command of concern is `magick ORIGNAL_FILE -scale NEW_IMAGE_WIDTH -trim -alpha set -bordercolor none -border 6x12 NEW_IMAGE`.

`-scale` doesn't work how I thought it would where a `2` would mean twice as large. Instead it seems like whatever number I put in, that's going to be the width of the image. Our requirements say we need the image to be x6 as large, so we do `6*IMG_WIDTH` to get `NEW_IMAGE_WIDTH`.

`-trim` shrinks down the image to the size of the content, which is super useful because some sprites have a ton of space.

`-alpha set -bordercolor none -border 6x12` makes transparency a thing and sets the border color to be transparent while also creating a 6x12 border. We choose 6x12 because our requirements want a 6x6 border around the content with 6px of padding on the top and bottom of the image, so we add 6px to the left and right of the image and 12px to the top and bottom, making the **creature's border** sit snug on the left and right edges of the image.

```
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
```

### Add 6x6 black border around sprite, saved as `*_x6_bordered.png`

<img src=".readme_assets/BorderedSprite.png" alt="A Borderless Sprite Side-By-Side with a Bordered Sprite" />

For most of this, we've gone from point A to point B, but to explain this part of the journey, we're going to go through some twists and turns to show you something closest to my actual journey and not just the final path.

#### **The Magnified Pixel**

When we scaled the image we basically take each pixel and insert duplicates across the x and y axis multiple times. In our case we did x6 scaling, so 1px = 6px and 1px of movement on the original image is 6px of movement on the scaled image.

To help manage this, we have The Magified Pixel.

```
class MagnifiedPx:
    top_left_x6px = (0,0)
    bottom_right_x6px = (5,5)

    # Some Implementation Details Removed

    def move_right(self, amount = 1):
        self._move_x(amount)

    def move_left(self, amount = 1):
        self._move_x(-amount)

    def move_up(self, amount = 1):
        self._move_y(-amount)

    def move_down(self, amount = 1):
        self._move_y(amount)

    def get_move_right(self, amount = 1):
        return self._get_move_x(amount)

    def get_move_left(self, amount = 1):
        return self._get_move_x(-amount)

    def get_move_up(self, amount = 1):
        return self._get_move_y(-amount)

    def get_move_down(self, amount = 1):
        return self._get_move_y(amount)

    def set_location(self, x, y):
        self.top_left_x6px = (x,y)
        self.bottom_right_x6px = (self.top_left_x6px[0]+5,self.top_left_x6px[1]+5)

    def align_left(self):
        tl = self.top_left_x6px
        br = self.bottom_right_x6px
        self.top_left_x6px = (0, tl[1])
        self.bottom_right_x6px = (5, br[1])
    
    def get_cursor_pixel_list(self):
        l = []
        tl = self.top_left_x6px

        y = 0
        while (y < 6):
            x = 0
            while (x < 6):
                l.append((tl[0]+x,tl[1]+y))
                x += 1
            y += 1
        return l

    def cursor(self):
        return (self.top_left_x6px, self.bottom_right_x6px)
```

The MagPx holds onto the coordinates for the top-left and bottom-right pixels on the scaled image that act as the bounds for what a single pixel is on the original image. Meaning, the color value of pixel `(0,0)` on the original image should match with every pixel between `(0,0)` and `(5,5)` on the scaled image.

A lot of what was done with this class was with intent to go programmatically go through the scaled image, moving the MagPx around. This didn't actually happen. Instead, I used this class to manual validate pixel values.

#### **Using Math to Create a Border**

After manually validating pixels, I worked on the programmatic movement of the MagPx and pixel processing to realize early on that none of that was required. 

### Move all `*_x6_bordered.png` images to a `x6` folder, separated into their indvidual creature folders



### Browse through the results with pride and eventually upload them


