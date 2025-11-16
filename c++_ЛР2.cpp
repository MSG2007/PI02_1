//Создание мультисписка (вложенного списка)
#include <iostream>
#include <vector>
using namespace std;
int main() {
    vector<vector<string>> multilist = {{"яблоки", "груши"}, {"молоко", "сыр"}, {"хлеб", "масло"}}
}
    
//Создание очереди
#include <iostream>
#include <queue>
using namespace std;
int main() {
    queue<string> q;

    // Добавление элементов в очередь
    q.push("Первый");
    q.push("Второй");
    q.push("Третий");
}

//Создание дека
#include <iostream>
#include <deque>
using namespace std;
int main() {
    deque<int> d;
    d.push_front(1);          
    d.push_back(2);           
}

//Создание приоритетной очереди с примитивным типом
#include <iostream>
#include <queue>
int main() {
    std::priority_queue<int> pq;
    pq.push(10); 
    pq.push(20); 
    pq.push(5);  
}

//Создание приоритетной очереди с пользовательскими структурами
#include <iostream>
#include <queue>
#include <string>
struct Task {
 std::string name;
 int priority;
 bool operator<(const Task& other) const {
 return priority < other.priority;
 }
};
int main() {
 std::priority_queue<Task> taskQueue;
 taskQueue.push({"Task 1", 2});
 taskQueue.push({"Task 2", 1});
 taskQueue.push({"Task 3", 3});
}
