import os  # Імпортуємо модуль os для роботи з файловою системою та шляхами.
baseDir = os.path.dirname(__file__)
import random  # Імпортуємо модуль random для генерації випадкових чисел, наприклад, для позицій спрайтів.
import time  # Імпортуємо модуль time для управління часом, наприклад, для паузи після завершення гри.
# Імпортуємо бібліотеку Pygame, що необхідна для роботи зі спрайтами та іншими графічними елементами
import pygame
enemy_bullets_sprite = pygame.sprite.Group()
pygame.init()  # Ініціалізуємо всі підсистеми Pygame, включаючи графіку, звук та інші функціональні можливості.

all_sprites = pygame.sprite.Group()
player_bullets_sprite = pygame.sprite.Group()



# Створюємо клас GameSprite, який наслідує pygame.sprite.Sprite, що дозволяє легко керувати спрайтами
class GameSprite(pygame.sprite.Sprite):
    # Метод ініціалізації (конструктор), що викликається при створенні об'єкта цього класу
    def __init__(self, x, y, image, width, height, speed, groups=[]):
        # Викликаємо конструктор батьківського класу Sprite, передаючи йому групи, в які має входити цей спрайт
        # Використовуємо розпакування (*groups), щоб передати всі групи окремим аргументами
        super().__init__(*groups)
        # Завантажуємо оригінальне зображення з файлу за вказаним шляхом і зберігаємо його
        # Завантаження зображення здійснюється за допомогою pygame.image.load
        self.original_image = pygame.image.load(image)
        # Масштабуємо оригінальне зображення до заданих ширини та висоти
        # Використовуємо pygame.transform.scale для зміни розмірів зображення
        self.image = pygame.transform.scale(self.original_image, (width, height))
        # Отримуємо прямокутник (rect) із зображення, який визначає його позицію та розмір
        # Встановлюємо початкову позицію верхнього лівого кута за координатами (x, y)
        self.rect = self.image.get_rect(topleft=(x, y))
        # Створюємо маску для зображення, яка дозволяє точно виявляти зіткнення
        # Маска створюється на основі непрозорих пікселів зображення
        self.mask = pygame.mask.from_surface(self.image)
        # Зберігаємо швидкість спрайта, що може використовуватись для його руху
        self.speed = speed


def draw(self, surface):
    # Малює червоний прямокутник, що відображає межі спрайта (сам по собі спрайт не видно, тільки його рамку)
    # surface - об'єкт поверхні, на якому виконується малювання (екран гри)
    # self.rect - прямокутник, що визначає положення і розмір спрайта
    pygame.draw.rect(surface, (255, 0, 0), self.rect)

    # Малює зелене коло з центром у центрі спрайта та радіусом, що дорівнює його ширині
    # surface - об'єкт поверхні, на якому виконується малювання (екран гри)
    # self.rect.center - координати центру спрайта
    # self.rect.width - ширина спрайта (використовується як радіус кола)
    pygame.draw.circle(surface, (0, 255, 0), self.rect.center, self.rect.width)

    # Створює нову поверхню для відображення маски спрайта
    # Розмір поверхні такий самий, як розмір маски
    mask_surface = pygame.Surface(self.mask.get_size())

    # Заповнює нову поверхню чорним кольором (колір фону)
    mask_surface.fill((0, 0, 0))

    # Два вкладених цикли проходять по всіх пікселях маски
    # self.mask.get_size()[0] - ширина маски
    # self.mask.get_size()[1] - висота маски
    for x in range(self.mask.get_size()[0]):
        for y in range(self.mask.get_size()[1]):
            # Перевіряє, чи піксель маски є непрозорим
            # Якщо так, то малює білий піксель на відповідному місці на масці
            if self.mask.get_at((x, y)):
                mask_surface.set_at((x, y), (255, 255, 255))

    # Відображає поверхню маски на екрані в позиції, що визначається rect спрайта
    surface.blit(mask_surface, self.rect)

    # Відображає на екрані зображення спрайта в позиції, що визначається rect спрайта
    # Це основна команда, яка малює спрайт на екрані гри
    surface.blit(self.image, self.rect)


