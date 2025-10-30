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

