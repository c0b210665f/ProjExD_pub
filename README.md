# プロジェクト演習Ⅰ・テーマD

## 第6回
### pygameでゲーム実装
#### 基本機能
- game概要:   
    - 初めにマレットはボールを跳ね返す器具である
    - rensyu06/hocke.pyを実行すると、1600x900のウインドウが作成され、マレットを移動させボールを跳ね返し得点を稼ぐゲーム
    - 結果画面で最終結果の点数表示する   # C0B21092 鈴木 
- 操作方法：矢印キーで赤いマレットを上下左右に動かし、W,S,A,Dキーで青いマレットを上下左右に動かす. Xキーで終了
- プログラムの説明
    - hocky.pyをコマンドラインから実行すると，pygameの初期化，main関数の順に処理が進む
    - main関数ではスクリーンの生成、赤と青のマレットの生成、ボールの生成、ゴールの生成、BGMの再生を行う
    - main関数の無限ループでは、キー操作に応じたマレットの移動、カウントダウン、指定速度に応じたボールの移動を行う。ボールが指定されているゴールに当たると当てた側の得点を増やしている
    - Screenクラスではスクリーンの幅高さとタイトルを設定している
    - Mallet_redクラスでは、コンストラクタでマレットの大きさ、形、色と座標を設定しているupdateメソッドでは、マレットをキーに応じて動くようにしている
    - Mallet_blueクラスでは、Mallet_redを親クラスとして色と座標をオーバーライドしている
    - Ballクラスではコンストラクタで、ボールの大きさ、形、色と座標を設定しているupdateメソッドでは、ボールが画面から出ないように設定している
    - Goal_rightクラスでは、赤のゴールの大きさ、形、色と座標を設定している
    - Goal_Leftクラスでは、Goal_rightクラスを親クラスとして色と座標をオーバーライドしている
    - Mirrorクラスでは長方形の壁を作り、その壁に当たるとボールが加速または減速する  # C0B21098 関
    - start関数では、試合前の画面にテクストを表示している
    - check_bound関数では、ボールがスクリーンからはみ出ないようにしている
    - check_range_red,check_range_blue関数では、赤と青マレットの移動範囲を設定している
    - red_bound,blue_bound関数では、ボールと赤、青マレットの当たり判定を行っている
    - timer関数ではタイマーのフォントの設定、座標の設定、表示を行っている
    - owari関数では、試合終了後の画面にテキストを表示、テキストは得点によって変わる
    - score関数では、青と赤の得点を表示している
    - pg.time.get_ticks()関数を使用し、Ballクラスのupdate()内に
    time_passed = pg.time.get_ticks() - start_time
    time_sec = time_passed / 1000.0
    self.rect.move_ip(self.vx * time_sec/20, self.vy * time_sec/20)
    を追加することでボールの速度を徐々に加速させる　　# C0B21116 寺川
#### ToDo
- [ ]ボールを増やす
- [ ]BGMをボタンによって変更する
- [ ]ゴール時演出の追加  #C0B21078 柴田恭佑

#### メモ
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

def start(screen, counter_start_time):
    list = [[80, "試合時間 : 60秒", (480,400)], [150, "エアホッケー", (400, 200)], [100, str(counter_start_time), (750, 500)]]
    for i in list:
        font = pg.font.Font("/Windows/Fonts/meiryo.ttc", i[0])     
        text = font.render(i[1], True, (255,255,255))
        screen.disp.blit(text, i[2])

 #  ボールのの移動範囲設定  
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
        text   = font.render(text, True, (255,255,0))
        screen.disp.blit(text, (500, 20))
    else:
        text   = font.render(text, True, (255,255,0))
        screen.disp.blit(text, (300, 20))

#  得点表示
def score(score_red, score_blue, screen):
    font = pg.font.Font("/Windows/Fonts/meiryo.ttc", 100)
    text = font.render(str(int(score_red/7)), True, (255,0, 0))
    screen.disp.blit(text, (1480,20))
    text = font.render(str(int(score_blue/7)), True, (0,0, 255))
    screen.disp.blit(text, (100,20))

## 第5回
### pygameでゲーム実装
#### 3限：基本機能
- game概要:
    - rensyu05/dodge_bomb.pyを実行すると、1600x900のウインドウが作成され、こうかとんを移動させ5個の爆弾から逃げるゲーム
    - 実行するたびに爆弾の初期位置が変化する