# Створюємо клас Player, який наслідує GameSprite, що дозволяє легко керувати спрайтами.
# Клас Player успадковує GameSprite і додає поведінку для управління гравцем.
class Player(GameSprite):
    # Ініціалізуємо екземпляр класу Player. Викликаємо конструктор базового класу GameSprite,
    # передаючи йому позицію (x, y), зображення (image), розмір (width, height),
    # швидкість (speed) і групи (groups), до яких цей спрайт буде додано.
    # Це дозволяє Player успадковувати всі властивості і методи GameSprite.
    def __init__(self, x, y, image, width, height, speed, groups=[]):
        super().__init__(x, y, image, width, height, speed, groups)
        
        # Параметри здоров'я
        self.MAX_HEALTH = 5
        self.current_health = self.MAX_HEALTH
        self.health_bar_length = self.rect.width  # Довжина шкали здоров'я в пікселях
        self.health_bar_height = 10  # Висота шкали здоров'я в пікселях
        
        # Перезарядки
        self.shots_fired = 0
        self.max_shots_fired = 5
        self.reload_time = 3
        self.start_reload_time = 0
        self.isReloading = False
        

    # Метод оновлення стану гравця, який викликається кожен кадр.
    # Він перевіряє, які клавіші натиснуті, і на основі цього переміщує гравця по екрану.
    
    def update(self):
        # Отримуємо стан всіх клавіш на клавіатурі у вигляді списку булевих значень.
        # Якщо клавіша натиснута, то відповідний елемент у списку буде True.
        keys = pygame.key.get_pressed()

        # Якщо натиснуто клавішу "A" (зліва) і гравець не виходить за межі екрану зліва (self.rect.x > 0),
        # то зменшуємо координату X прямокутника спрайта (self.rect.x) на швидкість (self.speed),
        # що рухає гравця вліво.
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

        # Якщо натиснуто клавішу "D" (праворуч) і гравець не виходить за межі екрану справа (self.rect.right < window.get_width()),
        # то збільшуємо координату X прямокутника спрайта (self.rect.x) на швидкість (self.speed),
        # що рухає гравця вправо.
        if keys[pygame.K_d] and self.rect.right < window.get_width():
            self.rect.x += self.speed

        self.reload_shots()

# Метод fire відповідає за стрільбу гравця.

def fire(self):
    # Створюємо новий об'єкт Bullet. Він буде з'являтися на екрані в точці (centerx, y) гравця,
    # має свій спрайт, розміри, швидкість, напрямок руху ("up") та групи, до яких його буде додано.
    baseDir = os.path.dirname(os.path.abspath(__file__))
    bullet = Bullet(self.rect.centerx,
                    self.rect.y,
                    os.path.join(baseDir, "assets/img/bullet.png"),
                    15,
                    20,
                    5,
                    "up",
                    [all_sprites, player_bullets_sprite]
                )


def draw_health_bar(self, surface):
    # Обчислюємо, яка частка здоров'я залишилася в порівнянні з максимальним здоров'ям
    health_ratio = self.current_health / self.MAX_HEALTH

    # Визначаємо ширину зеленої частини шкали здоров'я на основі поточного здоров'я
    green_bar_width = int(health_ratio * self.health_bar_length)

    # Малюємо червону шкалу (фон) для шкали здоров'я
    # surface – це поверхня, на якій ми малюємо (наприклад, вікно гри)
    # (255, 0, 0) – червоний колір
    # (self.rect.x, self.rect.bottom - 5) – координати верхнього лівого кута червоної шкали
    # self.health_bar_length – довжина шкали здоров'я
    # self.health_bar_height – висота шкали здоров'я
    pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.bottom + 5, self.health_bar_length, self.health_bar_height), 0, 10)

    # Малюємо зелену частину шкали, що показує поточне здоров'я
    # (0, 255, 0) – зелений колір
    pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.bottom + 5, green_bar_width, self.health_bar_height), 0, 10)

    # Створюємо текстову мітку, що показує поточне здоров'я гравця
    # Форматування тексту: "поточне здоров'я / максимальне здоров'я"
    hp_label = Label(f"{self.current_health}/{self.MAX_HEALTH}",
                     (self.rect.centerx, self.rect.bottom + 5 + self.health_bar_height / 2),
                     20,  # Розмір шрифту
                     (0, 0, 0),  # Колір тексту
                     None,  # Не потрібно фонового зображення
                     "center"  # Центруємо текст
                     )

    # Малюємо текстову мітку на поверхні
    hp_label.draw(surface)

pause_duration = 1  # Укажите нужное значение, например, 1 для паузы в 1 секунду

def reload_shots(self):
    current_time = time.time() - pause_duration

    if self.shots_fired >= self.max_shots_fired and not self.isReloading:
        self.isReloading = True
        self.start_reload_time = time.time()

    if current_time - self.start_reload_time >= self.reload_time and self.isReloading:
        self.isReloading = False
        self.shots_fired = 0


