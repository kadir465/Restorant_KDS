import json
import re
import random


input_path = r"C:\Software_project\Restorant_KDS\LLM_Aİ_Model\llm_data\training_dataset_grouped.jsonl"
train_path = r"C:\Software_project\Restorant_KDS\LLM_Aİ_Model\llm_data\train.jsonl"
val_path = r"C:\Software_project\Restorant_KDS\LLM_Aİ_Model\llm_data\validation.jsonl"

def clean_text(text):
    text = re.sub(r'\\', '', text)
    text = text.replace("  ", " ")
    return text.strip()

data = []

print("veri temizleme")
with open(input_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            try:
                item = json.loads(line)
                item['input'] = clean_text(item['input'])
                item['output'] = clean_text(item['output'])
                data.append(item)
            except json.JSONDecodeError:
                continue

print(f" {len(data)} adet temiz veri hazırlandı.")


random.shuffle(data)

split_index = int(len(data) * 0.9)
train_data = data[:split_index]
val_data = data[split_index:]

with open(train_path, "w", encoding="utf-8") as f:
    for item in train_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

with open(val_path, "w", encoding="utf-8") as f:
    for item in val_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Eğitim Seti: {len(train_data)} satır -> {train_path}")
print(f"Test Seti: {len(val_data)} satır -> {val_path}")