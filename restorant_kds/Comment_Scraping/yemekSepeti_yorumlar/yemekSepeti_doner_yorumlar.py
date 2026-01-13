import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()


class YemekSepetiDonerYorumları:
    def __init__(self):
        options=webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver=webdriver.Chrome(options=options)
        self.wait=WebDriverWait(self.driver,20)
        self.url="https://www.yemeksepeti.com/restaurants/new?lng=29.01074&lat=41.07683&vertical=restaurants&query=d%C3%B6ner"

    def arama_yap_ve_veri_cek(self):
        print(f"sayfa açılıyor {self.url}")
        self.driver.get(self.url)
        
        restorant_bilgileri=[]
        try:
            #restorantlar
            selector="vendor-name" 
            self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,selector)))
            restorant_name_elements=self.driver.find_elements(By.CLASS_NAME,selector)
            print(f"toplam{len(restorant_name_elements)} restornt bulundu")

            restoran_isimler=[]
            for name_element in restorant_name_elements:
                restoran_isimler.append(name_element.text.strip())

        except Exception as e:
            print(f"restornt bulurken hata var {e}")
            self.driver.quit()
        
        print("\n restorantlar\n")
        
        for i,name in enumerate(restoran_isimler):
            print(f"{i+1}. {name}")
        
        print("\nrestornt linkleri\n")
        urls_to_adres=[]
        try:
            selector="a[data-testid^='vendor-tile-new-link-']"
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,selector)))
            restornt_elements=self.driver.find_elements(By.CSS_SELECTOR,selector)
            print(f"toplam {len(restornt_elements)} restornt linki var")
        except Exception as e:
            print(f"restorant adresi alırken hata aldık {e}")
            self.driver.quit()
            return
        
        for element in restornt_elements:
            link =element.get_attribute("href")
            if link and link not in urls_to_adres:
                urls_to_adres.append(link)
        for i,url in enumerate(urls_to_adres):
            print(f"{i+1}. {url}")
        
        for i,(isim,link) in enumerate(zip(restoran_isimler,urls_to_adres)):
            restorant_bilgileri.append({
                'restoran_adi': isim,
                'link': link,
                'yorumlar': []
            })

        print("\nyorumlar alınacak \n")
        tum_veriler=[]
        
        for restoran in restorant_bilgileri:
            try:
                print(f"\n{restoran['restoran_adi']} yorum alınıyor")
                print(f"sayfa açılıyor: {restoran["link"]}")
                self.driver.get(restoran['link'])

                try:
                    yorum_button_xpath = "//button[.//span[contains(text(), 'Yorumlar')]]"
                    self.wait.until(EC.element_to_be_clickable((By.XPATH,yorum_button_xpath)))
                    yorum_button=self.driver.find_element(By.XPATH,yorum_button_xpath)

                    if yorum_button:
                        yorum_button.click()

                        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".info-reviews-modal-description")))
                        yorum_elements=self.driver.find_elements(By.CSS_SELECTOR,".info-reviews-modal-description")
                        print(f"tolam {len(yorum_elements)} yoorum bulundu")

                        for yorum_eleman in yorum_elements:
                            yorum_text=yorum_eleman.text.strip()
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
            df.to_csv("yemeksepeti_doner_yorumlar.csv", index=False, encoding="utf-8-sig")

            print(f"Toplam {len(tum_veriler)} kayıt DataFrame'e kaydedildi")
            print(f"Toplam {len(restorant_bilgileri)} restoran işlendi")
            return df
        else:
            print("Hiç veri bulunamadı!")
            return pd.DataFrame()

if __name__=="__main__":
    pizza_yorum = YemekSepetiDonerYorumları()
    df = pizza_yorum.arama_yap_ve_veri_cek()

