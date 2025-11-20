import java.util.Scanner;

public class SimulatedAnnealing {

    /**
     * Метод реализует алгоритм имитации отжига для минимизации функции f(x) = x²
     * @param temp начальная температура
     * @param cooling коэффициент охлаждения (0 < cooling < 1)
     * @return найденное значение x, минимизирующее x²
     */
    public static double saSquare(double temp, double cooling) {
        // Начальное случайное значение x в диапазоне [-10, 10]
        double x = Math.random() * 20 - 10;
        // Текущее значение функции (энергии)
        double energy = x * x;

        // Основной цикл: пока температура выше порога
        while (temp > 1e-6) {
            // Генерируем новое значение x в окрестности текущего с амплитудой, зависящей от температуры
            double xNew = x + (Math.random() * 2 - 1) * temp;
            // Вычисляем энергию нового состояния
            double energyNew = xNew * xNew;

            // Критерий Метрополиса: принимаем новое состояние, если:
            // 1. Энергия меньше (улучшение), ИЛИ
            // 2. Случайное число меньше вероятности перехода при ухудшении
            if (energyNew < energy || 
                Math.random() < Math.exp((energy - energyNew) / temp)) {
                x = xNew;      // переходим в новое состояние
                energy = energyNew;  // обновляем энергию
            }

            // Уменьшаем температуру
            temp *= cooling;
        }

        return x;  // возвращаем найденное значение x
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        try {
            System.out.print("Введите начальную температуру (temp > 0): ");
            double temp = scanner.nextDouble();

            if (temp <= 0) {
                System.out.println("Ошибка: температура должна быть положительной!");
                return;
            }

            System.out.print("Введите коэффициент охлаждения (0 < cooling < 1): ");
            double cooling = scanner.nextDouble();

            if (cooling <= 0 || cooling >= 1) {
                System.out.println("Ошибка: коэффициент охлаждения должен быть в интервале (0, 1)!");
                return;
            }

            // Запускаем алгоритм
            double result = saSquare(temp, cooling);

            // Выводим результаты
            System.out.println("\n--- Результаты ---");
            System.out.printf("Найденное значение x: %.6f\n", result);
            System.out.printf("Значение функции f(x) = x²: %.6f\n", result * result);

        } catch (Exception e) {
            System.out.println("Ошибка ввода: пожалуйста, введите числовые значения.");
        } finally {
            scanner.close();
        }
    }
}

Введите начальную температуру (temp > 0): 100
Введите коэффициент охлаждения (0 < cooling < 1): 0.98

--- Результаты ---
Найденное значение x: -0.071668
Значение функции f(x) = x²: 0.005136
