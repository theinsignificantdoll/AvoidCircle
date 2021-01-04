import pygame
import random


open("s.score", "a").close()

dimensionmultiplier = [0.8, 0.8]
width = 1920
height = 1080
playersize = 100
enemylist = []
plname = "N/A"
writingname = False
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
GRAY = (114, 114, 114)
RED = (189, 0, 0)
PINK = (255, 128, 128)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 245, 85 )
ORANGE = (255, 128, 0)
px = width//2
py = height//2
xsp = 0
ysp = 0
gameover = True
x1sp = 0
x2sp = 0
y1sp = 0
y2sp = 0
points = 0
ps = 0
attacklist = []
stamina = 0
stambackbone = 0
stamdiv = 4
gameovertext = "BALLET OF BALLS"
showingscores = False
scorescroll = 1
speedmulti = 1


def coord(coord, d):
    global dimensionmultiplier
    return int(coord*dimensionmultiplier[d])


def addenemy():
    if not gameover:
        if random.choice((True, False)):
            if random.choice((True, False)):
                enemylist.append(
                    [0, random.randint(0, 1080), random.randint(2, 8), random.randint(-8, 8), random.randint(50, 150)])
            else:
                enemylist.append(
                    [1920, random.randint(0, 1080), random.randint(-7, -2), random.randint(-8, 8), random.randint(50, 150)])
        else:
            if random.choice((True, False)):
                enemylist.append(
                    [random.randint(0, 1920), 0, random.randint(-8, 2), random.randint(2, 8), random.randint(50, 150)])
            else:
                enemylist.append(
                    [random.randint(0, 1920), 1080, random.randint(-8, 2), random.randint(-8, -2), random.randint(50, 150)])


def seconditem(elem):
    return elem[1]


def rearrangescorelist():
    f = open("s.score", "r")
    scores = []
    for line in f.readlines():
        if len(line) >= 5:
            scores.append([line[:3], int(line[5:])])
    f.close()
    open("s.score", "w+").close()
    f = open("s.score", "a")
    finallist = sorted(scores, reverse=True, key=seconditem)
    num = 0
    if len(finallist) > 100:
        finallist = finallist[:100]
    finallistlen = len(finallist)
    for line in finallist:
        num += 1
        f.write(line[0] + ", " + str(line[1]))
        if num != finallistlen:
            f.write("\n")
    f.close()


addenemy()

pygame.init()

screen = pygame.display.set_mode((coord(width, 0), coord(height, 1)))

pygame.display.set_caption("BALLET OF BALLS")

done = False


clock = pygame.time.Clock()

# enemytemplate = [x, y, xspeed, yspeed, size]


