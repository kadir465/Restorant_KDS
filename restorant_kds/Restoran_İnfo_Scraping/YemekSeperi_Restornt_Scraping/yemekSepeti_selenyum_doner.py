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
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)
        self.input = "Döner"
        self.url = "https://www.yemeksepeti.com/restaurants/new?lng=29.01074&lat=41.07683&vertical=restaurants"

    def arama_yap_ve_veri_cek(self):
        try:
            print("Siteye giriliyor...")
            self.driver.get(self.url)
            self.driver.maximize_window()

            search_input = self.wait.until(
                EC.element_to_be_clickable((By.ID, "search-input-side-filters"))
            )
            print(f"{self.input} için arama yapılıyor...")
            search_input.send_keys(self.input)
            search_input.send_keys(Keys.ENTER)

            # Sayfanın dinamik olarak yüklenmesini bekle
            time.sleep(5)

            restaurant_selector_css = ".vendor-tile-new-info"
            self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, restaurant_selector_css))
            )

            elementler = self.driver.find_elements(By.CSS_SELECTOR, restaurant_selector_css)
            print(f"Toplam {len(elementler)} adet restoran bulundu.")

            cekilen_veriler = []
            for element in elementler:
                cekilen_veri = element.text.strip()
                cekilen_veriler.append(cekilen_veri)
                print("--- BULUNAN RESTORAN ---")
                print(cekilen_veri)
                print("--------------------------")

            self.dosyaya_yaz(cekilen_veriler)

        except Exception as e:
            print(f"İşlem sırasında hata oluştu: {e}")
        finally:
            self.driver.quit()

    def dosyaya_yaz(self, veriler, dosya_adi="yemeksepeti_doner_sonuclar.txt"):
        if not veriler:
            print("Kaydedilecek veri yok.")
            return
        print(f"Veriler '{dosya_adi}' dosyasına kaydediliyor...")
        try:
            with open(dosya_adi, "w", encoding="utf-8") as file:
                for veri in veriler:
                    file.write(veri + "\n\n")
                    file.write("=================================================\n")
            print("Veriler başarıyla kaydedildi.")
        except Exception as e:
            print(f"Dosyaya yazılırken hata oluştu: {e}")


if __name__ == "__main__":
    bot = YemekSepetiDoner()
    bot.arama_yap_ve_veri_cek()