- 操作方法: 矢印キーでこうかとんを上下左右に移動させるゲーム
- プログラムの説明
    - main関数ではスクリーンの生成，背景画像の描画，こうかとんの描画，爆弾の描画
    を行う
    - dodge_bomb.pyをコマンドラインから実行すると，pygameの初期化，main関数の順に処理が進む
    - ゲームオーバーによりmain関数から抜けると，pygameの初期化を解除し，プログラムが終了する
    - main関数の無限ループでは，キー操作に応じたこうかとんの移動，指定速度に応じた爆弾の移動を行う。
    また、爆弾とこうかとんがウインドウからはみでないようにしている
    counter関数を一秒に1づつ足しているls
#### 4限：追加機能
    - BGMと壁にあたった時に効果音を再生
    - SPACEキーを押すとこうかとんが盾を持つ機能
    - tateクラスを作り、SPACEキーが押されたら盾が表示される機能
    - timerクラスを作り、タイマーを左上に表示
#### ToDo
- [ ]盾で爆弾を跳ね返す機能
- [ ]時間ごとに爆弾が増えていく機能

#### メモ
class Screen:
    def __init__(self, bg_img, wh, title):
        # bg_img背景画像のパス, wh:幅高浅野タプル, title:画面のタイトル
        pg.display.set_caption(title)
        self.width, self.height = wh  # wh = (1600, 900)
        self.disp = pg.display.set_mode((self.width, self.height))  # Surface
        self.rect = self.disp.get_rect()  # Rectクラス
        self.image = pg.image.load(bg_img)  # Surface


class Bird(pg.sprite.Sprite):
    key_delta = {pg.K_UP   : [0, -1],
                pg.K_DOWN : [0, +1],
                pg.K_LEFT : [-1, 0],
                pg.K_RIGHT: [+1, 0],
                }

    def __init__(self, tori_img, zoom, xy):
        super().__init__()
        # tori_img:鳥画像用のパス, zoom:拡大率, xy:初期配置座標
        self.image = pg.image.load(tori_img)    # Surface
        self.image = pg.transform.rotozoom(self.image, 0, zoom)  # 画像を拡大する
        self.rect  = self.image.get_rect()
        self.rect.center = xy

    def update(self, screen):
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[key] == True:
                self.rect.centerx += delta[0]
                self.rect.centery += delta[1]
                # 練習7
            if check_bound(screen.rect, self.rect) != (1,1): 
                self.rect.centerx -= delta[0]
                self.rect.centery -= delta[1]


class Bomb(pg.sprite.Sprite):
    def __init__(self, color, r, vxy, screen):
        # color: 爆弾の色, r: 爆弾の半径
        # vxy: 爆弾円の速度のタプル
        # screen: 描画用Screenオブジェクト
        super().__init__()

        self.image = pg.Surface((2*r, 2*r))  # 爆弾用のSurface
        self.image.set_colorkey((0,0,0))     # 黒色部分を透過する
        pg.draw.circle(self.image, color, (r, r), r)   # 爆弾用Surfaceに円を描く
        self.rect = self.image.get_rect()                    # 爆弾用Rect
        self.rect.centerx = random.randint(0, screen.rect.width)
        self.rect.centery = random.randint(0, screen.rect.height)
        self.vx, self.vy = vxy

    def update(self, screen):
        self.rect.move_ip(self.vx, self.vy)
        x, y = check_bound(screen.rect, self.rect)
        self.vx *= x # 横方向に画面外なら，横方向速度の符号反転
        self.vy *= y # 縦方向に画面外なら，縦方向速度の符号反転
        sounds[1].play()


class Tate(pg.sprite.Sprite):
    def __init__(self, tate_img, xy):
        super().__init__()
        self.image = pg.image.load(tate_img)    # Surface
        self.image = pg.transform.rotozoom(self.image, 0, 0.3)  # 画像を拡大する
        self.rect  = self.image.get_rect()
        self.rect.center = xy

class Timer:
    counter = 0
    def __init__(self, event):  
        if event.type == pg.USEREVENT:
            Timer.counter += 1     
        self.font = pg.font.Font("/Windows/Fonts/meiryo.ttc", 100)     # タイマーのフォントを指定
        self.text = self.font.render(str(Timer.counter), True, (255,255,0))

