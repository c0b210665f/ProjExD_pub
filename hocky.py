from turtle import color
import pygame as pg

#C0B21116
clock = pg.time.Clock()           #clock関数の設定
start_time = pg.time.get_ticks()
#C0B21116

class Screen:
    def __init__(self, wh, title):
        #  wh:幅高さのタプル, title:画面のタイトル
        pg.display.set_caption(title)
        self.width, self.height = wh         # wh = (1600, 900)
        self.disp = pg.display.set_mode((self.width, self.height))  # Surface
        self.rect = self.disp.get_rect()     # Rectクラス


class Mallet_red():
    key_delta = {pg.K_UP   : [0, -2],
                 pg.K_DOWN : [0, +2],
                 pg.K_LEFT : [-2, 0],
                 pg.K_RIGHT: [+2, 0],
                }

    def __init__(self, red_xy):
        #  red_xy:赤マレットの座標用のタプル
        self.image = pg.Surface((80, 80))             #  mallet_blue用のsurface
        self.image.set_colorkey((0,0,0))              #  黒色部分を透過する
        pg.draw.rect(self.image, (255, 0, 0), (0, 0, 80, 80))
        self.rect  = self.image.get_rect()  #Rectクラス
        self.rect.centerx, self.rect.centery = red_xy
    
    def update(self, screen):
        key_states = pg.key.get_pressed()
        for key, delta in Mallet_red.key_delta.items():
            if key_states[key] == True:
                self.rect.centerx += delta[0]
                self.rect.centery += delta[1]
            if check_range_red(screen.rect, self.rect) != (1,1): 
                self.rect.centerx -= delta[0]
                self.rect.centery -= delta[1]


class Mallet_blue(Mallet_red):
    key_delta = {pg.K_w  : [0, -2],      
                 pg.K_s : [0, +2],
                 pg.K_a : [-2, 0],
                 pg.K_d: [+2, 0],
                }

    def __init__(self, blue_xy):
        # blue_xy:青マレットの座標タプル
        super().__init__(blue_xy)
        pg.draw.rect(self.image, (0, 0, 255), (0, 0, 80, 80))
        self.rect.centerx, self.rect.centery = blue_xy

    def update(self, screen):
        key_states = pg.key.get_pressed()
        for key, delta in Mallet_blue.key_delta.items():
            if key_states[key] == True:
                self.rect.centerx += delta[0]
                self.rect.centery += delta[1]
            if check_range_blue(screen.rect, self.rect) != (1,1): 
                self.rect.centerx -= delta[0]
                self.rect.centery -= delta[1]


class Ball():
    def __init__(self, color, r, vxy):
        #  color:ボールの色,r:ボールの半径, vxy:ボールの移動速度
        self.image = pg.Surface((2*r, 2*r))           #  ball用のsurface
        self.image.set_colorkey((0,0,0))              #  黒色部分を透過する
        pg.draw.circle(self.image, color, (r, r), r)
        self.rect = self.image.get_rect()
        self.rect.centerx = 50
        self.rect.centery = 50
        self.vx, self.vy  = vxy

    def update(self, screen):
        self.rect.move_ip(self.vx, self.vy)
        x, y = check_bound(screen.rect, self.rect)
        self.vx *= x                                  #  横方向に画面外なら，横方向速度の符号反転 
        self.vy *= y                                  #  縦方向に画面外なら，縦方向速度の符号反転
        
        #C0B21116
        time_passed = pg.time.get_ticks() - start_time
        time_sec = time_passed / 1000.0
        #ボールの速度を徐々に加速指せる
        self.rect.move_ip(self.vx*time_sec/7, self.vy*time_sec/7)
        #C0B21116

class Goal_Right():
    def __init__(self, Rgoal_xy):
        #  Rgoal_xy:赤ゴールの座標
        self.image = pg.Surface((10, 400))
        self.image.set_colorkey((0, 0, 0))
        pg.draw.rect(self.image, (255, 255, 255), (0,0,10,400))
        self.rect  = self.image.get_rect()
        self.rect.centerx, self.rect.centery = Rgoal_xy


