class CalculatorMemory:
    """Класс, реализующий память калькулятора"""
    def __init__(self):
        """Инициализация объекта памяти значением 0"""
        self.__value = 0

    def get(self):
        """Получение значения из памяти"""
        return self.__value

    def store(self, new_value):
        """Запись нового значения в память"""
        self.__value = new_value

    def add(self, value):
        """Прибавление значения к значению в памяти"""
        self.__value += value

    def clear(self):
        """Очистка памяти"""
        self.__value = 0
