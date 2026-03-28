import tkinter as tk
from tkinter import messagebox, colorchooser
import random, sys, webbrowser, subprocess, os
from time import strftime

# --- SİSTEM DEĞİŞKENLERİ ---
USER = "SAHAN"
SIFRE = "1111"
COP_DOLU = False 
EN_YUKSEK_SKOR = 0 

class Windows9_Sahan_Fix:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows 9")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.bg_renk = "#008080" 
        self.boot_ekrani()

    def boot_ekrani(self):
        for w in self.root.winfo_children(): w.destroy()
        log = tk.Text(self.root, bg="black", fg="#00FF00", font=("Consolas", 12), bd=0, highlightthickness=0)
        log.pack(expand=True, fill="both", padx=50, pady=50)
        specs = ["HP 530 System Ready", "Snake Engine v4.0 Loaded", "---------------------------", "Windows 9 is starting..."]
        def yaz(i=0):
            if i < len(specs):
                log.insert("end", specs[i] + "\n")
                self.root.after(100, lambda: yaz(i+1))
            else:
                self.root.after(500, self.masaustu_kur)
        yaz()

    # --- YILAN OYUNU (TAMAMEN HATASIZ VERSİYON) ---
    def yilan_ac(self):
        global EN_YUKSEK_SKOR
        sw = tk.Toplevel(self.root)
        sw.title("Snake 9.0")
        sw.geometry("400x480")
        sw.resizable(False, False)
        sw.focus_force()
        sw.grab_set()
        
        can = tk.Canvas(sw, bg="black", width=400, height=400, highlightthickness=0)
        can.pack()

        # Oyun Değişkenleri
        self.snk = [[100, 100], [80, 100], [60, 100]]
        self.yon = "Right"
        self.yem = [200, 200]
        self.skor = 0
        self.oyun_aktif = True
        
        lbl = tk.Label(sw, text=f"Skor: {self.skor} | Rekor: {EN_YUKSEK_SKOR}", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        def hareket():
            if not self.oyun_aktif: return

            # Yeni kafa koordinatlarını belirle
            yeni_kafa = list(self.snk[0])
            if self.yon == "Up": yeni_kafa[1] -= 20
            elif self.yon == "Down": yeni_kafa[1] += 20
            elif self.yon == "Left": yeni_kafa[0] -= 20
            elif self.yon == "Right": yeni_kafa[0] += 20

            # 1. DUVARA ÇARPMA KONTROLÜ
            if yeni_kafa[0] < 0 or yeni_kafa[0] >= 400 or yeni_kafa[1] < 0 or yeni_kafa[1] >= 400:
                oyunu_bitir()
                return

            # 2. KENDİNE ÇARPMA KONTROLÜ
            if yeni_kafa in self.snk:
                oyunu_bitir()
                return

            # Kafayı ekle
            self.snk.insert(0, yeni_kafa)

            # 3. ELMA YEME KONTROLÜ
            if yeni_kafa == self.yem:
                self.skor += 10
                lbl.config(text=f"Skor: {self.skor} | Rekor: {EN_YUKSEK_SKOR}")
                # Elmayı yılanın üzerinde olmayacak şekilde yeniden oluştur
                while True:
                    yeni_yem = [random.randrange(0, 400, 20), random.randrange(0, 400, 20)]
                    if yeni_yem not in self.snk:
                        self.yem = yeni_yem
                        break
            else:
                # Elma yememişse kuyruğu sil (boy sabit kalsın)
                self.snk.pop()

            # ÇİZİM
            can.delete("all")
            # Elma
            can.create_oval(self.yem[0], self.yem[1], self.yem[0]+20, self.yem[1]+20, fill="red", outline="white")
            # Yılan
            for i, segment in enumerate(self.snk):
                renk = "#00FF00" if i == 0 else "#008000"
                can.create_rectangle(segment[0], segment[1], segment[0]+20, segment[1]+20, fill=renk, outline="black")
            
            sw.after(150, hareket)

        def oyunu_bitir():
            global EN_YUKSEK_SKOR
            self.oyun_aktif = False
            mesaj = ""
            if self.skor > EN_YUKSEK_SKOR:
                EN_YUKSEK_SKOR = self.skor
                mesaj = f"🏆 REKOR! 🏆\nYeni en yüksek skor: {self.skor}"
            else:
                mesaj = f"Oyun Bitti!\nSkorun: {self.skor}\nRekor: {EN_YUKSEK_SKOR}"
            
            messagebox.showinfo("Snake 9.0", mesaj)
            sw.destroy()

        def yon_degistir(y):
            zit = {"Up":"Down", "Down":"Up", "Left":"Right", "Right":"Left"}
            if y != zit.get(self.yon):
                self.yon = y

        # Tuş Atamaları
        sw.bind("<Up>", lambda e: yon_degistir("Up"))
        sw.bind("<Down>", lambda e: yon_degistir("Down"))
        sw.bind("<Left>", lambda e: yon_degistir("Left"))
        sw.bind("<Right>", lambda e: yon_degistir("Right"))
        
        hareket()

    # --- MASAÜSTÜ ---
    def masaustu_kur(self):
        for w in self.root.winfo_children(): w.destroy()
        self.root.configure(bg=self.bg_renk)
        
        bar = tk.Frame(self.root, bg="#c0c0c0", height=35, bd=2, relief="raised")
        bar.pack(side="bottom", fill="x")
        tk.Button(bar, text="Start", font=("Arial", 9, "bold"), command=self.start_menu).pack(side="left", padx=5)

        s_lbl = tk.Label(bar, bg="#c0c0c0", font=("Arial", 10, "bold"))
        s_lbl.pack(side="right", padx=10)
        def s(): s_lbl.config(text=strftime('%H:%M:%S')); s_lbl.after(1000, s)
        s()

        # İKONLAR
        self.ikon(40, 40, "Bilgisayarım", "💻", lambda: os.startfile("explorer.exe"), True)
        self.ikon(40, 130, "Not Defteri", "📝", lambda: subprocess.Popen("notepad.exe"))
        self.ikon(40, 220, "CMD", "⌨️", lambda: subprocess.Popen("start cmd", shell=True))
        self.ikon(130, 40, "Yılan Oyunu", "🐍", self.yilan_ac)
        self.ikon(130, 130, "Google", "🌐", lambda: webbrowser.open("https://www.google.com"))
        self.ikon(130, 220, "Hesap Mak.", "🧮", lambda: subprocess.Popen("calc.exe"))

    def ikon(self, x, y, isim, emoji, cmd, kritik=False):
        f = tk.Frame(self.root, bg=self.bg_renk)
        b = tk.Button(f, text=f"{emoji}\n{isim}", fg="white", bg=self.bg_renk, bd=0, command=cmd)
        b.pack(); f.place(x=x, y=y)
        im = tk.Menu(self.root, tearoff=0)
        im.add_command(label="Aç", command=cmd)
        def sil():
            if kritik: self.tetikle_bsod()
            else: f.destroy()
        im.add_command(label="SİL", command=sil)
        b.bind("<Button-3>", lambda e: im.post(e.x_root, e.y_root))

    def start_menu(self):
        sm = tk.Menu(self.root, tearoff=0)
        sm.add_command(label="🐍 Yılan", command=self.yilan_ac)
        sm.add_separator()
        sm.add_command(label="🛑 Kapat", command=sys.exit)
        sm.post(5, self.root.winfo_height() - 100)

    def tetikle_bsod(self):
        for w in self.root.winfo_children(): w.destroy()
        self.root.configure(bg="#0000AA")
        tk.Label(self.root, text=":( WINDOWS XP ERROR\n\nSTOP: 0x000000F4", fg="white", bg="#0000AA", font=("Lucida Console", 14)).pack(pady=100)
        self.root.after(3000, sys.exit)

if __name__ == "__main__":
    root = tk.Tk()
    app = Windows9_Sahan_Fix(root)
    root.mainloop()