## 第4回
### pygameでゲーム実装
#### 3限：基本機能
- game概要:
    - rensyu04/dodge_bomb.pyを実行すると、1600x900のウインドウが作成され、こうかとんを移動させ爆弾から逃げるゲーム
    - 実行するたびに爆弾の初期位置が変化する
- 操作方法: 矢印キーでこうかとんを上下左右に移動させるゲーム
- プログラムの説明
    - main関数では，clockの生成，スクリーンの生成，背景画像の描画，こうかとんの描画，爆弾の描画
    を行う
    - dodge_bomb.pyをコマンドラインから実行すると，pygameの初期化，main関数の順に処理が進む
    - ゲームオーバーによりmain関数から抜けると，pygameの初期化を解除し，プログラムが終了する
    - main関数の無限ループでは，キー操作に応じたこうかとんの移動，指定速度に応じた爆弾の移動を行う。
    また、爆弾とこうかとんがウインドウからはみでないようにしている
    counter関数を一秒に1づつ足している

#### 4限：追加機能
    - change_img関数でこうかとんが爆弾に当たった時に爆発画像と焼き鳥の画像が表示される機能
    - 背景画像を動かし、画像を焼き鳥屋と焼き鳥に変えることであたかもこうかとんが焼き鳥に変わり運ばれているように見せる機能
    - main関数の中に爆弾とこうかとんの当たり判定の条件式を付け足し、当たった時にタイマーが止まりウインドウが消えないにする機能
    - calc_dict関数でこうかとんが爆弾と当たった時にchenge_img関数を呼び出す
    - timer関数ではcounterの値を受け取り右上に表示している

#### ToDo
- [ ]時間ごとに増える爆弾が増殖する機能
- [ ]壁に当たると爆弾が大きくなる機能


#### メモ
def change_img():
    bakuhatu = pg.image.load("fig/12.png")
    bakuhatu_1 = pg.transform.rotozoom(bakuhatu,
    angle =0,scale = 0.5)

    yakitroi = pg.image.load("fig/10.png")
    yakitori_1 = pg.transform.rotozoom(yakitroi,
     angle =0,scale = 0.3)

    screen.blit(bakuhatu_1, (tx-70,ty-50)) 
    screen.blit(yakitori_1, (tx-15,ty-50))

def calc_dist():
    if math.sqrt((tx+vx+48-bx+vy)**2+(ty+70+vx-by+vy)**2) <= 60:
        change_img()
        return False

def timer():
    font = pg.font.Font("/Windows/Fonts/meiryo.ttc", 100)     # タイマーのフォントを指定
    text = font.render(str(counter), True, (255,255,0))
    screen.blit(text, (20,10))



## 第3回
### tkinterで迷路ゲーム実装
#### 3限：基本機能
- game概要:
    - rensyu03/maze.pyを実行すると、1500x900のcanvasに迷路が作成され、迷路に沿ってこうかとんを移動させるゲーム
    - 実行するたびに迷路の構造は変化する
- 操作方法: 矢印キーでこうかとんを上下左右に移動する
- プログラムの説明
    - maze_maker関数のshow_maze関数でcanvasに迷路を描画する
    - draw関数でcreate_imageメソッドでこうかとんの画像を(1,1)に描画する
    - bindメソッドでKeyPressにKey_down関数を、KeyReleaseにKey_up関数を紐づける
    - main_proc関数で矢印キーに応じて、こうかとんを上下左右に1マス移動させ、0.1秒後にmain_procを呼び出す


#### 4限　追加機能
- add_startgoal関数でstartをcreate_rectangleメソッドで(100,100,200,200)に描画するgoalはcreate_rectangleメソッドで描画するが座標指定をランダムで呼び出すことによって実行ごとに場所が変わるようになっているまた、条件文を入れることにより、goalが壁の中にできないようにしてる
- eval_fin関数でこうかとんの位置がgoalの位置が同じになったらタイマーを止める機能
- change_img関数でキーボード入力された数字に対応した画像が読みこまれ、元の画像を消し、読み込まれた画像を表示する機能
- main_proc関数に追加でボタン押されて1マス動く先が壁だったら、動かないようする機能
- count_up関数で一秒ずつカウントをして表示する

