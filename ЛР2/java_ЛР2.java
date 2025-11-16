//Создание мультисписка(вложенный список)
import java.util.ArrayList;
import java.util.List;
public class Main {
    public static void main(String[] args) {
        List<List<String>> multilist = new ArrayList<>();
        multilist.add(new ArrayList<>(List.of("яблоки", "груши")));
        multilist.add(new ArrayList<>(List.of("молоко", "сыр")));
        multilist.add(new ArrayList<>(List.of("хлеб", "масло")));
    }
}

//Создание очереди
import java.util.LinkedList;
import java.util.Queue;
public class Main {
    public static void main(String[] args) {
        Queue<String> queue = new LinkedList<>();
        queue.offer("Первый");
        queue.offer("Второй");
        queue.offer("Третий");
    }
}

//Создание дека
import java.util.Deque;
import java.util.ArrayDeque;
public class Main {
    public static void main(String[] args) {
        Deque<Integer> deque = new ArrayDeque<>();
        deque.addFirst(1);       // добавляет элемент спереди
        deque.addLast(2);        // добавляет элемент сзади
    }
}

//Создание приоритетной очереди
import java.util.PriorityQueue;
public class PriorityQueueExample {
    public static void main(String[] args) {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.offer(10);
        pq.offer(20);
        pq.offer(5);
    }
}

//Создание приоритетной очереди с компаратором
Comparator<Task> idComparator = Comparator.comparing(Task::id);
PriorityQueue<Task> priorityQueue = new PriorityQueue<>(idComparator);
priorityQueue.add(new Task(10001, "Task 1", 5));
priorityQueue.add(new Task(10003, "Task 3", 10));
priorityQueue.add(new Task(10002, "Task 2", 1));
