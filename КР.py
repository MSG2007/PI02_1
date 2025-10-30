АЛГОРИТМ БЛОЧНОЙ СОРТИРОВКИ
def bucket_sort(arr):

    # Находим минимальное и максимальное значения в массиве
    min_val = min(arr)
    max_val = max(arr)

    # Определяем количество блоков (ведёр)
    # Число блоков должно соответствовать числу уникальных возможных значений
    bucket_count = max_val - min_val + 1

    # Создаем блоки (ведра) в виде списка списков
    buckets = [[] for _ in range(bucket_count)]

    # Распределяем элементы по соответствующим блокам
    for num in arr:
        # Индекс блока, в который попадёт элемент
        idx = num - min_val
        buckets[idx].append(num)

    # Сортируем каждый блок индивидуально (можно использовать любую сортировку)
    for bucket in buckets:
        bucket.sort()

    # Соединяем отсортированные блоки в результирующий массив
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)

    return sorted_arr

# Пример использования
array = [3, 6, 2, 1, 9, 5, 8, 4, 7]
sorted_array = bucket_sort(array)
print("Отсортированный массив:", sorted_array)

Отсортированный массив: [1, 2, 3, 4, 5, 6, 7, 8, 9]

АЛГОРИТМ БЛИННОЙ СОРТИРОВКИ
def flip(arr, k):
    """
    Функция переворачивания (flip) подмассива от начала до k-го элемента включительно.
    Параметры:
    - arr: Список (массив), который нужно перевернуть.
    - k: Индекс последней позиции подмассива, который нужно перевернуть.
    """
    start = 0
    end = k
    while start < end:
        # Меняем местами элементы на противоположных концах подмассива
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1

def find_max_index(arr, n):
    """
    Функция для поиска индекса максимального элемента в подмассиве от начала до n-й позиции.
    Параметры:
    - arr: Список (массив), в котором ищем максимум.
    - n: Количество элементов, среди которых ищем максимум.
    """
    max_idx = 0
    for i in range(1, n):
        if arr[i] > arr[max_idx]:
            max_idx = i
    return max_idx

def pancake_sort(arr):
    """
    Реализация алгоритма блинной сортировки.
    Параметр:
    - arr: Список (массив), который нужно отсортировать.
    """
    curr_size = len(arr)
    while curr_size > 1:
        # Находим индекс максимального элемента в текущем несортированном сегменте
        max_idx = find_max_index(arr, curr_size)

        # Если максимальный элемент уже на нужной позиции, ничего не делаем
        if max_idx != curr_size - 1:
            # Перевертываем подмассив от начала до максимального элемента
            flip(arr, max_idx)
            # Перевертываем весь текущий сегмент, чтобы максимальный элемент попал в конец
            flip(arr, curr_size - 1)

        # Уменьшаем размер несортированного сегмента
        curr_size -= 1

    return arr

# Пример использования
array = [3, 6, 2, 7, 4, 1, 5]
sorted_array = pancake_sort(array)
print("Отсортированный массив:", sorted_array)

Отсортированный массив: [1, 2, 3, 4, 5, 6, 7]

АЛГОРИТМ СОРТИРОВКИ БУСИНАМИ
def bead_sort(arr):
    """
    Реализация алгоритма сортировки бусинами (bead sort).
    Параметр:
    - arr: Список положительных целых чисел, подлежащих сортировке.
    Возвращает отсортированный массив.
    """
    # Проверка на корректность данных (только положительные целые числа)
    if any(not isinstance(x, int) or x < 0 for x in arr):
        raise ValueError("Все элементы массива должны быть положительными целыми числами.")

    # Находим максимальную величину в массиве
    max_num = max(arr)

    # Формируем матрицу "бусин", где каждая строка представляет число из массива
    beads_matrix = [[1 if j < val else 0 for j in range(max_num)] for val in arr]

    # Проваливаем "бусины" вниз (каждый столбец должен быть выровнен снизу)
    for col in range(len(beads_matrix[0])):
        ones_in_col = sum(row[col] for row in beads_matrix)  # Считаем количество единиц в столбце
        zeros_in_col = len(beads_matrix) - ones_in_col       # Считаем количество нулей
        # Перестраиваем столбец, занося единицы вниз, а нули вверх
        for i in range(zeros_in_col):
            beads_matrix[i][col] = 0
        for i in range(zeros_in_col, len(beads_matrix)):
            beads_matrix[i][col] = 1

    # Читаем высоты столбцов сверху вниз, получая отсортированный массив
    sorted_arr = [sum(row) for row in zip(*beads_matrix)]

    return sorted_arr

