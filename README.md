# Dokumentasi API: Extract Colors

## Deskripsi
API ini digunakan untuk mengekstrak warna dominan dari gambar yang diberikan melalui URL. API ini menggunakan k-means clustering untuk mengekstrak warna dan mengembalikannya dalam format HEX.

## Kredit
Algoritma k-means untuk ekstraksi palet diadaptasi dari kode oleh Mas Aria Ghora di artikelnya yang dapat ditemukan [di sini](https://ghora.net/notes/20230818-kmeans-ekstraksi-palet/).

## Cara Penggunaan

### Instalasi Dependensi
Sebelum menjalankan API, pastikan untuk menginstal semua pustaka yang dibutuhkan dengan menjalankan:

```bash
pip install -r requirements.txt
```

### Menjalankan API
Untuk menjalankan API, jalankan perintah berikut:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Endpoint

#### POST `/extract_colors/`

##### Deskripsi
Menerima URL gambar dan mengembalikan 6 warna dominan dalam format HEX.

##### Request Body
Model Pydantic `ImageUrl` berisi satu field:

- `image_url`: URL gambar yang ingin diolah (Harus dimulai dengan "http://" atau "https://").

Contoh:
```json
{
    "image_url": "https://example.com/image.jpg"
}
```

##### Responses
###### HTTP 200
Array dari warna dominan dalam format HEX.

Contoh:
```json
{
    "warna_dominan": ["#FFFFFF", "#000000", "#FF5733", "#33FF57", "#4B0082", "#800080"]
}
```

###### HTTP 400
Invalid URL atau Unsupported file type.

Contoh:
```json
{
    "detail": "Invalid URL"
}
```

###### HTTP 500
Server error atau kegagalan lainnya.

Contoh:
```json
{
    "detail": "Internal Server Error"
}
```

### Contoh Request Menggunakan `curl`
```bash
curl --request POST \
  --url http://localhost:8000/extract_colors/ \
  --header 'Content-Type: application/json' \
  --data '{
    "image_url": "https://example.com/image.jpg"
}'
```
