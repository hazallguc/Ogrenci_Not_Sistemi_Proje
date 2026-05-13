import tkinter as tk
from tkinter import messagebox, ttk
import database as db
from models import Ogrenci, Ders

class NotSistemiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student AI Management Dashboard")
        self.root.geometry("1200x750")
        self.root.configure(bg="#0f172a") # Derin Gece Mavisi Arka Plan
        
        self.ogrenci_listesi = db.yukle()
        self.setup_styles()
        self.setup_ui()
        self.listeyi_guncelle()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Tablo Tasarımı
        style.configure("Treeview", 
                        background="#1e293b", 
                        foreground="white", 
                        fieldbackground="#1e293b",
                        rowheight=40,
                        font=('Segoe UI', 10))
        style.map("Treeview", background=[('selected', '#3b82f6')]) # Seçili satır canlı mavi
        
        style.configure("Treeview.Heading", 
                        background="#334155", 
                        foreground="white", 
                        font=('Segoe UI', 11, 'bold'),
                        borderwidth=0)

    def setup_ui(self):
        # --- Sol Kenar Çubuğu (Side Panel) ---
        side_panel = tk.Frame(self.root, bg="#1e293b", width=300)
        side_panel.pack(side="left", fill="y")
        
        tk.Label(side_panel, text="KONTROL PANELİ", fg="#3b82f6", bg="#1e293b", 
                 font=('Segoe UI', 14, 'bold'), pady=30).pack()

        # Giriş Alanları Fonksiyonu
        def create_input(label, attr):
            tk.Label(side_panel, text=label, fg="#94a3b8", bg="#1e293b", font=('Segoe UI', 9)).pack(anchor="w", padx=20)
            entry = tk.Entry(side_panel, bg="#0f172a", fg="white", insertbackground="white", 
                             relief="flat", font=('Segoe UI', 11))
            entry.pack(fill="x", padx=20, pady=(5, 15), ipady=8)
            setattr(self, attr, entry)
            return entry

        self.ent_no = create_input("Öğrenci Numarası", "ent_no")
        self.ent_no.bind("<KeyRelease>", lambda e: self.listeyi_guncelle())
        self.ent_ad = create_input("Ad Soyad", "ent_ad")
        self.ent_ders = create_input("Ders Adı", "ent_ders")
        self.ent_not = create_input("Not", "ent_not")

        # İşlem Butonu
        self.btn_islem = tk.Button(side_panel, text="KAYDET / GÜNCELLE", command=self.veri_islem, 
                                   bg="#3b82f6", fg="white", font=('Segoe UI', 10, 'bold'), 
                                   relief="flat", cursor="hand2", activebackground="#2563eb")
        self.btn_islem.pack(fill="x", padx=20, pady=20, ipady=10)

        # --- Sağ Ana Bölüm ---
        main_area = tk.Frame(self.root, bg="#0f172a")
        main_area.pack(side="right", fill="both", expand=True, padx=30, pady=30)

        # Üst Bilgi Kartları
        info_frame = tk.Frame(main_area, bg="#0f172a")
        info_frame.pack(fill="x", pady=(0, 20))
        
        self.lbl_stats = tk.Label(info_frame, text="Toplam Öğrenci: 0", fg="white", bg="#0f172a", font=('Segoe UI', 12))
        self.lbl_stats.pack(side="left")

        # Tablo Konteynırı (Rounded look effect)
        table_frame = tk.Frame(main_area, bg="#1e293b", bd=0)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("No", "Ad", "Ders1", "Ders2", "Ort", "Durum"), show="headings")
        
        cols = [("No", "ID"), ("Ad", "ÖĞRENCİ"), ("Ders1", "DERS 1"), ("Ders2", "DERS 2"), ("Ort", "ORT."), ("Durum", "DURUM")]
        for id, txt in cols:
            self.tree.heading(id, text=txt)
            self.tree.column(id, anchor="center", width=100)
        
        self.tree.column("Ad", width=200, anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.satir_secildi)

        # Alt Aksiyonlar
        bottom_frame = tk.Frame(main_area, bg="#0f172a", pady=20)
        bottom_frame.pack(fill="x")

        tk.Button(bottom_frame, text="🗑 SİL", command=self.ogrenci_sil, bg="#ef4444", fg="white", 
                  relief="flat", font=('Segoe UI', 9, 'bold'), padx=20).pack(side="left")
        
        tk.Button(bottom_frame, text="📥 VERİLERİ SİSTEME YEDEKLE", command=self.kaydet, bg="#10b981", fg="white", 
                  relief="flat", font=('Segoe UI', 9, 'bold'), padx=20).pack(side="right")

    def satir_secildi(self, event):
        secili = self.tree.selection()
        if not secili: return
        val = self.tree.item(secili[0])['values']
        self.ent_no.delete(0, tk.END); self.ent_no.insert(0, val[0])
        self.ent_ad.delete(0, tk.END); self.ent_ad.insert(0, val[1])

    def veri_islem(self):
        ad, no, ders, n_str = self.ent_ad.get().strip(), self.ent_no.get().strip(), \
                             self.ent_ders.get().strip(), self.ent_not.get().strip()
        
        if not no: return
        ogr = next((o for o in self.ogrenci_listesi if o.numara == no), None)
        if not ogr:
            if ad:
                ogr = Ogrenci(ad, no); self.ogrenci_listesi.append(ogr)
            else: return messagebox.showwarning("Hata", "Öğrenci bulunamadı!")

        if ders and n_str:
            try:
                n = float(n_str)
                if not ogr.ders_guncelle(ders, n): ogr.ders_ekle(Ders(ders, n))
            except Exception as e: return messagebox.showerror("Hata", str(e))
        
        self.listeyi_guncelle()
        self.ent_ders.delete(0, tk.END); self.ent_not.delete(0, tk.END)

    def listeyi_guncelle(self):
        ara = self.ent_no.get().strip().lower()
        for i in self.tree.get_children(): self.tree.delete(i)
        count = 0
        for o in self.ogrenci_listesi:
            if ara == "" or ara in o.numara.lower():
                count += 1
                d = o.dersler()
                d1 = str(d[0]) if len(d) > 0 else "---"
                d2 = str(d[1]) if len(d) > 1 else "---"
                self.tree.insert("", "end", values=(o.numara, o.ad_soyad, d1, d2, f"{o.ortalama():.2f}", o.durum()))
        self.lbl_stats.config(text=f"Sistemdeki Toplam Öğrenci: {count}")

    def ogrenci_sil(self):
        secili = self.tree.selection()
        if not secili: return
        if messagebox.askyesno("Onay", "Bu öğrenci kaydı kalıcı olarak silinsin mi?"):
            no = self.tree.item(secili[0])['values'][0]
            self.ogrenci_listesi = [o for o in self.ogrenci_listesi if o.numara != str(no)]
            self.listeyi_guncelle()

    def kaydet(self):
        db.kaydet(self.ogrenci_listesi)
        messagebox.showinfo("Sistem Mesajı", "Tüm veriler başarıyla SQLite veritabanına yedeklendi.")