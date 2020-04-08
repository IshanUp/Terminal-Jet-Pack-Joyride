import os
import signal
from time import time, sleep
from alarmexcpetion import AlarmException
from getInput import _getChUnix as getChar
from board import *
from Mandalorian import *
from Boss import *
from bullet import *
import colorama
init(autoreset=True)

a = Generate(40, 500)
a.genSky()
a.genGround()
a.genBeams()
a.genBoost()
a.genMag()
# bulletobj = Bullet(30,20,a)

# bulletobj.set_position(a,35,30) #coordinate system same as mando
# bulletobj.remove(a)
bulletList = []
b = Mando(35, 20, a)
# for a = Generate(40,200) , (3,191) is top right (32,191) is bottom right
boss = Bossman(32, 491, a, b)
uptime = 0
# lol = bossBull(10,10,a,b)
# lol.set_position(a,10,10)


def move():

    # encapsulation
    # input handelling
    def alarmhandler(signum, frame):
        raise AlarmException

    def user_input(timeout=0.15):
        signal.signal(signal.SIGALRM, alarmhandler)
        signal.setitimer(signal.ITIMER_REAL, timeout)

        try:
            text = getChar()()
            signal.alarm(0)
            return text

        except AlarmException:
            pass

        signal.signal(signal.SIGALRM, signal.SIG_IGN)

        return ''

    char = user_input()

    if char == 'd':
        b.disappear_mando(a)
        if (boost == 1):
            b.disappear_mando(a)
            b.set_position(a, b.xco, b.yco + 2)
        else:
            if(right - 3 < b.yco):
                b.set_position(a, b.xco, right - 2)
            else:
                b.set_position(a, b.xco, b.yco + 1)
        return 1
    if char == 'a':
        b.disappear_mando(a)
        if boost == 1:
            b.disappear_mando(a)
            b.set_position(a, b.xco, b.yco - 2)
        else:
            if(left + 3 > b.yco):
                b.set_position(a, b.xco, left + 2)
            else:
                b.set_position(a, b.xco, b.yco - 1)

        return 1
    if char == 'w':
        air = 0
        uptime = time.time()
        b.disappear_mando(a)
        boss.disappear(a)
        boss.set_position(a, boss.xco - 1, boss.yco)
        if boost == 1:
            b.disappear_mando(a)
            b.set_position(a, b.xco - 2, b.yco)
        else:
            if(left + 3 > b.yco):
                b.set_position(a, b.xco - 1, left + 2)
            elif(right - 3 < b.yco):
                b.set_position(a, b.xco - 1, right - 2)
            else:
                b.set_position(a, b.xco - 1, b.yco)
        return 0
    if char == " ":
        shield = 1
        if (time.time() - b.downTime() >= 10):
            b.activateShield()
    if char == "b":
        # bulletobj.set_position(a,b.xco,b.yco +2)
        bulletobj = Bullet(b.xco, b.yco, a, boss)
        bulletobj.shoot(a, b.xco, b.yco + 2)
        bulletList.append(bulletobj)
        return 0
    if not char:

        if(right - 3 < b.yco and boost == 0):
            b.disappear_mando(a)
            b.set_position(a, b.xco, right - 2)
        if(left + 3 > b.yco and boost == 0):
            b.disappear_mando(a)
            b.set_position(a, b.xco, left + 2)

    if char == 'q':
        quit()
    else:
        return 1


x = 0.4
left = 0
right = 100
before = time.time()
nf = before + x
i = 0
coinCount = 0
endtime = 0
starttime = time.time()
prev = 0
score = 0
boost = 0
shield = 0
livechangeTimer = 0
bossInFrame = 0
air = 1
snowlist = []

