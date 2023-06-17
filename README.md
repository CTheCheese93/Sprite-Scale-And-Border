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



### Process Asset.xml to get list of creatures



### Create folders based off list of creatures



### **Manually** extract Sprites into their designated folders created in Step 3



### Remove all spaces from files, replacing them with an `_`



### x6 Upscale, Crop, Center, and create Padding for Sprite, saved as `*_x6_borderless.png`



### Add 6x6 black border around sprite, saved as `*_x6_bordered.png`



### Move all `*_x6_bordered.png` images to a `x6` folder, separated into their indvidual creature folders



### Browse through the results with pride and eventually upload them


