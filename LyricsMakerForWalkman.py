import pygame.mixer
import time
import math
import datetime
import os
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from tkinter import messagebox
import tkinter as tk
import sys
import configparser
from configobj import ConfigObj
import chardet
from mutagen.mp3 import MP3 as mp3
from mutagen.wave import WAVE as wav


class GUI2():
    def __init__(self, lyrics, sound, output_dir, no_intro, timing):

        #パスとイントロの有無を入力
        self.lyrics = lyrics
        self.sound = sound
        self.output_dir = output_dir
        self.no_intro = no_intro
        self.timing = timing

        #変数の初期化
        self.ITIME: float = 0
        self.tmlist = []
        self.cnt: int = 0

        #歌詞の読み込み
        lyrics = r"" + lyrics
        with open(lyrics, "rb") as f: #エンコーディングの種類の検出
            tmp = f.read()
            enc = chardet.detect(tmp)

        f = open(lyrics, "r", encoding=enc["encoding"])

        self.lylist: list = f.readlines()

        #音声の読み込み
        filename = r""+self.sound
        if (".mp3" in filename)==True:
            pygame.mixer.init(frequency = mp3(filename).info.sample_rate)
        else: #wav
            pygame.mixer.init(frequency = wav(filename).info.sample_rate)
        pygame.mixer.music.load(filename)     # 音楽ファイルの読み込み


    def main(self):

        #GUIの表示
        self.lylist.insert(0,"...")
        self.lylist.append("...")
        self.lylist.append("...")
        
        if self.no_intro == "1":
            self.tmlist.append("00:00.00")
            self.cnt += 1

        self.root2 = tk.Tk()
        self.root2.focus_force()
        self.root2.title('Lyrics Maker for Walkman')
        self.root2.geometry('600x200')

        self.frame21 = ttk.Frame(self.root2, padding=(32))
        self.frame21.pack()

        self.label21 = ttk.Label(self.frame21, text=self.lylist[self.cnt],   padding = (5, 2), font = (None, 15))
        self.label22 = ttk.Label(self.frame21, text=self.lylist[self.cnt+1], padding = (5, 2))
        self.label23 = ttk.Label(self.frame21, text=self.lylist[self.cnt+2], padding = (5, 2))
        """
        もしイントロがなければ'...'から
        あれば歌詞の先頭から
        """

        self.label21.pack()
        self.label22.pack()
        self.label23.pack()

        #スタート時間の記録と再生
        pygame.mixer.music.play(1)              
        self.ITIME = time.time() + self.timing

        #キー入力の検出
        self.root2.bind("<KeyPress>", self.key_event)

        self.root2.mainloop()


    def time_stamp(self): 

        try:
            self.cnt+=1

            #表示する歌詞の更新
            self.label21["text"] = self.lylist[self.cnt]
            self.label22["text"] = self.lylist[self.cnt+1]
            self.label23["text"] = self.lylist[self.cnt+2]

            #呼び出されたら経過時間をリストに代入
            ct = datetime.timedelta(seconds = (math.floor((time.time()-self.ITIME)*100)/100)) #0:00:01.100000, current time
            ctstr = str(ct)
            ctstr=ctstr[2:10]
            self.tmlist.append(ctstr)

        except IndexError:
            self.output()




    def output(self): #最終処理

        #音声の停止
        pygame.mixer.music.stop()
        
        #時間を書き出し
        otlist=[]
        for n in range(len(self.tmlist)):
            otlist.append("["+self.tmlist[n]+"]"+self.lylist[n+1])

        file_name = os.path.basename(self.lyrics).replace("txt", "lrc")
        with open((r""+self.output_dir+"/"+file_name), mode="w") as f:
            f.writelines(otlist)

        self.root2.destroy()
        messagebox.showinfo("Info", "Successfully generated")

        #終了
        delete(self)


    def key_event(self, e): #キー入力処理
        key = e.keysym
        
        if key == "space":
            self.time_stamp()

        elif key == "Return":
            self.output()
    
    
    
