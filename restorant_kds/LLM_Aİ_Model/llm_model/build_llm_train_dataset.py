import json

input_path = r"C:\Software_project\Restorant_KDS\Comment_Scraping\restorant_comments.jsonl"

output_path = r"C:\Software_project\Restorant_KDS\LLM_Aİ_Model\llm_data\train.jsonl"

comments = []
with open(input_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            comments.append(json.loads(line))

print("Ham yorum sayısı:", len(comments))


with open(output_path, "w", encoding="utf-8") as out:
    for item in comments:
        restoran = item["restaurant_name"]
        yorum = item["comment"]

        data = {
            "instruction": "Aşağıdaki müşteri yorumuna göre restoran hakkında kısa bir öneri metni üret.",
            "input": f"Restoran: {restoran}\nYorum: {yorum}",
            "output": ""  
        }

        out.write(json.dumps(data, ensure_ascii=False) + "\n")

print("Training dataset oluşturuldu:", output_path)