# Створено клас Enemy, який наслідує GameSprite.
# Клас Enemy успадковує базові властивості спрайта і додає можливість руху вниз по екрану,
# а також випадковий інтервал стрільби, якщо параметр isShooting дорівнює True.
class Enemy(GameSprite):

    # Ініціалізуємо екземпляр класу Enemy. Викликаємо конструктор базового класу GameSprite
    # і передаємо позицію (x, y), зображення (image), розмір (width, height), швидкість (speed),
    # а також параметр isShooting, що визначає, чи може цей ворог стріляти.
    def __init__(self, x, y, image, width, height, speed, isShooting=False, groups=[]):
        super().__init__(x, y, image, width, height, speed, groups)
        # Встановлюємо значення isShooting. Якщо True, ворог зможе стріляти.
        self.isShooting = isShooting

        # Зберігаємо час, коли ворог з'явився на екрані або перезапускає інтервал стрільби.
        self.start_interval_time = time.time()

        # Поточний час для порівняння з інтервалом між пострілами.
        self.current_time = self.start_interval_time

        # Генеруємо випадковий інтервал (від 1 до 5 секунд) для пострілів, якщо ворог може стріляти.
        self.bullet_spawn_interval = random.uniform(1, 5)

    # Метод оновлення стану ворога, який викликається кожен кадр.
    # Він відповідає за рух ворога вниз по екрану і перевіряє, коли ворог виходить за межі екрану.
    # Якщо ворог може стріляти, перевіряється час між пострілами.
    def update(self):
        global enemy_lost

        # Переміщуємо ворога вниз по екрану на відстань, що дорівнює швидкості (self.speed).
        self.rect.y += self.speed

        # Якщо ворог виходить за межі екрану знизу (self.rect.y > window.get_height()),
        # його видаляємо зі спрайт-групи (kill()) і збільшуємо лічильник втрат ворогів (enemy_lost).
        if self.rect.y > window.get_height():
            self.kill()
            enemy_lost += 1

        # Оновлюємо поточний час для перевірки інтервалу стрільби.
        self.current_time = time.time() + pause_duration

        # Якщо минув випадковий інтервал пострілу і ворог може стріляти (self.isShooting),
        # то ворог робить постріл і генерується новий випадковий інтервал для наступного пострілу.
        if self.current_time - self.start_interval_time >= self.bullet_spawn_interval and self.isShooting:
            # Оновлюємо час початку інтервалу і задаємо новий випадковий інтервал пострілу.
            self.start_interval_time = self.current_time
            self.bullet_spawn_interval = random.uniform(1, 5)

            # Викликаємо метод fire для стрільби.
            self.fire()


# Метод fire відповідає за створення кулі, яка летить вниз з позиції ворога.
def fire(self):
    # Створюємо новий об'єкт Bullet. Він з'являється на екрані в центрі ворога (centerx) і нижче (bottom),
    # має спрайт, розміри, швидкість і напрямок руху ("down"). Куля додається до двох груп:
    # all_sprites і enemy_bullets_sprite, що дозволяє відстежувати кулі ворогів.
    bullet = Bullet(self.rect.centerx,
                    self.rect.bottom,
                    os.path.join(baseDir, "assets/img/bullet.png"),
                    15,
                    20,
                    5,

                    "down",
                    [all_sprites, enemy_bullets_sprite]
                    )
    # Повертаємо зображення кулі на 180 градусів, щоб вона була направлена вниз.
    bullet.image = pygame.transform.rotate(bullet.image, 180)

# Створюємо клас Bullet, який наслідує GameSprite.
# Клас Bullet представляє кулю, яка може рухатися в різних напрямках і видалятися, коли виходить за межі екрану.
class Bullet(GameSprite):

    # Ініціалізуємо екземпляр класу Bullet. Викликаємо конструктор базового класу GameSprite
    # і передаємо позицію (x, y), зображення (image), розмір (width, height), швидкість (speed),
    # напрямок руху (direction) та групи (groups), до яких цей спрайт буде додано.
    def __init__(self, x, y, image, width, height, speed, direction="up", groups=[]):
        super().__init__(x, y, image, width, height, speed, groups)
        # Встановлюємо напрямок руху кулі. За замовчуванням це "up" (вверх).
        self.direction = direction
        # Встановлюємо центр прямокутника кулі (self.rect.center) на позицію (x, y).
        self.rect.center = (x, y)


