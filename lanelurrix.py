#!/usr/bin/env python3
"""Lanelurrix: offline moving-lane crossing game."""
import curses,random,time,argparse
from terminal_ui import setup,text,title
class Game:
    width=20;height=12
    def __init__(self,seed=None):
        rng=random.Random(seed);self.x=10;self.y=11;self.ticks=0;self.dead=False;self.won=False
        self.lanes={y:(rng.randrange(7),1 if y%2 else -1,2 if y%3 else 3) for y in range(1,11) if y not in (4,8)}
    def occupied(self,x,y):
        if y not in self.lanes:return False
        start,direction,length=self.lanes[y];return (x-start-direction*self.ticks)%7<length
    def check(self):
        self.dead=self.occupied(self.x,self.y)
        self.won=self.y==0 and not self.dead
    def move(self,dx,dy):
        if self.dead or self.won:return
        self.x=max(0,min(19,self.x+dx));self.y=max(0,min(11,self.y+dy));self.check()
    def tick(self):
        if self.dead or self.won:return
        self.ticks+=1;self.check()
def run(stdscr,seed):
    setup(stdscr);stdscr.timeout(60);g=Game(seed);last=time.monotonic();paused=False
    while True:
        status='Reached home! R restarts.' if g.won else 'Collision. R restarts.' if g.dead else 'Paused' if paused else f'Rows crossed: {11-g.y}/11  Tick: {g.ticks}'
        title(stdscr,'Lanelurrix',status,'Arrows/WASD move | P pause | R restart | Q quit')
        h,w=stdscr.getmaxyx()
        if h<19 or w<46:text(stdscr,4,2,'Resize to at least 46x19. Game paused.',3);last=time.monotonic()
        else:
            for y in range(12):
                text(stdscr,4+y,2,''.join(' @' if (x,y)==(g.x,g.y) else '##' if g.occupied(x,y) else '..' if y in g.lanes else '  ' for x in range(20)),3 if y in g.lanes else 4)
            text(stdscr,3,2,'HOME: reach the top row',4);text(stdscr,16,2,'Traffic shifts every 0.35 seconds.',2)
            if not paused and time.monotonic()-last>=.35:g.tick();last=time.monotonic()
        stdscr.refresh();k=stdscr.getch()
        if k in (ord('q'),ord('Q')):return
        if k==ord('r'):g=Game(seed);last=time.monotonic();paused=False
        elif k==ord('p'):paused=not paused;last=time.monotonic()
        elif not paused and h>=19 and w>=46:
            d={curses.KEY_UP:(0,-1),ord('w'):(0,-1),curses.KEY_DOWN:(0,1),ord('s'):(0,1),curses.KEY_LEFT:(-1,0),ord('a'):(-1,0),curses.KEY_RIGHT:(1,0),ord('d'):(1,0)}.get(k)
            if d:g.move(*d)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--seed',type=int);p.add_argument('--demo',action='store_true');a=p.parse_args()
    if a.demo:
        g=Game(a.seed);print('LANELURRIX\n'+ '\n'.join(''.join('@' if (x,y)==(g.x,g.y) else '#' if g.occupied(x,y) else '.' for x in range(20)) for y in range(12)));return
    try:curses.wrapper(run,a.seed)
    except curses.error:print('Needs an interactive terminal with curses (46x19 minimum).')
    except KeyboardInterrupt:pass
if __name__=='__main__':main()
