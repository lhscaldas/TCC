import tkinter as tk
from tkinter import Label, ttk, messagebox
from tkinter.constants import DOTBOX
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from pathlib import Path
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.pyplot as plt
from matplotlib import cm
from math import pi, cos, sqrt, sin, tan, asin
import Genetic_Algorithm as GA
from time import time
import moos as moos



class NACMMsetup(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.originpixel=[7834,2090]
        self.originlatlong=[-23.0163,-43.9594] # Bernardo = [-23.0163,-43.9594], porto = [-22.9269,-43.867], irmãs = [-22.9392,-43.9727]
        self.shapepixel=(10488,75510)
        self.shapemeters=(2298, 16778)
        self.container=container
        
        # Mouse function
        self.click_flag=tk.IntVar()
        self.click_flag.set(0)

        # Pressionar células
        self.pressed_cells = list()
        self.rectangles = list()
        
        # caminho
        self.path_n = []
        self.path_id = []
        self.path_xy = []
        self.lines_id = []

        # navio
        self.pos0 = []
        self.pos0_id = -1
        self.posf=[]
        self.posf_id = -1
        self.heading = tk.StringVar(value=str(0))
        self.navios = list()
        self.vname = tk.StringVar(value="alfa")

        # selecionar origem
        self.latstring=tk.StringVar(value=str(self.originlatlong[0]))
        self.longstring=tk.StringVar(value=str(self.originlatlong[1]))
    
        # main canvas
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="left", fill="both",expand=True)

        
        # sub canvas
        self.chart_panel=tk.Canvas(self.canvas, width=0, height=0)
        self.chart_panel.pack(side="right", fill="both",expand=True)
        self.side_panel=tk.Canvas(self.canvas)
        self.side_panel.pack(side="left")
        

        # chart panel
        self.chart = 0
        self.chart_panel.bind("<Button-1>", self.mouse1_callback)
        
        # side panel
        button_load = tk.Button(self.side_panel, text="Carregar Carta", width=30, command=lambda : self.load_chart())
        button_load.grid(column=0, row=0, columnspan=2)

        latorigemlabel=tk.Label(self.side_panel, text = "Lat_origem = ")
        latorigemlabel.grid(column=0, row=1)
        self.latorigem=tk.Entry(self.side_panel, textvariable=self.latstring)
        self.latorigem.grid(column=1, row=1)

        longorigemlabel=tk.Label(self.side_panel, text = "Long_origem = ")    
        longorigemlabel.grid(column=0, row=2)
        self.longorigem=tk.Entry(self.side_panel, textvariable=self.longstring)
        self.longorigem.grid(column=1, row=2)   

        button_origin = tk.Button(self.side_panel, text="Definir origem", width=30, command=lambda : self.go_to_origin())
        button_origin.grid(column=0, row=3, columnspan=2)

        mouse = tk.Radiobutton(self.side_panel, text="Posição do clique:", var=self.click_flag, value=0)
        mouse.grid(column=0, row=4, columnspan=2)
        self.xlabel = tk.Label(self.side_panel, text = "x= 0")
        self.xlabel.grid(column=0, row=5)
        self.ylabel = tk.Label(self.side_panel, text = "y= 0")
        self.ylabel.grid(column=1, row=5)
        self.latlabel = tk.Label(self.side_panel, text = "Lat= 0")
        self.latlabel.grid(column=0, row=6)
        self.longlabel = tk.Label(self.side_panel, text = "Long= 0")
        self.longlabel.grid(column=1, row=6)
        

        # Manual tab
        mouse = tk.Radiobutton(self.side_panel, text="Inserir ponto", var=self.click_flag, value=4)
        mouse.grid(column=0, row=7, columnspan=2)
        mouse = tk.Radiobutton(self.side_panel, text="Modificar ponto inicial", var=self.click_flag, value=2)
        mouse.grid(column=0, row=8, columnspan=2)
        mouse = tk.Radiobutton(self.side_panel, text="Modificar ponto final", var=self.click_flag, value=3)
        mouse.grid(column=0, row=9, columnspan=2)
        mouse = tk.Radiobutton(self.side_panel, text="Inserir/remover obstáculos", var=self.click_flag, value=1)
        mouse.grid(column=0, row=10, columnspan=2)
        mouse = tk.Radiobutton(self.side_panel, text="Posição inicial do navio", var=self.click_flag, value=5)
        mouse.grid(column=0, row=11, columnspan=2)
        mouse = tk.Radiobutton(self.side_panel, text="Posição final do navio", var=self.click_flag, value=6)
        mouse.grid(column=0, row=12, columnspan=2)
        hdg0_label=tk.Label(self.side_panel, text = "Proa inicial")
        hdg0_label.grid(column=0, row=13)   
        hdg0=tk.Entry(self.side_panel, textvariable=self.heading)
        hdg0.grid(column=1, row=13)   
        button_optimize = tk.Button(self.side_panel, text = "Otimizar rota", width=30, command=lambda : self.opt_path())
        button_optimize.grid(column=0, row=14, columnspan=2)
        button_clear = tk.Button(self.side_panel, text="Limpar", width=30, command=lambda : self.clear())
        button_clear.grid(column=0, row=15, columnspan=2)
        ship_label=tk.Label(self.side_panel, text = "Nome do navio")
        ship_label.grid(column=0, row=16)   
        ship=tk.Entry(self.side_panel, textvariable=self.vname)
        ship.grid(column=1, row=16)
        button_file = tk.Button(self.side_panel, text="Gerar arquivos", width=30, command=lambda : self.gen_files())
        button_file.grid(column=0, row=17, columnspan=2)
        button_run = tk.Button(self.side_panel, text="Simular", width=30, command=lambda : moos.run())
        button_run.grid(column=0, row=18, columnspan=2)

        button_debug = tk.Button(self.side_panel, text="Degub", width=30, command=lambda : self.debug())
        button_debug.grid(column=0, row=19, columnspan=2)

    def debug(self):
        # print(self.pressed_cells)
        # print(self.path_xy)
        # print(self.path_n)

        self.pressed_cells = [(19.0, 41.0), (18.0, 42.0), (19.0, 42.0), (18.0, 41.0), (17.0, 41.0), (18.0, 40.0), (17.0, 40.0), (17.0, 39.0), (16.0, 40.0), (16.0, 39.0), (15.0, 39.0), (15.0, 38.0), (14.0, 38.0), (14.0, 39.0), (13.0, 39.0), (13.0, 38.0), (12.0, 39.0), (12.0, 38.0), (11.0, 39.0), (11.0, 38.0), (10.0, 40.0), (11.0, 40.0), (10.0, 38.0), (9.0, 40.0), (9.0, 39.0), (10.0, 39.0), (8.0, 39.0), (8.0, 40.0), (7.0, 40.0), (7.0, 39.0), (6.0, 39.0), (6.0, 40.0), (5.0, 40.0), (5.0, 39.0), (4.0, 40.0), (4.0, 41.0), (4.0, 42.0), (4.0, 43.0), (4.0, 44.0), (4.0, 46.0), (4.0, 45.0), (4.0, 47.0), (5.0, 48.0), (4.0, 48.0), (5.0, 49.0), (4.0, 49.0), (4.0, 50.0), (5.0, 50.0), (4.0, 51.0), (3.0, 51.0), (3.0, 52.0), (3.0, 53.0), (2.0, 53.0), (2.0, 54.0), (1.0, 55.0), (2.0, 55.0), (1.0, 56.0), (0.0, 56.0), (0.0, 57.0), (0.0, 58.0), (0.0, 59.0), (0.0, 60.0), (0.0, 61.0), (1.0, 61.0), (2.0, 61.0), (2.0, 62.0), (3.0, 62.0), (4.0, 62.0), (4.0, 63.0), (5.0, 63.0), (6.0, 63.0), (7.0, 62.0), (7.0, 63.0), (7.0, 61.0), (7.0, 60.0), (8.0, 60.0), (8.0, 59.0), (9.0, 59.0), (9.0, 58.0), (9.0, 57.0), (10.0, 57.0), (11.0, 57.0), (10.0, 56.0), (12.0, 57.0), (13.0, 58.0), (12.0, 58.0), (14.0, 58.0), (14.0, 57.0), (14.0, 56.0), (15.0, 56.0), (15.0, 55.0), (16.0, 55.0), (16.0, 56.0), (16.0, 57.0), (15.0, 57.0), (15.0, 58.0), (15.0, 59.0), (15.0, 60.0), (16.0, 60.0), (17.0, 59.0), (17.0, 60.0), (17.0, 58.0), (18.0, 58.0), (18.0, 57.0), (18.0, 56.0), (19.0, 56.0), (17.0, 55.0), (19.0, 55.0), (20.0, 55.0), (19.0, 58.0), (19.0, 57.0), (18.0, 59.0), (20.0, 56.0), (20.0, 54.0), (21.0, 55.0), (21.0, 53.0), (21.0, 54.0), (20.0, 53.0), (21.0, 52.0), (22.0, 53.0), (22.0, 51.0), (22.0, 52.0), (23.0, 51.0), (23.0, 50.0), (22.0, 50.0), (23.0, 49.0), (24.0, 49.0), (24.0, 48.0), (23.0, 47.0), (23.0, 48.0), (25.0, 47.0), (24.0, 47.0), (24.0, 46.0), (25.0, 46.0), (25.0, 45.0), (24.0, 45.0), (24.0, 44.0), (25.0, 44.0), (25.0, 43.0), (25.0, 42.0), (26.0, 42.0), (26.0, 43.0), (26.0, 44.0), (26.0, 41.0), (25.0, 41.0), (25.0, 40.0), (27.0, 39.0), (26.0, 40.0), (26.0, 39.0), (25.0, 39.0), (27.0, 40.0), (27.0, 41.0)]
        # self.path_xy=[[735, -975], [975, -825], [1305, -615], [1455, -375]]
        self.path_n = [3736, 3164, 2363, 1440]
        path_x = [(n%116)*30+15+7.5 for n in self.path_n]
        path_y = [-(n//116)*30-15-15-7.5 for n in self.path_n]
        self.path_xy=[]
        for i in range(0,4):
            self.path_xy.append([path_x[i],path_y[i]])
        self.plot_path()
        restrictions=GA.xy2n(self.pressed_cells)
        GA.plot_result(self.path_n, restrictions, 0.0, 0.0, 0.0) # para debug


    def gen_files(self):
        hdg = float(self.heading.get())
        vname = self.vname.get()
        if vname not in self.navios:
            self.navios.append(vname)
            moos.write_sh(self.navios)
        moos.write_bhv(self.path_xy,self.posf,vname)
        moos.write_moos(self.pos0,self.originlatlong, hdg, vname, self.navios)
        moos.write_ms(self.originlatlong)
    
    def clear(self):
        if len(self.pressed_cells)>0:
            self.pressed_cells = []
            for retangle in self.rectangles:
                self.chart_panel.delete(retangle)
            self.rectangles = []
        if len(self.path_n)>0:
            self.path_n = []
            self.path_xy = []
            for wp in self.path_id:
                self.chart_panel.delete(wp)
            self.path_id = []
            for idx in self.lines_id:
                self.chart_panel.delete(idx)
            self.lines_id = []
        if len(self.pos0)>0:
            self.chart_panel.delete(self.pos0_id)
            self.pos0 = []
            self.pos0_id = -1
        if len(self.posf)>0:
            self.chart_panel.delete(self.posf_id)
            self.posf = []
            self.posf_id = -1
        

    def plot_path(self):
        for idx in self.path_id:
            self.chart_panel.delete(idx)
        self.path_id = []
        for idx in self.lines_id:
            self.chart_panel.delete(idx)
        self.lines_id = []
        for i in range(1,len(self.path_xy)):
            x0,y0=self.path_xy[i-1]
            x1,y1=self.path_xy[i]
            xp0, yp0 = self.meters2pixel(x0,y0)
            xp1, yp1 = self.meters2pixel(x1,y1)
            new_line = self.chart_panel.create_line(xp0, yp0, xp1, yp1, fill="blue", width=2)
            self.lines_id.append(new_line)
        for wp in self.path_xy:
            [x,y] = wp
            xp, yp = self.meters2pixel(x,y)
            d = 5
            x1, y1 = (xp - d), (yp - d)
            x2, y2 = (xp + d), (yp + d)
            if wp==self.path_xy[0]:
                new_dot = self.chart_panel.create_oval(x1, y1, x2, y2, fill="green")
                self.path_id.append(new_dot)
            elif wp==self.path_xy[-1]:
                new_dot = self.chart_panel.create_oval(x1, y1, x2, y2, fill="red")
                self.path_id.append(new_dot)
            else:
                new_dot = self.chart_panel.create_oval(x1, y1, x2, y2, fill="blue")
                self.path_id.append(new_dot)

    def manual_path(self,event):
        x_, y_ = self.get_click_pos(event)
        x = (x_//15)*15
        y = (y_//15)*15
        if x_ % 15 > 7.5:
            x +=15
        if y_ % 15 > 7.5:
            y +=15
        if [x,y] not in self.path_xy:
            self.path_xy.append([x,y])
            self.path_n.append(round((-y-15)/30)*116+round((x-15)/30))
        else:
            wp_id = self.path_xy.index([x,y])
            self.path_xy.remove([x,y])
            self.path_n.pop(wp_id)
        self.plot_path()

    def get_begin(self,event):
        x_, y_ = self.get_click_pos(event)
        x = (x_//15)*15
        y = (y_//15)*15
        if x_ % 15 > 7.5:
            x +=15
        if y_ % 15 > 7.5:
            y +=15
        self.begin=[x,y]
        xp, yp = self.meters2pixel(x,y)
        d = 5
        x1, y1 = (xp - d), (yp - d)
        x2, y2 = (xp + d), (yp + d)
        if len(self.path_xy)>0:
            self.path_xy[0]=[x,y]
            self.path_n[0]=round((-y-15)/30)*116+round((x-15)/30)
        else:
            self.path_xy.append([x,y])
            self.path_n.append(round((-y-15)/30)*116+round((x-15)/30))
        self.plot_path()

    def get_end(self,event):
        x_, y_ = self.get_click_pos(event)
        x = (x_//15)*15
        y = (y_//15)*15
        if x_ % 15 > 7.5:
            x +=15
        if y_ % 15 > 7.5:
            y +=15
        self.end=[x,y]
        xp, yp = self.meters2pixel(x,y)
        d = 5
        x1, y1 = (xp - d), (yp - d)
        x2, y2 = (xp + d), (yp + d)
        if len(self.path_xy)>1:
            self.path_xy[-1]=[x,y]
            self.path_n[-1]=round((-y-15)/30)*116+round((x-15)/30)
        else:
            self.path_xy.append([x,y])
            self.path_n.append(round((-y-15)/30)*116+round((x-15)/30))
        self.plot_path()

    def get_pos0(self,event):
        x_, y_ = self.get_click_pos(event)
        x = (x_//15)*15
        y = (y_//15)*15
        if x_ % 15 > 7.5:
            x +=15
        if y_ % 15 > 7.5:
            y +=15
        if [x,y] != self.pos0:
            if len(self.pos0)>1:
                self.chart_panel.delete(self.pos0_id)
            self.pos0 = [x,y]
            xp, yp = self.meters2pixel(x,y)
            d = 5
            x1, y1 = (xp - d), (yp - d)
            x2, y2 = (xp + d), (yp + d)
            self.pos0_id = self.chart_panel.create_oval(x1, y1, x2, y2, fill="yellow")
        else:
            self.chart_panel.delete(self.pos0_id)
            self.pos0=[]
            self.pos0_id = -1

    def get_posf(self,event):
        x_, y_ = self.get_click_pos(event)
        x = (x_//15)*15
        y = (y_//15)*15
        if x_ % 15 > 7.5:
            x +=15
        if y_ % 15 > 7.5:
            y +=15
        if [x,y] != self.posf:
            if len(self.posf)>1:
                self.chart_panel.delete(self.posf_id)
            self.posf = [x,y]
            xp, yp = self.meters2pixel(x,y)
            d = 5
            x1, y1 = (xp - d), (yp - d)
            x2, y2 = (xp + d), (yp + d)
            self.posf_id = self.chart_panel.create_oval(x1, y1, x2, y2, fill="orange")
        else:
            self.chart_panel.delete(self.posf_id)
            self.posf=[]
            self.posf_id = -1


    def opt_path(self):
        restrictions=GA.xy2n(self.pressed_cells)
        beginend=[self.path_n[0],self.path_n[-1]]
        n_nodes=int(GA.length(beginend)/500)+3
        n_pop=40
        n_iter=100
        r_cross=0.9
        r_mut=1/(n_pop*sqrt(13*n_nodes)) # Tu e Yang 2003
        ti = time()
        best, best_eval, best_gen = GA.genetic_algorithm(GA.objective, restrictions, beginend, n_nodes, n_iter, n_pop, r_cross, r_mut)
        dt = time()-ti
        best_path = GA.decode(best)
        best_length = GA.length(best_path)
        # GA.plot_result(best_path, restrictions, best_length, best_gen+1, dt) # para debug
        self.path_n=best_path
        path_x = [(n%116)*30+15 for n in self.path_n]
        path_y = [-(n//116)*30-15 for n in self.path_n]
        self.path_xy=[]
        for i in range(0,n_nodes):
            if i>0 and i<n_nodes-1:
                self.path_xy.append([path_x[i]+7.5,path_y[i]-22.5])
            else:
                self.path_xy.append([path_x[i],path_y[i]])
        
        self.plot_path()
        result = f"Rota otimizada após {best_gen+1} gerações em {dt:2.2f} segundos.\nComprimento total da rota: {best_length:4.1f} metros."
        messagebox.showinfo("Resultado", result)        

    def go_to_origin(self):
        self.originlatlong[0]=float(self.latstring.get())
        self.originlatlong[1]=float(self.longstring.get())
        self.set_grid()
        self.chart_panel.xview_moveto(self.originpixel[0]/self.shapepixel[0])
        self.chart_panel.yview_moveto(self.originpixel[1]/self.shapepixel[1]) 

    def set_grid(self):
        params={}
        with open("itaguai.info", 'r') as f:
            text = f.readlines()
            for line in text:
                p = line.split(' ')
                p[:] = [x for x in p if x]
                params[p[0]]=float(p[2])
        xw, ys = self.latlong2local(params['lat_south'],params['lon_west'])
        xe, yn = self.latlong2local(params['lat_north'],params['lon_east'])
        self.shapemeters=(xe-xw,yn-ys)
        dx = self.shapepixel[0]/self.shapemeters[0]
        dy = self.shapepixel[1]/self.shapemeters[1]
        self.originpixel=[-xw*dx,yn*dy]   

    def load_chart(self):
        # filepath = Path(askopenfilename())
        # load = Image.open(filepath)
        filename = "itaguai.tif" # para debug
        load = Image.open(filename) # para debug
        self.chart = ImageTk.PhotoImage(load)
        self.shapepixel = (self.chart.width(),self.chart.height())
        self.chart_panel.create_image(0,0, image=self.chart, anchor='nw')
        xscrollbar = ttk.Scrollbar(self.chart_panel, orient="horizontal", command=self.chart_panel.xview)
        yscrollbar = ttk.Scrollbar(self.chart_panel, orient="vertical", command=self.chart_panel.yview)
        xscrollbar.pack(side="bottom", fill="both")
        yscrollbar.pack(side="right", fill="both")
        self.chart_panel.configure(xscrollcommand=xscrollbar.set)
        self.chart_panel.configure(yscrollcommand=yscrollbar.set)
        self.chart_panel.configure(width=self.shapepixel[0])
        self.chart_panel.configure(height=self.shapepixel[1])
        self.chart_panel.configure(scrollregion = self.chart_panel.bbox("all"))
        self.container.geometry('1800x900')
        self.side_panel.configure(height=900)
        self.set_grid()
        

    def mouse1_callback(self, event):
        if self.click_flag.get()==0:
            self.print_pos(event)
        elif self.click_flag.get()==1:
            self.choose_cell(event)
        elif self.click_flag.get()==2:
            self.get_begin(event)
        elif self.click_flag.get()==3:
            self.get_end(event)
        elif self.click_flag.get()==4:
            self.manual_path(event)
        elif self.click_flag.get()==5:
            self.get_pos0(event)
        elif self.click_flag.get()==6:
            self.get_posf(event)


    def get_click_pos(self,event):
        x = self.chart_panel.canvasx(event.x)
        y = self.chart_panel.canvasy(event.y)
        xm, ym = self.pixel2meters(x,y)
        return xm,ym

    def print_pos(self,event):
        xm,ym = self.get_click_pos(event)
        self.xlabel.configure(text=f"x= {round(xm,2)}")
        self.ylabel.configure(text=f"y= {round(ym,2)}")
        lat, long = self.local2latlong(xm,ym)
        self.latlabel.configure(text=f"Lat= {round(lat,4)}")
        self.longlabel.configure(text=f"long= {round(long,4)}")
        
    def choose_cell(self, event):
        dxm = 30 # metros
        dym = 30 # metros
        dxp = dxm*self.shapepixel[0]/self.shapemeters[0]
        dyp = dym*self.shapepixel[1]/self.shapemeters[1]
        n_cells = int(self.shapepixel[0]/dxp)
        m_cells = int(self.shapepixel[1]/dyp)  
        height = self.shapepixel[1]
        width =  self.shapepixel[0]
        first_cell = ((self.originpixel[1] * m_cells) // height + 1, (self.originpixel[0] * n_cells) // width + 1)
        x = self.chart_panel.canvasx(event.x)
        y = self.chart_panel.canvasy(event.y)
        i = (y * m_cells) // height + 1
        j = (x * n_cells) // width + 1
        i_local = i - first_cell[0] -1
        j_local = j - first_cell[1] -1
        if (i_local, j_local) not in self.pressed_cells:
            self.pressed_cells.append((i_local, j_local))
            x1 = (j-1) * width / n_cells
            y1 = (i-1) * height / m_cells
            x2 = j * width / n_cells
            y2 = i * height / m_cells
            rectangle = self.chart_panel.create_rectangle(x1, y1, x2, y2, width=1, fill="black", stipple="gray50")
            self.rectangles.append(rectangle)
        else:
            rectangle_id = self.pressed_cells.index((i_local, j_local))
            self.pressed_cells.remove((i_local, j_local))
            self.chart_panel.delete(self.rectangles[rectangle_id])
            self.rectangles.pop(rectangle_id)

    def pixel2meters(self,xp,yp):
        xp0=self.originpixel[0]
        yp0=self.originpixel[1]
        dx=self.shapemeters[0]/self.shapepixel[0]
        dy=self.shapemeters[1]/self.shapepixel[1]
        xm=(xp-xp0)*dx - 10
        ym=(yp-yp0)*dy - 4
        return xm, -ym

    def meters2pixel(self,xm,ym):
        xp0=self.originpixel[0]
        yp0=self.originpixel[1]
        dx=self.shapepixel[0]/self.shapemeters[0]
        dy=self.shapepixel[1]/self.shapemeters[1]
        xp=xp0+xm*dx
        yp=yp0-ym*dy
        return xp, yp

    def latlong2local(self,lat,long):
        deg2rad=pi/180
        dfa=6378137
        dfb=6356752
        dftanlat2 = tan(lat*deg2rad)**2
        dfRadius = dfb*sqrt(1+dftanlat2)/sqrt(dfb**2/dfa**2+dftanlat2)
        dXArcDeg  = (long - self.originlatlong[1]) * deg2rad
        x = dfRadius * sin(dXArcDeg)*cos(lat*deg2rad)
        dYArcDeg  = (lat - self.originlatlong[0]) * deg2rad
        y = dfRadius * sin(dYArcDeg)
        return x, y

    def local2latlong(self, x, y):
        deg2rad=pi/180
        rad2deg=180/pi
        dfa=6378137
        dfb=6356752
        dftanlat2 = tan(self.originlatlong[0]*deg2rad)**2
        dfRadius = dfb*sqrt(1+dftanlat2)/sqrt(dfb**2/dfa**2+dftanlat2)
        dfYArcRad = asin( y/dfRadius )
        dfYArcDeg = dfYArcRad * rad2deg
        dfXArcRad = asin( x/( dfRadius*cos( self.originlatlong[0]*deg2rad ) ) )
        dfXArcDeg = dfXArcRad * rad2deg
        Lat = dfYArcDeg + self.originlatlong[0]
        Long = dfXArcDeg + self.originlatlong[1]
        return Lat, Long
        


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('300x200')
    root.title('Planejador de Misões do NACMM')
    frame = NACMMsetup(root)
    frame.load_chart() # para debug
    frame.go_to_origin() # para debug
    frame.pack(side="left", fill="both", expand=True)
    root.mainloop()

    
    