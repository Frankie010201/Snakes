#coding=utf-8
'''
贪吃蛇
version: 1.0
Author: 陈舒天
Created: 09/02/17
functions;
1:  一条蛇 有头，身，尾
2： 在屏幕内，如果没有按键，就按一定速度一直向前，直到碰到屏幕外面，fail
3： 按方向键：上下左右，蛇头改变方向
4： 在一个随机的位置，出现食物
5： 按方向键，使蛇头朝向食物。等蛇头碰到食物，食物消失，蛇身长一节。食物在其他位置生成，不能碰到蛇身。
6： 蛇头不能碰到屏幕、自身。

version 2.0
1： 按一键，蛇头可穿屏幕边界。
2： 计分
3： 速度可选、可变
4： 蛇身可变形状、蛇头可变形状

version3.0
1： 。。。。

基本的数据结构：
。list

一个格，50 * 50
30 * 20个格
初始蛇头，占一个格，蛇尾一个格，蛇身5
初始位置：
蛇身的结构：x,y  一个list
方向
食物初始位置

蛇头前进一格
1，吃到食物
    食物变蛇头多一格
    新食物随机生成
2，没吃到食物
    前进方向前一格变蛇头，蛇尾少一格

多长时间，蛇头前进一格？


gameover：
x < 0 or x > margin
fx != x and fy != y

'''
import pygame
import sys
import logging
from pygame.locals import *
import random
import copy

keyBuff = None  # 上一次按键记录
logger =0 #for logging

#surface赋初值
snakeheadsurface = None
snakebodysurface = None
sanke = []

#图形尺寸
blockwidth = 50
blockheight = 50
Unitwidth = 30
Unitheight = 20
blankspace = 5
size = width, height = blockwidth * (Unitwidth + blankspace) , blockheight * (Unitheight)
#size = blockwidth * (Unitwidth) + blankspace , blockheight * (Unitheight)
layout = []
snake = []
InitialPOfsnakehead = [int(Unitwidth/2),int(Unitheight/2)]
InitialDirection = 'd'
Overlap = False
fx = 0
fy = 0
Timegap = 500
food = [0,0]

#snakebody初始位置
def sanke_init():
    global snake
    for i in range (7):
        snake.append([])
    snake[0].insert(0, InitialPOfsnakehead[0])
    snake[0].append(InitialPOfsnakehead[1])

    for i in range (1, 7):
        snake[i].insert(0, snake[i-1][0]-1)
        snake[i].append(snake[i-1][1])

#显示文本的函数
def printTxt(content, x, y, font, screen, color=(255, 255, 255)):
    '''显示文本
    args:
        content:待显示文本内容
        x,y:显示坐标
        font:字体
        screen:输出的screen
        color:颜色
    '''

    imgTxt = font.render(content, True, color)
    screen.blit(imgTxt, (x,y))
    # = "（x,y) = (%s,%s)  content = %s"  % (str(x), str(y),str(content))
    #logger.warning(msg)

#载入图片
def load_images():
    global foodimage,targetimage,Exit,Gameover
    foodimage = pygame.image.load('foodimage.png').convert()
    #targetimage = pygame.image.load('targetimage.png').convert()
    Exit = pygame.image.load('exit.png').convert()
    Gameover = pygame.image.load('gameover.png').convert()

#随机生成食物位置
def random_food():
    global layout,food,fx,fy,snake, overlap,logger
    overlap = 1

    while overlap > 0:
        overlap = 0
        fx = random.randint(0, Unitwidth - 1)
        fy = random.randint(0, Unitheight - 1)
        for i in range(len(snake)):
            if fx == snake[i][0] and fy == snake[i][1]:
                overlap =  1
    food = [fx,fy]

#判定是否吃到食物
def eating():
    global snake, food, snakeLast
    snake.append(snakeLast)

#向上移动
def Direction_UP():
    global snake
    tmp = copy.deepcopy(snake[0])
    tmp[1] -= 1
    snake.insert(0, tmp)
    snake.pop(len(snake) - 1)

#向下移动
def Direction_DOWN():
    global snake
    tmp = copy.deepcopy(snake[0])
    tmp[1] += 1
    snake.insert(0, tmp)
    snake.pop(len(snake) - 1)

#向右移动
def Direction_RIGHT():
    global snake
    tmp = copy.deepcopy(snake[0])
    tmp[0] += 1
    snake.insert(0,tmp)
    snake.pop(len(snake)-1)

#向左移动
def Direction_LEFT():
    global snake
    tmp = copy.deepcopy(snake[0])
    tmp[0] -= 1
    snake.insert(0, tmp)
    snake.pop(len(snake) - 1)

