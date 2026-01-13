import torch
from transformers import GPT2Config, GPT2LMHeadModel, GPT2TokenizerFast, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from datasets import load_dataset
import os

#  GPT-2 mimarisi
MODEL_CONFIG = GPT2Config(
    vocab_size=50257, # GPT-2 standart kelime hazinesi boyutu
    n_positions=1024, # Modelin hafızasında tutabileceği kelime sayısı
    n_ctx=1024,
    n_embd=768,       # Katman genişliği
    n_layer=6,        # Katman sayısı (Standart GPT-2'de 12'dir, biz 6 yapıyoruz ki hızlı öğrensin)
    n_head=12
)

TRAIN_FILE =r"C:\Software_project\Restorant_KDS\LLM_Aİ_Model\llm_data\train.jsonl"
VAL_FILE = r"C:\Software_project\Restorant_KDS\LLM_Aİ_Model\llm_data\validation.jsonl"
OUTPUT_DIR = "./restoran_modeli_sonuc"

def main():

    print("Tokenizer yükleniyor...")
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token 

    
    data_files = {"train": TRAIN_FILE, "validation": VAL_FILE}
    dataset = load_dataset("json", data_files=data_files)


    def preprocess_function(examples):
       
        
        inputs = examples["input"]
        outputs = examples["output"]
        instructions = examples["instruction"]
        
        texts = []
        for inst, inp, out in zip(instructions, inputs, outputs):
         
            text = f"{inst}\n\n{inp}\n\n--- ANALİZ ---\n{out}{tokenizer.eos_token}"
            texts.append(text)
        
        # Metinleri sayılara çevir (Tokenization)
        tokenized = tokenizer(texts, padding="max_length", truncation=True, max_length=512)
        return tokenized

    print("Veriler işleniyor (Tokenization)")
    tokenized_datasets = dataset.map(preprocess_function, batched=True, remove_columns=dataset["train"].column_names)

   
    print("Model sıfırdan oluşturuluyor")
    model = GPT2LMHeadModel(MODEL_CONFIG)
    
    
    model_size = sum(p.numel() for p in model.parameters()) / 1_000_000
    print(f"Model Boyutu: {model_size:.2f} Milyon Parametre")

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        overwrite_output_dir=True,
        num_train_epochs=10,             # Veri setini kaç tur döneceği (Az veriyle 10-15 iyidir)
        per_device_train_batch_size=4,   # GPU belleğinize göre artırıp azaltabilirsiniz (4 veya 8)
        per_device_eval_batch_size=4,
        eval_strategy="steps",           # DEĞİŞİKLİK BURADA: evaluation_strategy -> eval_strategy
        eval_steps=100,                  # Her 100 adımda bir test et
        save_steps=500,                  # Her 500 adımda bir kaydet
        logging_steps=50,                # Her 50 adımda ekrana bilgi yaz
        learning_rate=5e-4,              # Öğrenme hızı
        weight_decay=0.01,
        fp16=True,                       # GPU hızlandırması (Mixed Precision) - Sadece GPU varsa True yapın!
        save_total_limit=2,              # Sadece son 2 modeli sakla (yer kaplamasın)
    )

   
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        data_collator=data_collator,
    )

    print("model eğitimi yapılıyor")
    trainer.train()

   
    print("model eğitimi bitti")
    trainer.save_model(f"{OUTPUT_DIR}/final_model")
    tokenizer.save_pretrained(f"{OUTPUT_DIR}/final_model")
    print(f"Modeliniz '{OUTPUT_DIR}/final_model' klasörüne kaydedildi.")

if __name__ == "__main__":
    main()