# Метод оновлення стану кулі, яким викликається кожен кадр.
# Він переміщує кулю в залежності від напрямку і видаляє її, якщо вона виходить за межі екрану.
def update(self):
    # Якщо напрямок руху "up" (вверх), зменшуємо координату y на швидкість (self.speed),
    # що рухає кулю вгору.
    if self.direction == "up":
        self.rect.y -= self.speed

        # Якщо куля виходить за верхню межу екрану (self.rect.bottom <= 0),
        # видаляємо її з гри (kill()).
        if self.rect.bottom <= 0:
            self.kill()

    # Якщо напрямок руху "down" (вниз), збільшуємо координату y на швидкість (self.speed),
    # що рухає кулю вниз.
    elif self.direction == "down":
        self.rect.y += self.speed

        # Якщо куля виходить за нижню межу екрану (self.rect.y >= window.get_height()),
        # видаляємо її з гри (kill()).
        if self.rect.y >= window.get_height():
            self.kill()

    # Якщо напрямок руху "right" (праворуч), збільшуємо координату x на швидкість (self.speed),
    # що рухає кулю вправо.
    elif self.direction == "right":
        self.rect.x += self.speed

        # Якщо куля виходить за праву межу екрану (self.rect.x >= window.get_width()),
        # видаляємо її з гри (kill()).
        if self.rect.x >= window.get_width():
            self.kill()

    # Якщо напрямок руху "left" (ліворуч), зменшуємо координату x на швидкість (self.speed),
    # що рухає кулю вліво.
    elif self.direction == "left":
        self.rect.x -= self.speed

        # Якщо куля виходить за ліву межу екрану (self.rect.right <= 0),
        # видаляємо її з гри (kill()).
        if self.rect.right <= 0:
            self.kill()


# Визначаємо клас Label, який наслідується від pygame.sprite.Sprite
class Label(pygame.sprite.Sprite):
    # Метод ініціалізації, який встановлює властивості мітки
    def __init__(self, text, position, font_size = 30, font_color = (255, 255, 255), font_name = None, alignment = "topleft", groups = []):
        # Викликаємо конструктор батьківського класу Sprite
        super().__init__(*groups)
        # Проводимо ініціалізацію підсистеми шрифтів у pygame
        pygame.font.init()
        # Зберігаємо текст, який буде відображатися міткою
        self.text = text
        # Зберігаємо позицію мітки на екрані
        self.position = position
        # Зберігаємо колір тексту, використовуючи RGB кортеж
        self.font_color = font_color
        # Створюємо об'єкт шрифту з вказаним ім'ям і розміром, використовуючи системний шрифт
        self.font = pygame.font.SysFont(font_name, font_size)
        # Зберігаємо вирівнювання мітки (наприклад, 'topleft', 'center')
        self.alignment = alignment
        # Візуалізуємо текст у зображенні (Surface) з використанням вказаного шрифту та кольору
        self.image = self.font.render(self.text, True, self.font_color)
        # Створюємо прямокутник (Rect), який представлятиме позицію та розмір візуалізованого тексту
        self.rect = self.image.get_rect()
        # Встановлюємо початкову позицію мітки, використовуючи вказане вирівнювання
        self.set_position(self.position)
        

        # Метод для відображення мітки на заданій поверхні (наприклад, екрані)
def draw(self, surface):
    # Відображаємо (blit) візуалізоване зображення тексту на заданій поверхні у позиції мітки
    surface.blit(self.image, self.rect)

# Метод для оновлення тексту мітки
def update_text(self, new_text):
    # Оновлюємо збережений текст на новий
    self.text = new_text
    # Перевізуалізуємо текст із новим значенням
    self.image = self.font.render(str(self.text), True, self.font_color)
    # Оновлюємо прямокутник, щоб він відповідав новому тексту
    self.rect = self.image.get_rect()
    # Заново встановлюємо позицію для правильного вирівнювання нового тексту
    self.set_position(self.position)

# Метод для встановлення позиції мітки на екрані
def set_position(self, new_position):
    # Оновлюємо збережену позицію на нову позицію
    self.position = new_position
    # Встановлюємо атрибут вирівнювання прямокутника на нову позицію
    # setattr(obj, attr_name, value) — це вбудована функція в Python, яка дозволяє змінювати значення атрибуту об'єкта.
    setattr(self.rect, self.alignment, self.position)
    

# Умовні оператори для визначення вирівнювання
# if self.alignment == "topleft":
#     self.rect.topleft = self.position
# elif self.alignment == "topright":
#     self.rect.topright = self.position
# elif self.alignment == "center":
#     self.rect.center = self.position
# elif self.alignment == "midtop":
#     self.rect.midtop = self.position
# elif self.alignment == "midbottom":
#     self.rect.midbottom = self.position
# elif self.alignment == "bottomleft":
#     self.rect.bottomleft = self.position
# elif self.alignment == "bottomright":
#     self.rect.bottomright = self.position
# elif self.alignment == "midleft":
#     self.rect.midleft = self.position
# elif self.alignment == "midright":
#     self.rect.midright = self.position