while True:
    air = 1
    currenttime = time.time() - starttime
    # os.system("clear")
    print("\033[0;0H")
    now = time.time()
    print("coins", coinCount)
    print("Score", score + 10*abs((3-boss.lives)))
    print("Lives", b.lives)
    timeleft = 80 - int(currenttime)
    print("Time Left", timeleft)
    # print("Boost",boost)
    if(bossInFrame == 1):
        print("Boss", boss.lives)
    # if(boost == 1):
     #   print("boosttimer",now - boostTimer)
    # if (b.shield() == 1):
     #   print("SHEILD ON",now - b.startTime())

    if(boss.lives <= 0):
        os.system("clear")
        print("Game Completed!  You saved baby yoda! ")
        highscore = 0
        score = score+10*abs((3-boss.lives))
        with open("score", 'r') as scorelist:
            for ascore in scorelist:
                ascore = ascore.rstrip("\n")
                if(highscore < int(ascore)):
                    highscore = int(ascore)
        if(score > highscore):
            print(Fore.YELLOW+"Congrats! New High Score!!")
        else:
            print("High Score: ", highscore)
        f = open("score", "a")
        f.write(str(score) + "\n")
        f.close()
        print("Score", score)
        f = open("yoda", "r")
        for line in f:
            print(line, end="")
        print()
        quit()
    rowVal = b.xco
    colVal = b.yco

    if(b.lives <= 0 or timeleft == 0):
        os.system("clear")
        print("Game Over")
        highscore = 0
        with open("score", 'r') as scorelist:
            for ascore in scorelist:
                ascore = ascore.rstrip("\n")
                if(highscore < int(ascore)):
                    highscore = int(ascore)
        if(score > highscore):
            print(Fore.YELLOW+"Congrats! New High Score!!")
        else:
            print("High Score: ", highscore)
        f = open("score", "a")
        f.write(str(score) + "\n")
        f.close()
        print("Score", score)
        quit()

    for obj in bulletList:
        obj.move()
    for obj in snowlist:
        try:
            inter = len(b.mandopos().intersection(obj.bulletcord()))
            if (inter > 0):
                if(shield == 0):
                    b.decreaseLives()
            obj.move()
        except:
            pass

    if boost == 1 and int(now-boostTimer) > 5:
        boost = 0
    if b.shield() == 1 and int(now - b.startTime()) > 5:
        b.deactivateShield()
    try:
        inter = len(b.mandopos().intersection(a.colisionList()))
    except:
        inter = 0
    if(inter > 0 and int(now - livechangeTimer > 3)):
        if (b.lives > 1):
            for colobj in b.mandopos().intersection(a.colisionList()):
                a.removeCollisionList(colobj)
            if(b.shield() == 0):
                b.decreaseLives()
            else:
                b.deactivateShield()
            livechangeTimer = time.time()
        else:
            print("\033[0;0H")
            os.system("clear")
            highscore = 0
            with open("score", 'r') as scorelist:
                for ascore in scorelist:
                    ascore = ascore.rstrip("\n")
                    if(highscore < int(ascore)):
                        highscore = int(ascore)
            if(score > highscore):
                print(Fore.YELLOW+"Congrats! New High Score!!")
            else:
                print("High Score: ", highscore)
            f = open("score", "a")
            f.write(str(score) + "\n")
            f.close()
            print("Score", score)
            print("Game Over!")
            quit()

    try:
        length = len(b.mandopos().intersection(a.coinsList()))
        if (length > 0):
            for coinobj in b.mandopos().intersection(a.coinsList()):
                a.removeCoinsList(coinobj)
                coinCount += 1
    except:
        pass

    try:
        length = len(b.mandopos().intersection(a.boostList()))
        if (length > 0):
            for boostobj in b.mandopos().intersection(a.boostList()):
                a.removeBoostList(coinobj)
                score += 1
                boost = 1
                boostTimer = now+2
    except:
        pass

    try:
        length = len(b.mandopos().intersection(a.magList()))
        if (length > 0):
            b.disappear_mando(a)
            b.set_position(a, b.xco, b.yco - 1)
    except:
        pass

    try:
        length = len(b.mandopos().intersection(a.rightmagList()))
        if (length > 0):
            b.disappear_mando(a)
            b.set_position(a, b.xco, b.yco + 1)
    except:
        pass

    # for pos in b.mandopos():
        # if pos in a.coinsList():
        #   a.removeCoinsList(pos)
        #  coinCount+=1
        # if pos in a.boostList():
        #   a.removeBoostList(pos)
        # boost = 1
        # boostTimer = now + 2
        # if pos in a.magList():
        #   b.disappear_mando(a)
        #  b.set_position(a,b.xco,b.yco -1)
    if(0.05 < currenttime-endtime and boost == 0):
        if(prev+100 < a.colnum()):
            endtime = currenttime
            a.printit(prev)
            left = prev
            right = 100 + left
            prev += 1

        elif(bossInFrame == 0):
            a.printit(prev-1)
            left = prev - 1
            right = 100 + left
            bossInFrame = 1
            bosstimer = time.time()
        elif(bossInFrame == 1):
            a.printit(prev-1)
            left = prev - 1
            right = 100 + left
            if(int(time.time()-bosstimer) % 5 == 0):
                snow = bossBull(boss.xco - 2, boss.yco - 4, a, b)
                snow.shoot(a, boss.xco, boss.yco - 3)
                snowlist.append(snow)

    before = time.time()
    score = coinCount + int((before - starttime)/1)
    if (0.1 < currenttime-endtime and boost == 1):
        if(prev+100 < a.colnum()):
            endtime = currenttime
            a.printit(prev)
            prev += 2

        else:
            a.printit(prev-1)
    before = time.time()
    score = coinCount + int((before - starttime)/1)

    air = move()

    if(b.xco < 35 and before > nf and air == 1):
        b.disappear_mando(a)
        b.set_position(a, b.xco + 1, b.yco)
        if(boss.xco < 32):
            boss.disappear(a)
            boss.set_position(a, boss.xco + 1, boss.yco)
        before = time.time()
#        if (30<b.xco<35):
 #           x = 0.2
  #      if (20<b.xco<30):
   #         x = 0.1
    #    if (10<b.xco<20):
     #       x = 0.3
      #  if (1<b.xco<20):
       #     x = 0.4
        x = x*0.000001
        nf = before + x
