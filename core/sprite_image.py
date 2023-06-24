from PIL import Image

class SpriteImage:
    def __init__(self, img_path):
        self._im = Image.open(img_path)
        self.rgb_img = self._im.convert('RGBA')
        self.img = self.rgb_img.load()
        self.width, self.height = self._im.size
    
    def pixel_is_transparent(self, x, y):
        return self.img[x,y] == (0,0,0,0)

    def get_pixel_color(self, x, y):
        return self.img[x,y]

    def set_pixel_color(self, x, y, rgba):
        self.img[x,y] = rgba

    def save(self, file_path):
        self.rgb_img.save(file_path)