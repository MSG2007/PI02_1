//Список на C++
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> numbers = {1,15,9,36,18};

    cout << "Список чисел: ";
    for(int i=0; i < numbers.size(); i++) {
        cout << numbers[i] << " ";
    }
    return 0;
}

//Stack на C++
#include <iostream>
#include <stack>
using namespace std;
int main() {
    stack<int> numbers;
    numbers.push(1)
    numbers.push(15)
    numbers.push(9)
    numbers.push(36)
    numbers.push(18)

    return 0;
}