#绘制蛇头蛇身到surface
def drawsnake_init():
    global snakebodysurface, snakeheadsurface
    snakeheadsurfacesize = blockwidth, blockheight
    snakeheadsurface = pygame.Surface((snakeheadsurfacesize))
    snakeheadsurface.fill((255,255,255))
    pygame.draw.circle(snakeheadsurface, (20, 102, 12),(blockwidth / 2,blockheight / 2),blockwidth / 2)
    pygame.draw.circle(snakeheadsurface, (50, 110, 0),(blockwidth / 2,blockheight / 2),blockwidth / 3)

    snakebodysurfacesize =  blockwidth, blockheight
    snakebodysurface = pygame.Surface((snakebodysurfacesize))
    snakebodysurface.fill((255, 255, 255))
    pygame.draw.circle(snakebodysurface, (200,0,0), (blockwidth / 2, blockheight / 2), blockwidth / 2)
    pygame.draw.circle(snakebodysurface, (100,0,0 ), (blockwidth / 2, blockheight / 2), blockwidth / 3)

#将蛇头蛇身画到screen上
def draw_snake():
    #pygame.draw.circle(screen,(20,102,12),((snake[0][0] * blockwidth) + blockwidth/2 , (snake[0][1] * blockheight) + blockheight /2 ), blockwidth/2)
    #pygame.draw.circle(screen, (50, 110, 0),((snake[0][0] * blockwidth) + blockwidth / 2, (snake[0][1] * blockheight) + blockheight / 2),blockwidth / 3)
    screen.blit(snakeheadsurface,((snake[0][0] * blockwidth),(snake[0][1] * blockheight)))
    for i in range (1,len(snake)):
        #screen.blit(wallimage, ((snake[i][0] * blockwidth), (snake[i][1] * blockheight)))
        #pygame.draw.circle(screen,(200,0,0),((snake[i][0] * blockwidth) + blockwidth/2 , (snake[i][1] * blockheight) + blockheight /2 ), blockwidth/2)
        #pygame.draw.circle(screen, (100,0,0 ),((snake[i][0] * blockwidth) + blockwidth / 2, (snake[i][1] * blockheight) + blockheight / 2),blockwidth / 3)
        screen.blit(snakebodysurface,((snake[i][0] * blockwidth),(snake[i][1] * blockheight)))

#画出食物
def draw_food():
    screen.blit(foodimage, ((food[0] * blockwidth), (food[1] * blockheight)))

#绘制右侧文字区
def draw_blankspace():
    pygame.draw.rect(screen, (0,0,0), ((Unitwidth * blockwidth), 0, (blockwidth * blankspace) , (Unitheight * blockheight)), 0)
    #msg = "blankspace  length:  %s  " % (str(Unitwidth * blockwidth))
    #logger.warning(msg)

