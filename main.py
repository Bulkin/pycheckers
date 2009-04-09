#/usr/bin/env python

import gtk
from board import BoardView

def main():
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_name("Chess board")

    vbox = gtk.VBox(False, 0)
    window.add(vbox)
    vbox.show()
    
    window.connect("destroy", lambda w: gtk.main_quit())

    board = BoardView()
    vbox.pack_start(board, True, True, 0)

    board.show()
    window.show()
    gtk.main()
    return 0

if __name__ == "__main__":
    main()

        
