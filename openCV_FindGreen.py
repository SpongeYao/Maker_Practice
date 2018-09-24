# -*- coding: UTF-8 -*-
import json
import Tkinter
import tkFont
import cv2
import numpy as np
import tkFileDialog
from PIL import Image
from PIL import ImageTk

class App:
    # ======= 初始化設定 ===============
    def __init__(self,root):
        self.root = root
        self.root.update()
        #------------------
        # [1. 產生畫布]
        #------------------
        #'''
        #===== 設定字體 ======
        myfont14 = tkFont.Font(family="Verdana", size=14)
        myfont12 = tkFont.Font(family="Verdana", size=12)
        #===== 取得顯示畫面寬度、高度========
        self.screen_width, self.screen_height = self.root.winfo_width(), self.root.winfo_height()
        self.frame_width, self.frame_height= int(self.screen_width*0.8), int(self.screen_height)
        btn_width, btn_height= 15, 2
        
        #===== 設定畫布位置大小 ======
        self.frame= np.zeros((int(self.frame_height), int(self.frame_width), 3), np.uint8) 
        cv2.putText(self.frame, 'Display Image',(10,50),cv2.FONT_HERSHEY_SIMPLEX, 2,(255,255,255),2)
        print self.frame.shape 
        result = Image.fromarray(self.frame)
        result = ImageTk.PhotoImage(result)
        self.panel = Tkinter.Label(self.root , image = result)
        self.panel.image = result 
        self.panel.place(x=0, y=0)
        self.root.update()
        #'''


        #------------------
        # [2. 產生讀取圖片按鈕]
        #------------------
        #'''
        # ====== 設定按鈕位置大小 ============
        self.btn_loadImg= Tkinter.Button(self.root, text= '讀取圖片', command= self.btn_loadImg_click,font= myfont14, width= btn_width, height=btn_height)
        self.btn_loadImg.place(x= self.frame_width+12, y=6)
        self.root.update()
        #'''
        #------------------
        # [3. 產生尋找按鈕]
        #------------------
        #'''
        # ====== 設定按鈕位置大小 ============
        self.btn_saveImg= Tkinter.Button(self.root, text= '儲存圖片', command= self.btn_saveImg_click,font= myfont14, width= btn_width, height=btn_height)
        self.btn_saveImg.place(x= self.btn_loadImg.winfo_x(), y=self.btn_loadImg.winfo_y()+self.btn_loadImg.winfo_height()+ 6)
        self.root.update()
        #'''


        #------------------
        # [4. 產生二值化按鈕]
        #------------------
        #'''
        # ====== 設定按鈕位置大小 ============
        self.btn_binarization= Tkinter.Button(self.root, text='二值化', command= self.btn_binarization_click,font= myfont14, width= btn_width, height= btn_height)
        self.btn_binarization.place(x= self.btn_saveImg.winfo_x(), y=self.btn_saveImg.winfo_y()+self.btn_saveImg.winfo_height()+ 6)
        self.root.update()
        #'''
        #------------------
        # [5. 產生二值化閥值滾軸]
        #------------------
        #'''
        self.threshold_graylevel= 125
        self.scale_threshold_graylevel = Tkinter.Scale(self.root , from_= 0 , to = 255 , orient = Tkinter.HORIZONTAL , label = "二值化閥值（0~255）", font = myfont12, width = 7, length = 200 )
        self.scale_threshold_graylevel.set(self.threshold_graylevel)
        self.scale_threshold_graylevel.place(x= self.btn_binarization.winfo_x(), y=self.btn_binarization.winfo_y()+self.btn_binarization.winfo_height()+ 6)
        self.root.update()
        #'''
        #------------------
        # [6. 產生尋找綠色按鈕]
        #------------------
        #'''
        # ====== 設定按鈕位置大小 ============
        self.btn_findGreen= Tkinter.Button(self.root, text='尋找綠色', command= self.btn_findGreen_click,font= myfont14, width= btn_width, height= btn_height)
        self.btn_findGreen.place(x= self.scale_threshold_graylevel.winfo_x(), y=self.scale_threshold_graylevel.winfo_y()+self.scale_threshold_graylevel.winfo_height()+ 6)
        self.root.update()
        #'''

    # ======= 顯示圖片至畫布 ==========
    def display_panel(self, arg_frame):
        if len(arg_frame.shape)==3:
            tmp_frame= cv2.cvtColor(arg_frame, cv2.COLOR_BGR2RGB)
        else:
            tmp_frame= cv2.cvtColor(arg_frame, cv2.COLOR_GRAY2RGB)

        tmp_frame= cv2.resize(tmp_frame,(self.frame_width,self.frame_height),interpolation=cv2.INTER_LINEAR)	#2018.02.20-???
        result = Image.fromarray(tmp_frame)
        result = ImageTk.PhotoImage(result)
        self.panel.configure(image = result)
        self.panel.image = result 
        self.root.update()

    # ======= 讀取圖片 ============
    def btn_loadImg_click(self):
        str_imagePath = tkFileDialog.askopenfilename(title = "選擇圖檔",filetypes = (("all files","*.*"),("jpeg files","*.jpg"),("png files","*.png")))
        self.frame= cv2.imread(str_imagePath)
        self.display_panel(self.frame)
        pass 

    # ======= 儲存圖片 ============
    def btn_saveImg_click(self):
        str_imagePath = tkFileDialog.asksaveasfilename(title = "儲存檔案",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("tif files","*.tif")))
        cv2.imwrite(str_imagePath,self.frame)
        pass

    # ======= 二值化處理 ============
    def btn_binarization_click( self):
        tmp_frame= cv2.cvtColor(self.frame.copy(), cv2.COLOR_BGR2GRAY)
        self.threshold_graylevel= self.scale_threshold_graylevel.get()
        ret, img_thr= cv2.threshold(tmp_frame, self.threshold_graylevel, 255 , 0)
        self.display_panel( img_thr) 

    # ======= 尋找綠色 ===========
    def btn_findGreen_click(self):
        #---- BGR轉成 hsv通道
        imgHSV = cv2.cvtColor(self.frame.copy(), cv2.COLOR_BGR2HSV)
        #---- 定義上下界線 -------
        lower_color = np.array([35, 43, 46])
        upper_color = np.array([77, 225, 225])

        plants = cv2.inRange(imgHSV, lower_color , upper_color)
        ctrs,_ = cv2.findContours(plants,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
        ctrs = filter(lambda x : cv2.contourArea(x) > 13 , ctrs)
        image= self.frame.copy()
        for c in ctrs:
            cv2.drawContours(image, [c], 0, (0,0,255), 1)
        self.display_panel(image)

        pass 
    
    def mark_cross_line(self , frame):
        w = frame.shape[0] / 2
        h = frame.shape[1] / 2
        cv2.line(frame , (h - 15 , w) , (h + 15 , w) , (0 , 255 , 0) , 2)
        cv2.line(frame , (h , w - 15) , (h , w + 15) , (0 , 255 , 0) , 2)
        return frame




root = Tkinter.Tk()
root.title("範例")
root.attributes('-zoomed', True) #放到最大 
app = App(root)
root.mainloop()



