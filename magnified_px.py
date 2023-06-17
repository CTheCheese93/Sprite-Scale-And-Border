class MagnifiedPx:
    top_left_x6px = (0,0)
    bottom_right_x6px = (5,5)

    def _move_x(self, amount: 1):
        tl = self.top_left_x6px
        br = self.bottom_right_x6px
        self.top_left_x6px = (tl[0]+(6*amount), tl[1])
        self.bottom_right_x6px = (br[0]+(6*amount), br[1])

    def _move_y(self, amount: 1):
        tl = self.top_left_x6px
        br = self.bottom_right_x6px
        self.top_left_x6px = (tl[0], tl[1]+(6*amount))
        self.bottom_right_x6px = (br[0], br[1]+(6*amount))

    def _get_move_x(self, amount: 1):
        tl = self.top_left_x6px
        br = self.bottom_right_x6px
        return ((tl[0]+(6*amount), tl[1]), (br[0]+(6*amount), br[1]))

    def _get_move_y(self, amount: 1):
        tl = self.top_left_x6px
        br = self.bottom_right_x6px
        return ((tl[0], tl[1]+(6*amount)), (br[0], br[1]+(6*amount)))
    
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