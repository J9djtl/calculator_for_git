import math
import re


def evaluate_expression(expression: str) -> float:
    """
    Подается строка -- выражение, заданное калькулятору;
    возвращается число - ответ
    Поддерживаемые операции: +, -, *, /, %, ^, sin, cos, sqrt, floor, ceil
    """
    try:
        # Проверка на пустую строку
        if not expression.strip():
            return 0
            
        # Обработка специальных функций и констант
        expression = preprocess_expression(expression)
            
        # Обработка выражений в скобках и функций
        expression = process_functions_and_parentheses(expression)
        
        # Вычисление выражения
        result = calculate_expression(expression)
        
        return result
        
    except Exception as e:
        raise ValueError(f"Ошибка вычисления: {e}")


def preprocess_expression(expr: str) -> str:
    """Предварительная обработка выражения"""

    # Добавление умножения там, где оно подразумевается (например:2sin(30)->2*sin(30))
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    expr = re.sub(r'(\))(\d)', r'\1*\2', expr)
    expr = re.sub(r'(\))(\()', r'\1*\2', expr)
    
    while '--' in expr:
        expr = expr.replace('--', '+')
    while '++' in expr:
        expr = expr.replace('++', '+')
    while '+-' in expr:
        expr = expr.replace('+-', '-')
    while '-+' in expr:
        expr = expr.replace('-+', '-')
    # Обработка унарного минуса
    expr = re.sub(r'(^|[+\-*/^%(\)])-', r'\1u-', expr)
    
    return expr


def process_functions_and_parentheses(expr: str) -> str:
    """Обработка функций и выражений в скобках"""
    while True:
        # Ищем самую внутреннюю пару скобок
        match = re.search(r'([a-zA-Z]+)?\(([^()]+)\)', expr)
        if not match:
            break
            
        func_name = match.group(1) or ''
        inner_expr = match.group(2)
        
        # предварительная обработка внутри скобок
        inner_expr = preprocess_expression(inner_expr)

        # Вычисляем выражение внутри скобок
        inner_result = calculate_expression(inner_expr)
        
        # Применяем функцию если есть
        if func_name:
            inner_result = apply_function(func_name, inner_result)
        
        if inner_result < 0:
            result_str = 'u-' + str(abs(inner_result))
        else:
            result_str = str(inner_result)

        # Заменяем выражение в скобках на результат
        expr = expr.replace(match.group(0), result_str, 1)
    
    return expr


def apply_function(func_name: str, value: float) -> float:
    """Применение математических функций"""
    func_name = func_name.lower()
    
    if func_name == 'sin':
        result = math.sin(math.radians(value))  # Работаем с градусами
        return 0.0 if abs(result) < 1e-10 else result
    elif func_name == 'cos':
        result = math.cos(math.radians(value))
        return 0.0 if abs(result) < 1e-10 else result
    elif func_name == 'sqrt':
        if value < 0:
            raise ValueError("Квадратный корень из отрицательного числа")
        return math.sqrt(value)
    elif func_name == 'floor':
        return math.floor(value)
    elif func_name == 'ceil':
        return math.ceil(value)
    elif func_name == 'abs':
        return abs(value)
    else:
        raise ValueError(f"Неизвестная функция: {func_name}")


def calculate_expression(expr: str) -> float:
    """Вычисление базового арифметического выражения"""
    
    # Токенизация выражения
    tokens = tokenize(expr)
    
    # Конвертация в обратную польскую запись (RPN)
    rpn_tokens = shunting_yard(tokens)
    
    # Вычисление RPN
    return evaluate_rpn(rpn_tokens)


def tokenize(expr: str) -> list:
    """Разбиение выражения на токены"""
    # Регулярное выражение для токенизации чисел, операторов и функций
    token_pattern = r'\d+\.?\d*|u-|[a-zA-Z]+|[+\-*/%^()]'
    tokens = re.findall(token_pattern, expr)
    return tokens


def shunting_yard(tokens: list) -> list:
    """Алгоритм сортировочной станции (Shunting Yard) для преобразования в RPN"""
    output = []
    operators = []
    
    precedence = {
        '+': 1, '-': 1,
        '*': 2, '/': 2, '%': 2,
        '^': 3
    }

    for token in tokens:
        if re.match(r'\d+\.?\d*', token):  # Число
            output.append(float(token))
        elif token == 'u-':
            # Унарный минус — всегда идёт в стек с высоким приоритетом
            operators.append(token)
        elif token in precedence:  # Оператор
            while (operators and
                   operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # Удаляем '('
    
    while operators:
        output.append(operators.pop())
    
    return output


def evaluate_rpn(tokens: list) -> float:
    """Вычисление выражения в обратной польской записи"""
    stack = []
    
    for token in tokens:
        if isinstance(token, float):  # Число
            stack.append(token)
        elif token == 'u-':
            if not stack:
                raise ValueError("Унарный минус без операнда")
            a = stack.pop()
            stack.append(-a)
        else:  # Оператор
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для операции")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ValueError("Деление на ноль")
                stack.append(a / b)
            elif token == '%':
                if b == 0:
                    raise ValueError("Деление на ноль при взятии остатка")
                stack.append(a % b)
            elif token == '^':
                stack.append(a ** b)
    
    if len(stack) != 1:
        raise ValueError("Некорректное выражение")
    
    return stack[0]