# Метод для встановлення нового кольору для тексту мітки
def set_color(self, new_color):
    # Оновлюємо збережений колір шрифту на новий колір
    self.font_color = new_color
    # Перевізуалізуємо текст із новим кольором
    self.image = self.font.render(str(self.text), True, self.font_color)
    # Оновлюємо прямокутник, щоб він відповідав новому тексту
    self.rect = self.image.get_rect()
    # Заново встановлюємо позицію для правильного вирівнювання нового кольору тексту
    self.set_position(self.position)

# Метод для встановлення нового шрифту і розміру для тексту мітки
def set_font(self, new_font_name, new_font_size):
    # Створюємо новий об'єкт шрифту з вказаним іменем шрифту та розміром, використовуючи системний шрифт
    self.font = pygame.font.SysFont(new_font_name, new_font_size)
    # Перевізуалізуємо текст із новим шрифтом і розміром
    self.image = self.font.render(str(self.text), True, self.font_color)
    # Оновлюємо прямокутник, щоб він відповідав новому шрифту
    self.rect = self.image.get_rect()
    # Заново встановлюємо позицію для вирівнювання з новим розміром шрифту
    self.set_position(self.position)

# Клас Explosion
class Explosion(pygame.sprite.Sprite):  # Клас Explosion успадковується від базового класу Sprite для роботи зі спрайтами в Pygame
    def __init__(self, center, groups = []):
        # Викликаємо конструктор базового класу Sprite та додаємо спрайт у вказані групи
        super().__init__(*groups)
        imgs_explosion = [pygame.image.load('explosion1.png'), pygame.image.load('explosion2.png'), ...]
        # Завантажуємо колекцію зображень вибуху, які будуть відображатися послідовно, як кадри анімації
        self.images = imgs_explosion
        # Встановлюємо початкове зображення вибуху, яке буде показано спочатку
        self.image = self.images[0]
        # Встановлюємо прямокутник для позиціонування вибуху на екрані, центр якого знаходиться в заданій точці
        self.rect = self.image.get_rect(center=center)
        # Зберігаємо координати центру вибуху для оновлення кадрів
        self.center = center
        # Початковий номер кадру анімації, з якого почнеться показ
        self.frame = 0
        # Вказуємо швидкість анімації — скільки часу має пройти перед зміною кадру (більше число — повільніше)
        self.frame_speed = 5  # Що швидкість може змінювати, щоб вибух був швидшим або повільнішим
        # Лічильник оновлень, який відстежує, коли треба змінювати кадр
        self.frame_counter = 0



def update(self):
    # Збільшуємо лічильник оновлень щоразу, коли спрайт оновлюється
    self.frame_counter += 1

    # Якщо лічильник досяг швидкості анімації, значить пора змінити кадр
    if self.frame_counter >= self.frame_speed:
        # Переходимо до наступного кадру в анімації
        self.frame += 1
        # Скидаємо лічильник оновлень до нуля, щоб почати відлік заново
        self.frame_counter = 0

        # Перевіряємо, чи всі кадри анімації були показані
        if self.frame >= len(self.images):
            # Якщо всі кадри показані, видаляємо спрайт, бо вибух завершився
            self.kill()
        else:
            # Інакше, переходимо до наступного зображення вибуху
            self.image = self.images[self.frame]
            # Оновлюємо прямокутник для правильного позиціонування з новим кадром
            self.rect = self.image.get_rect(center=self.center)

# Створюємо нове вікно гри з розмірами 1000x700 пікселів
window = pygame.display.set_mode((1000, 700))
# Встановлюємо заголовок вікна гри на "Шутер".
pygame.display.set_caption("Шутер")
# Створюємо об'єкт для відстеження часу, що дозволяє контролювати частоту оновлення кадрів.
clock = pygame.time.Clock()




# Базові зміни

# Отримуємо директорію, де знаходиться файл скрипта. Використовується для побудови шляхів до ресурсів.
baseDir = os.path.dirname(os.path.abspath(__file__))

# Встановлюємо частоту кадрів гри (frames per second) на 60. Це визначає, скільки разів на секунду
# гра буде оновлюватися і малювати нові кадри.
FPS = 60

# Ініціалізуємо змінну для зберігання рахунку гри. Початкове значення - 0.
score = 0

# Ініціалізуємо змінну для зберігання кількості втрачених ворогів. Початкове значення - 0.
enemy_lost = 0

# Ініціалізуємо змінну для контролю завершення гри. Початкове значення - False (гра ще не закінчена).
end = False

# Ініціалізуємо змінну для контролю чи гра закінчена. Початкове значення - False.
game_over = False

# Ініціалізуємо змінну для контролю паузи гри. Початкове значення - False (гра не на паузі).
pause = False


# Музика

