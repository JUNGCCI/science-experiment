import pygame, math
pygame.init()

w=1000
h=700

clock=pygame.time.Clock()

white=(255,255,255)
black=(0,0,0)

font_str=pygame.font.Font('KBIZ_R.ttf',40)

playing=True
mousedown=False
drag=False
start=False

m=1 #물체의 질량(kg) (3d 프린터에서 물체를 만든 후 측정하여 넣기)
angle=30 #빗변의 각도
Flist=[0.1,0.4] #마찰력의 크기 -> 선택할 수 있게(그냥 마찰력과 부직포를 붙였을 때 마찰력) 아니지 마찰계수지
F=Flist[0]
angle90F= 0 #수직항력
g=0.5 #중력가속도
circlex=100 #각도 조절하기 위한 원의 x좌표
velocity_x=0 #x축으로의 속도
velocity_y=0 #y축으로의 속도
ticksec=0 #tick을 시간으로 변환

screen=pygame.display.set_mode((w,h))
mousexy=pygame.mouse.get_pos()

def click(rect):
    if rect[0]<mousexy[0]<rect[0]+rect[2] and rect[1]<mousexy[1]<rect[1]+rect[3]:
        return True

while playing:
    screen.fill(black)
    clock.tick(60)
    mousexy=pygame.mouse.get_pos()

    mousedown=False
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            playing=False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_s:
                start=not start
                print(start)
            if event.key==pygame.K_c:
                print(ticksec/60)
            if event.key==pygame.K_f:
                if F==Flist[0]:
                    F=Flist[1]
                else:
                    F=Flist[0]
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                if pygame.mouse.get_pressed()[0]==1:
                    mousedown=True

        if event.type==pygame.MOUSEBUTTONUP:
            if event.button==1:
                if drag:
                    drag=False

    if mousedown:
        if click([90,70,120,60]):
            drag=True

    angle=int((circlex-100)*90/100)
    pie_angle=angle*(math.pi/180)
    angle90F=m*g*math.cos(pie_angle)
    anglestr=font_str.render('각도:'+str(angle),True,white)
    Fstr=font_str.render('마찰력:'+str(F*angle90F)[:4],True,white)
    screen.blit(anglestr,[20,180])
    screen.blit(Fstr,[20,280])

    if start:
        drag=False
        if (movecirclexy[0]>=w/4 and movecirclexy[1]<=h*4/5) and angle90F*F<(math.cos(pie_angle)*math.sin(pie_angle))*g*m:
            velocity_x+=(math.cos(pie_angle)*math.sin(pie_angle))*g*m-angle90F*F #속도에다가 힘 더하기 (x방향)
            velocity_y+=(math.sin(pie_angle))**2*g*m-angle90F*F*math.tan(pie_angle) #속도에다가 힘 더하기 (y방향)
            movecirclexy=[movecirclexy[0]-velocity_x,movecirclexy[1]+velocity_y]
            ticksec+=1
    else:
        movecirclexy=[w/4+500*math.cos(pie_angle),h*4/5-500*math.sin(pie_angle)]
        velocity_x=0
        velocity_y=0
        ticksec=0

    if drag:
        circlex=mousexy[0]
        if circlex>200:
            circlex=200
        elif circlex<100:
            circlex=100


    #삼각형과 원 그리기
    pygame.draw.polygon(screen,white,[[w/4,h*4/5],[w/4+500*math.cos(pie_angle),h*4/5],[w/4+500*math.cos(pie_angle),h*4/5-500*math.sin(pie_angle)]])
    pygame.draw.line(screen,(255,0,0),[w/4,h*4/5],[w/4+500*math.cos(pie_angle),h*4/5-500*math.sin(pie_angle)],3)
    pygame.draw.circle(screen,white,[movecirclexy[0]-math.sin(pie_angle)*15,movecirclexy[1]-math.cos(pie_angle)*15],15)

    #드래그
    pygame.draw.line(screen,(100,100,100),[100,100],[200,100],3)
    pygame.draw.circle(screen,white,[circlex,100],10)

    pygame.display.flip()
pygame.quit()
