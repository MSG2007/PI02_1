# Создание мультисписка (вложенного списка)
multilist = [["яблоки", "груши"], ["молоко", "сыр"], ["хлеб", "масло"]]
                                        
#Создание очереди
from queue import Queue
q = Queue()
q.put(1)
q.put(2)
q.put(3)

#Создание дека
from collections import deque
dq = deque()
dq.append(10)        
dq.append(20) 
dq.append(30) 

#Создание приоритетная очереди с помощью PriorityQueue 
from queue import PriorityQueue
pq = PriorityQueue()
pq.put((1, "низкий приоритет"))
pq.put((3, "высокий приоритет"))
pq.put((2, "средний приоритет"))

#Создание приоритетной очереди с помощью heapq
import heapq
pq = []
heapq.heappush(pq, (3, 'Задача 3'))
heapq.heappush(pq, (1, 'Задача 1'))
heapq.heappush(pq, (2, 'Задача 2'))