#### ToDo
 - [ ]自動で動くお邪魔キャラの追加。
 - [ ]通過済みの床色の変更。

#### メモ
def add_startgoal():                                                                                   
    global goal_x, goal_y                                                
    while True:                                                          
        goal_x = random.randint(12,14)                                   
        goal_y = random.randint(5,8)                                    
        if meilo_list[goal_y][goal_x] == 0:                              
            break                                                        
    canvas.create_rectangle(100,100,200,200,fill = "red")               
    canvas.create_rectangle(goal_x*100,goal_y*100,(goal_x*100)+100,
    (goal_y*100)+100,fill = "blue")

def eval_fin():                                                          
    global jid                                                           
    if mx == goal_y and my == goal_x:
        message = tk.Message(maze, text="GOAL",font = ("",50),
        bg = "yellow",fg = "red")
        message.pack()                                
        maze.after_cancel(jid)     

def change_img():
    img_list = ["0","1","2","3","4","5","6","7","8","9"]
    if key in img_list:
        canvas.delete(tori_id)
        draw(key)
    maze.after(100, change_img)  

def main_proc():                                                         
    global cx, cy, key, tori, mx, my                                     
    if key == 'Up'      and  meilo_list[mx-1][my] == 0:                         
        cy -= 100                                                        
        mx -= 1                                                          
        
    elif key == 'Down'  and  meilo_list[mx+1][my] == 0:                    
        cy += 100                                                       
        mx += 1                                                         

    elif key == 'Right' and  meilo_list[mx][my+1] == 0:                   
        cx += 100                                                        
        my += 1                                                          

    elif key == 'Left'  and  meilo_list[mx][my-1] == 0:                    
        cx -= 100                                                        
        my -= 1                                                          
    
    canvas.coords("tori", cx, cy)
    if  mx == goal_y and  my == goal_x:                                  
        pass                                                             
    else:                                                                
        maze.after(100,main_proc)                                    
    eval_fin()

def counter():                                                           
    global tmr, jid                                                      
    tmr = tmr + 1                                                        
    label['text'] = tmr                                                  
    jid = maze.after(1000, counter)
     



## 第2回
### tkinterで電卓実装
#### 追加機能
- =ボタン           : entryに入力されている数式を計算し計算結果をentryに表示する
- オールクリアボタン : entryに入力されている数字、数式の文字列全体をdeleteする
- delボタン         : entryの入力されている数字、数式を一文字削除する
- +/-ボタン         : entryに入力された数字の符号を変換
- 平方根ボタン      : entryに入力されている数字を平方根へ変換
- sinボタン         : entryに入力されている数字をsinに変換
- cosボタン         : entryに入力されている数字をcosに変換
- tanボタン         : entryに入力されている数字をtanに変換
- 階乗ボタン        : entryに入力されている数字を階乗する

#### メモ
def equal(event):
    siki = entry.get()
    entry.delete(0, tk.END)
    kotae = eval(siki)
    entry.insert(tk.END, kotae)
    
def delete(event):
    entry.delete(0, tk.END)

def delete(event):
    pos_end_prew = len(entry.get())-1
    entry.delete(pos_end_prew,tk.END)

def minus(event):
    a = entry.get()
    b = int(a) * -1
    entry.delete(0, tk.END)
    entry.insert(tk.END, b)

def root(event):
    a = entry.get()
    b = math.sqrt(int(a))
    entry.delete(0, tk.END)
    entry.insert(tk.END, b)

def sin(event):
    a = entry.get()
    b = math.radians(int(a))
    c = math.sin(b)
    d = round(c,1)
    entry.delete(0, tk.END)
    entry.insert(tk.END, d)

def cos(event):
    a = entry.get()
    b = math.radians(int(a))
    c = math.cos(b)
    d = round(c,1)
    entry.delete(0, tk.END)
    entry.insert(tk.END, d)

def tan(event):
    a = entry.get()
    b = math.radians(int(a))
    c = math.tan(b)
    d = round(c,1)
    entry.delete(0, tk.END)
    entry.insert(tk.END, d)

def kaijou(event):
    a = entry.get()
    b = int(a) * int(a)
    entry.delete(0, tk.END)
    entry.insert(tk.END, b)

