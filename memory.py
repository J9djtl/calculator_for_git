class CalculatorMemory:
    def __init__(self):
        self.__value = 0

    def get(self):
        return self.__value

    def store(self, new_value):
        self.__value = new_value

    def add(self, value):
        self.__value += value

    def clear(self):
        self.__value = 0