# Завантажуємо фонову музику для гри з файлу.
background_music = pygame.mixer.Sound(os.path.join(baseDir, "assets/music/space.ogg"))
# Встановлюємо гучність фонової музики. Значення 0.15 означає, що музика буде тихішою.
background_music.set_volume(0.15)
# Відтворюємо фонову музику нескінченно. `-1` означає, що музика буде грати без кінця.
background_music.play(-1)

# Завантажуємо звуковий ефект для стрільби з файлу.
fire_music = pygame.mixer.Sound(os.path.join(baseDir, "assets/music/fire.ogg"))
# Встановлюємо гучність звукового ефекту стрільби. Значення 0.2 означає, що звуковий ефект буде трохи гучнішим.
fire_music.set_volume(0.2)

# Час

start_game = time.time()  # Записуємо час початку гри.
current_time = start_game  # Ініціалізуємо поточний час як час початку гри.
start_pause_time = 0  # Ініціалізуємо змінну для паузи
pause_duration = 0  # Тривалість паузи

start_time_enemy = start_game  # Ініціалізуємо час для початку генерації ворогів.
spawn_enemy_interval = random.uniform(1, 5)  # Генеруємо випадковий інтервал між появами ворогів у секундах.



# Види ворогів
types_of_enemies = {
    0: {  # Тип ворога з ідентифікатором 0
        "image": "assets/img/ufo.png",  # Назва зображення для цього типу ворога.
        "isShooting": True,  # Вказує, чи може цей ворог стріляти.
        "speed_range": (1, 3),  # Діапазон швидкостей для цього типу ворога (мінімальна і максимальна швидкість).
        "size": (80, 50),  # Розмір ворога (ширина, висота).
        "probability": 0.5,  # Імовірність появи цього типу ворога (від 0 до 1).
    },
    1: {  # Тип ворога з ідентифікатором 1
        "image": "assets/img/asteroid.png",  # Назва зображення для цього типу ворога.
        "isShooting": False,  # Вказує, чи може цей ворог стріляти.
        "speed_range": (1, 3),  # Діапазон швидкостей для цього типу ворога (мінімальна і максимальна швидкість).
        "size": (80, 50),  # Розмір ворога (ширина, висота).
        "probability": 0.1,  # Імовірність появи цього типу ворога (від 0 до 1).
    }
}

# Розрахунок імовірностей автоматично
# Отримуємо список всіх ідентифікаторів типів ворогів.
enemy_types = list(types_of_enemies.keys())

# Створюємо список імовірностей появи кожного типу ворога на основі їхніх імовірностей.
probabilities = [types_of_enemies[key]["probability"] for key in enemy_types]

# Списки

# Список картинок для анімації вибуху
imgs_explosion = [pygame.transform.scale(pygame.image.load(os.path.join(baseDir, f"assets/img/explosion/exp{i}.png")), (50, 50)) for i in range(1, 6)]

# або

# imgs_explosion = []
# for i in range(1, 6):
#     img = pygame.transform.scale(pygame.image.load(os.path.join(baseDir, f"assets/img/explosion/exp{i}.png")), (50, 50))
#     imgs_explosion.add(img)



# Групи
# Створюємо групу для зберігання всіх спрайтів у грі. Це дозволяє зручно управляти всіма спрайтами одночасно.
all_sprites = pygame.sprite.Group()
# Створюємо групу для зберігання ворогів.
enemy_sprites = pygame.sprite.Group()
# Це спеціальний контейнер, який дозволяє нам легко управляти всіма ворогами разом.
enemy_bullets_sprite = pygame.sprite.Group()
# Це спеціальний контейнер, який дозволяє нам легко управляти всіма кулями ворога разом.
player_bullets_sprite = pygame.sprite.Group()


# Об'єкти
background = GameSprite(
    0,  # x-координата верхнього лівого кута фону.
    0,  # y-координата верхнього лівого кута фону.
    os.path.join(baseDir, "assets/img/galaxy.jpg"),  # Шлях до зображення фону.
    window.get_width(),  # Ширина фону.
    window.get_height(),  # Висота фону (не рухається, тому 0).
    0,
    [all]
)
all_sprites = pygame.sprite.Group()
player_bullets_sprite = pygame.sprite.Group()

player = Player(
    random.randint(0, window.get_width() - 80),  # Випадкова x-координата для гравця в межах екрану.
    window.get_height() - 130,  # y-координата для гравця (внизу екрану).
    os.path.join(baseDir, "assets/img/rocket.png"),  # Шлях до зображення гравця.
    80,  # Ширина гравця.
    100,  # Висота гравця.
    10,  # Швидкість гравця.
)
all_sprites = pygame.sprite.Group()

