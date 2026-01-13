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
        restornt_bilgiler=[]

        try:
            selector = ".text-neutral-darker.title-3-semibold.truncate.w-full"
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            restaurant_name_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"Toplam {len(restaurant_name_elements)} adet restornt bulundu.")

            restoran_isimler=[]
            for name_element in restaurant_name_elements:
                restoran_isimler.append(name_element.text.strip())

        except Exception as e:
            print(f"restont bulunamadı. {e}")
            self.driver.quit()
            
        print("\n restorntlar\n")
        for i,name in enumerate (restoran_isimler):
            print(f"{i+1}. {name}")
        
        print("\n restornt linkleri\n")
        urls_to_visit = []
        restornt_url_selector='.group.flex.flex-col'
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, restornt_url_selector)))
        restaurant_url_elements = self.driver.find_elements(By.CSS_SELECTOR, restornt_url_selector)
        for element in restaurant_url_elements:
            relative_link = element.get_attribute("href")
            if relative_link and relative_link not in urls_to_visit:
                urls_to_visit.append(relative_link)

        print("\n--- Toplanan URL'ler ---")
        for i,url in enumerate(urls_to_visit):
            print(f"{i+1}. {url}")

        for i,(isim,link) in enumerate(zip(restoran_isimler,urls_to_visit)):
            restornt_bilgiler.append({
                'restoran_adi': isim,
                'link': link,
                'yorumlar': []
            })

        print("\n yorumlar alınacak\n")
        tum_veriler = []

        for restoran in restornt_bilgiler:
            try:
                print(f"\n{restoran['restoran_adi']} yorum alınıyor")
                print(f"sayfa açılıyor: {restoran["link"]}")
                self.driver.get(restoran['link'])

                try:
                    yorum_buton_xpath = "/html/body/div[1]/main/div[3]/div/div[1]/div/div[2]/button[2]"
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, yorum_buton_xpath)))
                    yorum_button = self.driver.find_element(By.XPATH, yorum_buton_xpath)
                    if yorum_button:
                        yorum_button.click()

                        self.wait.until(EC.presence_of_all_elements_located(
                             (By.CSS_SELECTOR, ".body-2-regular.text-neutral-dark.mt-2")
                            ))
                        yorum_elements = self.driver.find_elements(By.CSS_SELECTOR, ".body-2-regular.text-neutral-dark.mt-2")
                        print(f"Toplam {len(yorum_elements)} adet yorum bulundu.")


                        for yorum_elemt in yorum_elements:
                            yorum_text = yorum_elemt.text.strip()
                            if yorum_text:
                                restoran['yorumlar'].append(yorum_text)

                                tum_veriler.append({
                                    'Restoran_Adi': restoran['restoran_adi'],
                                    'Yorum': yorum_text,
                                    'Restoran_Link': restoran['link']
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
                        'Restoran_Adi': restoran['restoran_adi'],
                        'Yorum': 'Yorum bulunamadı',
                        'Restoran_Link': restoran['link']
                    })
                    continue
            except Exception as e:
                print(f"hata oluştu ({restoran['restoran_adi']}): {e}")
                tum_veriler.append({
                    'Restoran_Adi': restoran['restoran_adi'],
                    'Yorum': f'Hata: {str(e)}',
                    'Restoran_Link': restoran['link']
                })
                continue
        self.driver.quit()

        if tum_veriler:
            df = pd.DataFrame(tum_veriler)
            df.to_csv("trendyol_doner_yorumlar.csv", index=False, encoding="utf-8-sig")

            print(f"Toplam {len(tum_veriler)} kayıt DataFrame'e kaydedildi")
            print(f"Toplam {len(restornt_bilgiler)} restoran işlendi")
            return df
        else:
            print("Hiç veri bulunamadı!")
            return pd.DataFrame()

          
if __name__ == "__main__":
    doner_yorumlar = TrendYolDonerYorumlar()
    doner_yorumlar.arama_yap_ve_veri_cek()
