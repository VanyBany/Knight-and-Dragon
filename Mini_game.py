import random
import time


class Character:
    """Базовый класс для всех персонажей"""
    # Имя, здоровье, сила атаки, класс брони
    def __init__(self, name, health, attack_power, armor_class=10):
        self._name = name
        self._health = health
        self._max_health = health
        self._attack_power = attack_power
        self._critical = False
        self._is_alive = True
        self._armor_class = armor_class

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @property
    def is_alive(self):
        return self._is_alive

    def take_damage(self, damage):
        """Получение урона"""

        self._health -= damage

        if self._health <= 0:
            self._health = 0
            self._is_alive = False



    def heal(self,hp):
        """Лечение"""
        self._health = min(self._health + hp, self._max_health)


    def attack(self):
        """Базовая атака"""
        if self._critical:
            print("Критический удар!")
            self._critical = False
            return self._attack_power * 2
        return self._attack_power

    # Бросок на попадание по цели
    def attack_roll(self):
        return 20

    def hit(self,attack_roll):
        critical = attack_roll == 20
        self._critical = critical
        return attack_roll >= self._armor_class

    def __str__(self):
        return f"{self._name} (Здоровье: {self._health})(Класс брони: {self._armor_class})"


class Knight(Character):
    """Класс Рыцаря с особыми способностями"""

    def __init__(self, name):
        super().__init__(name, 100, 15,15 )
        self.heal_potions = 3
        self._shield_activated = False
        self._special_attack_available = True

    def shield_block(self):
        """Активация щита для снижения урона"""
        self._shield_activated = True
        return "🛡️ Рыцарь поднимает щит! Следующая атака будет ослаблена."

    def special_attack(self):
        """Особая атака рыцаря"""
        if self._special_attack_available:
            self._special_attack_available = False
            damage = self.attack() * 2
            message = ""
            return damage, message
        else:
            message = "Особая атака уже была использована!"
            return self.attack(), message

    def take_damage(self, damage):
        """Переопределение получения урона с учетом щита"""
        if self._shield_activated:
            damage = max(1, damage // 2)  # Щит уменьшает урон вдвое
            self._shield_activated = False

        super().take_damage(damage)
        return damage

    def heal(self):
        """Лечение"""
        if self.heal_potions > 0:
            self.heal_potions-=1
            super().heal(30)
            return True
        else:
            print("Зелий здоровья больше не осталось.")
            return False

class Dragon(Character):
    """Класс Дракона с особыми способностями"""

    def __init__(self, name):
        super().__init__(name, 150, 20,14)
        self._fly_used = False

    def fire_breath(self):
        """Огненное дыхание дракона"""

        damage = random.randint(15, 30)
        if self._critical:
            self._critical = False
            print("Критический удар!")
            damage *= 2
        return damage

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
        self.knight = None
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

        print(f"РЫЦАРЬ: {self.knight}(Кол-во зелий лечения: {self.knight.heal_potions})")
        print(f"ДРАКОН: {self.dragon}")
        self.print_separator()

    def knight_turn(self):
        """Ход рыцаря"""
        action = True
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
            attack_roll = self.knight.attack_roll()
            check_hit = self.knight.hit(attack_roll)

            if check_hit:
                damage = self.knight.attack()
                actual_damage = self.dragon.take_damage(damage)
                self.slow_print(f"⚔️ Вы атакуете дракона и наносите {actual_damage} урона!")

            else:
                self.slow_print(f"Атака не увенчалась успехом и не пробила цель. {attack_roll} vs {self.dragon._armor_class}")


        elif choice == 2:
            message = self.knight.shield_block()
            self.slow_print(message)

        elif choice == 3:
            attack_roll = self.knight.attack_roll()
            check_hit = self.knight.hit(attack_roll)
            if check_hit:
                self.slow_print("⚔️ Рыцарь использует особую атаку! Усиленный удар!")
                damage, message = self.knight.special_attack()
                actual_damage = self.dragon.take_damage(damage)
                self.slow_print(f"{message} Вы атакуете дракона и наносите {actual_damage} урона!")


            else:
                self.slow_print(f"Атака не увенчалась успехом и не пробила цель. {attack_roll} vs {self.dragon._armor_class}")





        elif choice == 4:
            if self.knight.heal():
                self.slow_print("❤️ Вы выпили зелье здоровья! +30 HP")
            else:
                action = False
        return action



    def dragon_turn(self):
        """Ход дракона"""
        self.slow_print("\n🐉 Ход дракона...")
        time.sleep(1)

        # ИИ дракона
        if self.dragon.health < 50 and not hasattr(self.dragon, '_fly_used'):
            # Дракон пытается улететь при низком здоровье
            success, message = self.dragon.fly()
            self.slow_print(message)

            if success:
                self.dragon._dodging = True
                return

        attack_roll = self.dragon.attack_roll()
        check_hit = self.dragon.hit(attack_roll)

        if check_hit:

            if random.random() < 0.4:  # 40% шанс на огненное дыхание
                message = "🔥 Дракон использует огненное дыхание!"
                self.slow_print(message)
                damage= self.dragon.fire_breath()


            else:
                message = "🐉 Дракон атакует когтями!"
                self.slow_print(message)
                damage = self.dragon.attack()



            actual_damage = self.knight.take_damage(damage)
            self.slow_print(f"Дракон наносит вам {actual_damage} урона!")


        else:
            self.slow_print(f"Атака не увенчалась успехом и не пробила цель. {attack_roll} vs {self.knight._armor_class}")







    def check_game_end(self):
        """Проверка условий окончания игры"""
        if not self.knight.is_alive:
            self.game_over = True
            ending = self.get_ending("heroic_death")
            self.show_ending(ending)
            return True

        if not self.dragon.is_alive:
            self.game_over = True
            ending = self.get_ending("victory")
            self.show_ending(ending)
            return True

        # Проверка на особые концовки
        if self.knight.health > 80 and not self.dragon.is_alive:
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
                "text": f"После ожесточенной битвы, {self.knight.name} побеждает ужасного дракона! \n"
                        "Королевство спасено, и ваше имя войдет в легенды!"
            },
            "heroic_death": {
                "title": "💀 ГЕРОИЧЕСКАЯ ГИБЕЛЬ",
                "text": f"Отважный рыцарь {self.knight.name} пал в битве с драконом. \n"
                        "Хотя вы и проиграли, ваша храбрость будет воспета в песнях!"
            },
            "flawless_victory": {
                "title": "⭐ БЕЗУПРЕЧНАЯ ПОБЕДА!",
                "text": f"С невероятным мастерством {self.knight.name} побеждает дракона \n"
                        "практически не получив повреждений! Вы - настоящий герой!"
            },
            "peace": {
                "title": "🕊️ МИРНОЕ СОГЛАШЕНИЕ",
                "text": "В разгар битвы происходит неожиданное - дракон предлагает мир! \n"
                        "Оказывается, он защищал свои яйца. Вы находите взаимопонимание \n"
                        "и становитесь защитниками королевства вместе!"
            }
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
        self.slow_print("Вы - отважный рыцарь, посланный чтобы остановить его!")
        self.print_separator()

    def start_game(self):
        """Запуск игры"""
        self.show_intro()

        # Создание персонажей
        knight_name = input("Введите имя вашего рыцаря: ") or "Сэр Ланселот"
        self.knight = Knight(knight_name)
        self.dragon = Dragon("Смауг")

        self.slow_print(f"\nОтважный {self.knight.name} выступает против дракона {self.dragon.name}!")

        # Основной игровой цикл
        turn = 1
        while not self.game_over:
            print(f"\n🌀 Ход {turn}")
            self.show_status()

            # Ход рыцаря
            action = self.knight_turn()
            while not action:
                print("Действие не сработало, выберите снова!")
                action = self.knight_turn()
            if self.check_game_end():
                break

            # Ход дракона
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

        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower().strip()
        if play_again in ['да', 'д', 'yes', 'y']:
            self.__init__()  # Сброс игры
            self.start_game()
        else:
            self.slow_print("Спасибо за игру! До свидания!")


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.start_game()


