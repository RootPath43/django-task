# Django projesi için temel imaj olarak Python kullanıyoruz
FROM python:3.8-slim

# Çalışma dizinini belirliyoruz
WORKDIR /app

# Gereken paketleri yükleyelim
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyalayalım
COPY . .

# Django projesini çalıştırma komutu
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