#在文字区打字
def write():
    defaultFont = pygame.font.Font("yh.ttf", 20)  # yh.ttf这个字体文件请自行上网搜索下载，如果找不到就随便用个ttf格式字体文件替换一下。
    #backSurface = pygame.Surface((width,height))
    #=================================================================
    # #这个backSurface 最后没有blit到screen上去，所以文字没有看到。
    # =================================================================
    #printTxt("Length : %s " %(len(snake)), (Unitwidth * blockwidth), (Unitheight * blockheight)/2, defaultFont, backSurface, (255,255,255))
    printTxt("W for UP", (Unitwidth * blockwidth), (Unitheight * blockheight) / 6,defaultFont,screen, (255, 255, 255))
    printTxt("S for down", (Unitwidth * blockwidth), (Unitheight * blockheight) / 6 + 50,defaultFont,screen, (255, 255, 255))
    printTxt("A for left", (Unitwidth * blockwidth), (Unitheight * blockheight) / 6 + 100,defaultFont,screen, (255, 255, 255))
    printTxt("D for right", (Unitwidth * blockwidth), (Unitheight * blockheight) / 6 + 150,defaultFont,screen, (255, 255, 255))
    printTxt("x/Esc for exit", (Unitwidth * blockwidth), (Unitheight * blockheight) / 6 + 200, defaultFont, screen,(255, 255, 255))
    printTxt("Length:  %s " %str(len(snake)), (Unitwidth * blockwidth), 3*(Unitheight * blockheight)/6 , defaultFont, screen, (255,255,255))
    printTxt("Time:  %s s " %str(pygame.time.get_ticks() // 1000), (Unitwidth * blockwidth), 4*(Unitheight * blockheight) / 6, defaultFont,screen, (255, 255, 255))
    #printTxt("Length : %s " %(len(snake)), 100, 100, defaultFont, screen, (0,0,255))
    #msg = " %s" % (str(Unitwidth * blockwidth))
    #logger.warning(msg)


    if len(snake) > Record:
        printTxt("New Record: %s " %str(len(snake)), (Unitwidth * blockwidth), 5 * (Unitheight * blockheight) / 6, defaultFont,screen, (255, 0, 0))
    else:
        printTxt("Best Record: %s " % str(Record), (Unitwidth * blockwidth), 5 * (Unitheight * blockheight) / 6,defaultFont, screen, (255, 255, 255))


def main():
    global snake, food, snakeLast,screen, keyBuff,Time,Record
    FormerOrder = InitialDirection
    Death = False
    Exitcode = 0

    clock = pygame.time.Clock()
    random_food()

    # 第一步，创建一个logger
    global logger

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关

    # 第二步，创建一个handler，用于写入日志文件
    # logfile = './log/logger.txt'
    # fh = logging.FileHandler(logfile, mode='w')
    # fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

    # 第三步，再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关

    # 第四步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    # fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 第五步，将logger添加到handler里面
    # logger.addHandler(fh)
    logger.addHandler(ch)

    #初始化，创建窗口
    pygame.init()
    sanke_init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('贪吃蛇')

    #窗口中隐藏鼠标
    pygame.mouse.set_visible(False)
    #载入蛇头蛇身surface
    drawsnake_init()

    load_images()

    #Timmer计时器
    MYTIMER = USEREVENT + 1
    pygame.time.set_timer(MYTIMER, Timegap)

    #读取文档中先前最高纪录
    FileHandle = open('Record.txt', 'r')
    lineOfFile = FileHandle.readline()
    Record = int(lineOfFile)
    FileHandle.close()

    #程序主循环
    while Death == False:
        Order = 0

        #处理event
        for event in pygame.event.get():

            #msg = "event type : %s   Length : %s" % (str(event.type), str(len(snake)) )
            #logger.warning(msg)
            snakeLast = snake[len(snake) - 1]
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                #msg = "event key:  %s  " % (str(event.key))
                #logger.warning(msg)
                if event.key == K_w or event.key == K_UP:
                    if FormerOrder == 'a' or  FormerOrder == 'd' or FormerOrder == 'w':
                        Direction_UP()
                        FormerOrder = 'w'
                        Order = 1

                elif event.key == K_s or event.key == K_DOWN:
                    if FormerOrder == 'a' or FormerOrder == 'd'or FormerOrder == 's':
                        Direction_DOWN()
                        FormerOrder = 's'
                        Order = 1

                elif event.key == K_a or event.key == K_LEFT:
                    if FormerOrder == 'w' or FormerOrder == 's' or FormerOrder == 'a':
                        Direction_LEFT()
                        FormerOrder = 'a'
                        Order = 1

                elif event.key == K_d or event.key == K_RIGHT:
                    if FormerOrder == 'w' or FormerOrder == 's' or FormerOrder == 'd':
                        Direction_RIGHT()
                        FormerOrder = 'd'
                        Order = 1

                elif event.key == K_x or event.key == K_ESCAPE:
                    Exitcode = 1
                    break

                if Order == 1 :
                    #pygame.time.set_timer(MYTIMER, 0)
                    pygame.time.set_timer(MYTIMER, Timegap)

            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_DOWN or event.key == K_UP:
                    keyBuff = None
            elif event.type == MYTIMER:
                if Order != 1:
                    if FormerOrder == 'w':
                        Direction_UP()
                    elif FormerOrder == 's':
                        Direction_DOWN()
                    elif FormerOrder == 'a':
                        Direction_LEFT()
                    elif FormerOrder == 'd':
                        Direction_RIGHT()

        if snake[0][0]< 0 :
            snake[0][0] = Unitwidth - 1

        elif snake[0][0]> (Unitwidth - 1):
            snake[0][0] = 0

        elif snake[0][1]<0:
            snake[0][1] = Unitheight - 1

        elif snake[0][1]> (Unitheight - 1):
            snake[0][1] = 0

        for i in range (1,len(snake)):
            if snake[i][0] == snake[0][0] and snake[i][1] == snake[0][1]:
                Death = True

        if snake[0][0] == food[0] and snake[0][1] == food[1]:
            eating()
            random_food()

        if Exitcode == 1:
            break

        screen.fill((255,255,255))
        draw_food()
        draw_snake()
        draw_blankspace()
        write()

        #msg = "food: %s snake: %s Time: %s" % (str(food), str(snake),str(MYTIMER))
        #logger.warning(msg)

        pygame.display.update()
        clock.tick(30)

    if len(snake) > Record:
        FileHandle = open('Record.txt', 'w')
        FileHandle.write(str(len(snake)))
        FileHandle.close()

    if Exitcode == 1:
        screen.blit(Exit, ((screen.get_rect().width - Exit.get_rect().width) / 2, (screen.get_rect().height - Exit.get_rect().height) / 2))
    elif Death == True:
        screen.blit(Gameover, ((screen.get_rect().width - Gameover.get_rect().width) / 2, (scre4en.get_rect().height - Gameover.get_rect().height) / 2))


    pygame.display.update()
    pygame.time.delay(3000)


main()

