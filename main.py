import os
import random
import sys
import time

if os.name == 'nt':
    import msvcrt
else:
    import tty
    import termios

def get_char():
    if os.name == 'nt':
        return msvcrt.getch().decode('utf-8', errors='ignore').lower()
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.lower()

def init_game():
    global p_x, p_y, my_party, map_size, pokemon_db
    p_x, p_y = 16, 16
    map_size = 32
    pokemon_db = [
        ["피카츄", 50, 50, 15],
        ["파이리", 60, 60, 12],
        ["꼬부기", 55, 55, 13],
        ["이상해씨", 58, 58, 11],
        ["구구", 40, 40, 8],
        ["꼬렛", 35, 35, 7]
    ]
    my_party = [["피카츄", 50, 50, 15]]

def draw_map():
    os.system('cls' if os.name == 'nt' else 'clear')
    for y in range(map_size):
        row = ""
        for x in range(map_size):
            if x == p_x and y == p_y:
                row += "P "
            elif x == 0 or x == map_size - 1 or y == 0 or y == map_size - 1:
                row += "# "
            else:
                row += ". "
        print(row)
    print("\n[WASD] 이동 | [Q] 종료")

def battle():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("⚠️ 야생의 포켓몬이 나타났다!")
    time.sleep(1)
    
    enemy = list(random.choice(pokemon_db))
    enemy_name = enemy[0]
    enemy_max_hp = enemy[1]
    enemy_hp = enemy[2]
    enemy_atk = enemy[3]
    
    cur_idx = 0
    
    while enemy_hp > 0 and len(my_party) > 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        my_p = my_party[cur_idx]
        
        print(f"=== 전투 화면 ===")
        print(f"상대: {enemy_name} (HP: {enemy_hp}/{enemy_max_hp})")
        print(f"나의 포켓몬: {my_p[0]} (HP: {my_p[1]}/{my_p[2]})")
        print("-----------------")
        print("1. 싸우기 | 2. 가방 (몬스터볼/상처약) | 3. 포켓몬 교체 | 4. 도망치기")
        
        sel = get_char()
        
        if sel == '1':
            dmg = my_p[3]
            enemy_hp -= dmg
            print(f"\n{my_p[0]}의 공격! {enemy_name}에게 {dmg}의 피해!")
            time.sleep(1)
            
            if enemy_hp <= 0:
                print(f"\n{enemy_name}을(를) 쓰러뜨렸다!")
                time.sleep(1)
                break
                
        elif sel == '2':
            print("\n[가방] 1. 몬스터볼 (무한) | 2. 상처약 (무한)")
            bag_sel = get_char()
            if bag_sel == '1':
                prob = (1 - (enemy_hp / enemy_max_hp)) * 100
                if prob < 20: prob = 20
                
                print("\n몬스터볼을 던졌다!")
                time.sleep(1)
                
                if random.randint(1, 100) <= prob:
                    print(f"\n🎉 {enemy_name}을(를) 붙잡았다!")
                    if len(my_party) < 6:
                        my_party.append([enemy_name, enemy_max_hp, enemy_max_hp, enemy_atk])
                        print(f"{enemy_name}이(가) 동료가 되었다!")
                    else:
                        print("포켓몬이 가득 차서 보낼 수 없습니다. (최대 6마리)")
                    time.sleep(1.5)
                    break
                else:
                    print(f"\n아깝다! {enemy_name}이(가) 탈출했다!")
                    time.sleep(1)
            elif bag_sel == '2':
                heal = int(my_p[2] * 0.5)
                my_p[1] += heal
                if my_p[1] > my_p[2]:
                    my_p[1] = my_p[2]
                print(f"\n상처약을 사용했다! {my_p[0]}의 HP가 {heal}만큼 회복되었다.")
                time.sleep(1)
                continue
            else:
                continue
                
        elif sel == '3':
            print("\n=== 포켓몬 파티 ===")
            for i, p in enumerate(my_party):
                print(f"{i+1}. {p[0]} (HP: {p[1]}/{p[2]})")
            print("교체할 포켓몬 번호를 누르세요 (취소: 0)")
            
            ch_sel = get_char()
            if ch_sel.isdigit():
                idx = int(ch_sel) - 1
                if 0 <= idx < len(my_party):
                    if my_party[idx][1] <= 0:
                        print("\n그 포켓몬은 기절해서 싸울 수 없다!")
                        time.sleep(1)
                    else:
                        cur_idx = idx
                        print(f"\n가라, {my_party[cur_idx][0]}!")
                        time.sleep(1)
                        continue
            continue
            
        elif sel == '4':
            print("\n무사히 도망쳤다!")
            time.sleep(1)
            break
        else:
            continue
            
        if enemy_hp > 0:
            e_dmg = enemy_atk
            my_p[1] -= e_dmg
            print(f"\n{enemy_name}의 공격! {my_p[0]}은(는) {e_dmg}의 피해를 입었다.")
            time.sleep(1)
            
            if my_p[1] <= 0:
                my_p[1] = 0
                print(f"\n{my_p[0]}이(가) 쓰러졌다!")
                time.sleep(1)
                
                alive = False
                for i, p in enumerate(my_party):
                    if p[1] > 0:
                        cur_idx = i
                        alive = True
                        print(f"\n자동으로 {p[0]}이(가) 출전합니다!")
                        time.sleep(1)
                        break
                
                if not alive:
                    print("\n💀 모든 포켓몬이 전멸했습니다... GAME OVER")
                    time.sleep(2)
                    init_game()
                    break

def main():
    init_game()
    while True:
        draw_map()
        key = get_char()
        global p_x, p_y
        next_x, next_y = p_x, p_y
        if key == 'w': next_y -= 1
        elif key == 's': next_y += 1
        elif key == 'a': next_x -= 1
        elif key == 'd': next_x += 1
        elif key == 'q':
            break
            
        if 0 < next_x < map_size - 1 and 0 < next_y < map_size - 1:
            
            p_x, p_y = next_x, next_y
            
            if random.randint(1, 100) <= 15:
                battle()

if __name__ == "__main__":
    main()