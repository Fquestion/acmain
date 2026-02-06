# ========== 2026碧海宝安区设计大赛-唐荣麒作品 ©2026 唐荣麒 ==========
# 
# 唐荣麒的作品：小马接金币游戏 - 超级金币雨版
# 本作品使用pyzero库作为编码主库
# 
# 游戏特色：
# 1. 小马接金币基础玩法
# 2. 超级金币雨特效
# 3. 三种道具系统
# 4. 多种金币类型
# 
# 控制说明：
# ← → 键：移动小马
# 1键：使用密度道具
# 2键：触发超级金币雨
# 3键：使用时间道具
# R键：重新开始游戏
# ESC键：退出游戏
# P键：暂停/继续
# 
# ============================================================

print("="*120)
print("="*10,"2026碧海宝安区设计大赛-唐荣麒作品 ©2026 唐荣麒","="*10)
print("\n唐荣麒的作品：小马接金币游戏 - 超级金币雨版")
print("本作品使用pyzero库作为编码主库\n")

import pgzrun
import random
import math
import time
import os

# 检查图片文件
print("检查图片文件...")
for img_file in ["aaaa.png", "gold.png", "yw.jpg", "yw.png"]:
    if os.path.exists(img_file):
        print(f"✓ 找到: {img_file}")
    else:
        print(f"✗ 未找到: {img_file}")

WIDTH = 800
HEIGHT = 600

# 计时器
start_time = time.time()

# 游戏角色
horse = Actor("aaaa", (400, 500))
horse.speed = 6

# 金币系统
gold_coins = []
special_coins = []
super_coins = []
items = []

# 超级金币雨系统
super_rain_active = False
super_rain_time = 0
rain_density = 1.0

# 游戏状态
score = 0
game_time = 60
game_active = True
coins_collected = 0
items_collected = {"density": 0, "rain": 0, "time": 0}

