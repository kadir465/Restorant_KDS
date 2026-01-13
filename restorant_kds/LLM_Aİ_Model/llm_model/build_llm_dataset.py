import json
from collections import defaultdict

input_path = r"C:\Software_project\Restorant_KDS\Comment_Scraping\restorant_comments.jsonl"
output_path = r"C:\Software_project\Restorant_KDS\LLM_Aİ_Model\llm_data\training_dataset_grouped.jsonl"

restaurant_reviews = defaultdict(list)

print("Dosya okunuyor ve gruplanıyor...")

with open(input_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            item = json.loads(line)
            rest_name = item.get("restaurant_name", "Bilinmeyen Restoran")
            comment = item.get("comment", "")
            
            if comment:
                restaurant_reviews[rest_name].append(comment)

print(f"Toplam {len(restaurant_reviews)} farklı restoran için yorumlar gruplandı.")


with open(output_path, "w", encoding="utf-8") as out:
    for rest_name, comments in restaurant_reviews.items():
        
    
        combined_comments = ""
        for i, c in enumerate(comments, 1):
            combined_comments += f"- {c}\n"
        
        instruction = (
            "Aşağıda bir restoran hakkında yapılmış müşteri yorumları listelenmiştir. "
            "Bu yorumları analiz et ve restoranın genel performansı (lezzet, hız, servis) hakkında "
            "objektif, özetleyici bir değerlendirme yazısı oluştur."
        )

        data = {
            "instruction": instruction,
            "input": f"Restoran: {rest_name}\n\nMüşteri Yorumları:\n{combined_comments}",
            "output": ""
        }

        out.write(json.dumps(data, ensure_ascii=False) + "\n")

print(f"Gruplanmış dataset  oluşturuldu: {output_path}")
