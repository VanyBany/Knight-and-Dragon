import random
import time


class Character:
    """Базовый класс для всех персонажей"""
    # Имя, здоровье, сила атаки, класс брони

    def __init__(self, name, health, attack_power, class_name, armor_class=10):
        self._name = name
        self._health = health
        self._max_health = health
        self._attack_power = attack_power
        self._critical = False
        self._is_alive = True
        self._armor_class = armor_class
        self._status_effects = {}
        self._class_name = class_name

    @property
    def class_name(self):
        return self._class_name

    @property
    def name(self):
        return self._name

    @property
    def access_status_effects(self):
        return self._status_effects

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def max_health(self):
        return self._max_health

    @property
    def is_alive(self):
        return self._is_alive

    @property
    def armor_class(self):
        return self._armor_class

    @staticmethod
    def add_status_effect(target, status):
        target_effects = target.access_status_effects
        target_effects[status] = 3

    def poison_status(self):
        if self._status_effects.get("Отравление", 0) > 0:
            self._status_effects["Отравление"] -= 1
            self.health -= 10
            print(f"{self.class_name} получает урон ядом!")

    def take_damage(self, damage):
        """Получение урона"""

        self._health -= damage

        if self._health <= 0:
            self._health = 0
            self._is_alive = False
        return damage

    def heal(self, hp):
        """Лечение"""
        current_hp = self._health
        self._health = min(self._health + hp, self._max_health)
        return self._health - current_hp

    def is_critical(self):
        """Проверка на крит.урон"""
        if self._critical:
            self._critical = False
            return True
        return False

    def attack_power(self):
        """Получение значения базовой атаки с учётом крит.урона"""
        if self.is_critical():
            return self._attack_power * 2, "Критический удар!"
        return self._attack_power, ""

    def attack(self, target):
        """Урон по цели с получением информации об ударе"""
        damage, check_crit = self.attack_power()
        damage = target.take_damage(damage)
        attack_info = {"Damage": damage, "Crit_damage": check_crit}
        return attack_info

    # Бросок на попадание по цели

    @staticmethod
    def attack_roll():
        """Вычисление вероятности попадания"""
        return random.randint(1, 20)

    def hit(self, target):
        """Проверка на попадание по цели"""
        attack_roll = self.attack_roll()
        if attack_roll == 20:
            self._critical = True
            return True, attack_roll
        if attack_roll == 1:
            return False, attack_roll
        else:
            return attack_roll >= target.armor_class, attack_roll

    def __str__(self):

        return f"{self.name} (Здоровье: {self.health} / {self.max_health}) (Класс брони: {self.armor_class})"


class Knight(Character):
    """Класс Рыцаря с особыми способностями"""

    def __init__(self, name):
        super().__init__(name, 130, 20, "Рыцарь", 12)
        self._heal_potions = 3
        self._shield_activated = False
        self._special_attack_available = True

    def shield_block(self):
        """Активация щита для снижения урона"""
        self._shield_activated = True
        return "🛡️ Рыцарь поднимает щит! Следующая атака будет ослаблена."

    def special_attack(self, target):
        """Особая атака рыцаря"""
        damage, check_crit = self.attack_power()
        if self._special_attack_available:
            self._special_attack_available = False
            damage *= 2
            message = ""
        else:
            message = "Особая атака уже была использована!"

        damage = target.take_damage(damage)
        attack_info = {"Damage": damage, "Crit_damage": check_crit}
        return attack_info, message

    def take_damage(self, damage):
        """Переопределение получения урона с учетом щита"""
        if self._shield_activated:
            damage = max(1, damage // 2)  # Щит уменьшает урон вдвое
            self._shield_activated = False

        damage = super().take_damage(damage)
        return damage

    def heal_potion(self):
        """Лечение"""
        if self._heal_potions > 0:
            self._heal_potions -= 1
            hp_recovered = super().heal(30)
            return True, hp_recovered
        else:
            print("Зелий здоровья больше не осталось.")
            return False, 0

    def __str__(self):
        return f"{super().__str__()} (Кол-во зелий здоровья: {self._heal_potions}) (Специальная атака: {"есть" if self._special_attack_available else "нет"})"


class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, 110, 25, "Плут", 11)
        self._heal_potions = 3
        self._special_attack_available = True

    def special_attack(self, target):
        """Особая атака рыцаря"""
        damage, check_crit = self.attack_power()
        if self._special_attack_available:
            self._special_attack_available = False

            message = ""
        else:
            message = "Особая атака уже была использована!"

        target.add_status_effect(target, "Отравление")
        damage = target.take_damage(damage)
        attack_info = {"Damage": damage, "Crit_damage": check_crit}
        return attack_info, message

    def hit(self, target):
        """Проверка на попадание по цели c шансом на уменьшение попадания по плуту"""

        attack_roll = self.attack_roll()
        if attack_roll == 20:
            self._critical = True
            return True, attack_roll
        elif attack_roll == 1:
            return False, attack_roll
        else:
            dodge_ability, message = (
                2, "Плут активно уворачивается!") if random.random() > 0.5 else (0, "")
            print(message)
            return attack_roll - dodge_ability >= target.armor_class, attack_roll - dodge_ability

    def heal_potion(self):
        """Лечение"""
        if self._heal_potions > 0:
            self._heal_potions -= 1
            hp_recovered = super().heal(30)
            return True, hp_recovered
        else:
            print("Зелий здоровья больше не осталось.")
            return False, 0

    def __str__(self):
        return f"{super().__str__()} (Кол-во зелий здоровья: {self._heal_potions}) (Специальная атака: {"есть" if self._special_attack_available else "нет"})"


