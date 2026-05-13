import sqlite3
import os
from models import Ogrenci, Ders

DB_DOSYASI = "ogrenci_not_sistemi.db"

def baglanti_al():
    return sqlite3.connect(DB_DOSYASI)

def kaydet(ogrenci_listesi: list[Ogrenci]):
    conn = baglanti_al()
    cursor = conn.cursor()
    
    # Mevcut verileri temizle
    cursor.execute("DELETE FROM dersler")
    cursor.execute("DELETE FROM ogrenciler")
    
    # Güncel listeyi tabloya yaz
    for ogr in ogrenci_listesi:
        cursor.execute("INSERT INTO ogrenciler (numara, ad_soyad) VALUES (?, ?)", 
                       (ogr.numara, ogr.ad_soyad))
        for ders in ogr.dersler():
            cursor.execute("INSERT INTO dersler (ogrenci_numara, ders_adi, not_degeri) VALUES (?, ?, ?)", 
                           (ogr.numara, ders.ders_adi, ders.not_degeri))
    
    conn.commit()
    conn.close()

def yukle() -> list[Ogrenci]:
    if not os.path.exists(DB_DOSYASI):
        return []

    conn = baglanti_al()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ogrenciler")
    ogrenciler_rows = cursor.fetchall()
    
    ogrenci_listesi = []
    for ogr_row in ogrenciler_rows:
        ogr = Ogrenci(ogr_row["ad_soyad"], ogr_row["numara"])
        
        cursor.execute("SELECT ders_adi, not_degeri FROM dersler WHERE ogrenci_numara = ?", (ogr.numara,))
        ders_rows = cursor.fetchall()
        for d_row in ders_rows:
            ogr.ders_ekle(Ders(d_row["ders_adi"], d_row["not_degeri"]))
            
        ogrenci_listesi.append(ogr)
        
    conn.close()
    return ogrenci_listesi

def numara_var_mi(ogrenci_listesi, numara):
    return any(ogr.numara == numara for ogr in ogrenci_listesi)

def numara_ile_bul(ogrenci_listesi, numara):
    for ogr in ogrenci_listesi:
        if ogr.numara == numara:
            return ogr
    return None