class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.type = item_type
        self.speed = random.randint(3, 6)
        self.color = {
            "density": "purple",
            "rain": "orange",
            "time": "green"
        }[item_type]
        self.size = 30
        self.rect = Rect(x - 15, y - 15, 30, 30)
    
    def draw(self):
        # 绘制道具
        screen.draw.filled_circle((self.x, self.y), self.size//2, self.color)
        screen.draw.filled_circle((self.x, self.y), self.size//2 - 2, "white")
        
        # 绘制图标
        if self.type == "density":
            screen.draw.text("D", center=(self.x, self.y), fontsize=20, color="purple")
        elif self.type == "rain":
            screen.draw.text("R", center=(self.x, self.y), fontsize=20, color="orange")
        elif self.type == "time":
            screen.draw.text("T", center=(self.x, self.y), fontsize=20, color="green")
    
    def update(self):
        self.y += self.speed
        self.rect.y = self.y - 15

def create_gold_coin():
    coin = Actor("gold", (random.randint(50, WIDTH-50), -30))
    coin.speed = random.randint(4, 8)
    coin.type = "normal"
    coin.value = 10
    gold_coins.append(coin)

def create_special_coin():
    coin = Actor("gold", (random.randint(100, WIDTH-100), -50))
    coin.speed = random.randint(3, 6)
    coin.type = "special"
    coin.value = 50  # 提高特殊金币价值
    special_coins.append(coin)

def create_super_coin():
    coin = Actor("gold", (random.randint(50, WIDTH-50), -30))
    coin.speed = random.randint(5, 10)
    coin.type = "super"
    coin.value = 100  # 提高超级金币价值
    super_coins.append(coin)

def create_item():
    item_types = ["density", "rain", "time"]
    weights = [0.5, 0.3, 0.2]
    item_type = random.choices(item_types, weights=weights)[0]
    item = Item(random.randint(80, WIDTH-80), -40, item_type)
    items.append(item)

def activate_super_rain():
    global super_rain_active, super_rain_time
    if items_collected["rain"] > 0 and not super_rain_active:
        super_rain_active = True
        super_rain_time = 10.0
        items_collected["rain"] -= 1
        return True
    return False

def use_density_item():
    global rain_density
    if items_collected["density"] > 0:
        rain_density = min(3.0, rain_density + 0.5)
        items_collected["density"] -= 1
        return True
    return False

def use_time_item():
    global game_time
    if items_collected["time"] > 0:
        game_time += 10
        items_collected["time"] -= 1
        return True
    return False

def draw():
    current_time = time.time() - start_time
    
    # 绘制背景
    try:
        bg = images.yw
        screen.blit("yw", (400 - bg.get_width()//2, 300 - bg.get_height()//2))
    except:
        screen.fill((15, 25, 45))
        for _ in range(100):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 2)
            alpha = random.randint(100, 200)
            screen.draw.filled_circle((x, y), size, (255, 255, 255, alpha))
    
    if game_active:
        # 超级金币雨特效
        if super_rain_active:
            for y in range(0, HEIGHT, 20):
                alpha = int(50 * abs(math.sin(current_time * 2 + y/100)))
                screen.draw.filled_rect(Rect(0, y, WIDTH, 20), (255, 215, 0, alpha))
            
            for _ in range(20):
                x = random.randint(0, WIDTH)
                y = int((current_time * 100 + random.randint(0, 100)) % HEIGHT)
                screen.draw.line((x, y), (x, y+10), (255, 255, 100, 150))
        
        # 绘制游戏元素
        horse.draw()
        
        # 绘制所有金币
        for coin in gold_coins:
            coin.draw()
        
        for coin in special_coins:
            coin.draw()
            # 红色光环
            pulse_size = 25 + 5 * math.sin(current_time * 3)
            screen.draw.circle(coin.pos, int(pulse_size), (255, 50, 50, 150))
        
        for coin in super_coins:
            coin.draw()
            # 旋转星星
            angle = current_time * 5
            for i in range(5):
                rad = angle + i * 2 * math.pi / 5
                x = coin.x + 30 * math.cos(rad)
                y = coin.y + 30 * math.sin(rad)
                screen.draw.filled_circle((int(x), int(y)), 4, (255, 255, 0, 200))
        
        for item in items:
            item.draw()
        
        # === 游戏信息 ===
        screen.draw.text(f"分数: {score}", (20, 20), fontsize=32, color="white", fontname="font")
        screen.draw.text(f"时间: {int(game_time)}秒", (20, 60), fontsize=32, color="white", fontname="font")
        screen.draw.text(f"金币: {coins_collected}", (20, 100), fontsize=32, color="gold", fontname="font")
        
        # 金币雨状态
        if super_rain_active:
            screen.draw.text(f"金币雨: {max(0, int(super_rain_time))}秒", (20, 140), fontsize=26, color="gold", fontname="font")
        
        # 道具信息
        screen.draw.text("道具:", (WIDTH-350, 20), fontsize=30, color="white", fontname="font")
        y_offset = 60
        for item_type, count in items_collected.items():
            color = {"density": "purple", "rain": "orange", "time": "green"}[item_type]
            name = {"density": "密度+", "rain": "金币雨", "time": "时间+"}[item_type]
            screen.draw.text(f"{name}: {count}", (WIDTH-350, y_offset), fontsize=26, color=color, fontname="font")
            y_offset += 35
        
        # 控制说明
        screen.draw.text("控制:", (20, HEIGHT-120), fontsize=26, color="yellow", fontname="font")
        screen.draw.text("← → : 移动小马", (20, HEIGHT-90), fontsize=22, color="white", fontname="font")
        screen.draw.text("1: 密度+  2: 金币雨  3: 时间+", (20, HEIGHT-60), fontsize=22, color="white", fontname="font")
        screen.draw.text("R: 重玩  ESC: 退出  P: 暂停", (20, HEIGHT-30), fontsize=22, color="white", fontname="font")
        
        # 密度显示
        screen.draw.text(f"密度: {rain_density:.1f}x", (WIDTH-200, HEIGHT-40), fontsize=24, color="white", fontname="font")
        
        # 时间进度条
        bar_width = int((game_time / 60) * 300)
        bar_color = (int(255 * (1 - game_time/60)), int(255 * (game_time/60)), 0)
        screen.draw.filled_rect(Rect(WIDTH-320, HEIGHT-30, 300, 15), (50, 50, 70))
        screen.draw.filled_rect(Rect(WIDTH-320, HEIGHT-30, bar_width, 15), bar_color)
        
    else:
        # 游戏结束画面
        screen.draw.text("游戏结束", center=(400, 160), fontsize=72, color="red", fontname="font", shadow=(2, 2))
        screen.draw.text(f"最终分数: {score}", center=(400, 240), fontsize=48, color="white", fontname="font")
        screen.draw.text(f"收集金币: {coins_collected}", center=(400, 300), fontsize=36, color="gold", fontname="font")
        
        # 道具使用统计
        total_items_used = sum(items_collected.values())
        screen.draw.text(f"使用道具: {total_items_used}", center=(400, 350), fontsize=36, color="cyan", fontname="font")
        
        # 评价系统
        if score >= 1000:
            result = "🏆 传奇大师!"
            color = "#FFD700"
        elif score >= 600:
            result = "🎖️ 钻石玩家!"
            color = "#B9F2FF"
        elif score >= 300:
            result = "⭐ 黄金高手!"
            color = "gold"
        elif score >= 100:
            result = "✨ 白银玩家!"
            color = "silver"
        else:
            result = "💪 继续努力!"
            color = "#CD7F32"
        
        screen.draw.text(result, center=(400, 410), fontsize=42, color=color, fontname="font")
        screen.draw.text("按R键重新开始", center=(400, 480), fontsize=32, color="cyan", fontname="font")
        screen.draw.text("按ESC退出游戏", center=(400, 520), fontsize=28, color="gray", fontname="font")

def update():
    global score, game_time, game_active, coins_collected
    global super_rain_active, super_rain_time, rain_density
    
    if not game_active:
        return
    
    # 控制小马移动（始终可用）
    if keyboard.left and horse.x > 50:
        horse.x -= horse.speed
    if keyboard.right and horse.x < WIDTH - 50:
        horse.x += horse.speed
    
    # 金币雨计时
    if super_rain_active:
        super_rain_time -= 1/60
        if super_rain_time <= 0:
            super_rain_active = False
            rain_density = 1.0
            print("金币雨结束")
    
    # 生成金币（根据密度调整）
    base_rate = 0.04 * rain_density
    if random.random() < base_rate:
        create_gold_coin()
    
    # 超级金币雨期间大量生成金币
    if super_rain_active and random.random() < 0.1:
        for _ in range(int(rain_density * 2)):
            create_gold_coin()
    
    # 生成超级金币
    if random.random() < 0.01 * rain_density:
        create_super_coin()
    
    # 生成特殊金币（奖励时间）
    if random.random() < 0.008 and len(special_coins) < 2:
        create_special_coin()
    
    # 生成道具
    if random.random() < 0.006:
        create_item()
    
    # 更新普通金币
    coins_to_remove = []
    for coin in gold_coins:
        coin.y += coin.speed
        
        # 检测碰撞
        if horse.colliderect(coin):
            coins_to_remove.append(coin)
            score += coin.value
            coins_collected += 1
        elif coin.y > HEIGHT + 100:
            coins_to_remove.append(coin)
    
    # 移除已处理的普通金币
    for coin in coins_to_remove:
        if coin in gold_coins:
            gold_coins.remove(coin)
    
    # 更新特殊金币（奖励时间）
    special_to_remove = []
    for coin in special_coins:
        coin.y += coin.speed
        
        if horse.colliderect(coin):
            special_to_remove.append(coin)
            game_time += 5  # 增加5秒游戏时间
            score += coin.value
            print(f"收集特殊金币！增加5秒游戏时间")
        elif coin.y > HEIGHT + 100:
            special_to_remove.append(coin)
    
    for coin in special_to_remove:
        if coin in special_coins:
            special_coins.remove(coin)
    
    # 更新超级金币
    super_to_remove = []
    for coin in super_coins:
        coin.y += coin.speed
        
        if horse.colliderect(coin):
            super_to_remove.append(coin)
            score += 100
            coins_collected += 3
        elif coin.y > HEIGHT + 100:
            super_to_remove.append(coin)
    
    for coin in super_to_remove:
        if coin in super_coins:
            super_coins.remove(coin)
    
    # 更新道具
    items_to_remove = []
    for item in items:
        item.update()
        
        # 使用rect进行碰撞检测
        horse_rect = Rect(horse.x - 30, horse.y - 30, 60, 60)
        if horse_rect.colliderect(item.rect):
            items_to_remove.append(item)
            items_collected[item.type] += 1
            score += 20
            print(f"收集{item.type}道具！当前数量: {items_collected[item.type]}")
        elif item.y > HEIGHT + 100:
            items_to_remove.append(item)
    
    for item in items_to_remove:
        if item in items:
            items.remove(item)
    
    # 更新时间
    if game_time > 0:
        game_time -= 1/60
    else:
        game_active = False
        game_time = 0

def on_key_down(key):
    global game_active, score, game_time, coins_collected, gold_coins, special_coins, super_coins
    global items, items_collected, rain_density
    
    if key == keys.R:
        # 重新开始游戏
        horse.pos = (400, 500)
        horse.speed = 6
        
        gold_coins.clear()
        special_coins.clear()
        super_coins.clear()
        items.clear()
        
        score = 0
        game_time = 60
        game_active = True
        coins_collected = 0
        
        super_rain_active = False
        super_rain_time = 0
        rain_density = 1.0
        
        items_collected = {"density": 0, "rain": 0, "time": 0}
        
        print("游戏重新开始！")
    
    elif key == keys.ESCAPE:
        exit()
    
    elif key == keys.K_1 and game_active:
        # 使用密度道具
        if use_density_item():
            print(f"使用密度道具！当前密度: {rain_density:.1f}x")
    
    elif key == keys.K_2 and game_active:
        # 触发金币雨
        if activate_super_rain():
            print("触发超级金币雨！")
    
    elif key == keys.K_3 and game_active:
        # 使用时间道具
        if use_time_item():
            print(f"使用时间道具！当前时间: {int(game_time)}秒")
    
    elif key == keys.P and game_active:
        # 暂停/继续
        game_active = not game_active
        print(f"游戏{'暂停' if not game_active else '继续'}")

pgzrun.go()