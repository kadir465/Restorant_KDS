import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

class YemekSepetiDoner:
    def __init__(self):
        self.driver=webdriver.Chrome()
        self.wait=WebDriverWait(self.driver,20)
        self.url="https://tgoyemek.com/arama?searchQuery=d%C3%B6ner"
    
    def arama_yap_ve_veri_cek(self):
        try:
            print("siteye giriliyor...")
            self.driver.get(self.url)
            self.driver.maximize_window()

            restaurant_css_selctor=".group.flex.flex-col.text-neutral-dark"

            print("restoranların yüklenmesi bekleniyor...")
            self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,restaurant_css_selctor))

            )
            print("restoranlar yüklendi.")
            elementler=self.driver.find_elements(By.CSS_SELECTOR,restaurant_css_selctor)
            print(f"toplam {len(elementler)} adet restoran bulundu.")

            cekilen_veriler=[]
            for element in elementler:
                cekilen_veri=element.text.strip()
                cekilen_veriler.append(cekilen_veri)
                print("--- BULUNAN RESTORAN ---")
                print(cekilen_veri)
                print("--------------------------")
            self.dosyaya_yaz(cekilen_veriler)

        except Exception as e:
            print(f"işlem sırasında hata oluştu: {e}")
        finally:
            print("tarayıcı kapatılıyor.")
            self.driver.quit()
    
    def dosyaya_yaz(self,veriler,dosya_adi="trendyol_doner_sonuclari.txt"):
        if not veriler:
            print("kaydedilen veri yok")
            return
        try:
            with open(dosya_adi,"w",encoding="utf-8") as f:
                for veri in veriler:
                    f.write(veri+"\n\n")
                    f.write("================================\n")
            print(f"Veriler {dosya_adi} dosyasına kaydedildi.")
        
        except Exception as e:
            print(f"Dosyaya yazma sırasında hata oluştu: {e}")
        
if __name__=="__main__":
    trendyol_doner=YemekSepetiDoner()
    trendyol_doner.arama_yap_ve_veri_cek()