# Пример использования
array = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
sorted_array = bead_sort(array)
print("Отсортированный массив:", sorted_array)

Отсортированный массив: [11, 9, 8, 6, 5, 2, 1, 1, 1]

АЛГОРИТМ ПОИСКА СКАЧКАМИ
import math

def jump_search(arr, target):
    """
    Реализация алгоритма поиска скачками (jump search).
    Параметры:
    - arr: Отсортированный массив, в котором нужно произвести поиск.
    - target: Целевое значение, которое мы ищем.
    Возвращает индекс элемента, если он найден, иначе -1.
    """
    n = len(arr)                      # Длина массива
    step = int(math.sqrt(n))          # Величина скачка (примерно квадратный корень из длины массива)

    prev = 0                           # Индекс начала текущего блока
    next_block_start = step            # Индекс начала следующего блока

    # Ищем блок, в котором может находиться искомый элемент
    while next_block_start < n and arr[next_block_start] <= target:
        prev = next_block_start        # Переходим к началу следующего блока
        next_block_start += step       # Пересчитываем индекс начала следующего блока

    # Линенрый поиск в найденном блоке
    for i in range(prev, min(next_block_start, n)):
        if arr[i] == target:
            return i                   # Вернули индекс найденного элемента

    # Если элемент не найден, возвращаем -1
    return -1

# Пример использования
array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
target_value = 13

result = jump_search(array, target_value)

if result != -1:
    print(f"Элемент {target_value} найден на индексе {result}.")
else:
    print(f"Элемент {target_value} не найден.")

Элемент 13 найден на индексе 6.

АЛГОРИТМ ЭКСПОНЕНЦИАЛЬНОГО ПОИСКА
def exponential_search(arr, target):
    """
    Реализует алгоритм экспоненциального поиска.
    Параметры:
    arr - отсортированный массив, в котором ведется поиск.
    target - искомое значение.
    Возвращает индекс найденного элемента или -1, если элемент не найден.
    """
    if arr[0] == target:  # Если первый элемент совпадает с искомым, вернуть его индекс
        return 0
    
    # Находим индекс, начиная с двойного увеличения
    i = 1
    while i < len(arr) and arr[i] <= target:
        i *= 2  # Удвоение индекса
    
    # Диапазон для бинарного поиска
    low = i // 2  # Нижняя граница
    high = min(i, len(arr) - 1)  # Верхняя граница
    
    # Используем встроенную функцию bisect_left для бинарного поиска
    from bisect import bisect_left
    position = bisect_left(arr, target, low, high + 1)
    
    # Проверяем, нашел ли бисект нужный элемент
    if position != len(arr) and arr[position] == target:
        return position
    else:
        return -1

# Демонстрация работы
if __name__ == "__main__":
    arr = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    target = 55
    result = exponential_search(arr, target)
    if result != -1:
        print(f"Элемент {target} найден на позиции {result}.")
    else:
        print(f"Элемент {target} не найден.")

Элемент 55 найден на позиции 10.

АЛГОРИТМ ТЕРНАРНОГО ПОИСКА
def ternary_search(arr, target):
    """
    Реализация алгоритма тернарного поиска.
    Алгоритм делит массив на три части и проводит поиск в соответствующей трети.
    """
    left = 0                                # Левая граница поиска
    right = len(arr) - 1                    # Правая граница поиска

    while left <= right:
        # Определяем две средние точки
        third_left = left + (right - left) // 3
        third_right = right - (right - left) // 3

        # Если элемент найден в третьей слева
        if arr[third_left] == target:
            return third_left

        # Если элемент найден в третьей справа
        if arr[third_right] == target:
            return third_right

        # Если искомый элемент меньше левой трети, сузим поиск слева
        if target < arr[third_left]:
            right = third_left - 1
        # Если искомый элемент больше правой трети, сузим поиск справа
        elif target > arr[third_right]:
            left = third_right + 1
        # Если элемент находится между третями, сузим поиск в центре
        else:
            left = third_left + 1
            right = third_right - 1

    # Если элемент не найден, возвращаем -1
    return -1

# Пример использования
array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
target_value = 13

result = ternary_search(array, target_value)

if result != -1:
    print(f"Элемент {target_value} найден на индексе {result}.")
else:
    print(f"Элемент {target_value} не найден.")

Элемент 13 найден на индексе 6.
