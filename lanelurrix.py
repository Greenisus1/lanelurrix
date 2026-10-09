#!/usr/bin/env python3
"""Lanelurrix: original offline fullscreen lane crossing with levels and endless mode."""
import curses,random,time,argparse,os
from terminal_ui import setup,text
VERSION='1.1.0'
class Game:
    width=20;height=12
    def __init__(self,seed=None,level=1):
        self.seed=seed;self.level=level;rng=random.Random(seed);self.x=10;self.y=11;self.ticks=0;self.dead=False;self.won=False
        self.period=max(5,7-(level-1)//4)
        self.lanes={y:(rng.randrange(self.period),1 if y%2 else -1,min(self.period-2,2 if y%3 else 3)) for y in range(1,11) if y not in (4,8)}
    @property
    def interval(self):return max(.12,.35-(self.level-1)*.022)
    @property
    def progress(self):return 11-self.y
    def occupied(self,x,y):
        if y not in self.lanes:return False
        start,direction,length=self.lanes[y];return (x-start-direction*self.ticks)%self.period<length
    def check(self):self.dead=self.occupied(self.x,self.y);self.won=self.y==0 and not self.dead
    def move(self,dx,dy):
        if self.dead or self.won:return
        self.x=max(0,min(19,self.x+dx));self.y=max(0,min(11,self.y+dy));self.check()
    def tick(self):
        if self.dead or self.won:return
        self.ticks+=1;self.check()
class Endless:
    width=20;height=12
    def __init__(self,seed=None):
        self.seed=seed if seed is not None else random.randrange(2**32);self.x=10;self.row=0;self.best=0;self.ticks=0;self.dead=False;self.won=False;self.lanes={}
    @property
    def level(self):return 1+self.best//25
    @property
    def interval(self):return max(.12,.35-(self.level-1)*.018)
    @property
    def progress(self):return self.best
    @property
    def bottom(self):return max(0,self.best-3)
    def lane(self,row):
        if row%4==0:return None
        if row not in self.lanes:
            rng=random.Random(self.seed+row*1000003);self.lanes[row]=(rng.randrange(7),rng.choice((-1,1)),rng.choice((2,3)))
        return self.lanes[row]
    def occupied(self,x,row):
        lane=self.lane(row)
        return bool(lane and (x-lane[0]-lane[1]*self.ticks)%7<lane[2])
    def move(self,dx,dy):
        if self.dead:return
        self.x=max(0,min(19,self.x+dx));self.row=max(self.bottom,self.row-dy);self.best=max(self.best,self.row)
        self.dead=self.occupied(self.x,self.row)
        self.lanes={y:v for y,v in self.lanes.items() if self.bottom<=y<=self.bottom+24}
    def tick(self):
        if self.dead:return
        self.ticks+=1;self.dead=self.occupied(self.x,self.row)
def draw(s,g,mode,paused):
    s.erase();h,w=s.getmaxyx();text(s,0,1,'LANELURRIX '+VERSION+'   '+('INFINITY' if mode=='endless' else f'LEVEL {g.level}/10'),1,True)
    status='COLLISION - R retry | M menu' if g.dead else ('ALL10 LEVELS COMPLETE! M menu' if g.level==10 else 'HOME REACHED! Enter next level') if g.won else 'PAUSED' if paused else f'Rows: {g.progress}  Traffic tick: {g.ticks}'
    text(s,1,1,status,2,True);text(s,h-1,1,'Arrows/WASD move | P/Space pause | R retry | M modes | Esc/Q exit',1)
    if h<19 or w<46:text(s,4,1,'Resize to46x19 or larger. Game paused.',3);return False
    cw=max(2,(w-2)//20);rh=max(1,(h-5)//12);left=(w-cw*20)//2;top=3
    for row in range(12):
        world=g.bottom+11-row if mode=='endless' else row
        road=g.lane(world) is not None if mode=='endless' else world in g.lanes
        for x in range(20):
            occupied=g.occupied(x,world);player=x==g.x and world==(g.row if mode=='endless' else g.y)
            for dy in range(rh):
                mark=('▄'*cw if dy==rh-1 else '█'*cw) if occupied else ('─' if (x+g.ticks)%4==0 else ' ')*cw if road else '░'*cw
                text(s,top+row*rh+dy,left+x*cw,mark,3 if occupied else 6 if road else 4)
            if occupied and cw>=4:text(s,top+row*rh,left+x*cw+1,'oo',2)
            if player:
                if cw>=4 and rh>=2:
                    text(s,top+row*rh,left+x*cw,' /o>'.ljust(cw),4,True);text(s,top+row*rh+1,left+x*cw,' /| '.ljust(cw),4,True)
                else:text(s,top+row*rh,left+x*cw,'@'.center(cw),4,True)
        if not road and world!=(g.row if mode=='endless' else g.y):text(s,top+row*rh,left,'REST '+str(world) if mode=='endless' else 'HOME' if row==0 else 'REST',4)
    text(s,h-2,1,'Original lane crossing - no online features or saved scores.',2);return True
def run(s,seed):
    setup(s);s.keypad(True);s.timeout(50);mode=None;g=None;paused=True;last=time.monotonic();choice=0
    while True:
        k=s.getch();now=time.monotonic()
        if k in (27,ord('q'),ord('Q')):return
        if mode is None:
            s.erase();h,w=s.getmaxyx();text(s,1,2,'LANELURRIX '+VERSION,1,True);text(s,3,2,'Fullscreen original crossing game',2)
            text(s,6,4,('> ' if choice==0 else '  ')+'LEVELS - ten crossings, harder traffic',4,True);text(s,8,4,('> ' if choice==1 else '  ')+'INFINITY - keep moving through new lanes',4,True);text(s,h-2,2,'Up/Down choose | Enter start | Esc/Q exit',1)
            if k in (curses.KEY_UP,curses.KEY_DOWN):choice=1-choice
            if k in (ord('1'),ord('2')):choice=k-ord('1');k=10
            if k in (10,13):mode='endless' if choice else 'levels';g=Endless(seed) if choice else Game(seed);paused=True;last=now
            s.refresh();continue
        if k in (ord('m'),ord('M')):mode=None;continue
        h,w=s.getmaxyx();fits=h>=19 and w>=46
        if k in (ord('r'),ord('R')):g=Endless(seed) if mode=='endless' else Game(g.seed,g.level);paused=True;last=now
        elif k in (ord('p'),ord('P'),ord(' ')):paused=not paused;last=now
        elif k in (10,13) and g.won and g.level<10:
            level=g.level+1;g=Game(None if seed is None else seed+level-1,level);paused=True;last=now
        elif fits:
            d={curses.KEY_UP:(0,-1),ord('w'):(0,-1),curses.KEY_DOWN:(0,1),ord('s'):(0,1),curses.KEY_LEFT:(-1,0),ord('a'):(-1,0),curses.KEY_RIGHT:(1,0),ord('d'):(1,0)}.get(k)
            if d:paused=False;g.move(*d)
        if not fits or paused or g.dead or g.won:last=now
        elif now-last>=g.interval:g.tick();last=now
        draw(s,g,mode,paused);s.refresh()
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--seed',type=int);p.add_argument('--demo',action='store_true');p.add_argument('--version',action='store_true');a=p.parse_args()
    if a.version:print(VERSION);return 0
    if a.demo:
        g=Game(a.seed);print('LANELURRIX\n'+'\n'.join(''.join('@' if (x,y)==(g.x,g.y) else '#' if g.occupied(x,y) else '.' for x in range(20)) for y in range(12)));return 0
    if not os.isatty(0) or not os.isatty(1):print('Needs an interactive terminal. Use --demo for a snapshot.');return 1
    try:curses.wrapper(run,a.seed);return 0
    except curses.error as exc:print('Terminal unavailable:',exc);return 1
    except KeyboardInterrupt:return 0
if __name__=='__main__':raise SystemExit(main())