class  GUI1:
    def main(self):

        #GUIの表示
        root = Tk()
        root.title('Lyrics Maker for Walkman')
        root.resizable(False, False)
        root.focus_force()
        frame1 = ttk.Frame(root, padding=(32))
        frame1.pack()

        """label"""
        label1 = ttk.Label(frame1, text='Lyrics', padding=(5, 2))
        label1.grid(row=0, column=0, sticky=E)

        label2 = ttk.Label(frame1, text='Sound Source', padding=(5, 2))
        label2.grid(row=1, column=0, sticky=E)

        label3 = ttk.Label(frame1, text='Output', padding=(5, 2))
        label3.grid(row=2, column=0, sticky=E)

        label4 = ttk.Label(frame1, text='Timing(ms)', padding=(5, 2))
        label4.grid(row=3, column=0, sticky=E)

        tm_val = tk.IntVar()
        label4 = ttk.Label(frame1, text="0", textvariable=tm_val, padding=(5, 2))
        label4.grid(row=3, column=2, sticky=W)

        """entry"""
        # lyrics Entry
        lrc = StringVar()
        lrc_entry = ttk.Entry(
            frame1,
            textvariable=lrc,
            width=40)
        lrc_entry.grid(row=0, column=1)

        # sound sorce Entry
        snd = StringVar()
        snd_entry = ttk.Entry(
            frame1,
            textvariable=snd,
            width=40)
        snd_entry.grid(row=1, column=1)

        # output Entry
        out = StringVar()
        out_entry = ttk.Entry(
            frame1,
            textvariable=out,
            width=40)
        out_entry.grid(row=2, column=1)

        #初期値入力
        LSOT_list = self.config_r()
        lrc.set(LSOT_list[0])
        snd.set(LSOT_list[1])
        out.set(LSOT_list[2])

        """button"""

        lrc_bt = ttk.Button(
            frame1, text='Browse',
            command=lambda: lrc.set(self.fileget("lrc", "テキストファイル", "*.txt")))
        lrc_bt.grid(row=0, column=2)

        snd_bt = ttk.Button(
            frame1, text='Browse',
            command=lambda: snd.set(self.fileget("snd", "音声ファイル", "*.mp3;*.wav")))
        snd_bt.grid(row=1, column=2)

        out_bt = ttk.Button(
            frame1, text='Browse',
            command=lambda: out.set(self.dirget()))
        out_bt.grid(row=2, column=2)

        reset_bt = ttk.Button(
            frame1, text='Timing Reset',
            command= lambda: [sc_val.set(0), tm_val.set(0)]

        )
        reset_bt.grid(row=4, column=2, sticky=E)

        """scale"""

        sc_val = tk.DoubleVar()
        sc = ttk.Scale(
            frame1, 
            variable=sc_val,
            orient=HORIZONTAL,
            length=250,
            from_=-500,
            to=500,
            command=lambda e: tm_val.set(value=round(sc_val.get()))
        )
        sc.set(LSOT_list[3]*1000)    
        sc.grid(row=3, column=1, sticky=W)
            
        """check box"""
        v1 = StringVar()
        v1.set('0') # 初期化、checkありで１
        cb1 = ttk.Checkbutton(
            frame1, padding=(10), text='No intro',
            variable=v1,
            )
        cb1.grid(row=4, column=1, sticky=W)

        """Start or Cancel Button"""
        frame2 = ttk.Frame(frame1, padding=(0, 5))
        frame2.grid(row=5, column=1, sticky=N)

        button1 = ttk.Button(
            frame2, text='Start',
            command=lambda: switch(lrc.get(), snd.get(), out.get(),
                                    v1.get(), (sc_val.get()/1000), self, root))
        button1.pack(side=LEFT)

        button2 = ttk.Button(frame2, text='Cancel', command=sys.exit)
        button2.pack(side=LEFT)

        root.mainloop()


    def config_r(self): #config読み込み

        if os.path.isfile("config.ini") == True:

            cnfg = configparser.ConfigParser()
            cnfg.read("config.ini", encoding = "utf-8")

            lrc = cnfg.get("DEFAULT", "lyrics")
            snd = cnfg.get("DEFAULT", "sound_source")
            out = cnfg.get("DEFAULT", "output")
            tmg = float(cnfg.get("DEFAULT", "timing"))

            return lrc, snd, out, tmg
        
        else:

            new_config = configparser.ConfigParser()
            new_config["DEFAULT"] = {
                "lyrics" : " ",
                "sound_source" : " ",
                "output" : " ",
                "timing" : "0"
            }
            
            with open("config.ini", "w") as f:
                new_config.write(f)
            
            lrc = ""
            snd = ""
            out = ""
            tmg = 0

            return lrc, snd, out, tmg


    def config_w(self, lyrics, sound_source, output, timing): #config書き込み
        config = ConfigObj("config.ini", encoding = "utf-8")
        
        config["DEFAULT"]["lyrics"] = lyrics
        config["DEFAULT"]["sound_source"] = sound_source
        config["DEFAULT"]["output"] =output
        config["DEFAULT"]["timing"] =timing

        config.write()


    def fileget(self, val_name, filetype, ext): #initialdirが存在しないときは勝手に最近開いたフォルダが表示される
        
        fTyp = [(filetype, ext)]

        if val_name == "lrc":
            file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp,
                                                            initialdir=os.path.dirname(self.config_r()[0]))
            if file_name == "":
                file_name = self.config_r()[0]
        elif val_name == "snd":
            file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp,
                                                            initialdir=os.path.dirname(self.config_r()[1]))
            if file_name == "":
                file_name = self.config_r()[1]

        return file_name


    def dirget(self):
        DirPath = tkinter.filedialog.askdirectory(initialdir = self.config_r()[2])
        if DirPath == "":
            DirPath =  self.config_r()[2]  
        return DirPath



def switch(lrc, snd, out, no_intro, timing, instance, root): #GUIを１から２へ

    #設定画面の削除
    root.destroy()

    #パスの存在確認
    if os.path.isfile(lrc) == False:
        messagebox.showwarning("Warning", "Lyrics file NOT exsiting")
        del instance
        win = GUI1()
        win.main()
    elif os.path.isfile(snd) == False:
        messagebox.showwarning("Warning", "Sound file NOT exsiting")
        del instance
        win = GUI1()
        win.main()
    elif os.path.isdir(out) == False:
        messagebox.showwarning("Warning", "Output directory NOT exsiting")
        del instance
        win = GUI1()
        win.main()

    else: #インスタンス削除とGUI1で入力された情報の記録と歌詞画面の作成
        instance.config_w(lrc, snd, out, str(timing))
        del instance
        win = GUI2(lrc, snd, out, no_intro, timing)
        win.main()


def delete(instance):
    del instance
    pygame.mixer.music.stop()
    win = GUI1()
    win.main()
                   




if __name__=="__main__":
    win = GUI1()
    win.main()