# Створюємо мітку для відображення рахунку
# Мітка показує поточний рахунок гри. Вона розташована в верхньому лівому куті екрану.
score_label = Label(
    text="Score: 0",
    font="Arial",  # Убедитесь, что это строка
    position=(10, 10),  # Позиция на экране
    font_size=30,
    font_color=(255, 255, 255)  # Цвет в формате (R, G, B)
)
all_sprites.add(score_label)
all_sprites.add(score_label)

player_bullets_sprite = pygame.sprite.Group()


# Створюємо мітку для відображення кількості пропущених ворогів
enemy_lost_label = Label(
    f"Пропущено: {enemy_lost}",  # Текст мітки, що показує кількість пропущених ворогів.
    (0, score_label.rect.bottom + 10),  # Позиція мітки, розташована під попередньою міткою.
    30,  # Розмір шрифту.
    (255, 255, 255),  # Колір шрифту (білий).
    None,  # Використовується стандартний шрифт.
    "topleft"  # Вирівнювання тексту (ліворуч зверху).
)
all_sprites.add(enemy_lost_label)  # Додаємо мітку до групи спрайтів для малювання та оновлення.

# Створюємо мітку для відображення тривалості гри
duration_game_label = Label(
    f"Тривалість: {int(current_time - start_game)}",  # Текст мітки, що показує тривалість гри.
    (window.get_width(), 0),  # Позиція мітки в правому верхньому куті екрану.
    30,  # Розмір шрифту.
    (255, 255, 255),  # Колір шрифту (білий).
    None,  # Використовується стандартний шрифт.
    "topright"  # Вирівнювання тексту (праворуч зверху).
)
all_sprites.add(duration_game_label)  # Додаємо мітку до групи спрайтів для малювання та оновлення.




# Игровой цикл
while not end:
    # Проверка всех событий игры.
    for event in pygame.event.get():
        # Если событие – выход из программы:
        if event.type == pygame.QUIT:
            # Завершаем игровой цикл.
            end = True

        # Проверяем, является ли событие нажатием клавиши
        if event.type == pygame.KEYDOWN:
            # Если нажата клавиша пробела (SPACE)
            if event.key == pygame.K_SPACE and not game_over and not pause and not player.isReloading:
                # Считаем количество выпущенных пуль
                player.shots_fired += 1
                # Воспроизводим звук стрельбы
                fire_music.play()
                # Вызываем метод стрельбы игрока, чтобы запустить пулю
                player.fire()

            if event.key == pygame.K_p and not game_over:  # Если нажата клавиша P:
                # Оператор присваивания, который инвертирует значение переменной pause.
                # Если значение переменной pause было True (т.е., пауза активирована),
                # оно изменится на False (т.е., пауза будет снята), и наоборот.
                # Это полезно для реализации паузы в играх или приложениях,
                # где одно нажатие кнопки может поставить игру на паузу, а следующее – снять её.
                pause = not pause

                if pause:
                    pause_start_time = time.time()  # Запоминаем время начала паузы
                    pause_label = Label("Пауза. Для продолжения нажмите 'Р'", 
                                        (window.get_width() / 2, window.get_height() / 2), 
                                        50, (255, 255, 0), None, "center")
                else:
                    pause_duration += time.time() - pause_start_time  # Обновляем длительность паузы

    # Если игра на паузе, непрерывно отображаем надпись "Пауза"
    if pause:
        pause_label.draw(window)
        pygame.display.flip()  # Обновляем экран, чтобы надпись была видна


if not game_over and not pause:
    # Обновляем текущий час
    current_time = time.time() - pause_duration

    # Обновляем все спрайты из группы all_sprites (вызываем метод update() для каждого спрайта).
    all_sprites.update()

    # Если прошло достаточно времени для генерации нового врага
    # Инициализация переменной в начале игры
start_interval_generate_enemy = time.time()  # или 0, в зависимости от логики игры
# Инициализация переменных
enemy_spawn_interval = random.uniform(1, 5)


if current_time - start_interval_generate_enemy > enemy_spawn_interval:
        # Обновляем время последней генерации
        start_interval_generate_enemy = current_time
        # Устанавливаем новый интервал между генерациями
        enemy_spawn_interval = random.uniform(1, 5)

        # Выбираем тип врага на основе вероятности
        selected_type_of_enemy = random.choices(enemy_types, probabilities, k=1)[0]

        # Получаем данные для выбранного типа врага
        enemy_data = types_of_enemies[selected_type_of_enemy]

        # Создаем новый объект врага
        Enemy(
            random.randint(0, window.get_width() - enemy_data["size"][0]),  # Случайная x-координата для врага.
            -enemy_data["size"][1],  # y-координата для врага (начало за границами экрана).
            os.path.join(baseDir, enemy_data["image"]),  # Путь до изображения врага.
            enemy_data["size"][0],  # Ширина врага.
            enemy_data["size"][1],  # Высота врага.
            random.randint(*enemy_data["speed_range"]),  # Случайная скорость врага.
            enemy_data["isShooting"],  # Будет ли враг стрелять.
            [all_sprites, enemy_sprites]  # Группы, в которые будет добавлен враг.
        )

