import unittest
from bot import hmtimeswork, hmtimeshome

class bot_test(unittest.TestCase):
  def test(self):
    self.assertEqual(hmtimeswork(12), 48)
  def test1(self):
    self.assertEqual(hmtimeswork(15), 60)
  def test2(self):
    self.assertEqual(hmtimeshome(15), 9)
  def test3(self):
    self.assertEqual(hmtimeshome(10), 13)
                     
if __name__ == "__main__":
    unittest.main()
