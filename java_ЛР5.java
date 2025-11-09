// Класс узла бинарного дерева
class TreeNode {
    int val;          // Значение узла
    TreeNode left;    // Ссылка на левый дочерний узел
    TreeNode right;   // Ссылка на правый дочерний узел

    // Конструктор для создания узла с заданным значением
    TreeNode(int val) {
        this.val = val;
        this.left = null;
        this.right = null;
    }
}

// Класс, реализующий обходы бинарного дерева
public class BinaryTreeTraversal {

    // Метод для preorder обхода (узел → левое поддерево → правое поддерево)
    public static void preorder(TreeNode root) {
        // Если текущий узел null — выходим из рекурсии (базовый случай)
        if (root == null) {
            return;
        }

        // 1. Обрабатываем корень: выводим значение текущего узла
        System.out.print(root.val + " ");

        // 2. Рекурсивно обходим левое поддерево
        preorder(root.left);

        // 3. Рекурсивно обходим правое поддерево
        preorder(root.right);
    }

    // Метод для inorder обхода (левое поддерево → узел → правое поддерево)
    public static void inorder(TreeNode root) {
        // Если текущий узел null — выходим из рекурсии (базовый случай)
        if (root == null) {
            return;
        }

        // 1. Рекурсивно обходим левое поддерево
        inorder(root.left);

        // 2. Обрабатываем корень: выводим значение текущего узла
        System.out.print(root.val + " ");

        // 3. Рекурсивно обходим правое поддерево
        inorder(root.right);
    }

    // Метод для postorder обхода (левое поддерево → правое поддерево → узел)
    public static void postorder(TreeNode root) {
        // Если текущий узел null — выходим из рекурсии (базовый случай)
        if (root == null) {
            return;
        }

        // 1. Рекурсивно обходим левое поддерево
        postorder(root.left);

        // 2. Рекурсивно обходим правое поддерево
        postorder(root.right);

        // 3. Обрабатываем корень: выводим значение текущего узла
        System.out.print(root.val + " ");
    }

    // Основной метод для демонстрации работы обходов
    public static void main(String[] args) {
        // Создаём корневое дерево:
        //       1
        //      / \
        //     2   3
        //    / \
        //   4   5

        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);

        System.out.println("Preorder обход:");
        preorder(root);  // Ожидаемый вывод: 1 2 4 5 3
        System.out.println();  // Переход на новую строку

        System.out.println("Inorder обход:");
        inorder(root);   // Ожидаемый вывод: 4 2 5 1 3
        System.out.println();  // Переход на новую строку

        System.out.println("Postorder обход:");
        postorder(root); // Ожидаемый вывод: 4 5 2 3 1
        System.out.println();  // Переход на новую строку
    }
}

ВЫВОД:

Preorder обход:
1 2 4 5 3 
Inorder обход:
4 2 5 1 3 
Postorder обход:
4 5 2 3 1 

