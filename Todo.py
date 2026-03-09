import datetime
import os

GOREV_DOSYASI_ADI = "benim_gorevlerim.txt"

def gorevleri_getir_oku():
    gorevler = []
    if os.path.exists(GOREV_DOSYASI_ADI):
        with open(GOREV_DOSYASI_ADI, "r", encoding="utf-8") as dosya:
            for satir in dosya:
                try:
                    parcalar = satir.strip().split("|")
                    if len(parcalar) == 4:
                        gorevler.append({
                            "ne_yapilacak": parcalar[0],
                            "ne_zaman_eklendi": parcalar[1],
                            "kac_puan": int(parcalar[2]),
                            "bitti_mi": parcalar[3] == "True"
                        })
                    else:
                        print(f"Uyarı: Hatalı formatta satır atlandı: {satir.strip()}")
                except ValueError:
                    print(f"Uyarı: Puan dönüşüm hatası, satır atlandı: {satir.strip()}")
    return gorevler

def gorevleri_diska_yaz(gorevler):
    with open(GOREV_DOSYASI_ADI, "w", encoding="utf-8") as dosya:
        for gorev in gorevler:
            dosya.write(f"{gorev['ne_yapilacak']}|{gorev['ne_zaman_eklendi']}|{gorev['kac_puan']}|{gorev['bitti_mi']}\n")

def yeni_gorev_ekle(gorevler):
    while True:
        gorev_adi = input("Eklenecek görevi girin: ").strip()
        if gorev_adi:
            break
        else:
            print("Görev adı boş olamaz. Lütfen geçerli bir görev girin.")

    while True:
        try:
            puan = int(input("Görevin puanını girin (sayı): "))
            break
        except ValueError:
            print("Geçersiz puan. Lütfen bir sayı girin.")

    simdiki_zaman = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    gorevler.append({
        "ne_yapilacak": gorev_adi,
        "ne_zaman_eklendi": simdiki_zaman,
        "kac_puan": puan,
        "bitti_mi": False
    })
    gorevleri_diska_yaz(gorevler)
    print("Görev başarıyla eklendi.")

def gorev_ustunde_oyna(gorevler):
    if not gorevler:
        print("Görev listesi boş.")
        return

    gorevleri_goster_hepsini(gorevler)
    try:
        secilen_index = int(input("Düzenlemek istediğiniz görevin numarasını girin (1'den başlar): ")) - 1
        if 0 <= secilen_index < len(gorevler):
            yeni_ad = input(f"'{gorevler[secilen_index]['ne_yapilacak']}' için yeni görev adı (değiştirmek istemiyorsanız boş bırakın): ")
            if yeni_ad:
                gorevler[secilen_index]["ne_yapilacak"] = yeni_ad

            while True:
                yeni_puan_str = input(f"'{gorevler[secilen_index]['ne_yapilacak']}' için yeni puan (değiştirmek istemiyorsanız boş bırakın): ")
                if not yeni_puan_str:
                    break
                try:
                    gorevler[secilen_index]["kac_puan"] = int(yeni_puan_str)
                    break
                except ValueError:
                    print("Geçersiz puan. Lütfen bir sayı girin.")

            gorevler[secilen_index]["ne_zaman_eklendi"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            gorevleri_diska_yaz(gorevler)
            print("Görev başarıyla güncellendi.")
        else:
            print("Geçersiz görev numarası.")
    except ValueError:
        print("Geçersiz giriş. Lütfen bir sayı girin.")

def gorev_yok_et(gorevler):
    if not gorevler:
        print("Silinecek görev bulunmuyor.")
        return

    gorevleri_goster_hepsini(gorevler)
    try:
        secilen_index = int(input("Silmek istediğiniz görevin numarasını girin (1'den başlar): ")) - 1
        if 0 <= secilen_index < len(gorevler):
            silinen = gorevler.pop(secilen_index)
            gorevleri_diska_yaz(gorevler)
            print(f"'{silinen['ne_yapilacak']}' görevi silindi.")
        else:
            print("Geçersiz görev numarası.")
    except ValueError:
        print("Geçersiz giriş. Lütfen bir sayı girin.")

def gorev_bitir_isaretle(gorevler):
    if not gorevler:
        print("Tamamlanacak görev bulunmuyor.")
        return

    gorevleri_goster_hepsini(gorevler)

    try:
        secilen_index = int(input("Tamamlamak istediğiniz görevin numarasını girin (1'den başlar): ")) - 1

        if 0 <= secilen_index < len(gorevler):
            gorevler[secilen_index]["bitti_mi"] = not gorevler[secilen_index]["bitti_mi"]

            if gorevler[secilen_index]["bitti_mi"]:
                mesaj = "tamamlandı"
            else:
                mesaj = "tamamlanmadı olarak işaretlendi"

            gorevleri_diska_yaz(gorevler)

            print(f"'{gorevler[secilen_index]['ne_yapilacak']}' görevi {mesaj}.")
        else:
            print("Geçersiz görev numarası. Lütfen listeden bir sayı seçin.")

    except ValueError:
        print("Hatalı giriş. Lütfen yalnızca bir sayı girin.")

def tum_gorevleri_temizle(gorevler):
    if not gorevler:
        print("Silinecek görev bulunmuyor.")
        return

    onay = input("Tüm görevleri silmek istediğinizden emin misiniz? (evet/hayır): ").lower()
    if onay == "evet":
        gorevler.clear()
        gorevleri_diska_yaz(gorevler)
        print("Tüm görevler silindi.")
    else:
        print("İşlem iptal edildi.")

def gorevleri_goster_hepsini(gorevler):
    if not gorevler:
        print("Yapılacaklar listesi boş.")
        return

    print("\n--- Yapılacaklar Listesi ---")
    for i, gorev in enumerate(gorevler):
        durum_isareti = "✓" if gorev['bitti_mi'] else " "
        print(f"{i + 1}. [{durum_isareti}] Görev: {gorev['ne_yapilacak']} | Eklendiği Tarih: {gorev['ne_zaman_eklendi']} | Puan: {gorev['kac_puan']}")
    print("----------------------------\n")

def ana_ekran():
    benim_gorevlerim = gorevleri_getir_oku()

    while True:
        print("\n--- Menü ---")
        print("1. Görev Ekle")
        print("2. Görev Düzenle")
        print("3. Görev Sil")
        print("4. Görev Tamamlandı Olarak İşaretle")
        print("5. Tüm Görevleri Sil")
        print("6. Görevleri Listele")
        print("7. Çıkış")
        print("------------")

        secimim = input("Lütfen bir seçenek girin (1-7): ")

        if secimim == "1":
            yeni_gorev_ekle(benim_gorevlerim)
        elif secimim == "2":
            gorev_ustunde_oyna(benim_gorevlerim)
        elif secimim == "3":
            gorev_yok_et(benim_gorevlerim)
        elif secimim == "4":
            gorev_bitir_isaretle(benim_gorevlerim)
        elif secimim == "5":
            tum_gorevleri_temizle(benim_gorevlerim)
        elif secimim == "6":
            gorevleri_goster_hepsini(benim_gorevlerim)
        elif secimim == "7":
            print("Uygulamadan çıkılıyor.")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    ana_ekran()