class Dragon(Character):
    """Класс Дракона с особыми способностями"""

    def __init__(self, name):
        super().__init__(name, 200, 35, "Дракон", 14)
        self._fly_used = False

    def fire_breath(self, target):
        """Огненное дыхание дракона"""
        damage = random.randint(15, 40)
        check_crit = ""

        if self.is_critical():
            check_crit = "Критический удар!"
            damage *= 2

        damage = target.take_damage(damage)
        attack_info = {"Damage": damage, "Crit_damage": check_crit}
        return attack_info

    def fly(self):
        """Дракон взлетает, уклоняясь от атаки"""
        if not self._fly_used:
            self._fly_used = True
            return True, "🐉 Дракон взлетает в воздух! Следующая атака промахнется!"
        return False, "Дракон уже использовал полет!"

    def take_damage(self, damage):
        """Переопределение с учетом полета"""
        if hasattr(self, '_dodging') and self._dodging:
            self._dodging = False
            return 0  # Уклонение от атаки

        super().take_damage(damage)
        return damage


class Game:
    """Основной класс игры"""

    def __init__(self):
        self.character = None
        self.dragon = None
        self.game_over = False
        self.endings_unlocked = []

    def print_separator(self):
        print("\n" + "=" * 50)

    def slow_print(self, text, delay=0.03):
        """Медленный вывод текста для драматического эффекта"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def show_status(self):
        """Показать статус персонажей"""
        self.print_separator()

        print(f"{self.character.class_name}: {self.character}")
        print(f"{self.dragon.class_name}: {self.dragon}")
        self.print_separator()

    def character_turn(self):
        # Имя класса персонажа
        class_character = type(self.character).__name__
        action = True
        # Выбор интерфейса
        if class_character == "Knight":
            action = self.knight_turn()

        elif class_character == "Rogue":
            action = self.rogue_turn()

        return action

    def knight_turn(self):
        """Ход рыцаря"""

        self.slow_print("\n🎯 Ваш ход! Выберите действие:")
        print("1. ⚔️  Атака мечом")
        print("2. 🛡️  Защита щитом")
        print("3. 💥 Особая атака")
        print("4. ❤️  Выпить зелье здоровья (+30 HP)")

        while True:
            try:
                choice = int(input("Ваш выбор (1-4): "))
                if 1 <= choice <= 4:
                    break
                else:
                    print("Пожалуйста, выберите число от 1 до 4")
            except ValueError:
                print("Пожалуйста, введите число")

        if choice == 1:
            self.slow_print("Рыцарь использует атаку мечом!")

            check_hit, attack_roll = self.dragon.hit(self.dragon)

            if check_hit:
                attack_result = self.character.attack(self.dragon)
                self.slow_print(
                    f"⚔️ {attack_result["Crit_damage"]} Вы атакуете дракона и наносите {attack_result["Damage"]} урона!")

            else:
                self.slow_print(
                    f"Атака не увенчалась успехом и не пробила цель. {attack_roll} vs {self.dragon.armor_class}")

        elif choice == 2:
            message = self.character.shield_block()
            self.slow_print(message)

        elif choice == 3:

            check_hit, attack_roll = self.character.hit(self.dragon)

            if check_hit:
                self.slow_print(
                    "⚔️ Рыцарь использует особую атаку! Усиленный удар!")
                attack_result, message = self.character.special_attack(self.dragon)

                self.slow_print(
                    f"{message} {attack_result["Crit_damage"]}Вы атакуете дракона и наносите {attack_result["Damage"]} урона!")

            else:
                self.slow_print(
                    f"Атака не увенчалась успехом и не пробила цель. {attack_roll} vs {self.dragon.armor_class}")

        elif choice == 4:
            condition, hp_recovered = self.character.heal_potion()
            if condition:
                self.slow_print(
                    f"❤️ Вы выпили зелье здоровья! Вы восстановили {hp_recovered} хп!")
            else:
                return False
        return True

    def rogue_turn(self):
        """Ход плута"""

        self.slow_print("\n🎯 Ваш ход! Выберите действие:")
        self.dragon.poison_status()
        print("1. ⚔️  Атака кинжалом")
        print("2. 💥 Особая атака")
        print("3. ❤️  Выпить зелье здоровья (+30 HP)")

        while True:
            try:
                choice = int(input("Ваш выбор (1-3): "))
                if 1 <= choice <= 3:
                    break
                else:
                    print("Пожалуйста, выберите число от 1 до 4")
            except ValueError:
                print("Пожалуйста, введите число")

        if choice == 1:
            self.slow_print("Плут использует атаку кинжалом!")
            check_hit, attack_roll = self.dragon.hit(self.dragon)

            if check_hit:
                attack_result = self.character.attack(self.dragon)
                self.slow_print(
                    f"⚔️ {attack_result["Crit_damage"]} Вы атакуете дракона и наносите {attack_result["Damage"]} урона!")

            else:
                self.slow_print(
                    f"Атака не увенчалась успехом и не пробила цель. {attack_roll} vs {self.dragon.armor_class}")

        elif choice == 2:

            check_hit, attack_roll = self.dragon.hit(self.dragon)

            if check_hit:
                self.slow_print(
                    "⚔️ Плут использует особую атаку! Ядовитый выпад!")
                attack_result, message = self.character.special_attack(
                    self.dragon)
                self.slow_print(
                    f"{message} {attack_result["Crit_damage"]}Вы атакуете дракона и наносите {attack_result["Damage"]} урона!")

            else:
                self.slow_print(
                    f"Атака не увенчалась успехом и не пробила цель. {attack_roll} vs {self.dragon.armor_class}")

        elif choice == 3:
            condition, hp_recovered = self.character.heal_potion()
            if condition:
                self.slow_print(
                    f"❤️ Вы выпили зелье здоровья! Вы восстановили {hp_recovered} хп!")
            else:
                return False
        return True

    def dragon_turn(self):
        """Ход дракона"""
        self.slow_print("\n🐉 Ход дракона...")
        time.sleep(1)
        self.dragon.poison_status()

        # ИИ дракона
        if self.dragon.health < 50 and not hasattr(self.dragon, '_fly_used'):
            # Дракон пытается улететь при низком здоровье
            success, message = self.dragon.fly()
            self.slow_print(message)

            if success:
                self.dragon._dodging = True
                return

        check_hit, attack_roll = self.character.hit(self.character)

        if check_hit:

            if random.random() < 0.4:  # 40% шанс на огненное дыхание
                message = "🔥 Дракон использует огненное дыхание!"
                self.slow_print(message)
                attack_result = self.dragon.fire_breath(self.character)

            else:
                message = "🐉 Дракон атакует когтями!"
                self.slow_print(message)
                attack_result = self.dragon.attack(self.character)

            self.slow_print(
                f"{attack_result["Crit_damage"]} Дракон наносит вам {attack_result["Damage"]} урона!")

        else:
            self.slow_print(
                f"Атака не увенчалась успехом и не пробила цель. {attack_roll} vs {self.character.armor_class}")

    def check_game_end(self):
        """Проверка условий окончания игры"""
        if not self.character.is_alive:
            self.game_over = True
            if isinstance(self.character, Knight):
                ending = self.get_ending("heroic_knight_death")
                self.show_ending(ending)
            elif isinstance(self.character, Rogue):
                ending = self.get_ending("tragic_rogue_death")
                self.show_ending(ending)
            return True

        if not self.dragon.is_alive:
            self.game_over = True
            ending = self.get_ending("victory")
            self.show_ending(ending)
            return True

        # Проверка на особые концовки
        if self.character.health > 80 and not self.dragon.is_alive:
            self.game_over = True
            ending = self.get_ending("flawless_victory")
            self.show_ending(ending)
            return True

        # if random.random() < 0.1 and not self.game_over:  # 10% шанс на мирную концовку
        #     self.game_over = True
        #     ending = self.get_ending("peace")
        #     self.show_ending(ending)
        #     return True

        return False

    def get_ending(self, ending_type):
        """Получить текст концовки"""
        endings = {
            "victory": {
                "title": "🏆 ПОБЕДА!",
                "text": f"После ожесточенной битвы, {self.character.name} побеждает ужасного дракона! \n"
                "Королевство спасено, и ваше имя войдет в легенды!"
            },
            "heroic_knight_death": {
                "title": "💀 ГЕРОИЧЕСКАЯ ГИБЕЛЬ",
                "text": f"Отважный {self.character.class_name.lower()} {self.character.name} пал в битве с драконом. \n"
                "Хотя вы и проиграли, ваша храбрость будет воспета в песнях!"
            },

            "tragic_rogue_death": {
                "title": "💀 ТРАГИЧЕСКАЯ ГИБЕЛЬ",
                "text": f"Проворный {self.character.class_name.lower()} {self.character.name} был раздавлен драконом, пока подбирался к нему. \n"
                "Хотя вы и проиграли, ваша проворность будет воспета в песнях!"

            },
            "flawless_victory": {
                "title": "⭐ БЕЗУПРЕЧНАЯ ПОБЕДА!",
                "text": f"С невероятным мастерством {self.character.name} побеждает дракона \n"
                "практически не получив повреждений! Вы - настоящий герой!"
            },
        }
        return endings.get(ending_type, endings["victory"])

    def show_ending(self, ending):
        """Показать концовку игры"""
        self.print_separator()
        self.slow_print(ending["title"])
        self.print_separator()
        self.slow_print(ending["text"])
        self.print_separator()

        if ending["title"] not in self.endings_unlocked:
            self.endings_unlocked.append(ending["title"])

    def show_intro(self):
        """Показать вступление"""
        self.slow_print("🐉 ДРАКОН ПРОТИВ РЫЦАРЯ 🛡️")
        self.print_separator()
        self.slow_print("Давным-давно, в далеком королевстве...")
        self.slow_print("Ужасный дракон терроризирует мирных жителей.")
        self.slow_print("Вы - истинный герой, посланный чтобы остановить его!")
        self.print_separator()

    def start_game(self):
        """Запуск игры"""
        self.show_intro()

        # Создание персонажей
        self.slow_print("Выбери класс персонажа, чтобы противостоять дракону!")

        print("1. ⚔️  Бравый рыцарь")
        print("2. 🗡️  Проворный плут")

        while True:
            try:
                choice = int(input("Ваш выбор (1-2): "))
                if 1 <= choice <= 2:
                    break
                else:
                    print("Пожалуйста, выберите число от 1 до 2")
            except ValueError:
                print("Пожалуйста, введите число")

        self.dragon = Dragon("Смауг")

        if choice == 1:
            knight_name = input(
                "Введите имя вашего рыцаря: ") or "Сэр Ланселот"
            self.character = Knight(knight_name)
            self.slow_print(
                f"\nОтважный {self.character.name} выступает против дракона {self.dragon.name}!")

        if choice == 2:
            rogue_name = input("Введите имя вашего плута: ") or "Эцио Аудиторе"
            self.character = Rogue(rogue_name)
            self.slow_print(
                f"\nПроворный {self.character.name} выступает против дракона {self.dragon.name}!")

        # Основной игровой цикл
        turn = 1
        while not self.game_over:
            print(f"\n🌀 Ход {turn}")
            self.show_status()

            # Ход героя
            # Проверка на наличие статус эффектов

            action = self.character_turn()
            while not action:
                print("Действие не сработало, выберите снова!")
                action = self.character_turn()
            if self.check_game_end():
                break

            # Ход дракона
            # Проверка на наличие статус эффектов

            self.dragon_turn()
            if self.check_game_end():
                break

            turn += 1

        # Статистика игры
        self.show_statistics()

    def show_statistics(self):
        """Показать статистику игры"""
        self.print_separator()
        self.slow_print("📊 СТАТИСТИКА ИГРЫ:")
        print(f"Открыто концовок: {len(self.endings_unlocked)}/4")
        if self.endings_unlocked:
            print("Ваши концовки:")
            for ending in self.endings_unlocked:
                print(f"  - {ending}")

        play_again = input(
            "\nХотите сыграть еще раз? (да/нет): ").lower().strip()
        if play_again in ['да', 'д', 'yes', 'y']:
            self.__init__()  # Сброс игры
            self.start_game()
        else:
            self.slow_print("Спасибо за игру! До свидания!")


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.start_game()
