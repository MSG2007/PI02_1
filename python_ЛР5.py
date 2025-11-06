# Определение класса узла бинарного дерева
class TreeNode:
    def __init__(self, val=0):
        # Инициализация узла: значение (val) и ссылки на левого/правого потомков
        self.val = val          # Значение узла
        self.left = None        # Ссылка на левого потомка (изначально None)
        self.right = None       # Ссылка на правого потомка (изначально None)

# Функция прямого обхода (preorder): корень → левый → правый
def preorder(root):
    if root is not None:                # Если узел существует (не None)
        print(root.val, end=' ')     # Выводим значение текущего узла
        preorder(root.left)          # Рекурсивно обходим левое поддерево
        preorder(root.right)         # Рекурсивно обходим правое поддерево

# Функция центрированного обхода (inorder): левый → корень → правый
def inorder(root):
    if root is not None:                # Если узел существует
        inorder(root.left)            # Рекурсивно обходим левое поддерево
        print(root.val, end=' ')     # Выводим значение текущего узла
        inorder(root.right)          # Рекурсивно обходим правое поддерево

# Функция обратного обхода (postorder): левый → правый → корень
def postorder(root):
    if root is not None:                # Если узел существует
        postorder(root.left)         # Рекурсивно обходим левое поддерево
        postorder(root.right)        # Рекурсивно обходим правое поддерево
        print(root.val, end=' ')     # Выводим значение текущего узла

# Основная часть программы: создание дерева и вызов обходов
if __name__ == "__main__":
    # Создаём узлы дерева
    root = TreeNode(1)           # Корень дерева со значением 1
    root.left = TreeNode(2)      # Левый потомок корня: значение 2
    root.right = TreeNode(3)     # Правый потомок корня: значение 3
    root.left.left = TreeNode(4) # Левый потомок узла 2: значение 4
    root.left.right = TreeNode(5) # Правый потомок узла 2: значение 5

    # Выводим результаты обходов
    print("Preorder traversal:")
    preorder(root)                 # Вызов preorder-обхода
    print()                       # Перевод строки

    print("Inorder traversal:")
    inorder(root)                # Вызов inorder-обхода
    print()                      # Перевод строки

    print("Postorder traversal:")
    postorder(root)              # Вызов postorder-обхода
    print()                     # Перевод строки

ВЫВОД:
Preorder traversal:
1 2 4 5 3 
Inorder traversal:
4 2 5 1 3 
Postorder traversal:
4 5 2 3 1 