class Goal_Left(Goal_Right):
    def __init__(self, Lgoal_xy):
        #  Rgoal_xy:赤ゴールの座標
        super().__init__(Lgoal_xy)
        self.rect.centerx, self.rect.centery = Lgoal_xy


def main():
    #  コンストラクタを呼び出す 
    clock       = pg.time.Clock()
    screen      = Screen((1600, 900), "ホッケー")  
    mallet_red  = Mallet_red((1300, 450))                      
    mallet_blue = Mallet_blue((300, 450))                   
    ball        = Ball((0, 255 ,0), 25, (+2, +2))       
    red_goal    = Goal_Right((1595, 450))
    blue_goal   = Goal_Left((5, 450))
    #  変数の定義
    score_red, score_blue = 0, 0      #  青と赤の得点の初期値
    counter_time = 33                 #  試合時間の初期値
    counter_start_time = 3            #　試合前のカウント初期値
    sounds = []                       #  音楽保存リスト
    sounds.append(pg.mixer.Sound("fig/hockyBGM.wav"))
    sounds.append(pg.mixer.Sound("fig/壁効果音木琴.wav"))
    sounds.append(pg.mixer.Sound("fig/ゴール.wav"))
    sounds.append(pg.mixer.Sound("fig/カウントダウン.wav"))

    sounds[0].play()                  #  BGMの再生

    pg.time.set_timer(pg.USEREVENT, 1000)

    while True:
        screen.disp.fill((0, 0, 0))                  #  スクリーンを黒に塗りつぶし
        for event in pg.event.get():
            if event.type == pg.QUIT: return         #  ✕ボタンでmain関数から戻る 
            if event.type == pg.USEREVENT:           #  １秒ごとにカウントする
                    counter_time -= 1
                    counter_start_time -= 1
        #  試合開始前の挙動
        if counter_time > 30:
            start(screen, counter_start_time)
            sounds[3].play()
        #  試合中の挙動
        elif 1 <= counter_time <= 30:
            #  赤いマレットを表示       
            mallet_red.update(screen)
            screen.disp.blit(mallet_red.image, mallet_red.rect)
            #  青いマレットを表示
            mallet_blue.update(screen) 
            screen.disp.blit(mallet_blue.image, mallet_blue.rect)
            #  ボールを表示
            ball.update(screen)
            screen.disp.blit(ball.image, ball.rect)
            #  ゴールを左右に表示
            screen.disp.blit(red_goal.image, red_goal.rect)
            screen.disp.blit(blue_goal.image, blue_goal.rect)
            #　関数の呼び出し
            score(score_red, score_blue, screen)
            red_bound(ball, mallet_red, sounds)
            blue_bound(ball, mallet_blue, sounds)
            timer(counter_time,screen)

            if pg.sprite.collide_rect(ball,red_goal) :
            #  ボールと赤ゴールが当たったら
                score_blue += 1    #  青の得点を増やす
                sounds[2].play()   #  効果音の再生
            if pg.sprite.collide_rect(ball, blue_goal):
            #  ボールと青ゴールが当たったら
                score_red += 1     #  赤の得点を増やす
                sounds[2].play()   #  効果音の再生
        #  試合後の挙動
        else:
            sounds[0].stop()       #  BGMを止める
            sounds[1].stop()       #  効果音がならないようにする
            owari(score_red, score_blue, screen)
        

        pg.display.update()  
        clock.tick(1000) 

#  スタート前の画面の設定
def start(screen, counter_start_time):
    list = [[80, "試合時間 : 30秒", (480,400)], [150, "エアホッケー", (400, 200)],
            [100, str(counter_start_time), (750, 500)]]
    for i in list:
        font = pg.font.Font("/Windows/Fonts/meiryo.ttc", i[0])     
        text = font.render(i[1], True, (255,255,255))
        screen.disp.blit(text, i[2])

 #  ボールの移動範囲設定  
def check_bound(sc_r, obj_r): 
    x, y = +1, +1
    if obj_r.left < sc_r.left or sc_r.right  < obj_r.right : x = -1
    if obj_r.top  < sc_r.top  or sc_r.bottom < obj_r.bottom: y = -1
    return x, y

