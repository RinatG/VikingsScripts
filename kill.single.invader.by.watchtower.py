# -*- coding: utf-8 -*-
from bot.penguee import Position, Region, Action
from java.awt.event import InputEvent, KeyEvent
#from win32gui import win32gui


# config ...
#invaderName = "royalguardsman"
#invaderName = "gascon"
invaderName = "khasar"
#invaderName = "maneater"
#invaderName = "celt"
# ... config

a = Action()

# обязательно поместить окно в эти координаты
x = 33
y = 33
wnd = Region(x, y, x+900, y+900)
wndHead = Region(x, y, x+80, y+30)
#

wndC = Position((wnd.p2.x-wnd.p1.x)/2+x, (wnd.p2.y-wnd.p1.y)/2+y)

toolbar = Region(240, 104, 444, 154)
watchtower = Region(wnd.p1.x + (wnd.p2.x-wnd.p1.x - 850)/2, wnd.p1.y + 149, wnd.p1.x + (wnd.p2.x-wnd.p1.x - 850)/2 + 850, wnd.p1.y + 149 +665)
relocate = Region(255, 490, 714, 642)
lair = Region(233, 171, 233+500, 171+598)

aroundPositions = [Position(-160, 0), Position(-70, 50), Position(0, 100), Position(70, 50), Position(160, 0)]

killedInvaders = 0;
shots = 0;

while True:
    # search Vikings window
    a.grab(wndHead.p1, wndHead.p2)
    a.searchRect(wndHead.p1, wndHead.p2)
    if a.find("vikings.ico") == False:
        print("Vikings not found")
        break
    
    # click on watchtower button
    a.grab(toolbar.p1, toolbar.p2)
    a.searchRect(toolbar.p1, toolbar.p2)    
    if a.findClick("vikings.watchtowerbutton"):
        coalRecentPos = a.recentPos()
        print(coalRecentPos.name)
        a.sleep(700)

        a.grab(watchtower.p1, watchtower.p2)
        a.searchRect(watchtower.p1, watchtower.p2)

        a.mouseMove(120, 420) # first invader
        while a.find("vikings.invaders."+invaderName) == False:            
            a.sleep(200)
            a.mouseWheel(300)
            a.sleep(200)
            a.grab(watchtower.p1, watchtower.p2)
            
        if a.findClick("vikings.invaders."+invaderName):
            a.sleep(800)
            a.grab(watchtower.p1, watchtower.p2)
            a.searchRect(watchtower.p1, watchtower.p2)
            #if a.findClick("vikings.yes") == False:
            #    print("Yes not found")
            a.mouseClick(390, 620) # Yes
            a.sleep(500)
            # отображение в центре окна wndC

            resultPosition = Position(0, 0)
            for i in range(len(aroundPositions)):
                a.mouseClick(wndC.add(aroundPositions[i]))
                a.sleep(700)
                a.grab(relocate.p1, relocate.p2)
                a.searchRect(relocate.p1, relocate.p2)
                if a.find("vikings.view"):
                    a.sleep(800)
                    a.findClick("vikings.Xclose")
                    a.sleep(800)
                    print("already on position")
                    resultPosition = Position(aroundPositions[i])
                    break
                elif a.findClick("vikings.relocate.buyandapply") or a.findClick("vikings.relocate.buyandapply2"):
                    a.sleep(800)
                    a.mouseClick(390, 620) # Yes
                    a.sleep(800)
                    print("found position")
                    resultPosition = Position(aroundPositions[i])
                    break
                else:
                    a.grab(wnd.p1.add(450, 0), wnd.p2.add(0, -450))
                    a.searchRect(wnd.p1.add(450, 0), wnd.p2.add(0, -450))
                    a.sleep(500)
                    a.findClick("vikings.Xclose")
                    a.sleep(500)

            print("ready to kill")
            a.mouseClick(wndC.add(-resultPosition.x, -resultPosition.y))
            a.sleep(600)

            shots = 0
            a.searchRect(lair.p1, lair.p2)
            while True:
                a.grab(lair.p1, lair.p2)
                if a.find("vikings.sustainedattack"):
                    a.sleep(150)
                    if a.find("vikings.normalattack"):
                        attack = a.findPos("vikings.normalattack")
                        a.mouseMove(attack)
                        a.sleep(150)
                        a.mouseClick(a.mousePos())
                        shots = shots + 1
                        a.sleep(400)
                        a.mouseMove(a.mousePos().add(15, 35))
                        a.sleep(1200)
                elif a.find("vikings.store"):
                    a.sleep(150)
                    a.findClick("vikings.store")
                    a.sleep(400)
                    a.grab(lair.p1, lair.p2)
                    if a.find("vikings.buyandapply"):
                        buy = a.findPos("vikings.buyandapply")
                    elif a.find("vikings.apply"):
                        buy = a.findPos("vikings.apply")
                    a.mouseMove(buy)
                    a.sleep(400)
                    a.mouseMove(buy.add(0, 40)) # More
                    a.sleep(300)
                    a.mouseClick(a.mousePos()) # More
                    a.sleep(500)
                    a.grab(lair.p1, lair.p2)
                    a.mouseClick(695, 650) # spinner
                    a.sleep(500)
                    a.findClick("vikings.buyandapply2") # Buy and apply
                    a.sleep(700)
##                    a.grab(lair.p1, lair.p2)
##                    a.findClick("vikings.Xclose") # X close
                    a.mouseClick(710, 260) # X close
                    a.sleep(600)

                    
                    
##                    a.mouseClick(600, 670) # Close
##                    a.sleep(200)
##                    a.mouseClick(640, 480) # Add
##                    a.sleep(400)
##                    a.mouseMove(660, 420) # Buy and apply
##                    a.sleep(500)
##                    a.mouseMove(660, 460) # More
##                    a.sleep(200)
##                    a.mouseClick(a.mousePos()) # More
##                    a.sleep(500)
##                    a.mouseClick(695, 650) # spinner
##                    a.sleep(500)
##                    a.mouseClick(365, 720) # Buy and apply
##                    a.sleep(700)
##                    a.mouseClick(710, 260) # X close
##                    a.sleep(600)
                elif a.find("vikings.tileamountof"):
                    killedInvaders = killedInvaders + 1
                    print("invader %s was killed in %s shots! killed %s invaders" % (invaderName, shots, killedInvaders))
                    a.sleep(200)
                    while a.findClick("vikings.Xclose") == True:
                        a.sleep(800)
                        a.grab(lair.p1, lair.p2)
                    break
                
                a.sleep(150)

##            a.grab(wnd.p1.add(450, 0), wnd.p2.add(0, -450))
##            a.searchRect(wnd.p1.add(450, 0), wnd.p2.add(0, -450))
##            a.sleep(3000)
##            a.findClick("vikings.Xclose")
##            a.sleep(800)
            
        else:
            print("invader " + invaderName + " not found")
            break
    else:
        print("watchtowerbutton not found")
        a.sleep(1200)
        a.grab(wnd.p1, wnd.p2)
        a.searchRect(wnd.p1, wnd.p2)
        while a.findClick("vikings.Xclose"):
            a.sleep(600)
            a.grab(wnd.p1, wnd.p2)

a.grab(wnd.p1, wnd.p2)
a.searchRect(wnd.p1, wnd.p2)
while a.findClick("vikings.Xclose"):
    a.sleep(200)
    a.grab(wnd.p1, wnd.p2)

print("Happy end!")
