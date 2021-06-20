# -*- coding: utf-8 -*-
from bot.penguee import Position, Region, Action
from java.awt.event import InputEvent, KeyEvent
#from win32gui import win32gui

maxHits = 0

# config ... vikings.invaders.
#invaderName = "royalguardsman"
#invaderName = "gascon"
#invaderName = "khasar"
#invaderName = "maneater"
#invaderName = "celt"
#invaderName = "wildboar"
#invaderName = "hounds"
#invaderName = "lynx"
#invaderName = "saracen"
#invaderName = "serpent"
#invaderName = "cavelion"
#invaderName = "canis"
#invaderName = "hun"
#invaderName = "barbarian"

#invaderName = "abbysguard"
#invaderName = "northernvulture"
#invaderName = "moonwolf"
invaderName = "rockboar"
#invaderName = "plagueraven"
#invaderName = "helheimwarrior"
#invaderName = "waylandsbride"
#invaderName = "jotunheimursus"
#invaderName = "marshnixa"

maxHits = 20
# ... config
print ("configuration: invaderName=%s, maxHits=%s" % (invaderName, maxHits))

a = Action()
a.setMouseDelay(320)

# обязательно поместить окно в эти координаты
x = 33
y = 33
wnd = Region(x, y, x+900, y+900)
wndHead = Region(x, y, x+80, y+30)
#

wndC = Position((wnd.p2.x-wnd.p1.x)/2+x, (wnd.p2.y-wnd.p1.y)/2+y)

toolbar = Region(240, 104, 444, 154)
watchtower = Region(wnd.p1.x + (wnd.p2.x-wnd.p1.x - 850)/2, wnd.p1.y + 149, wnd.p1.x + (wnd.p2.x-wnd.p1.x - 850)/2 + 850, wnd.p1.y + 149 +665)
relocate = Region(230, 230, 730, 760)
lair = Region(233, 171, 233+500, 171+598)

aroundPositions = [Position(-160, 0), Position(160, 0), Position(-70, 50), Position(70, 50), Position(70, -50), Position(-70, -50), Position(0, 100)]

killedInvaders = 0;
shots = 0;

