# Python resmi imajını kullanma
FROM python:3.9-slim

# Çalışma dizinini ayarlama
WORKDIR /app

# Gerekli paketleri yüklemek için gereksinimler dosyasını kopyalama
COPY requirements.txt .

# Gerekli paketleri yüklemek için pip kullanma
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyalamaaa
COPY . .

# Expose

EXPOSE 8000

# Gunicorn sunucusunu çalıştırma
CMD ["gunicorn", "appinstance.wsgi:application", "--bind", "0.0.0.0:8000"]
