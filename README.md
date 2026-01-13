# Restorant AI - Restoran Karar Destek Sistemi

Bu proje, popüler yemek sipariş platformlarından (Trendyol Yemek, Yemeksepeti) elde edilen müşteri yorumlarını toplayan, işleyen ve doğal dil işleme (NLP) yöntemleriyle analiz eden kapsamlı bir yapay zeka uygulamasıdır.

Proje, dağınık haldeki binlerce müşteri yorumunu analiz ederek restoranlar için lezzet, hız ve servis kriterlerine göre özet niteliğinde, okunabilir raporlar ve değerlendirmeler üretir.

**Canlı Demo:** [Hugging Face Space - Restorant AI](https://huggingface.co/spaces/emirdfg/Restorant_Ai)

## Model Dosyaları ve Veri Setleri
GitHub dosya boyutu sınırları nedeniyle, eğitilmiş büyük model dosyaları ve kapsamlı veri setleri bu depoya yüklenememiştir. Projeyi yerelinizde eksiksiz çalıştırmak için gerekli olan model ve veri dosyalarına aşağıdaki Google Drive bağlantısından erişebilirsiniz:

📂 **[Proje Dosyaları ve Modeller (Google Drive)](https://drive.google.com/drive/folders/1Y6mVlSS3_nrOZhbY5aUT-LlvgO-_gXsQ?hl=tr)**

## Proje Hakkında

Restorant AI, veri madenciliği ve Büyük Dil Modelleri (LLM) teknolojilerini birleştirir. Selenium kütüphanesi kullanılarak web kazıma (scraping) yöntemiyle toplanan veriler, temizlenip yapılandırıldıktan sonra özel olarak eğitilmiş veya ince ayar (fine-tuning) yapılmış yapay zeka modellerine beslenir. Sonuç olarak, potansiyel müşterilere veya restoran sahiplerine işletmenin genel performansı hakkında objektif bir özet sunulur.

## Temel Özellikler

* **Veri Kazıma (Web Scraping):** Trendyol Yemek ve Yemeksepeti üzerindeki restoranların bilgilerini ve kullanıcı yorumlarını otomatik olarak çeken Selenium botları.
* **Veri İşleme ve Temizleme:** Çekilen ham verilerin temizlenmesi, anonimleştirilmesi ve model eğitimi için uygun formata (JSONL/CSV) getirilmesi.
* **Yapay Zeka Modelleri:**
    * **GPT-2 Eğitimi:** Toplanan verilerle sıfırdan veya fine-tuning yöntemiyle eğitilen dil modelleri.
    * **Mistral-7B Entegrasyonu:** Daha gelişmiş analizler için PEFT ve LoRA teknikleri kullanılarak özelleştirilmiş Mistral model desteği.
* **Otomatik Analiz:** Müşteri yorumlarına dayanarak restoranın güçlü ve zayıf yönlerini belirleyen metin tabanlı analiz üretimi.

## Kullanılan Teknolojiler

* **Programlama Dili:** Python
* **Veri Çekme:** Selenium, Chromedriver
* **Veri Analizi:** Pandas, NumPy
* **Yapay Zeka ve NLP:** Hugging Face Transformers, PyTorch, PEFT, BitsAndBytes, LLM-NLP
* **Veri Görselleştirme:** Matplotlib (Analiz notebooklarında)
