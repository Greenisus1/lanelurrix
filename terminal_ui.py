import curses

def setup(stdscr):
    try:curses.curs_set(0)
    except curses.error:pass
    if curses.has_colors():
        curses.start_color();curses.use_default_colors()
        for i,c in enumerate((curses.COLOR_CYAN,curses.COLOR_YELLOW,curses.COLOR_RED,curses.COLOR_GREEN,curses.COLOR_MAGENTA,curses.COLOR_BLUE),1):curses.init_pair(i,c,-1)
def text(stdscr,y,x,value,color=0,bold=False):
    h,w=stdscr.getmaxyx()
    if 0<=y<h and 0<=x<w-1:
        try:stdscr.addnstr(y,x,str(value),w-x-1,curses.color_pair(color)|(curses.A_BOLD if bold else 0))
        except curses.error:pass
def title(stdscr,name,status,help):
    stdscr.erase();h,w=stdscr.getmaxyx();text(stdscr,1,2,name.upper(),1,True);text(stdscr,2,2,status,2);text(stdscr,h-2,2,help,1)