icoPosition = Position(wnd.p1.x, wnd.p1.y)

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
        a.sleep(700)
        a.mouseMove(a.mousePos().add(50, 10))
        print("watchtowerbutton was found and clicked")

        # check if watchtower is open
        a.grab(watchtower.p1, watchtower.p2)
        a.searchRect(watchtower.p1, watchtower.p2)
        while a.find("vikings.navigator") == False:
            print("watchtower's navigator not found")
            a.grab(toolbar.p1, toolbar.p2)
            a.searchRect(toolbar.p1, toolbar.p2)
            if a.findClick("vikings.watchtowerbutton"):
                a.sleep(200)
                a.mouseMove(a.mousePos().add(50, 10))
                break
            a.grab(watchtower.p1, watchtower.p2)
            a.searchRect(watchtower.p1, watchtower.p2)
            a.sleep(200)

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
                a.sleep(600)
                a.grab(relocate.p1, relocate.p2)
                a.searchRect(relocate.p1, relocate.p2)
                if a.find("vikings.location.view"):
                    a.sleep(800)
                    # a.findClick("vikings.Xclose")
                    a.mouseClick(710, 320) # X close
                    a.sleep(800)
                    print("already on position")
                    resultPosition = Position(0, 0)
                    break
                elif a.findClick("vikings.relocate.buyandapply"):
                    a.sleep(800)
                    a.mouseClick(390, 620) # Yes
                    a.sleep(800)
                    print("found position")
                    resultPosition = Position(aroundPositions[i])
                    break
                elif a.find("vikings.relocate.relocation"):
                    a.sleep(800)
                    a.mouseClick(610, 630) # Buy and apply
                    a.sleep(300)
                    a.mouseClick(390, 620) # Yes
                    a.sleep(800)
                    print("found position")
                    resultPosition = Position(aroundPositions[i])
                    break
                elif a.findClick("vikings.relocate.apply"):
                    a.sleep(800)
                    a.mouseClick(390, 620) # Yes
                    a.sleep(800)
                    print("found position")
                    resultPosition = Position(aroundPositions[i])
                    break
                elif a.find("vikings.location.level"):
                    print("found level")
                    while a.find("vikings.location.Xclose"):
                        a.findClick("vikings.location.Xclose")
                        a.sleep(200)
                        a.mouseMove(a.mousePos().add(50, 50))
                        a.sleep(600)
                        a.grab(relocate.p1, relocate.p2)
                elif a.find("vikings.occupied"):
                    print("found occupied")
                    a.grab(wnd.p1, wnd.p2)
                    a.searchRect(wnd.p1, wnd.p2)
                    while a.find("vikings.close"):
                        a.findClick("vikings.close")
                        a.sleep(200)
                        a.mouseMove(a.mousePos().add(50, 50))
                        a.sleep(600)
                        a.grab(wnd.p1, wnd.p2)
                elif a.find("vikings.close"):
                    print("found close")
                    a.grab(wnd.p1, wnd.p2)
                    a.searchRect(wnd.p1, wnd.p2)
                    while a.find("vikings.close"):
                        a.findClick("vikings.close")
                        a.sleep(200)
                        a.mouseMove(a.mousePos().add(50, 50))
                        a.sleep(600)
                        a.grab(wnd.p1, wnd.p2)
                else:
                    print("found nothing")
                    a.grab(wnd.p1, wnd.p2)
                    a.searchRect(wnd.p1, wnd.p2)
                    while a.find("vikings.Xclose"):
                        a.findClick("vikings.Xclose")
                        a.sleep(200)
                        a.mouseMove(a.mousePos().add(50, 50))
                        a.sleep(600)
                        a.grab(wnd.p1, wnd.p2)

            print("ready to kill")
            a.mouseClick(wndC.add(-resultPosition.x, -resultPosition.y))
            a.sleep(600)

            shots = 0
            a.searchRect(lair.p1, lair.p2)
            while True:
                a.grab(lair.p1, lair.p2)
                if a.find("vikings.sustainedattack"):
                    a.sleep(150)
                    if maxHits > 0 and shots >= maxHits:
                        #print("time to kill: %s shots of %s" % (shots, maxHits))
                        if a.find("vikings.enhancedattack"):
                            attack = a.findPos("vikings.enhancedattack")
                            a.mouseMove(attack)
                            a.sleep(150)
                            a.mouseClick(a.mousePos())
                            shots = shots + 1
                            a.sleep(400)
                            #print("shot %s/%s" % (shots, maxHits))
                    elif a.find("vikings.normalattack"):
                        attack = a.findPos("vikings.normalattack")
                        a.mouseMove(attack)
                        a.sleep(150)
                        a.mouseClick(a.mousePos())
                        shots = shots + 1
                        a.sleep(400)
                        #print("shot %s/%s" % (shots, maxHits))
                        a.mouseMove(a.mousePos().add(15, 35))
                        a.sleep(1200)
                elif a.find("vikings.store"):
                    a.sleep(150)
                    a.findClick("vikings.store")
                    a.sleep(400)
                    a.grab(lair.p1, lair.p2)
                    if a.find("vikings.purchase.buyandapply"):
                        buy = a.findPos("vikings.purchase.buyandapply")
                    elif a.find("vikings.purchase.apply"):
                        buy = a.findPos("vikings.purchase.apply")
                    a.mouseMove(buy)
                    a.sleep(400)
                    a.mouseMove(buy.add(0, 40)) # More
                    a.sleep(300)
                    a.mouseClick(a.mousePos()) # More
                    a.sleep(500)
                    a.grab(lair.p1, lair.p2)
                    a.mouseClick(695, 650) # spinner
                    a.sleep(500)
                    if a.findClick("vikings.store.buyandapply"): # Buy and apply
                        a.sleep(700)
                    elif a.findClick("vikings.store.apply"): # or Apply
                        a.sleep(700)
##                    a.grab(lair.p1, lair.p2)
##                    a.findClick("vikings.Xclose") # X close
                    a.mouseClick(770, 170) # X close
                    a.sleep(600)
                elif a.find("vikings.tileamountof"):
                    killedInvaders = killedInvaders + 1
                    print("invader %s was killed in %s shots! killed %s invaders" % (invaderName, shots, killedInvaders))
                    a.sleep(1200)
                    while a.find("vikings.Xclose") == True:
                        a.sleep(100)
                        a.findClick("vikings.Xclose")
                        a.sleep(300)
                        a.mouseMove(a.mousePos().add(50, 10))
                        a.sleep(500)
                        a.grab(lair.p1, lair.p2)
                    break
                a.sleep(150)
        else:
            print("invader " + invaderName + " not found")
            break
    else:
        print("watchtowerbutton not found")
        a.sleep(1200)
        a.grab(wnd.p1, wnd.p2)
        a.searchRect(wnd.p1, wnd.p2)
        while a.find("vikings.Xclose2"):
            a.findClick("vikings.Xclose2")
            a.sleep(200)
            a.mouseMove(a.mousePos().add(50, 50))
            a.sleep(600)
            a.grab(wnd.p1, wnd.p2)

a.grab(wnd.p1, wnd.p2)
a.searchRect(wnd.p1, wnd.p2)
while a.findClick("vikings.Xclose"):
    a.mouseMove(a.mousePos().add(50, 50))
    a.sleep(200)
    a.grab(wnd.p1, wnd.p2)

print("Happy end!")
