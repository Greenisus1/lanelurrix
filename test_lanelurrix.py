import unittest
from lanelurrix import Game
class Tests(unittest.TestCase):
 def test_safe_rows(self):
  g=Game(1)
  for y in (0,4,8,11):self.assertFalse(any(g.occupied(x,y) for x in range(20)))
 def test_boundary(self):
  g=Game();g.move(100,0);self.assertEqual(g.x,19);g.move(-100,0);self.assertEqual(g.x,0);g.move(0,100);self.assertEqual(g.y,11)
 def test_collision(self):
  g=Game(1);x=next(x for x in range(20) if g.occupied(x,1));g.x=x;g.y=2;g.move(0,-1);self.assertTrue(g.dead);old=g.ticks;g.tick();self.assertEqual(g.ticks,old)
 def test_win(self):
  g=Game();g.y=1;g.move(0,-1);self.assertTrue(g.won)
 def test_motion(self):
  g=Game(1);before=[g.occupied(x,1) for x in range(20)];g.tick();self.assertNotEqual(before,[g.occupied(x,1) for x in range(20)])
 def test_seed(self):self.assertEqual(Game(42).lanes,Game(42).lanes)
 def test_tick_collision(self):
  g=Game(1);g.y=1;g.x=next(x for x in range(20) if not g.occupied(x,1) and (x-g.lanes[1][0]-g.lanes[1][1])%7<g.lanes[1][2]);g.tick();self.assertTrue(g.dead)
if __name__=='__main__':unittest.main()
