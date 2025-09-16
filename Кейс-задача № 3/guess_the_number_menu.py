import random
import json
import time
import os

STATS_FILE = "game_stats.json"

levels = {
    '1': {'name': 'Лёгкий', 'min': 1, 'max': 50, 'attempts': 10},
    '2': {'name': 'Средний', 'min': 1, 'max': 100, 'attempts': 10},
    '3': {'name': 'Сложный', 'min': 1, 'max': 1000, 'attempts': 15}
}

def save_stats(stats):
    try:
        with open(STATS_FILE, "a", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False)
            f.write("\n")
    except Exception as e:
        print(f"Ошибка сохранения статистики: {e}")

def load_stats():
    if not os.path.exists(STATS_FILE):
        print("Статистика игр отсутствует.")
        return
    print("\n📊 Статистика прошлых игр:")
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            try:
                record = json.loads(line)
                status = "Угадал" if record["успех"] else "Не угадал"
                print(f"- Уровень: {record['уровень']}, Результат: {status}, "
                      f"Попыток: {record['попыток']}, Время: {record['время_сек']} сек.")
            except json.JSONDecodeError:
                continue
    print()

def instructions():
    print("""
📝 Инструкции игры «Угадай число»:
- Выберите уровень сложности.
- Компьютер загадает число из диапазона.
- Ваша задача — угадать число за ограниченное количество попыток.
- После каждой попытки вы получите подсказку: число больше или меньше загаданного.
- После 5 попыток будет дана подсказка с диапазоном.
- Введите 'выход' для выхода из игры в любой момент.
""")

def get_valid_input(prompt, min_val, max_val):
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() in ['выход', 'exit']:
            print("Выход из игры...")
            exit()
        if user_input.isdigit():
            num = int(user_input)
            if min_val <= num <= max_val:
                return num
            else:
                print(f"Введите число от {min_val} до {max_val}.")
        else:
            print("Пожалуйста, введите целое число.")

def play_game():
    print("\nВыберите уровень сложности:")
    for k, v in levels.items():
        print(f"{k} - {v['name']} (от {v['min']} до {v['max']}, попыток: {v['attempts']})")
    level_choice = input("Введите номер уровня: ").strip()
    while level_choice not in levels:
        level_choice = input("Неверный выбор. Введите 1, 2 или 3: ").strip()
    level = levels[level_choice]
    target = random.randint(level['min'], level['max'])
    attempts = 0
    guessed = False
    start_time = time.time()
    print(f"\nЯ загадал число от {level['min']} до {level['max']}. Попробуйте угадать!")

    while attempts < level['attempts']:
        guess = get_valid_input(f"Попытка {attempts + 1}: ", level['min'], level['max'])
        attempts += 1
        if guess == target:
            guessed = True
            print("Поздравляю! Вы угадали число!")
            break
        elif guess < target:
            print("Слишком маленькое.")
        else:
            print("Слишком большое.")
        if attempts == 5 and not guessed:
            hint_range = 10 if level['max'] <= 100 else 50
            low = max(target - hint_range, level['min'])
            high = min(target + hint_range, level['max'])
            print(f"Подсказка: число в диапазоне {low} - {high}")

    if not guessed:
        print(f"Вы проиграли! Загаданное число было: {target}")
    duration = round(time.time() - start_time, 2)
    stats = {"уровень": level['name'], "успех": guessed, "попыток": attempts, "время_сек": duration}
    save_stats(stats)

def main_menu():
    while True:
        print("""
==== Главное меню ====
1. Начать игру
2. Инструкции
3. Статистика
4. Выход
""")
        choice = input("Выберите действие (1-4): ").strip()
        if choice == '1':
            play_game()
        elif choice == '2':
            instructions()
        elif choice == '3':
            load_stats()
        elif choice == '4':
            print("Спасибо за игру! Пока!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()
