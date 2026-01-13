import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

# ChromeDriver'ı otomatik olarak yükle/güncelle
chromedriver_autoinstaller.install()

class TrendyolPizza:
    def __init__(self):
        self.driver = webdriver.Chrome()
        # Bekleme süresini 20 saniye olarak ayarlıyoruz
        self.wait = WebDriverWait(self.driver, 20)
        self.url = "https://tgoyemek.com/arama?searchQuery=pizza"

    def arama_yap_ve_veri_cek(self):
        try:
            print("Siteye giriliyor...")
            self.driver.get(self.url)
            self.driver.maximize_window()
            
            # class name yerine css selector kullan birden çok class da işe yarar ve  class adının aralşarına nokta koysan yeterli olur
            restaurant_css_selector = ".group.flex.flex-col.text-neutral-dark"
            
            print("Restoranların yüklenmesi bekleniyor...")
            self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, restaurant_css_selector))
            )
            
            print("Restoranlar yüklendi.")
            elementler = self.driver.find_elements(By.CSS_SELECTOR, restaurant_css_selector)
            print(f"Toplam {len(elementler)} adet restoran bulundu.")

            cekilen_veriler=[]
            for element in elementler:
                cekilen_veri=element.text.strip()#strip ile baştaki sondaki boşlukları atıyoruz
                cekilen_veriler.append(cekilen_veri)
                print("--- BULUNAN RESTORAN ---")
                print(cekilen_veri)
                print("--------------------------")

            self.dosyaya_yaz(cekilen_veriler)
              

        except Exception as e:
            print(f"İşlem sırasında hata oluştu: {e}")
        
        finally:
            print("Tarayıcı kapatılıyor.")
            self.driver.quit()
    
    def dosyaya_yaz(self, veriler,dosya_adi="trendyol_pizza_sonuclari.txt"):
        if not veriler:
            print("kaydedilen veri yok")
            return
        try:
            with open(dosya_adi,"w",encoding="utf-8") as f:
                for veri in veriler:
                    f.write(veri+"\n\n")
            print(f"Veriler {dosya_adi} dosyasına kaydedildi.")
        except Exception as e:
            print(f"Dosyaya yazma sırasında hata oluştu: {e}")
        finally:
            print("Dosya yazma işlemi tamamlandı.")


if __name__ == "__main__":
    trendyol_pizza = TrendyolPizza()
    trendyol_pizza.arama_yap_ve_veri_cek()