#  赤マレットの移動範囲設定
def check_range_red(sc_r, obj_r): 
    x, y = +1, +1
    if obj_r.left < (sc_r.right)/2+40 or sc_r.right  < obj_r.right : x = -1
    if obj_r.top  < sc_r.top  or sc_r.bottom < obj_r.bottom: y = -1
    return x, y

#  青マレットの移動範囲設定
def check_range_blue(sc_r, obj_r): 
    x, y = +1, +1
    if obj_r.right > (sc_r.right)/2+40 or sc_r.left  > obj_r.left : x = -1
    if obj_r.top  < sc_r.top  or sc_r.bottom < obj_r.bottom: y = -1
    return x, y

#  ボールと赤マレットの当たり判定
def red_bound(ball, mallet_red, sounds):
     #  ballとmallet_redが当たったら
    if pg.sprite.collide_rect(ball,mallet_red) :  
        sounds[1].play()  #  効果音を再生
        #  当たった時のボールの位置でバウンド方向を変える
        if mallet_red.rect.centery-40 <= ball.rect.centery\
            <= mallet_red.rect.centery+40:
                ball.vx *= -1
        if mallet_red.rect.centerx-40 <= ball.rect.centerx\
            <= mallet_red.rect.centerx+40:
                ball.vy *= -1

#  ボールと青マレットの当たり判定
def blue_bound(ball, mallet_blue, sounds):
    #  ballとmallet_blueが当たったら
    if pg.sprite.collide_rect(ball,mallet_blue) :
        sounds[1].play()  #  効果音を再生
        #  当たった時のボールの位置でバウンド方向を変える
        if mallet_blue.rect.centery-40 <= ball.rect.centery\
            <= mallet_blue.rect.centery+40:
                ball.vx *= -1
        if mallet_blue.rect.centerx-40 <= ball.rect.centerx\
            <= mallet_blue.rect.centerx+40:
                ball.vy *= -1

# タイマー表示
def timer(counter_time, screen):
    font = pg.font.Font("/Windows/Fonts/meiryo.ttc", 100)     
    text = font.render(str(counter_time), True, (255,255,255))
    screen.disp.blit(text, (770,30))

#  試合終了後の反応表示
def owari(score_red, score_blue, screen):
    font       = pg.font.Font("/Windows/Fonts/meiryo.ttc", 200)
    text_lst   = ["RED_WIN", "BLUE_WIN", "DRAW"]
    score_red  = int(score_red/7)
    score_blue = int(score_blue/7)
    #  テキストの決定
    if   score_red >  score_blue:
          text = text_lst[0]
    elif score_red <  score_blue:
          text = text_lst[1]
    elif score_red == score_blue:
          text = text_lst[2]
    #  DRAWの場合だけ表示座標をずらす
    if text == "DRAW":
        text   = font.render(text, True, (255, 255, 0))
        screen.disp.blit(text, (500, 20))
    else:
        text   = font.render(text, True,(255, 255, 0))
        screen.disp.blit(text, (300, 20))
    text_red = font.render(str(int(score_red)), True, (255,0, 0))       #鈴木飛鳥
    text_blue = font.render(str(int(score_blue)), True, (0,0, 255))     #鈴木飛鳥
    text_minus = font.render("-", True, (255,255, 255))                 #鈴木飛鳥
    screen.disp.blit(text_red, (600, 300))                              #鈴木飛鳥
    screen.disp.blit(text_minus, (775, 300))                            #鈴木飛鳥
    screen.disp.blit(text_blue, (900, 300))                             #鈴木飛鳥

#  得点表示
def score(score_red, score_blue, screen):
    font = pg.font.Font("/Windows/Fonts/meiryo.ttc", 100)
    text = font.render(str(int(score_red/7)), True, (255,0, 0))
    screen.disp.blit(text, (1480,20))
    text = font.render(str(int(score_blue/7)), True, (0,0, 255))
    screen.disp.blit(text, (100,20))


if __name__ == "__main__":
    pg.init()
    main()