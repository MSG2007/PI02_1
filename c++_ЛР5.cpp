#include <iostream>  // Подключение библиотеки для ввода-вывода
using namespace std; // Использование пространства имён std

// Определение структуры узла бинарного дерева
struct TreeNode {
    int val;           // Значение узла
    TreeNode* left;    // Указатель на левого потомка
    TreeNode* right;   // Указатель на правого потомка

    // Конструктор узла: инициализирует значение и указатели
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

// Функция прямого обхода (preorder): корень → левый → правый
void preorder(TreeNode* root) {
    if (root != nullptr) {           // Если узел не нулевой
        cout << root->val << " ";  // Выводим значение узла
        preorder(root->left);       // Рекурсивно обходим левое поддерево
        preorder(root->right);      // Рекурсивно обходим правое поддерево
    }
}

// Функция центрированного обхода (inorder): левый → корень → правый
void inorder(TreeNode* root) {
    if (root != nullptr) {           // Если узел не нулевой
        inorder(root->left);        // Рекурсивно обходим левое поддерево
        cout << root->val << " ";   // Выводим значение узла
        inorder(root->right);       // Рекурсивно обходим правое поддерево
    }
}

// Функция обратного обхода (postorder): левый → правый → корень
void postorder(TreeNode* root) {
    if (root != nullptr) {           // Если узел не нулевой
        postorder(root->left);      // Рекурсивно обходим левое поддерево
        postorder(root->right);     // Рекурсивно обходим правое поддерево
        cout << root->val << " ";  // Выводим значение узла
    }
}

int main() {
    // Создаём узлы дерева
    TreeNode* root = new TreeNode(1);         // Корень со значением 1
    root->left = new TreeNode(2);             // Левый потомок: 2
    root->right = new TreeNode(3);            // Правый потомок: 3
    root->left->left = new TreeNode(4);      // Левый потомок узла 2: 4
    root->left->right = new TreeNode(5);     // Правый потомок узла 2: 5

    // Выводим результаты обходов
    cout << "Preorder traversal:" << endl;
    preorder(root);                           // Вызов preorder
    cout << endl;

    cout << "Inorder traversal:" << endl;
    inorder(root);                            // Вызов inorder
    cout << endl;

    cout << "Postorder traversal:" << endl;
    postorder(root);                          // Вызов postorder
    cout << endl;

    return 0;
}

ВЫВОД:
Preorder traversal:
1 2 4 5 3 
Inorder traversal:
4 2 5 1 3 
Postorder traversal:
4 5 2 3 1 

