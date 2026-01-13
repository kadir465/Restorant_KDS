import pandas as pd
import json

df=pd.read_csv(r"C:\Software_project\Restorant_KDS\Comment_Scraping\restorant_pizza_doner_yorumları_cleared.csv")

with open("restorant_comments.jsonl","w",encoding="utf-8") as f:
    for _, index in df.iterrows():
        record={
            "restaurant_name": index["Restoran_Adi"],
            "restaurant_link": index["Restoran_Link"],
            "comment": index["new_Yorum"]
        }
        f.write(json.dumps(record,ensure_ascii=False)+"\n")

print("json dosyası oluşturuldu")