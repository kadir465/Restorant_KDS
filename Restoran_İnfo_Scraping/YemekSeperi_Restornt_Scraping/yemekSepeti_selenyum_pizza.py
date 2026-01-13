import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

class YemekSepetiBot: 
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15) 
        self.input = "Pizza"
        self.url = "https://www.yemeksepeti.com/restaurants/new?lng=29.01074&lat=41.07683&vertical=restaurants"

    def arama_yap_ve_veri_cek(self):
        try:
            print("Siteye gidiliyor...")
            self.driver.get(self.url)
            self.driver.maximize_window()

            search_input = self.wait.until(#?"------->>arama kutusu aktiv olana kadar bekler"
                EC.element_to_be_clickable((By.ID, "search-input-side-filters"))
            )

            print(f"'{self.input}' için arama yapılıyor...")
            search_input.send_keys(self.input)
            search_input.send_keys(Keys.ENTER)

            restaurant_selector_css = ".box-flex.vendor-tile-new-info.fd-column"
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, restaurant_selector_css))
            )
            
            print("Sonuçlar yüklendi. Veriler çekiliyor...")
            elementler = self.driver.find_elements(By.CSS_SELECTOR, restaurant_selector_css)

            print(f"Toplam {len(elementler)} adet restoran sonucu bulundu.")
            cekilen_veriler = [] 
            for element in elementler:
                cekilen_veri = element.text 
                if cekilen_veri: 
                    cekilen_veriler.append(cekilen_veri)
                    print("--- BULUNAN RESTORAN ---")
                    print(cekilen_veri)
                    print("--------------------------")
            
            self.dosyaya_yaz(cekilen_veriler)

        except Exception as e:
            print(f"İşlem sırasında bir hata oluştu: {e}")
        
        finally:
            self.driver.quit()

    def dosyaya_yaz(self, veriler, dosya_adi="yemeksepeti_sonuclar.txt"):
        """
        Verilen listedeki verileri bir dosyaya yazar.
        """
        if not veriler:
            print("Dosyaya yazılacak veri bulunamadı.")
            return

        print(f"Veriler '{dosya_adi}' dosyasına yazılıyor...")
        with open(dosya_adi, "w", encoding="utf-8") as f:
            for veri in veriler:
                f.write(veri + "\n")
                f.write("========================================\n")
        
        print("Dosyaya yazma tamamlandı.")



if __name__ == "__main__":
    bot = YemekSepetiBot()
    bot.arama_yap_ve_veri_cek()