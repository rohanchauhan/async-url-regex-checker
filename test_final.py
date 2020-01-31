import unittest
import final_program as fp
import asyncio
from itertools import cycle

"""

Very simple unit tests for the final program.
More complex test could have been written for async functions. 

"""

class TestFinal(unittest.TestCase):
	dataset = cycle(fp.load_dataset())
	
	def test_load_dataset(self):
		""" Tests that dataset is not empty"""
		self.assertIsNotNone(self.dataset)

	def test_producer(self):
		""" Tests that we can cycle through dataset"""
		self.assertIsNotNone(next(self.dataset))

	def test_write_results(self):
		""" Tests that filename is not empty"""
		self.assertIsNotNone(fp.filename)

if __name__ == '__main__':
	unittest.main()