class attacks:
    global enemylist

    def circle(info):
        radius = info[0]
        maxradius = info[1]
        width1 = info[2]
        color1 = info[3]
        speed = info[4]
        x = info[5]
        y = info[6]
        global ps
        toberemoved = []
        radius += speed
        if radius > maxradius:
            return [False]
        for enemy in range(0, len(enemylist)):
            if (enemylist[enemy][0] - x)**2 + (y - enemylist[enemy][1])**2 <= (radius+enemylist[enemy][4]//2)**2:
                toberemoved.append(enemylist[enemy])
                ps += 200

        pygame.draw.ellipse(screen, color1, [coord(x-radius, 0), coord(y-radius, 1),
                                                 coord(radius*2, 0), coord(radius*2, 1)], width1)

        for matter in toberemoved:
            enemylist.remove(matter)

        return [radius, maxradius, width1, color1, speed, x, y]


def gameoverf():
    global gameover
    global gameovertext
    gameovertext = "GAMEOVER"
    enemylist = []
    if not gameover:
        f = open("s.score", "a")
        f.write("\n" + plname + ", " + str(points))
        f.close()
    rearrangescorelist()
    gameover = True


def updateallenemies():
    global enemylist
    global gameover
    global screen

    toberemoved = []
    for enemy in range(0, len(enemylist)):
        if (enemylist[enemy][0]-px)**2 + (py-enemylist[enemy][1])**2 <= (enemylist[enemy][4]//2+playersize)**2:
            gameoverf()
            toberemoved.append(enemylist[enemy])
            break
        enemylist[enemy][0] += enemylist[enemy][2]*speedmulti
        enemylist[enemy][1] += enemylist[enemy][3]*speedmulti
        pygame.draw.ellipse(screen, RED, [coord(enemylist[enemy][0]-enemylist[enemy][4]//2, 0), coord(enemylist[enemy][1]-enemylist[enemy][4]//2, 1),
                                          coord(enemylist[enemy][4], 0), coord(enemylist[enemy][4], 1)])
        if enemylist[enemy][0] < 0-enemylist[enemy][4] or enemylist[enemy][1] < 0-enemylist[enemy][4] or gameover:
            toberemoved.append(enemylist[enemy])
        elif enemylist[enemy][0] > width+enemylist[enemy][4] or enemylist[enemy][1] > height+enemylist[enemy][4]:
            toberemoved.append(enemylist[enemy])

    for x in toberemoved:
        enemylist.remove(x)


def showscores():
    fontlist = pygame.font.SysFont('Times New Roman', 70, True, False)
    f = open("s.score", "r")
    lines = f.readlines()
    for k in range(0, (len(lines)-100)*-1):
        lines.append("NONE, N/A")
    mtext = fontlist.render(str(1 + (scorescroll-1) * 10) + " - " + str(scorescroll * 10), True, GREEN)
    fontlist = pygame.font.SysFont('Calibri', 60, True, False)
    screen.blit(mtext, [coord(width // 2 - mtext.get_size()[0] // 2, 0), coord(10, 1)])
    for mn in range(0, 10):
        page = (scorescroll-1)*10
        mtext = fontlist.render(lines[mn+page].rstrip("\n"), True, WHITE)
        screen.blit(mtext, [coord(width//2 - mtext.get_size()[0] // 2, 0), coord(100+75*mn, 1)])
    f.close()


def displaystamina():
    if px > 440+playersize or py > 100+playersize:
        pygame.draw.rect(screen, BLACK, [coord(21, 0), coord(21, 1), coord(402, 0), coord(58, 1)])
        pygame.draw.rect(screen, WHITE, [coord(18, 0), coord(18, 1), coord(408, 0), coord(64, 1)], 6)
        part = stamina
        if part > 100:
            part = 100
        pygame.draw.rect(screen, RED, [coord(23, 0), coord(23, 1), coord(part, 0), coord(55, 1)])
        part = stamina-100
        if stamina > 100:
            if part > 100:
                part = 100
            pygame.draw.rect(screen, ORANGE, [coord(123, 0), coord(23, 1), coord(part, 0), coord(55, 1)])
        part = stamina - 200
        if stamina > 200:
            if part > 100:
                part = 100
            pygame.draw.rect(screen, YELLOW, [coord(223, 0), coord(23, 1), coord(part, 0), coord(55, 1)])
        if stamina > 300:
            part = stamina - 300
            if part > 100:
                part = 100
            pygame.draw.rect(screen, GREEN, [coord(323, 0), coord(23, 1), coord(part, 0), coord(55, 1)])



while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                if writingname is True:
                    plname = plname + "B"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_c:
                if writingname is True:
                    plname = plname + "C"
                    if len(plname) >= 3:
                        writingname = False

            if event.key == pygame.K_e:
                if writingname is True:
                    plname = plname + "E"
                    if len(plname) >= 3:
                        writingname = False

                elif gameover and showingscores:
                    showingscores = False
                    scorescroll = 1
                elif gameover and not writingname:
                    showingscores = True

            if event.key == pygame.K_f:
                if writingname is True:
                    plname = plname + "F"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_g:
                if writingname is True:
                    plname = plname + "G"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_h:
                if writingname is True:
                    plname = plname + "H"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_i:
                if writingname is True:
                    plname = plname + "I"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_j:
                if writingname is True:
                    plname = plname + "J"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_k:
                if writingname is True:
                    plname = plname + "K"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_l:
                if writingname is True:
                    plname = plname + "L"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_m:
                if writingname is True:
                    plname = plname + "M"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_o:
                if writingname is True:
                    plname = plname + "O"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_p:
                if writingname is True:
                    plname = plname + "P"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_q:
                if writingname is True:
                    plname = plname + "Q"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_r:
                if writingname is True:
                    plname = plname + "R"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_t:
                if writingname is True:
                    plname = plname + "T"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_u:
                if writingname is True:
                    plname = plname + "U"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_v:
                if writingname is True:
                    plname = plname + "V"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_x:
                if writingname is True:
                    plname = plname + "X"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_y:
                if writingname is True:
                    plname = plname + "Y"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_z:
                if writingname is True:
                    plname = plname + "Z"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_LEFT:
                x1sp -= 20
            if event.key == pygame.K_RIGHT:
                x2sp += 20
            if event.key == pygame.K_UP:
                y1sp -= 20
                if showingscores:
                    scorescroll -= 1
                    if scorescroll < 1:
                        scorescroll = 1
            if event.key == pygame.K_DOWN:
                y2sp += 20
                if showingscores:
                    scorescroll += 1
                    if scorescroll > 10:
                        scorescroll = 10
            if event.key == pygame.K_a:
                x1sp -= 20
                if writingname is True:
                    plname = plname + "A"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_d:
                x2sp += 20
                if writingname is True:
                    plname = plname + "D"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_w:
                y1sp -= 20
                if showingscores:
                    scorescroll -= 1
                    if scorescroll < 1:
                        scorescroll = 1
                if writingname is True:
                    plname = plname + "W"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_s:
                y2sp += 20
                if showingscores:
                    scorescroll += 1
                    if scorescroll > 10:
                        scorescroll = 10
                if writingname is True:
                    plname = plname + "S"
                    if len(plname) >= 3:
                        writingname = False
            if event.key == pygame.K_n:
                if writingname is True:
                    plname = plname + "N"
                    if len(plname) >= 3:
                        writingname = False
                elif writingname is False and gameover is True and not showingscores:
                    writingname = True
                    plname = ""
            if event.key == pygame.K_SPACE:
                if stamina > 100 and not gameover:
                    if stamina > 300:
                        attacklist.append([playersize + 30, playersize * 5, 30, BLUE, 10, px, py])
                    elif stamina > 200:
                        attacklist.append([playersize + 30, playersize * 4, 30, GREEN, 10, px, py])
                    elif stamina > 100:
                        attacklist.append([playersize + 30, playersize * 3, 30, YELLOW, 10, px, py])
                    else:
                        attacklist.append([playersize + 30, playersize * 2, 30, ORANGE, 10, px, py])
                    stambackbone -= stamdiv * 100
                elif ysp == 0 and xsp == 0 and not writingname:
                    gameover = False
                    ps = 0
                    gameoverwait = -1
                    showingscores = False
                    scorescroll = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x1sp = 0
            if event.key == pygame.K_RIGHT:
                x2sp = 0
            if event.key == pygame.K_UP:
                y1sp = 0
            if event.key == pygame.K_DOWN:
                y2sp = 0
            if event.key == pygame.K_a:
                x1sp = 0
            if event.key == pygame.K_d:
                x2sp = 0
            if event.key == pygame.K_w:
                y1sp = 0
            if event.key == pygame.K_s:
                y2sp = 0

    xsp = x1sp + x2sp
    ysp = y1sp + y2sp

    screen.fill(BLACK)

    # attacks.circle([100, 1000, 10, RED, 50, px, py])

    if gameover and not showingscores:
        font1 = pygame.font.SysFont('Calibri', 100, True, True)
        font3 = pygame.font.SysFont('Calibri', 70, True, True)
        font2 = pygame.font.SysFont("Calibri", 30, True, True)
        pressn = font2.render("Press N to define name", True, WHITE)
        presse = font2.render("Press E to see scores", True, WHITE)
        text = font1.render(gameovertext, True, WHITE)
        nametext = font3.render(plname, True, WHITE)
        pressspace = font2.render("Press SPACE to continue", True, WHITE)
        screen.blit(presse, [coord(width-presse.get_size()[0]-70, 0), coord(height-(presse.get_size()[1]+20), 1)])
        screen.blit(pressn, [coord(width-pressn.get_size()[0]-70, 0), coord(80, 1)])
        screen.blit(nametext, [coord(width-(nametext.get_size()[0]+50), 0), coord(0, 1)])
        screen.blit(text, [coord((width//2)-(text.get_size()[0]//2), 0), coord((height//2)-(text.get_size()[1]//2), 1)])
        screen.blit(pressspace, [coord((width//2)-(pressspace.get_size()[0]//2), 0),
                                 coord(((height//2)-(pressspace.get_size()[1])//2)+100, 1)])
        stambackbone = 0
        px = width//2
        py = height//2
    elif gameover and showingscores:
        showscores()
        px = width // 2
        py = height // 2
    else:
        plspeedmulti = speedmulti
        if plspeedmulti < 1:
            plspeedmulti = 1
        px += xsp*(plspeedmulti)
        py += ysp*(plspeedmulti)
        pygame.draw.ellipse(screen, WHITE, [coord(px - playersize, 0), coord(py - playersize, 1),
                                            coord(playersize*2, 0), coord(playersize*2, 1)])
        ps += 1
        points = ps//15
        speedmulti = points/10000+1
        if stamina > 300:
            stambackbone += 0.1*speedmulti
        elif stamina > 200:
            stambackbone += 0.5*speedmulti
        elif stamina > 100:
            stambackbone += 1*speedmulti
        else:
            stambackbone += 1.5*speedmulti
        stamina = stambackbone // stamdiv
        if stamina > 400:
            stambackbone = 400*stamdiv

    if px+playersize > width or px-playersize < 0:
        gameoverf()
    elif py+playersize > height or py-playersize < 0:
        gameoverf()

    if random.randint(1, 40) == 1 and not gameover:
        addenemy()

    if len(enemylist) < 3 and not gameover:
        addenemy()


    toberemoved = []
    for i in range(0, len(attacklist)):
        n = attacks.circle(attacklist[i])
        if n[0] is False:
            toberemoved.append(attacklist[i])
        else:
            attacklist[i] = n

    for m in toberemoved:
        attacklist.remove(m)

    pointfont = pygame.font.SysFont('Calibri', 50, True, True)
    pointtext = pointfont.render("Score: " + str(points), True, WHITE)
    if pointtext.get_size()[0]+130+playersize < px or 1000-playersize > py:
        screen.blit(pointtext, [coord(30, 0), coord(1000, 1)])

    updateallenemies()

    displaystamina()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
