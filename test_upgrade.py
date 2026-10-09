import unittest
from lanelurrix import Game,Endless
class Tests(unittest.TestCase):
 def test_speed(self):self.assertLess(Game(1,10).interval,Game(1,1).interval)
 def test_levels_safe(self):
  for level in range(1,11):
   g=Game(2,level)
   for y in (0,4,8,11):self.assertFalse(g.occupied(1,y))
 def test_endless_seed(self):
  a,b=Endless(42),Endless(42)
  self.assertEqual([a.lane(i) for i in range(100)],[b.lane(i) for i in range(100)])
 def test_endless_rest(self):
  g=Endless(1)
  for y in range(0,100,4):self.assertFalse(any(g.occupied(x,y) for x in range(20)))
 def test_scroll(self):
  g=Endless(1);g.row=g.best=100;g.move(0,100);self.assertEqual(g.row,97)
 def test_endless_collision(self):
  g=Endless(1);x=next(x for x in range(20) if g.occupied(x,1));g.x=x;g.move(0,-1);self.assertTrue(g.dead)
 def test_cache_bounded(self):
  g=Endless(1)
  for n in range(1000):
   g.dead=False;g.row=g.best=n;g.move(0,0)
   for row in range(g.bottom,g.bottom+12):g.lane(row)
  self.assertLessEqual(len(g.lanes),25)
 def test_endless_speed(self):
  g=Endless(1);before=g.interval;g.best=100;self.assertLess(g.interval,before)
if __name__=='__main__':unittest.main()
