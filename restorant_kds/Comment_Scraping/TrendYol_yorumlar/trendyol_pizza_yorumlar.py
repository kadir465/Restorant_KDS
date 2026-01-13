import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

class TrendYolPizzaYorumlar:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.url = "https://tgoyemek.com/arama?searchQuery=pizza"

    def arama_yap_ve_veri_cek(self):
        print(f"Sayfa açılıyor: {self.url}")
        self.driver.get(self.url)
        restorant_bilgileri=[]

        try:
            selector =".text-neutral-darker.title-3-semibold.truncate.w-full"
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            restaurant_name_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"Toplam {len(restaurant_name_elements)} restoran bulundu.")

            restoran_isimleri=[]
            for name_element in restaurant_name_elements:
                restoran_isimleri.append(name_element.text.strip())

        except Exception as e:
            print(f"restornt bulunmadı: {e}")
            self.driver.quit()
            
        print("\n restornatlar\n")
        urls_to_visit = []
        restorant_url_selector='.group.flex.flex-col'
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,restorant_url_selector)))
        restorant_url_elements=self.driver.find_elements(By.CSS_SELECTOR,restorant_url_selector)

        for element in restorant_url_elements:
            link = element.get_attribute("href")
            if link and link not in urls_to_visit:
                urls_to_visit.append(link)

        print("\n--- Toplam URL ---\n")
        for i,url in enumerate(urls_to_visit):
            print(f"{i+1}. {url}")

        for i,(isim,link) in enumerate(zip(restoran_isimleri,urls_to_visit)):
            restorant_bilgileri.append({
                'restoran_adi': isim,
                'link': link,
                'yorumlar': []
            })

        print("\n yorumlar alınacak\n")
        tum_veriler = []

        for restorn in restorant_bilgileri:
            try:
                print(f"\n{restorn['restoran_adi']} yorum alınıyor")
                print(f"sayfa açılıyor: {restorn["link"]}")
                self.driver.get(restorn['link'])

                try:
                    yorum_button_xpath = "/html/body/div[1]/main/div[3]/div/div[1]/div/div[2]/button[2]"
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, yorum_button_xpath)))
                    yorum_button = self.driver.find_element(By.XPATH, yorum_button_xpath)
                    if yorum_button:
                        yorum_button.click()


                        self.wait.until(EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, ".body-2-regular.text-neutral-dark.mt-2")
                        ))
                        yorum_elements = self.driver.find_elements(By.CSS_SELECTOR, ".body-2-regular.text-neutral-dark.mt-2")
                        print(f"Toplam {len(yorum_elements)} tane yorum bulundu.")


                        for yorum_element in yorum_elements:
                            yorum_text = yorum_element.text.strip()
                            if yorum_text:
                                restorn["yorumlar"].append(yorum_text)
                                tum_veriler.append({
                                    'Restoran_Adi': restorn['restoran_adi'],
                                    'Yorum': yorum_text,
                                    'Restoran_Link': restorn['link']
                                })
                                print(f"yorum: {yorum_text}")
                        try:
                            kapat_button = self.driver.find_element(By.CSS_SELECTOR, "[aria-label*='kapat'], .close, button[class*='close']")
                            kapat_button.click()
                            time.sleep(1)
                        except:
                            pass
                except Exception as e:
                    print(f"yorum yok {e}")
                    tum_veriler.append({
                        'Restoran_Adi': restorn['restoran_adi'],
                        'Yorum': 'Yorum bulunamadı',
                        'Restoran_Link': restorn['link']
                    })
                    continue
            except Exception as e:
                print(f"hata oluştu ({restorn['restoran_adi']}): {e}")
                tum_veriler.append({
                    'Restoran_Adi': restorn['restoran_adi'],
                    'Yorum': f'Hata: {str(e)}',
                    'Restoran_Link': restorn['link']
                })
                continue
        self.driver.quit()
        
        if tum_veriler:
            df = pd.DataFrame(tum_veriler)
            df.to_csv("trendyol_pizza_yorumlar.csv", index=False, encoding="utf-8-sig")

            print(f"Toplam {len(tum_veriler)} kayıt DataFrame'e kaydedildi")
            print(f"Toplam {len(restorant_bilgileri)} restoran işlendi")
            return df
        else:
            print("Hiç veri bulunamadı!")
            return pd.DataFrame()


    
if __name__ == "__main__":
    pizza_yorumlar = TrendYolPizzaYorumlar()
    pizza_yorumlar.arama_yap_ve_veri_cek()
