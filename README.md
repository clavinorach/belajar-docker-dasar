# Panduan Belajar Docker dengan Python dan PostgreSQL

## Daftar Isi
- [Pendahuluan Docker](#pendahuluan-docker)
- [Tujuan Project](#tujuan-project)
- [Struktur Direktori Project](#struktur-direktori-project)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Penjelasan Detail Setiap Komponen](#penjelasan-detail-setiap-komponen)
- [Cara Menjalankan Project](#cara-menjalankan-project)
- [Inisialisasi Schema Database](#inisialisasi-schema-database)
- [Cara Melakukan Query ke PostgreSQL](#cara-melakukan-query-ke-postgresql)
- [Test API Endpoint](#test-api-endpoint)
- [Troubleshooting Umum](#troubleshooting-umum)
- [Penutup](#penutup)

---

## Pendahuluan Docker

Docker adalah platform yang memungkinkan developer untuk mengemas aplikasi beserta seluruh dependencies-nya ke dalam unit standar yang disebut container. Container berjalan secara terisolasi dari sistem host dan container lainnya, namun tetap berbagi kernel sistem operasi yang sama.

### Konsep Dasar Docker

**Image**  
Image adalah template read-only yang berisi instruksi untuk membuat container. Image dibuat dari Dockerfile dan dapat disimpan di registry seperti Docker Hub. Image bersifat immutable dan dapat digunakan berkali-kali untuk membuat container.

**Container**  
Container adalah instance yang dapat dijalankan dari sebuah image. Container bersifat ephemeral (sementara) dan isolated, memiliki filesystem, network, dan process space tersendiri. Ketika container dihapus, semua perubahan yang tidak disimpan di volume akan hilang.

**Volume**  
Volume adalah mekanisme untuk menyimpan data secara persisten di luar container. Data yang disimpan di volume akan tetap ada meskipun container dihapus atau dibuat ulang. Volume sangat penting untuk database dan aplikasi yang memerlukan persistensi data.

**Networking**  
Docker menyediakan network driver yang memungkinkan container untuk berkomunikasi satu sama lain atau dengan dunia luar. Secara default, docker-compose membuat network internal sehingga service dalam satu file compose dapat saling berkomunikasi menggunakan nama service sebagai hostname.

**Isolation**  
Container berjalan dalam lingkungan terisolasi dari sistem host. Setiap container memiliki filesystem, proses, dan network interface tersendiri. Isolasi ini memastikan bahwa aplikasi dalam container tidak akan mengganggu sistem host atau container lainnya.

**Reproducibility**  
Docker memastikan bahwa aplikasi berjalan dengan cara yang sama di berbagai environment (development, staging, production). Dengan mendefinisikan environment dalam Dockerfile dan docker-compose.yml, developer dapat mereproduksi environment yang sama persis di mesin mana pun.

### Manfaat Docker dalam Pengembangan Aplikasi Python

1. **Konsistensi Environment**: Menghilangkan masalah "works on my machine" dengan memastikan semua developer menggunakan versi Python, library, dan dependencies yang sama.

2. **Isolasi Dependencies**: Setiap project dapat menggunakan versi library yang berbeda tanpa konflik dengan project lain atau system-wide packages.

3. **Kemudahan Setup**: Developer baru dapat menjalankan project hanya dengan `docker-compose up` tanpa perlu instalasi manual Python, PostgreSQL, atau dependencies lainnya.

4. **Portabilitas**: Aplikasi dapat dipindahkan ke server production dengan konfigurasi yang sama, mengurangi risiko error saat deployment.

5. **Skalabilitas**: Container dapat dengan mudah di-scale up atau down sesuai kebutuhan load aplikasi.

---

## Tujuan Project

Project ini dirancang sebagai pembelajaran dasar untuk memahami bagaimana Docker bekerja dalam konteks aplikasi Python dengan database PostgreSQL. Setelah menyelesaikan tutorial ini, Anda akan mampu:

1. **Menjalankan aplikasi Python dalam Docker**  
   Memahami cara membuat Dockerfile untuk aplikasi Python Flask dan menjalankannya sebagai container.

2. **Menjalankan database PostgreSQL dalam Docker**  
   Menggunakan official image PostgreSQL dari Docker Hub dan mengkonfigurasinya melalui environment variables.

3. **Menghubungkan keduanya menggunakan docker-compose**  
   Menggunakan docker-compose untuk mengorkestrasi multiple containers (web service dan database service) sehingga dapat berkomunikasi dalam satu network.

4. **Menginisialisasi schema database menggunakan file SQL**  
   Memanfaatkan fitur PostgreSQL Docker image untuk menjalankan script SQL secara otomatis saat container pertama kali dibuat.

5. **Melakukan query sederhana (INSERT, SELECT)**  
   Membuat REST API sederhana dengan Flask untuk melakukan operasi CRUD (Create, Read) pada database PostgreSQL.

Project ini cocok untuk pemula yang ingin memahami dasar-dasar containerization dan integrasi aplikasi Python dengan database relational dalam lingkungan Docker.

---

## Struktur Direktori Project

```
belajar-docker/
├── docker-compose.yml
├── Dockerfile
├── README.md
├── app/
│   ├── main.py
│   ├── db.py
│   ├── requirements.txt
│   └── __pycache__/
└── db/
    └── init.sql
```

### Penjelasan Struktur

**docker-compose.yml**  
File konfigurasi untuk mengorkestrasi multiple services (web dan database). File ini mendefinisikan bagaimana container akan dibuat, port yang akan di-expose, environment variables, dan dependencies antar services.

**Dockerfile**  
Berisi instruksi langkah demi langkah untuk membuat Docker image aplikasi Python. Dockerfile ini akan di-build menjadi image yang kemudian digunakan oleh service web dalam docker-compose.

**README.md**  
Dokumentasi lengkap project ini yang Anda baca saat ini.

**app/**  
Direktori yang berisi source code aplikasi Python.

- `main.py`: File utama aplikasi Flask yang mendefinisikan REST API endpoints.
- `db.py`: File helper yang berisi fungsi-fungsi untuk koneksi dan query database PostgreSQL.
- `requirements.txt`: Daftar dependencies Python yang diperlukan aplikasi.
- `__pycache__/`: Direktori cache Python (auto-generated, tidak perlu di-commit ke git).

**db/**  
Direktori yang berisi file-file terkait database.

- `init.sql`: Script SQL untuk inisialisasi schema dan data awal. Script ini akan dijalankan otomatis oleh PostgreSQL container saat pertama kali dibuat.

---

## Persyaratan Sistem

Sebelum menjalankan project ini, pastikan sistem Anda telah memenuhi persyaratan berikut:

### Docker
- **Versi minimum**: Docker 20.10 atau lebih baru
- **Instalasi**: Unduh dan install Docker Desktop dari [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- **Verifikasi instalasi**:
  ```bash
  docker --version
  ```

### Docker Compose
- **Versi minimum**: Docker Compose 2.0 atau lebih baru
- **Catatan**: Docker Compose sudah termasuk dalam Docker Desktop untuk Windows dan macOS
- **Verifikasi instalasi**:
  ```bash
  docker-compose --version
  ```

### Python (Opsional)
- **Versi**: Python 3.11 (jika ingin menjalankan development lokal tanpa Docker)
- **Catatan**: Python tidak wajib jika Anda hanya ingin menjalankan aplikasi dalam Docker container

### Sistem Operasi
Project ini dapat berjalan di:
- Windows 10/11 (dengan WSL2 enabled untuk Docker Desktop)
- macOS 10.15 atau lebih baru
- Linux (distribusi modern dengan kernel 3.10 atau lebih baru)

### Resource Minimum
- **RAM**: Minimal 4GB (disarankan 8GB atau lebih)
- **Disk Space**: Minimal 2GB ruang kosong untuk images dan containers
- **CPU**: 2 cores atau lebih (disarankan)

---

## Penjelasan Detail Setiap Komponen

### 1. Dockerfile

File Dockerfile mendefinisikan bagaimana Docker image untuk aplikasi Python akan dibuat. Berikut penjelasan setiap baris:

```dockerfile
# 1. Base Image
FROM python:3.11-slim
```
Menggunakan official Python 3.11 slim sebagai base image. Versi slim dipilih karena ukurannya lebih kecil dibanding versi standard, namun tetap berisi semua tools yang diperlukan untuk menjalankan aplikasi Python.

```dockerfile
# 2. Working Directory
WORKDIR /app
```
Menetapkan `/app` sebagai working directory di dalam container. Semua perintah selanjutnya akan dijalankan dari direktori ini.

```dockerfile
# 3. Copy requirements and install
COPY app/requirements.txt .
```
Meng-copy file `requirements.txt` dari direktori `app/` di host ke working directory di container (`.` merujuk ke `/app`).

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```
Menginstall semua dependencies Python yang terdaftar di `requirements.txt`. Flag `--no-cache-dir` digunakan untuk mengurangi ukuran layer dengan tidak menyimpan cache pip.

```dockerfile
#4. Copy source code
COPY app/ .
```
Meng-copy semua file dari direktori `app/` di host ke working directory di container. Ini dilakukan setelah install dependencies agar Docker dapat menggunakan layer cache ketika hanya source code yang berubah.

```dockerfile
# 5. EXPOSE port
EXPOSE 5000
```
Mendokumentasikan bahwa container akan listen pada port 5000. Port ini adalah port default Flask development server.

```dockerfile
# 6. Default Command
CMD ["python", "main.py"]
```
Perintah yang akan dijalankan ketika container dimulai. Perintah ini menjalankan aplikasi Flask melalui file `main.py`.

### 2. docker-compose.yml

File docker-compose.yml mengatur orchestration dari multiple services. Project ini memiliki dua services: `db` (PostgreSQL) dan `web` (aplikasi Python).

**Service: db (PostgreSQL)**

```yaml
db:
  image: postgres:16
  container_name: belajar-docker-db
```
Menggunakan official PostgreSQL image versi 16. Container diberi nama `belajar-docker-db` untuk memudahkan identifikasi.

```yaml
environment:
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres
  POSTGRES_DB: db_docker
```
Environment variables untuk konfigurasi PostgreSQL: username, password, dan nama database yang akan dibuat saat container pertama kali dijalankan.

```yaml
ports:
  - "5432:5432"
```
Mapping port 5432 dari container ke port 5432 di host. Ini memungkinkan akses database dari host menggunakan `localhost:5432`.

```yaml
volumes:
  - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
```
Mount file `init.sql` ke direktori khusus `/docker-entrypoint-initdb.d/` di container. File SQL di direktori ini akan dijalankan otomatis saat database pertama kali diinisialisasi. Flag `:ro` (read-only) memastikan container tidak dapat memodifikasi file di host.

**Service: web (Aplikasi Python)**

```yaml
web: 
  build: .
  container_name: python-belajar-docker-db
```
Service ini akan di-build dari Dockerfile yang ada di root direktori (`.`). Container diberi nama `python-belajar-docker-db`.

```yaml
depends_on:
  - db
```
Menentukan bahwa service `web` bergantung pada service `db`. Docker Compose akan memastikan container `db` distart terlebih dahulu sebelum container `web`.

```yaml
ports:
  - "5000:5000"
```
Mapping port 5000 dari container ke port 5000 di host. Aplikasi Flask dapat diakses melalui `http://localhost:5000`.

```yaml
environment:
  DB_HOST: db
  DB_PORT: 5432
  DB_NAME: db_docker
  DB_USER: postgres
  DB_PASSWORD: postgres
```
Environment variables yang akan dibaca oleh aplikasi Python untuk koneksi ke database. `DB_HOST: db` menggunakan nama service sebagai hostname, karena Docker Compose secara otomatis membuat DNS resolution antar container dalam network yang sama.

### 3. app/main.py

File ini adalah entry point aplikasi Flask yang mendefinisikan REST API endpoints.

```python
from flask import Flask, jsonify, request
from db import get_all_customers, create_customer

app = Flask(__name__)
```
Import Flask dan fungsi-fungsi database dari modul `db.py`. Membuat instance Flask app.

```python
@app.route("/")
def root():
    return jsonify(message="Python + Docker + PostgreSQL is running")
```
Endpoint root untuk health check, memastikan aplikasi berjalan dengan baik.

```python
@app.route("/customers", methods=["GET"])
def list_customers():
    customers = get_all_customers()
    return jsonify(customers)
```
Endpoint GET untuk mengambil semua data customers dari database.

```python
@app.route("/customers", methods=["POST"])
def add_customer():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify(error="Name and email are required"), 400
    
    try:
        new_customer = create_customer(name, email)
        return jsonify(new_customer), 201
    except Exception as e:
        return jsonify(error=str(e)), 500
```
Endpoint POST untuk menambahkan customer baru. Endpoint ini melakukan validasi input dan error handling.

```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```
Menjalankan Flask development server pada semua network interfaces (`0.0.0.0`) di port 5000 dengan debug mode aktif.

### 4. app/db.py

File ini berisi fungsi-fungsi helper untuk koneksi dan query database PostgreSQL.

```python
import os
import psycopg2
from psycopg2.extras import RealDictCursor
```
Import library yang diperlukan. `RealDictCursor` digunakan untuk mengembalikan hasil query sebagai dictionary.

```python
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "db_docker")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
```
Membaca konfigurasi database dari environment variables. Jika environment variable tidak ada, akan menggunakan nilai default.

```python
def get_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn
```
Fungsi untuk membuat koneksi baru ke database PostgreSQL.

```python
def get_all_customers():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id, name, email, is_active, created_at FROM customers ORDER BY id;")
            rows = cursor.fetchall()
        return rows
    finally:
        conn.close()
```
Fungsi untuk mengambil semua data customers. Menggunakan context manager (`with`) untuk memastikan cursor ditutup dengan benar.

```python
def create_customer(name, email):
    conn = get_connection()
    try: 
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO customers (name,email)
                VALUES (%s, %s)
                RETURNING id, name, email, is_active, created_at;
                """,
                (name, email)
            )
            new_row = cursor.fetchone()
        conn.commit()
        return new_row
    finally:
        conn.close()
```
Fungsi untuk menambahkan customer baru. Menggunakan parameterized query untuk mencegah SQL injection. Clause `RETURNING` mengembalikan data yang baru di-insert.

### 5. app/requirements.txt

File ini berisi daftar dependencies Python yang diperlukan aplikasi.

```
flask===3.0.0
psycopg2-binary==2.9.10
python-dotenv==1.0.1
```

- **flask**: Web framework untuk membuat REST API
- **psycopg2-binary**: PostgreSQL adapter untuk Python (versi binary yang sudah tercompile)
- **python-dotenv**: Library untuk membaca environment variables dari file `.env` (opsional untuk development lokal)

### 6. db/init.sql

File SQL untuk inisialisasi schema dan data awal database.

```sql
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```
Membuat tabel `customers` dengan kolom id (auto-increment), name, email (unique), is_active (boolean), dan created_at (timestamp).

```sql
INSERT INTO customers (name, email) 
VALUES
('John', 'john@example.com'),
('Bagus', 'bagus@example.com'),
('Tenxi', 'tenxi@example.com')
ON CONFLICT (email) DO NOTHING;
```
Insert data awal. Clause `ON CONFLICT DO NOTHING` mencegah error jika data dengan email yang sama sudah ada (idempotent).

---

## Cara Menjalankan Project

### 1. Clone atau Download Project

Pastikan Anda memiliki semua file project di direktori lokal Anda.

### 2. Buka Terminal/Command Prompt

Navigasi ke direktori root project:

```bash
cd belajar-docker
```

### 3. Build dan Jalankan Containers

Jalankan perintah berikut untuk build image dan start semua services:

```bash
docker-compose up --build
```

**Penjelasan flag:**
- `up`: Membuat dan menjalankan containers
- `--build`: Memaksa rebuild image sebelum menjalankan containers

**Catatan:** Proses pertama kali akan memakan waktu beberapa menit karena Docker perlu download base images (Python dan PostgreSQL) dan install dependencies.

### 4. Verifikasi Containers Berjalan

Buka terminal baru dan jalankan:

```bash
docker ps
```

Output yang diharapkan:

```
CONTAINER ID   IMAGE                    COMMAND                  STATUS         PORTS                    NAMES
xxxxxxxxxxxx   belajar-docker-web       "python main.py"         Up 2 minutes   0.0.0.0:5000->5000/tcp   python-belajar-docker-db
xxxxxxxxxxxx   postgres:16              "docker-entrypoint.s…"   Up 2 minutes   0.0.0.0:5432->5432/tcp   belajar-docker-db
```

### 5. Akses Aplikasi di Browser

Buka browser dan akses:

```
http://localhost:5000
```

Anda akan melihat response JSON:

```json
{
  "message": "Python + Docker + PostgreSQL is running"
}
```

### 6. Verifikasi PostgreSQL Berjalan

PostgreSQL dapat diakses di `localhost:5432`. Anda dapat menggunakan client PostgreSQL seperti pgAdmin, DBeaver, atau psql untuk terkoneksi dengan kredensial:

- **Host**: localhost
- **Port**: 5432
- **Database**: db_docker
- **User**: postgres
- **Password**: postgres

### 7. Menghentikan Containers

Untuk menghentikan containers, tekan `Ctrl+C` di terminal yang menjalankan `docker-compose up`, kemudian jalankan:

```bash
docker-compose down
```

Jika ingin menghapus volume (data database) juga:

```bash
docker-compose down -v
```

**Peringatan:** Flag `-v` akan menghapus semua data yang ada di database. Gunakan hanya jika Anda ingin reset database ke kondisi awal.

### 8. Menjalankan di Background (Detached Mode)

Jika Anda ingin menjalankan containers di background:

```bash
docker-compose up -d
```

Untuk melihat logs:

```bash
docker-compose logs -f
```

Flag `-f` (follow) akan menampilkan logs secara real-time.

---

## Inisialisasi Schema Database

File `db/init.sql` digunakan untuk inisialisasi schema database secara otomatis. PostgreSQL Docker image memiliki fitur khusus yang akan menjalankan semua file `.sql` atau `.sh` yang ada di direktori `/docker-entrypoint-initdb.d/` saat container pertama kali dibuat.

### Cara Kerja Inisialisasi

1. Saat container PostgreSQL pertama kali dijalankan, Docker akan mengecek apakah database sudah ada.
2. Jika database belum ada (direktori data kosong), PostgreSQL akan menjalankan semua script di `/docker-entrypoint-initdb.d/` secara berurutan.
3. File `init.sql` kita di-mount ke direktori tersebut melalui volume dalam `docker-compose.yml`.
4. Script akan dijalankan dengan user yang didefinisikan di environment variables (`POSTGRES_USER`).

### Contoh Schema Tabel

File `db/init.sql` berisi schema sederhana untuk tabel `customers`:

```sql
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO customers (name, email) 
VALUES
('John', 'john@example.com'),
('Bagus', 'bagus@example.com'),
('Tenxi', 'tenxi@example.com')
ON CONFLICT (email) DO NOTHING;
```

**Penjelasan Schema:**

- `id SERIAL PRIMARY KEY`: Auto-increment integer sebagai primary key
- `name VARCHAR(100) NOT NULL`: Nama customer, maksimal 100 karakter, wajib diisi
- `email VARCHAR(150) UNIQUE NOT NULL`: Email customer, harus unik dan wajib diisi
- `is_active BOOLEAN NOT NULL DEFAULT TRUE`: Status aktif customer, default true
- `created_at TIMESTAMP NOT NULL DEFAULT NOW()`: Timestamp saat record dibuat, default waktu sekarang

### Kapan Script Inisialisasi Dijalankan

Script inisialisasi hanya dijalankan sekali saat container pertama kali dibuat. Jika Anda:

- Restart container: Script tidak dijalankan lagi
- Stop dan start container: Script tidak dijalankan lagi
- Hapus container tapi volume tetap ada: Script tidak dijalankan lagi

### Cara Menjalankan Ulang Script Inisialisasi

Jika Anda ingin menjalankan ulang script inisialisasi (misalnya setelah mengubah `init.sql`), Anda harus menghapus volume database:

```bash
docker-compose down -v
docker-compose up --build
```

Flag `-v` akan menghapus semua volume, termasuk data database. Database akan dibuat ulang dari awal dengan menjalankan `init.sql` lagi.

---

## Cara Melakukan Query ke PostgreSQL

### 1. Masuk ke Container PostgreSQL

Untuk mengakses PostgreSQL CLI (psql) di dalam container, gunakan perintah:

```bash
docker exec -it belajar-docker-db psql -U postgres -d db_docker
```

**Penjelasan perintah:**
- `docker exec`: Menjalankan perintah di dalam container yang sedang berjalan
- `-it`: Flag untuk interactive terminal
- `belajar-docker-db`: Nama container PostgreSQL
- `psql`: PostgreSQL client command
- `-U postgres`: Login sebagai user postgres
- `-d db_docker`: Connect ke database db_docker

Anda akan masuk ke PostgreSQL prompt:

```
psql (16.10)
Type "help" for help.

db_docker=#
```

### 2. Menjalankan Query SELECT

Untuk melihat semua data customers:

```sql
SELECT * FROM customers;
```

Output:

```
 id | name  |        email        | is_active |         created_at
----+-------+---------------------+-----------+----------------------------
  1 | John  | john@example.com    | t         | 2025-11-26 15:04:59.720515
  2 | Bagus | bagus@example.com   | t         | 2025-11-26 15:04:59.720515
  3 | Tenxi | tenxi@example.com   | t         | 2025-11-26 15:04:59.720515
(3 rows)
```

Query dengan filter:

```sql
SELECT name, email FROM customers WHERE is_active = true;
```

### 3. Menjalankan Query INSERT

Untuk menambahkan customer baru:

```sql
INSERT INTO customers (name, email) 
VALUES ('Alice', 'alice@example.com');
```

Output:

```
INSERT 0 1
```

Verifikasi data yang baru di-insert:

```sql
SELECT * FROM customers WHERE name = 'Alice';
```

### 4. Menjalankan Query UPDATE

Untuk mengupdate data:

```sql
UPDATE customers 
SET is_active = false 
WHERE email = 'john@example.com';
```

Verifikasi perubahan:

```sql
SELECT name, email, is_active FROM customers WHERE email = 'john@example.com';
```

### 5. Menjalankan Query DELETE

Untuk menghapus data:

```sql
DELETE FROM customers WHERE email = 'alice@example.com';
```

### 6. Menjalankan SQL dari File

Jika Anda memiliki file SQL di host dan ingin menjalankannya di container, gunakan:

```bash
docker exec -i belajar-docker-db psql -U postgres -d db_docker < path/to/your/file.sql
```

Atau, copy file ke container terlebih dahulu:

```bash
docker cp path/to/your/file.sql belajar-docker-db:/tmp/file.sql
docker exec -it belajar-docker-db psql -U postgres -d db_docker -f /tmp/file.sql
```

### 7. Perintah Berguna di psql

Berikut beberapa perintah meta command yang berguna di psql:

```sql
\dt              -- List semua tabel
\d customers     -- Describe struktur tabel customers
\l               -- List semua database
\c db_name       -- Connect ke database lain
\q               -- Keluar dari psql
\?               -- Help untuk meta commands
\h               -- Help untuk SQL commands
```

### 8. Keluar dari psql

Untuk keluar dari PostgreSQL prompt, ketik:

```sql
\q
```

Atau tekan `Ctrl+D`.

---

## Test API Endpoint

Aplikasi menyediakan dua endpoint utama untuk operasi CRUD pada tabel customers.

### 1. GET /customers - Mengambil Semua Data

**Request:**

Menggunakan curl (Windows PowerShell):

```powershell
Invoke-WebRequest -Uri http://localhost:5000/customers -Method GET
```

Menggunakan curl (Linux/macOS atau Git Bash):

```bash
curl http://localhost:5000/customers
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "John",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2025-11-26T15:04:59.720515"
  },
  {
    "id": 2,
    "name": "Bagus",
    "email": "bagus@example.com",
    "is_active": true,
    "created_at": "2025-11-26T15:04:59.720515"
  },
  {
    "id": 3,
    "name": "Tenxi",
    "email": "tenxi@example.com",
    "is_active": true,
    "created_at": "2025-11-26T15:04:59.720515"
  }
]
```

**Status Code:** 200 OK

### 2. POST /customers - Menambahkan Customer Baru

**Request:**

Menggunakan PowerShell:

```powershell
$body = @{
    name = "Alice"
    email = "alice@example.com"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:5000/customers -Method POST -Body $body -ContentType "application/json"
```

Menggunakan curl (Linux/macOS atau Git Bash):

```bash
curl -X POST http://localhost:5000/customers \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'
```

**Request Body:**

```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```

**Response (Success):**

```json
{
  "id": 4,
  "name": "Alice",
  "email": "alice@example.com",
  "is_active": true,
  "created_at": "2025-11-26T15:10:30.123456"
}
```

**Status Code:** 201 Created

**Response (Validation Error):**

Jika name atau email tidak diberikan:

```json
{
  "error": "Name and email are required"
}
```

**Status Code:** 400 Bad Request

**Response (Duplicate Email):**

Jika email sudah ada di database:

```json
{
  "error": "duplicate key value violates unique constraint \"customers_email_key\""
}
```

**Status Code:** 500 Internal Server Error

### 3. Test dengan Postman

Jika Anda menggunakan Postman:

**GET Request:**
1. Buat request baru dengan method GET
2. URL: `http://localhost:5000/customers`
3. Click Send

**POST Request:**
1. Buat request baru dengan method POST
2. URL: `http://localhost:5000/customers`
3. Pilih tab Body
4. Pilih raw dan JSON
5. Masukkan JSON body:
   ```json
   {
     "name": "Bob",
     "email": "bob@example.com"
   }
   ```
6. Click Send

### 4. Test dengan Python Requests

Jika ingin test menggunakan Python script:

```python
import requests

# GET Request
response = requests.get('http://localhost:5000/customers')
print(response.json())

# POST Request
new_customer = {
    'name': 'Charlie',
    'email': 'charlie@example.com'
}
response = requests.post('http://localhost:5000/customers', json=new_customer)
print(response.status_code)
print(response.json())
```

---

## Troubleshooting Umum

### 1. Port Sudah Digunakan

**Problem:**

```
Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use
```

atau

```
Error starting userland proxy: listen tcp4 0.0.0.0:5000: bind: address already in use
```

**Penyebab:**  
Port 5432 (PostgreSQL) atau 5000 (Flask) sudah digunakan oleh aplikasi lain di host Anda.

**Solusi:**

**Opsi 1: Stop aplikasi yang menggunakan port tersebut**

Windows PowerShell:
```powershell
# Cek proses yang menggunakan port 5432
netstat -ano | findstr :5432

# Kill proses dengan PID tertentu (ganti <PID> dengan process ID dari hasil di atas)
taskkill /PID <PID> /F
```

Linux/macOS:
```bash
# Cek proses yang menggunakan port 5432
lsof -i :5432

# Kill proses dengan PID tertentu
kill -9 <PID>
```

**Opsi 2: Ubah port mapping di docker-compose.yml**

Edit file `docker-compose.yml`, ubah port mapping:

```yaml
# Untuk database (ubah port host, biarkan port container tetap 5432)
ports:
  - "5433:5432"  # Akses menggunakan localhost:5433

# Untuk web (ubah port host, biarkan port container tetap 5000)
ports:
  - "5001:5000"  # Akses menggunakan localhost:5001
```

Setelah mengubah, rebuild containers:

```bash
docker-compose down
docker-compose up --build
```

### 2. Koneksi Database Gagal

**Problem:**

```
psycopg2.OperationalError: could not translate host name "db" to address
```

atau aplikasi tidak bisa connect ke database.

**Penyebab:**  
- Container web start sebelum container database siap menerima koneksi
- Network Docker tidak terbuat dengan benar
- Environment variables salah

**Solusi:**

**Opsi 1: Tambahkan healthcheck dan wait condition**

Edit `docker-compose.yml` untuk service db:

```yaml
db:
  image: postgres:16
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 5s
    timeout: 5s
    retries: 5
```

Dan untuk service web, ubah `depends_on`:

```yaml
web:
  depends_on:
    db:
      condition: service_healthy
```

**Opsi 2: Restart container web**

Kadang container web start terlalu cepat sebelum database ready:

```bash
docker-compose restart web
```

**Opsi 3: Verifikasi environment variables**

Pastikan `DB_HOST` di service web sama dengan nama service database:

```yaml
environment:
  DB_HOST: db  # Harus sama dengan nama service database
```

### 3. File SQL Tidak Dieksekusi

**Problem:**

Tabel tidak terbuat atau data initial tidak ada, padahal sudah ada file `init.sql`.

**Penyebab:**  
Container PostgreSQL sudah pernah dibuat sebelumnya, sehingga volume database sudah ada. Script di `/docker-entrypoint-initdb.d/` hanya dijalankan saat database pertama kali dibuat.

**Solusi:**

Hapus volume dan recreate containers:

```bash
docker-compose down -v
docker-compose up --build
```

**Peringatan:** Perintah ini akan menghapus semua data yang ada di database.

**Alternatif:** Jika tidak ingin menghapus semua data, jalankan script SQL secara manual:

```bash
docker exec -i belajar-docker-db psql -U postgres -d db_docker < db/init.sql
```

### 4. Permission Denied pada Volume

**Problem:**

```
Error: permission denied
```

saat mengakses file yang di-mount sebagai volume.

**Penyebab:**  
Masalah permission antara user di container dan user di host, terutama di Linux.

**Solusi:**

**Untuk Linux:**

Ubah ownership file:

```bash
sudo chown -R $USER:$USER db/
```

Atau jalankan Docker dengan user yang sesuai di `docker-compose.yml`:

```yaml
web:
  user: "${UID}:${GID}"
```

**Untuk Windows:**  
Pastikan Docker Desktop memiliki akses ke drive yang digunakan. Buka Docker Desktop Settings > Resources > File Sharing dan pastikan drive Anda sudah di-share.

### 5. Container Terus Restart

**Problem:**

Container langsung exit setelah start dan terus restart.

**Penyebab:**  
Aplikasi error atau crash saat start.

**Solusi:**

Lihat logs untuk mengetahui error:

```bash
docker-compose logs web
```

atau untuk real-time logs:

```bash
docker-compose logs -f web
```

Periksa logs untuk error message dan perbaiki sesuai error yang muncul.

### 6. Image Tidak Ter-update Setelah Edit Kode

**Problem:**

Perubahan kode tidak muncul setelah restart container.

**Penyebab:**  
Docker menggunakan cache layer lama.

**Solusi:**

Rebuild image dengan flag `--no-cache`:

```bash
docker-compose build --no-cache
docker-compose up
```

### 7. Disk Space Penuh

**Problem:**

```
Error: no space left on device
```

**Penyebab:**  
Docker images, containers, dan volumes yang tidak terpakai memenuhi disk.

**Solusi:**

Bersihkan resources Docker yang tidak terpakai:

```bash
# Hapus semua stopped containers
docker container prune

# Hapus semua unused images
docker image prune -a

# Hapus semua unused volumes
docker volume prune

# Atau hapus semua sekaligus (hati-hati, akan menghapus semua data!)
docker system prune -a --volumes
```

---

## Penutup

### Ringkasan

Melalui project ini, Anda telah mempelajari dasar-dasar penggunaan Docker untuk containerization aplikasi Python dengan database PostgreSQL. Anda telah berhasil:

1. Memahami konsep fundamental Docker: image, container, volume, networking, dan isolation.
2. Membuat Dockerfile untuk aplikasi Python Flask.
3. Menggunakan docker-compose untuk mengorkestrasi multiple services.
4. Menginisialisasi database PostgreSQL dengan script SQL otomatis.
5. Membuat REST API sederhana untuk operasi CRUD.
6. Melakukan query langsung ke database PostgreSQL di dalam container.
7. Testing API endpoint menggunakan berbagai tools.
8. Menangani troubleshooting umum yang mungkin terjadi.

### Manfaat yang Didapat

**Konsistensi Environment**  
Dengan Docker, Anda memastikan aplikasi berjalan dengan cara yang sama di mesin development, staging, dan production. Tidak ada lagi masalah "works on my machine".

**Isolasi Dependencies**  
Setiap project dapat memiliki versi Python, library, dan database yang berbeda tanpa konflik dengan project lain.

**Kemudahan Kolaborasi**  
Tim development dapat langsung menjalankan project hanya dengan `docker-compose up` tanpa setup manual yang kompleks.

**Portabilitas**  
Aplikasi dapat dengan mudah dipindahkan ke server atau cloud platform yang berbeda.

### Arah Pengembangan Lanjutan

Setelah menguasai dasar-dasar ini, Anda dapat melanjutkan pembelajaran dengan topik-topik berikut:

**1. Menambahkan ORM dengan SQLAlchemy**

Gunakan SQLAlchemy untuk abstraksi database yang lebih powerful dan type-safe:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/db_docker'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
```

**2. Implementasi Authentication dan Authorization**

Tambahkan JWT authentication untuk mengamankan API:

```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    # Authentication logic
    access_token = create_access_token(identity=user_id)
    return jsonify(access_token=access_token)

@app.route('/customers', methods=['GET'])
@jwt_required()
def list_customers():
    # Protected endpoint
```

**3. Migration Database dengan Alembic**

Gunakan Alembic untuk version control database schema:

```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "Create customers table"
alembic upgrade head
```

**4. Implementasi Testing**

Tambahkan unit test dan integration test:

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_customers(client):
    response = client.get('/customers')
    assert response.status_code == 200
```

**5. Setup CI/CD Pipeline**

Buat GitHub Actions workflow untuk automated testing dan deployment:

```yaml
name: CI/CD Pipeline

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and test
        run: |
          docker-compose up -d
          docker-compose exec web pytest
```

**6. Deploy ke Cloud Platform**

Deploy aplikasi ke platform seperti:
- **AWS ECS/Fargate**: Managed container service
- **Google Cloud Run**: Serverless container platform
- **Azure Container Instances**: Managed container service
- **DigitalOcean App Platform**: Platform-as-a-Service
- **Heroku Container Registry**: Deploy Docker containers ke Heroku

**7. Implementasi Caching dengan Redis**

Tambahkan Redis untuk caching dan meningkatkan performance:

```yaml
# docker-compose.yml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
```

**8. Monitoring dan Logging**

Implementasi monitoring dengan Prometheus dan Grafana, serta centralized logging dengan ELK Stack (Elasticsearch, Logstash, Kibana).

**9. Load Balancing dan Scalability**

Gunakan Docker Swarm atau Kubernetes untuk orchestration multi-container pada production scale.

**10. Security Hardening**

- Gunakan non-root user di Dockerfile
- Scan image untuk vulnerabilities dengan Trivy atau Snyk
- Implementasi secrets management dengan Docker secrets atau HashiCorp Vault
- Setup SSL/TLS untuk HTTPS

### Referensi Lanjutan

**Dokumentasi Resmi:**
- Docker Documentation: [https://docs.docker.com](https://docs.docker.com)
- Docker Compose: [https://docs.docker.com/compose](https://docs.docker.com/compose)
- PostgreSQL Docker Image: [https://hub.docker.com/_/postgres](https://hub.docker.com/_/postgres)
- Flask Documentation: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)

**Best Practices:**
- Docker Best Practices: [https://docs.docker.com/develop/dev-best-practices](https://docs.docker.com/develop/dev-best-practices)
- 12-Factor App: [https://12factor.net](https://12factor.net)

Selamat belajar dan semoga project ini bermanfaat sebagai fondasi untuk pengembangan aplikasi modern dengan Docker.

---

**Lisensi:** MIT License

**Kontributor:** Dokumentasi ini dibuat untuk tujuan pembelajaran Docker dengan Python dan PostgreSQL.

**Versi:** 1.0.0

**Terakhir Diperbarui:** 26 November 2025
#   b e l a j a r - d o c k e r - d a s a r  
 