# Коллизии (столкновения)

# Проверяем, если игрок столкнулся с врагами.
# Если так, выводим врагов и возвращаем список врагов, которые столкнулись с игроком.
player_vs_enemies = pygame.sprite.spritecollide(player, enemy_sprites, True, pygame.sprite.collide_mask)

# Проверяем, столкнулся ли игрок с пулями врагов.
# Если так, выводим пули и возвращаем список пуль, которые попали в игрока.
player_vs_enemy_bullets = pygame.sprite.spritecollide(player, enemy_bullets_sprite, True, pygame.sprite.collide_mask)

# Проверяем, если пули игрока столкнулись с врагами.
# Если так, выводим как врагов, так и пули, что столкнулись, и возвращаем пары столкновений.
enemies_vs_player_bullets = pygame.sprite.groupcollide(enemy_sprites, player_bullets_sprite, True, True, pygame.sprite.collide_mask)

# Проверяем, если пули игрока столкнулись с пулями врагов.
# Если так, выводим обе пули, что столкнулись.
player_bullets_vs_enemy_bullets = pygame.sprite.groupcollide(player_bullets_sprite, enemy_bullets_sprite, True, True, pygame.sprite.collide_mask)

# Подсчет уничтоженных врагов
# Для каждого врага, уничтоженного пулями игрока:
for enemy in enemies_vs_player_bullets:
    score += 1  # Добавляем 1 балл к счету.
    Explosion(enemy.rect.center, [all_sprites])  # Создаем анимацию взрыва в месте уничтоженного врага.

# Если игрок был поражен пулями врагов или столкнулся с врагом:
if player_vs_enemy_bullets or player_vs_enemies:
    player.current_health -= 1  # Уменьшаем здоровье игрока на 1.


    # Малюємо оновлену інформацію

# Оновлюємо текст з підрахунку з новим значенням
# Ця команда змінює текст підрахунку, щоб показати поточний рахунок гри.
score_label.update_text(f"Рахунок: {score}")

# Оновлюємо текст мітки пропущених ворогів з новим значенням
# Ця команда змінює текст мітки пропущених ворогів, щоб відобразити кількість ворогів, які втекли.
enemy_lost_label.update_text(f"Пропущено: {enemy_lost}")

# Оновлюємо текст мітки тривалості гри з новим значенням
# Ця команда змінює текст мітки тривалості гри, щоб відобразити, скільки часу пройшло з використанням функції діли і перетворюючи це число.
duration_game_label.update_text(f"Тривалість: {int(current_time - start_game)}")

# Малюємо всі спрайти з групи all_sprites на вікні.
all_sprites.draw(window)

# Малюємо індикатор здоров'я гравця на екрані.
player.draw_health_bar(window)

# Процес перезарядки (напис)
if player.isReloading:
    reload_text = Label("Wait, reloading....", 
                         (window.get_width(), duration_game_label.rect.bottom + 5), 
                         30, 
                         (255, 0, 0), 
                         None, 
                         "topright")
    reload_text.draw(window)

# Умова програшу
# Перевіряємо, чи гравець програв: якщо вороги пропущені більше ніж 3 рази або здоров'я гравця стало нульовим.
if enemy_lost > 3 or player.current_health <= 0:
    game_over = True # Гра завершується.
    # Виводимо повідомлення про програш у центрі екрану.
    lose_label = Label("YOU LOSE", (window.get_width() / 2, window.get_height() / 2), 50, (255, 0, 0), None, "center")
    lose_label.draw(window)

# Умова перемоги
# Перевіряємо, чи гравець виграв: якщо знищено 10 або більше ворогів.
if score >= 10:
    game_over = True # Гра завершується.
    # Виводимо повідомлення про перемогу у центрі екрану.
    win_label = Label("YOU WIN", (window.get_width() / 2, window.get_height() / 2), 50, (0, 255, 0), None, "center")
    win_label.draw(window)

# Оновлюємо дисплей, щоб відобразити новий кадр гри.
pygame.display.update()

# Контроль частоти кадрів до значення FPS (60 кадрів за секунду).
clock.tick(FPS)

# Завершуємо роботу з Pygame і закриваємо вікно гри.
pygame.quit()

