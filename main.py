import re
from tkinter import *
import clases as cs
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.patches import Circle
app = Tk()
app.title("Geo-Expofisica")
app.geometry("1024x650")
app.resizable(height=False, width=False)
#Fondos
imagen = PhotoImage(file="imagenes/Homescreen.png")
campoinfo = PhotoImage(file="imagenes/FondoCE.png")
dipolo = PhotoImage(file="imagenes/FondoDipo.png")
#Botones
entrar = PhotoImage(file="imagenes/entrar.png")
calcular = PhotoImage(file="imagenes/calcular.png")
dipolobtn = PhotoImage(file="imagenes/dipolobtn.png")
campobtn = PhotoImage(file="imagenes/campobtn.png")
back = PhotoImage(file="imagenes/backbtn.png")
def Mainmenu(): 
    
    def entrada():
        def dipolos():
            def calculos():
                for ele in app.winfo_children():
                    ele.destroy()
                app.config(background="white")
                frame = Frame(app, width=500 , height=500)
                frame.pack(side=LEFT)
                def grafica(n:int):
                    # # Función que retorna el campo Eléctrico.
                    def E(q, r0, x, y):
                        """Retorna el vector de campo eléctrico E=(Ex,Ey) de una carga q en r0"""
                        den = np.hypot(x-r0[0], y-r0[1])**3
                        return q * (x - r0[0]) / den, q * (y - r0[1]) / den

                    # # puntos de los ejes x e y.
                    nx, ny = 64, 64
                    x = np.linspace(-2, 2, nx)
                    y = np.linspace(-2, 2, ny)
                    X, Y = np.meshgrid(x, y)

                    # # Crear un multipolo con nq cargas
                    # count = número de q. En ese caso es 1 dipolo
                    count = n
                    nq = 2**int(count)
                    charges = []
                    for i in range(nq):
                        q = i%2 * 2 - 1
                        charges.append((q, (np.cos(2*np.pi*i/nq), np.sin(2*np.pi*i/nq))))

                    # # Vector de campo eléctrico como componentes separados (Ex,Ey)
                    Ex, Ey = np.zeros((ny, nx)), np.zeros((ny, nx))
                    for charge in charges:
                        ex, ey = E(*charge, x=X, y=Y)
                        Ex += ex
                        Ey += ey

                    fig = plt.figure()
                    ax = fig.add_subplot(111)


                    # # Dibujar las líneas de flujo con mapa de colores y estilos apropiados.
                    color = 2 * np.log(np.hypot(Ex, Ey))
                    ax.streamplot(x, y, Ex, Ey, color=color, linewidth=1, cmap=plt.cm.inferno,
                                density=2, arrowstyle='->', arrowsize=1.5)


                    # # Agregar circulos para las cargas.
                    charge_colors = {True: '#aa0000', False: '#0000aa'}
                    for q, pos in charges:
                        ax.add_artist(Circle(pos, 0.05, color=charge_colors[q>0]))


                    # # Graficar
                    ax.set_xlabel('$x$')
                    ax.set_ylabel('$y$')
                    ax.set_xlim(-2,2)
                    ax.set_ylim(-2,2)
                    ax.set_aspect('equal')

                    canvas = FigureCanvasTkAgg(fig, master=frame)
                    canvas.draw()
                    canvas.get_tk_widget().grid(column=0, row=0, rowspan=1)
                grafica(1)
                def validate_cc(text: str):
                    return text.isdecimal()
                titulo = Label(app, text="Líneas de campo en dipolos", font=("Microsoft Sans Serif", 30), anchor=NW, fg="RoyalBlue1", bg="white")
                titulo.place(x=30, y= 19, height=60, width=1000)
                numero = Label(app, text="Número de dipolos:", font=("Microsoft Sans Serif", 15), bg="white")
                numero.place(x=642, y= 270, width=200, height=30)
                txtnum = Entry(app, bg="grey89",font=15, borderwidth=0, validate="key",
                                 validatecommand=(app.register(validate_cc), "%S"))
                txtnum.place(x=830, y=270, width=45, height=30)
                Error = Label(app, text="",font=("Microsoft Sans Serif", 20), fg="red", bg="white")
                Error.place(x=642, y=460, width=300, height=50)
                def graf():
                    Error.config(text="")
                    numero = txtnum.get()
                    if numero == "":
                        Error.config(text="Campo vacio")
                    else:
                        if int(numero)>15:
                            Error.config(text="Cantidad no valida")
                        else:
                            grafica(numero)
                botonentrar = Button(image=calcular, borderwidth=0, command=graf)
                botonentrar.place(x=740, y=540, height=72, width=224)
                btnback = Button(image=back, borderwidth=0, command=entrada)
                btnback.place(x=930, y=28, height=76, width=48)
            for ele in app.winfo_children():
                ele.destroy()
            interfaz = Canvas(app)
            interfaz.pack()
            backgrounddip = Label(interfaz, image=dipolo)
            backgrounddip.pack()
            botonentrar = Button(image=entrar, borderwidth=0, command=calculos)
            botonentrar.place(x=740, y=540, height=72, width=224)
            botoncamp = Button(image=campobtn, borderwidth=0, command=entrada)
            botoncamp.place(x=0, y = 213, width=290, height=93)
        def campores():
            def graficar(xP :float,yP: float, xq1: float, yq1:float,mq1: float, xq2: float, yq2:float,mq2: float):
                fig, ax = plt.subplots()
                #------------------------
                #Carga Q
                P = cs.Punto(xP,yP)
                #Carga q1
                q1 = cs.Carga(xq1,yq1,mq1, 0, 0,0,0)
                #Carga q2
                q2 = cs.Carga(xq2,yq2,mq2,0,0,0,0)
                #-------------------------------
                #puntos
                punto1 = ax.scatter(P.x, P.y)
                ax.annotate("P", (P.x-0.5, P.y))

                punto2 = ax.scatter(q1.x, q1.y)
                if(q1.carga>0):
                    sig1= "+"
                else:
                    sig1 = "-"
                ax.annotate(sig1+"q1", (q1.x-0.5, q1.y+0.5))
                if(q2.carga>0):
                    sig2= "+"
                else:
                    sig2 = "-"
                punto3 = ax.scatter(q2.x, q2.y)
                ax.annotate(sig2+"q2", (q2.x-0.5,q2.y+0.5))

                #Conección de q1 a p
                ax.plot([P.x,q1.x],[P.y,q1.y],'k--')

                #Conección de q2 a p
                ax.plot([P.x,q2.x],[P.y,q2.y],'k--')
                #------------------------------------
                #Datos de q1
                q1.distancia = q1.distancia_ap(q1.x, q1.y, P.x, P.y)
                q1.magnitud = q1.magnitudT(q1.carga, q1.distancia)
                q1.vecx = q1.vectorx(q1.x, P.x)
                q1.vecy = q1.vectory(q1.y, P.y)
                #print("Datos q1:")
                #print(q1.vecx)
                #print(q1.vecy)
                #print(q1.magnitud)
                #print(q1.distancia)
                #--------------------------------------
                #Datos de q2
                q2.distancia = q2.distancia_ap(q2.x, q2.y, P.x, P.y)
                q2.magnitud = q2.magnitudT(q2.carga, q2.distancia)
                q2.vecx = q2.vectorx(q2.x, P.x)
                q2.vecy = q2.vectory(q2.y, P.y)
                #print("Datos q2:")
                #print(q2.vecx)
                #print(q2.vecy)
                #print(q2.magnitud)
                #print(q2.distancia)
                #--------------------------------------
                #Vector q1
                q1.vecx = (q1.magnitud*q1.vecx)/q1.distancia
                q1.vecy = (q1.magnitud*q1.vecy)/q1.distancia
                ax.quiver(P.x,P.y, q1.vecx/10,q1.vecy/10, color='orange', scale_units= 'xy', scale=1,angles ='xy')

                #-----------------------------------------------
                #Vector q2
                q2.vecx = (q2.magnitud*q2.vecx)/q2.distancia
                q2.vecy = (q2.magnitud*q2.vecy)/q2.distancia
                ax.quiver(P.x,P.y,q2.vecx/10,q2.vecy/10, color='green', scale_units= 'xy', scale=1,angles ='xy')
                #-----------------------------------------------
                #Vector resultantes
                resx= q1.vecx + q2.vecx
                resy= q1.vecy + q2.vecy
                ax.quiver(P.x,P.y,resx/10,resy/10, color='black', scale_units= 'xy', scale=1,angles ='xy')
                plt.xlabel("X")
                plt.ylabel("Y")
                plt.title("Campo electrico")

                plt.xlim(0,20)
                plt.ylim(-10,30)
                ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
                ax.grid(axis = 'x', color = 'gray', linestyle = 'dashed')
                canvas = FigureCanvasTkAgg(fig, master=frame)
                toolbar = NavigationToolbar2Tk(canvas, app)
                #toolbar.pack(side=BOTTOM, anchor=SW, fill=X)
                toolbar.place(x=17, y= 550)
                canvas.draw()
                canvas.get_tk_widget().grid(column=0, row=0, rowspan=1)
                #-------Label carga 1 (naranja)-----------
                xc1 = str(round(q1.vecx*10,2))
                yc1 = str(round(q1.vecy*10,2))
                xc2 = str(round(q2.vecx*10,2))
                yc2 =str(round(q2.vecy*10,2))
                xt = str(round(resx*10, 2))
                yt = str(round(resy*10, 2))
                tituloc1 = Label(app, text="Carga 1: "+str(q1.carga)+"µC",font=("Microsoft Sans Serif", 20), fg="orange", bg="white")
                tituloc1.place(x=642, y=220, width=300, height=50)
                vecotorc1 = Label(app, text="E= ("+ xc1+ "î + ("+yc1+")Ĵ)N/C", font=("Microsoft Sans Serif", 20), fg="orange", bg="white")
                vecotorc1.place(x=630, y=260, width=400, height=50)
                #--------- Label carga 2 (verde)---------
                tituloc2 = Label(app, text="Carga 2: "+str(q2.carga)+"µC",font=("Microsoft Sans Serif", 20), fg="green", bg="white")
                tituloc2.place(x=642, y=300, width=300, height=50)
                vecotorc2 = Label(app, text= "E= ("+xc2+ "î + ("+yc2+")Ĵ)N/C", font=("Microsoft Sans Serif", 20), fg="green", bg="white")
                vecotorc2.place(x=630, y=340, width=400, height=50)
                #------------Label total (negro)-----------
                tituloc2R = Label(app, text="Campo resultante",font=("Microsoft Sans Serif", 20), fg="black", bg="white")
                tituloc2R.place(x=642, y=380, width=300, height=50)
                vecotorc2R = Label(app, text="E= ("+ xt+ "î + ("+yt+")Ĵ)N/C", font=("Microsoft Sans Serif", 20), fg="black", bg="white")
                vecotorc2R.place(x=630, y=420, width=400, height=50)
            def isfloat(num:str):
                try:
                    float(num)
                    return True
                except ValueError:
                    return False
            for ele in app.winfo_children():
                ele.destroy()
            app.config(background="white")
            
            frame = Frame(app, width=20 , height=20)
            frame.pack(side=LEFT)
            frame.config(bg="mint cream")  
            #frame.grid(column=0, row=0, sticky='nsew')
            #-------------------------------
            #Grafica de ejemplo
            graficar(10, 5, 5, 2, -1, 4, 7,0.8)
            
            
            titulo = Label(app, text="     Campo eléctrico resultante", font=("Microsoft Sans Serif", 30), anchor=NW, fg="RoyalBlue1", bg="white")
            titulo.place(x=30, y= 19, height=60, width=1000)
            #----------Punto------------------------------
            punto = Label(app, text="Punto:", font=("Microsoft Sans Serif", 15), bg="white")
            punto.place(x=642, y= 70, width=60, height=30)
            txtPX = Entry(app, bg="grey89",font=15, borderwidth=0)
            txtPX.place(x=730, y=70, width=45, height=30)
            txtPy = Entry(app, bg="grey89",font=15, borderwidth=0)
            txtPy.place(x=785, y=70, width=45, height=30)
            #---------Etiquetas, x,y, magnitud------------------
            labelx = Label(app, text= "X",font=("Microsoft Sans Serif", 15), bg="white")
            labelx.place(x=740, y=47, width=20, height=20)
            labely = Label(app, text= "Y",font=("Microsoft Sans Serif", 15), bg="white")
            labely.place(x=795, y=47, width=20, height=20)
            labelMG = Label(app, text= "Magnitud",font=("Microsoft Sans Serif", 15), bg="white")
            labelMG.place(x=840, y=42, width=90, height=30)
            #----------Carga 1---------------------------
            carga1 = Label(app, text="Carga 1:", font=("Microsoft Sans Serif", 15), bg="white")
            carga1.place(x=642, y= 120, width=80, height=30)
            txtC1x = Entry(app, bg="grey89",font=15, borderwidth=0)
            txtC1x.place(x=730, y=120, width=45, height=30)
            txtC1y = Entry(app, bg="grey89",font=15, borderwidth=0)
            txtC1y.place(x=785, y=120, width=45, height=30)
            txtMG = Entry(app, bg="grey89",font=15, borderwidth=0)
            txtMG.place(x=845, y=120, width=45, height=30)
            unidad = Label(app, text="µC", font=("Microsoft Sans Serif", 15), bg="white")
            unidad.place(x=890, y=120, width=45, height=30)
            #----------Carga 2-------------------------
            carga2 = Label(app, text="Carga 2:", font=("Microsoft Sans Serif", 15), bg="white")
            carga2.place(x=642, y= 170, width=80, height=30)
            txtC2x = Entry(app, bg="grey89",font=15, borderwidth=0)
            txtC2x.place(x=730, y=170, width=45, height=30)
            txtC2y = Entry(app, bg="grey89",font=15, borderwidth=0)
            txtC2y.place(x=785, y=170, width=45, height=30)
            txtMG2 = Entry(app, bg="grey89",font=15, borderwidth=0)
            txtMG2.place(x=845, y=170, width=45, height=30)
            unidad2 = Label(app, text="µC", font=("Microsoft Sans Serif", 15), bg="white")
            unidad2.place(x=890, y=170, width=45, height=30)
            #---------Error-----------
            Error = Label(app, text="",font=("Microsoft Sans Serif", 20), fg="red", bg="white")
            Error.place(x=642, y=460, width=300, height=50)
            #-----------Metodos----------------
            def graf():
                #----------Captura de todos los datos--------------
                Px= txtPX.get()
                Py = txtPy.get()
                C1 = txtMG.get()
                C1x = txtC1x.get()
                C1y = txtC1y.get()
                C2 = txtMG2.get()
                C2x= txtC2x.get()
                C2y= txtC2y.get()
                key1=False
                key2=False
                key3=False
                key4=False
                key5=False
                key6=False
                key7=False
                key8=False
                if(isfloat(Px)==True):
                    key1= True
                if(isfloat(Py)==True):
                    key2= True
                if(isfloat(C1)==True):
                    key3= True
                if(isfloat(C1x)==True):
                    key4= True
                if(isfloat(C1y)==True):
                    key5= True
                if(isfloat(C2)==True):
                    key6= True
                if(isfloat(C2x)==True):
                    key7= True
                if(isfloat(C2y)==True):
                    key8= True
                if(key1 ==True and key2 ==True and key3 ==True and key4 ==True and key5 ==True and key6 ==True and key7 ==True and key8 ==True):
                    Error.config(text="")
                    graficar(float(Px), float(Py), float(C1x), float(C1y), float(C1), float(C2x), float(C2y), float(C2))
                else:
                    Error.config(text="Datos no aptos")
            #--------Boton--------
            botonentrar = Button(image=calcular, borderwidth=0, command=graf)
            botonentrar.place(x=740, y=540, height=72, width=224)
            btnback = Button(image=back, borderwidth=0, command=entrada)
            btnback.place(x=10, y=28, height=76, width=48)
        
        for ele in app.winfo_children():
            ele.destroy()
        interfaz = Canvas(app)
        interfaz.pack()
        background2_2 = Label(interfaz, image=campoinfo)
        background2_2.pack()
        botonentrar = Button(image=entrar, borderwidth=0, command=campores)
        botonentrar.place(x=740, y=540, height=72, width=224)
        botondipo = Button(image=dipolobtn, borderwidth=0, command=dipolos)
        botondipo.place(x=0, y = 375, width=289, height=90)
        #Para el otro boton=x=0, y = 213, width=289, height=90
        
    background = Label(image=imagen, text="fondo")
    background.place(x=0, y=0, relwidth=1, relheight=1)
    botonentrar = Button(image=entrar, borderwidth=0, command=entrada)
    botonentrar.place(x=650, y=426, height=72, width=224)
    
Mainmenu()
app.mainloop()