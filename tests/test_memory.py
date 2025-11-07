import unittest
from memory import CalculatorMemory

class TestCalculatorMemory(unittest.TestCase):
    def setUp(cls):
        cls.memory = CalculatorMemory()

    def testStoreAndGet(self):
        """Проверка сохранения значения в память и его получение"""
        self.memory.store('10')
        self.assertEqual(self.memory.get(), 10)

    def testSum(self):
        """Проверка добавления значения к значению в памяти"""
        self.memory.add('5')
        self.assertEqual(self.memory.get(), 5)

    def testSubtract(self):
        """Проверка вычитания значения из памяти"""
        self.memory.subtract('7')
        self.assertEqual(self.memory.get(), -7)

    def testClear(self):
        """Проверка очистки памяти"""
        self.memory.clear()
        self.assertEqual(self.memory.get(), 0)
