import os
from huggingface_hub import HfApi, login

# --- AYARLAR ---
# Write token'ını buraya yapıştır
TOKEN = "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"


REPO_ID = "emirdfg/restornt_model"
LOCAL_FILE = r"C:\Software_project\Restorant_KDS\restoran_modeli_sonuc\final_model\model.safetensors" # Eksik olan dosya bu!

print(f"Eksik dosya ({LOCAL_FILE}) kontrol ediliyor...")

if not os.path.exists(LOCAL_FILE):
    print("HATA: Bilgisayarında 'final_model' klasörünün içinde 'model.safetensors' yok!")
    print("Lütfen dosyanın orada olduğundan emin ol.")
    exit()

api = HfApi(token=TOKEN)

print(f"🚀 {LOCAL_FILE} dosyası depoya yükleniyor... Bu biraz sürebilir.")

try:
    api.upload_file(
        path_or_fileobj=LOCAL_FILE,
        path_in_repo="gpt2_files/model.safetensors", # Tam olarak buraya gitmeli
        repo_id=REPO_ID,
        repo_type="model"
    )
    print("✅✅✅ TAMİR BAŞARILI! Dosya yüklendi.")
    print("Şimdi Space sayfasına gidip 'Restart Space' butonuna basabilirsin.")
except Exception as e:
    print(f"❌ Hata: {e}")