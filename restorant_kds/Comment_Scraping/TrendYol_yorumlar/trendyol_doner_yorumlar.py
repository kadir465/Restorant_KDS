import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

class TrendYolDonerYorumlar:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.url = "https://tgoyemek.com/arama?searchQuery=d%C3%B6ner"

    def arama_yap_ve_veri_cek(self):
        print(f"Arama sayfası açılıyor: {self.url}")
        self.driver.get(self.url)

        try:
            selector = "a[href^='/restoranlar/']"
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            restaurant_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"Toplam {len(restaurant_elements)} adet link bulundu.")
        except Exception as e:
            print(f"Hata: Restoran linkleri bulunamadı. {e}")
            self.driver.quit()
            return

        urls_to_visit = []
        for element in restaurant_elements:
            relative_link = element.get_attribute("href")
            if relative_link and relative_link not in urls_to_visit:
                urls_to_visit.append(relative_link)

        print("\n--- Toplanan URL'ler ---")
        for url in urls_to_visit:
            print(url)

        yorumlar = []

        for url in urls_to_visit:
            try:
                print(f"\nRestoran sayfası açılıyor: {url}")
                self.driver.get(url)

                yorum_buton_xpath = "/html/body/div[1]/main/div[3]/div/div[1]/div/div[2]/button[2]"
                self.wait.until(EC.element_to_be_clickable((By.XPATH, yorum_buton_xpath)))
                yorum_button = self.driver.find_element(By.XPATH, yorum_buton_xpath)
                yorum_button.click()

                self.wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".body-2-regular.text-neutral-dark.mt-2")
                ))
                yorum_elements = self.driver.find_elements(By.CSS_SELECTOR, ".body-2-regular.text-neutral-dark.mt-2")

                print(f"Toplam {len(yorum_elements)} adet yorum bulundu.")

                for yorum_elemt in yorum_elements:
                    yorum_text = yorum_elemt.text.strip()
                    yorumlar.append(yorum_text)
                    print("----- Yorum -----")
                    print(yorum_text)

            except Exception as e:
                print(f"Hata oluştu: {e}")
                continue

        print("\nTarayıcı kapatılıyor.")
        self.driver.quit()

        # Yorumları kaydet
        df = pd.DataFrame({"Yorumlar": yorumlar})
        df.to_csv("trendyol_doner_yorumlar.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    doner_yorumlar = TrendYolDonerYorumlar()
    doner_yorumlar.arama_yap_ve_veri_cek()