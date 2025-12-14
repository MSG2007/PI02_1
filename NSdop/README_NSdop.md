1.Задание 15: Object Detection с YOLO. Задача: реализовать простую версию YOLO для детекции объектов. Требования: Grid-based detection (7x7 или 13x13); Bounding box predictions (x, y, w, h); Confidence score и class probabilities; Non-Maximum Suppression (NMS).

2.Алгоритм работы НС:
1)Инициализация параметров. Задание основных гиперпараметров нейронной сети. Метод: __init__().
2)Построение архитектуры модели. Создание сверточной архитектуры для извлечения признаков. Метод _build_model() класса YOLO.
3)Конволюционный блок с регуляризацией (def _conv_block(x, filters, kernel_size, dropout_rate=0.3)).
4)Создание синтетического датасета (create_synthetic_dataset()). Для каждого изображения: Создаём пустое 416x416 изображение; Добавляем 1-3 цветных прямоугольника (Red, Green, Blue); Кодируем в грид 13x13: gt[i, j, 0:2] = (x_offset, y_offset)... 
5)Прямой проход (Forward Pass) (predictions = yolo.model(batch_X, training=True)).
6)Обратное распространение (Backpropagation).
gradients = tape.gradient(total_loss, model.trainable_variables)
gradients, _ = tf.clip_by_global_norm(gradients, 5.0)  # Gradient clipping
optimizer.apply_gradients(zip(gradients, model.trainable_variables))
7)Декодирование предсказаний.
box_xy = (box_xy + grid) / 13 * 416    
box_wh = box_wh / 13 * 416
8)Фильтрация по confidence (mask = best_scores > confidence_threshold).
9)Non-Maximum Suppression (NMS) (def non_maximum_suppression(self, detections, iou_threshold=0.5)).
10)Вычисление IoU (Intersection over Union) (def compute_iou(box1, box2)).
11)Вычисление mAP (Mean Average Precision)(mAP = yolo.compute_map(all_val_detections, val_gt, iou_threshold=0.5)).

3.Контрольный вопрос. 15. Как Alpha-Beta Pruning оптимизирует Minimax? Какую сложность он позволяет достичь?
Alpha-Beta Pruning оптимизирует алгоритм Minimax путём отсечения ветвей дерева игры, которые не влияют на окончательное решение.
Алгоритм ведёт две переменные:
Alpha — лучшая уже найденная оценка для максимизирующего игрока (текущий нижний предел);
Beta — лучшая уже найденная оценка для минимизирующего игрока (текущий верхний предел).
Если в процессе поиска обнаруживается, что текущий узел для одного игрока хуже, чем уже гарантированный вариант в предыдущем ходе для другого игрока (alpha >= beta), то поиск в этой ветви немедленно прекращается. Это означает, что дальнейшие ходы в этой ветви не изменят итоговое решение.

Таким образом, Alpha-Beta Pruning находит точно такое же оптимальное решение, что и полный Minimax, но делает это быстрее, просматривая лишь небольшую часть дерева.

Временная сложность. При применении Alpha-Beta Pruning сложность уменьшается с O(b^d) до O(b^(d/2)), где:
b — коэффициент ветвления (количество возможных ходов на каждом уровне),
d — глубина дерева (поиска).
