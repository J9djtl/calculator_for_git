import unittest
import tkinter as tk
from frontend import CalculatorGUI
from unittest.mock import patch

class TestCalculatorGUI(unittest.TestCase):
    # фиктсуры
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # скрываем окно, чтобы не мешало тестам
        self.gui = CalculatorGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    # Тесты для поля ввода
    def test_set_and_get_text(self):
        """текст корректно записывается и читается из GUI, в состоянии disable"""
        self.gui.set_text("42")
        self.assertEqual(self.gui.get_text(), "42")

    def test_append_text(self):
        """append_text не перезаписывает, а именно дописывает"""
        self.gui.set_text("4")
        self.gui.append_text("+2")
        self.assertEqual(self.gui.get_text(), "4+2")

    # Тесты для сообщения
    def test_show_message(self):
        """Cообщение действительно появляется и имеет нужный цвет"""
        self.gui.show_message("Ошибка", color="red")
        self.assertEqual(self.gui.message_label.cget("text"), "Ошибка")
        self.assertEqual(self.gui.message_label.cget("foreground"), "red")

    def test_hide_message(self):
        "Сообщение исчезает из интерфейса, когда надо"
        self.gui.show_message("Тест")
        self.gui.hide_message()
        self.assertFalse(self.gui.message_label.winfo_ismapped())

    # Тесты для кнопок
    def test_on_button_click(self):
        "При нажатии простой кнопки символ действительно добавляется в поле"
        self.gui.set_text("")
        self.gui.on_button_click("7")
        self.assertEqual(self.gui.get_text(), "7")

    def test_on_clear(self):
        """функциональность кнопки "C" — очистка текущего выражения"""
        self.gui.set_text("123")
        self.gui.on_clear()
        self.assertEqual(self.gui.get_text(), "")

    def test_on_backspace(self):
        """Проверка логики удаления последнего символа."""
        self.gui.set_text("123")
        self.gui.on_backspace()
        self.assertEqual(self.gui.get_text(), "12")

    def test_on_all_clear(self):
        """Проверка полной очистки интерфейса.Подготовка к расширению логики ( сброс памяти)."""
        self.gui.set_text("456")
        self.gui.on_all_clear()
        self.assertEqual(self.gui.get_text(), "")

    def test_on_insert_function(self):
        """Проверка корректности вставки математических функций."""
        self.gui.set_text("")
        self.gui.on_insert_function("sin")
        self.assertEqual(self.gui.get_text(), "sin(")

    def test_on_insert_special(self):
        """Проверкак корректности вывода специальных функций"""
        self.gui.set_text("")
        self.gui.on_insert_special("10^(")
        self.assertEqual(self.gui.get_text(), "10^(")

    # Тесты памяти (заглушки)
    def test_on_memory_clear(self):
        self.gui.on_memory_clear()
        self.assertEqual(self.gui.message_label.cget("text"), "Память очищена")

    def test_on_memory_recall(self):
        self.gui.on_memory_recall()
        self.assertEqual(self.gui.message_label.cget("text"), "MEM_VALUE")

    def test_on_memory_store(self):
        self.gui.set_text("123")
        self.gui.on_memory_store()
        self.assertIn("123", self.gui.message_label.cget("text"))

    def test_on_memory_add(self):
        self.gui.set_text("5")
        self.gui.on_memory_add()
        self.assertIn("5", self.gui.message_label.cget("text"))

    def test_on_memory_subtract(self):
        self.gui.set_text("3")
        self.gui.on_memory_subtract()
        self.assertIn("3", self.gui.message_label.cget("text"))

    # Тест для вычисления выражения (с моканым evaluate_expression)
    @patch("logic.evaluate_expression", return_value=42)
    def test_on_equal_press_success(self, mock_eval):
        """Вычесленное выражение действительно выводится"""
        self.gui.set_text("1+2")
        self.gui.on_equal_press()
        self.assertEqual(self.gui.get_text(), "42")

    @patch("logic.evaluate_expression", side_effect=Exception("Ошибка"))
    def test_on_equal_press_error(self, mock_eval):
        """Ошибка при вычмслении корректно отображается"""
        self.gui.set_text("1/0")
        self.gui.on_equal_press()
        self.assertEqual(self.gui.get_text(), "Ошибка")

    # Тест для генерации команд
    def test_get_button_command_returns_callable(self):
        """Убедиться, что каждая кнопка получает корректную команду"""
        cmd = self.gui.get_button_command("1")
        self.assertTrue(callable(cmd))

    def test_get_button_type_basic(self):
        self.assertEqual(self.gui.get_button_type("1", 30), "basic")

    def test_get_button_type_extended(self):
        self.assertEqual(self.gui.get_button_type("sqrt", 16), "extended")

    def test_get_button_type_memory(self):
        self.assertEqual(self.gui.get_button_type("MR", 1), "memory")


if __name__ == "__main__":
    unittest.main()
