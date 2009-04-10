import gtk
from checkers import Checkers

class BoardView(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        
        self.tile_size = 100
        self.tile_count = 8
        self.w = self.h = self.tile_count * self.tile_size
        
        cmap = self.get_colormap()
        self.color_black = cmap.alloc_color('#000000')
        self.color_white = cmap.alloc_color('#FFFFFF')    
        self.color_red   = cmap.alloc_color('#BB3333')
        self.color_green = cmap.alloc_color('#33DD33')
        self.set_size_request(320, 320)

        self.connect("expose_event", self.exposeEvent)
        self.connect("size-allocate", self.__sizeAllocate)
        self.connect("button_press_event", self.buttonPressEvent)
        self.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.BUTTON_PRESS_MASK)

        #TODO: use settings
        self.tile_w = gtk.gdk.pixbuf_new_from_file("images/tile_w.jpg")
        self.tile_b = gtk.gdk.pixbuf_new_from_file("images/tile_b.jpg")
        self.selector = gtk.gdk.pixbuf_new_from_file("images/selector.png")

        self.checkers = Checkers()
        self.checkers.setSelected((2,5))
    
    def __sizeAllocate(self, widget, rect):
        if rect.width < rect.height:
            self.tile_size = rect.width / self.tile_count
        else:
            self.tile_size = rect.height / self.tile_count
        self.w = self.h = self.tile_count * self.tile_size

    def exposeEvent(self, widget, event):
        window = self.window
        gc = window.new_gc()

        rect = gtk.gdk.Rectangle(0, 0, self.w, self.h)

        window.begin_paint_rect(rect)
        self.__drawBoard(window, gc, rect)
        window.end_paint()

    def __drawBackground(self, window, gc, rect):
        bg_w = self.tile_w.get_width()
        bg_h = self.tile_w.get_height() 
        mod = True
        for i in range(self.tile_count):
            for ii in range(self.tile_count):
                if mod:
                    window.draw_pixbuf(gc, self.tile_w, (bg_w - self.tile_size) / 2, 
                                       (bg_h - self.tile_size) / 2,
                                       i * self.tile_size, ii * self.tile_size,
                                       self.tile_size, self.tile_size)
                else:
                    window.draw_pixbuf(gc, self.tile_b, (bg_w - self.tile_size) / 2, 
                                       (bg_h - self.tile_size) / 2,
                                       i * self.tile_size, ii * self.tile_size,
                                       self.tile_size, self.tile_size)
                mod = not mod
            mod = not mod
                    
        
    def __drawPiece(self, window, gc, rect, type, x, y):
        gc
        s = self.tile_size
        if abs(type) == Checkers.WH:
            gc.set_foreground(self.color_white)
            window.draw_arc(gc, True, s*x+s/10, s*y+s/10, s - s/5, s - s/5, 0, 65*360)
            if type < 0:
                gc.set_foreground(self.color_black)
                window.draw_arc(gc, True, s*x+3*s/20, s*y+3*s/20, s/2, s/2, 0, 65*360)
        elif abs(type) == Checkers.BL:
            gc.set_foreground(self.color_black)
            window.draw_arc(gc, True, s*x+s/10, s*y+s/10, s - s/5, s - s/5,
                            0, 65*360)
            if type < 0:
                gc.set_foreground(self.color_white)
                window.draw_arc(gc, True, s*x+3*s/20, s*y+3*s/20, s/10, s/2, 0, 65*360)

    def __drawPieces(self, window, gc, rect):
        for i in range(8):
            for ii in range(8):
                if (i+ii)%2:
                    self.__drawPiece(window, gc, rect, self.checkers.checkTile(ii,i), ii, i)
        
    def __drawSelector(self, window, gc):
        a = self.checkers.getSelected()[0]
        if a:
            gc.set_line_attributes(self.tile_size / 20,
                                   gtk.gdk.LINE_SOLID,
                                   gtk.gdk.CAP_NOT_LAST,
                                   gtk.gdk.JOIN_MITER)
            gc.set_foreground(self.color_red)
            window.draw_rectangle(gc, False, a[0] * self.tile_size, a[1] * self.tile_size,
                                  self.tile_size, self.tile_size)
           
    def __drawMoves(self, window, gc):
        a = self.checkers.getSelected()[1:]
        for i in a:
            gc.set_line_attributes(self.tile_size / 20,
                                   gtk.gdk.LINE_SOLID,
                                   gtk.gdk.CAP_NOT_LAST,
                                   gtk.gdk.JOIN_MITER)
            gc.set_foreground(self.color_green)
            window.draw_rectangle(gc, False, i[0] * self.tile_size, i[1] * self.tile_size,
                                  self.tile_size, self.tile_size)
        
    def __drawBoard(self, window, gc, rect):
        self.__drawBackground(window, gc, rect)
        self.__drawPieces(window, gc, rect)
        self.__drawSelector(window, gc)
        self.__drawMoves(window, gc)

    def __getCoords(self, x, y):
        x = int(x / self.tile_size)
        y = int(y / self.tile_size)
        if x > 7 or y > 7:
            return None
        else:
            return (x, y)

    def buttonPressEvent(self, widget, event):
        if event.button != 1:
            return
        target = self.__getCoords(event.x, event.y)
        if not target:
            return
        m = self.checkers.getSelected()
        if target in m[1:]:
            self.checkers.move(m, target)
        else:
            self.checkers.setSelected(target)
        self.exposeEvent(None, None)
