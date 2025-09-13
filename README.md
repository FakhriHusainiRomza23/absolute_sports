# Absolute Sports
## Aplikasi football shop saya dapat di akses di link berikut: https://fakhri-husaini41-absolutesports.pbp.cs.ui.ac.id/ 

Nama Aplikasi: Absolute Sports\
Nama: Fakhri Husaini Romza\
NPM: 2406436972\
Kelas: PBP C

## 1. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
   1. Membuat proyek Django
      Saya membuka terminal pada direktori kerja lalu menjalankan perintah `django-admin startproject absolute_sports` untuk membuat struktur proyek dasar. Perintah ini menghasilkan file `manage.py` beserta folder absolute_sports yang berisi file konfigurasi seperti settings.py, urls.py, dan lainnya. Setelah itu, saya membuat virtual environment baru menggunakan `python -m venv venv` dan mengaktifkannya dengan perintah `venv\Scripts\activate`. Langkah berikutnya adalah menginstal Django beserta dependensi lain yang tercantum dalam `requirements.txt` menggunakan perintah `pip install -r requirements.txt`.
      
   2. Membuat aplikasi bernama main
      Setelah berada di dalam direktori proyek, saya menjalankan perintah `python manage.py startapp main` untuk membuat aplikasi baru. Perintah ini menghasilkan sebuah folder bernama main yang berisi beberapa file standar seperti `models.py`, `views.py`, `urls.py`, dan `admin.py` yang nantinya digunakan untuk mengatur logika aplikasi, struktur data, serta konfigurasi admin. Agar aplikasi ini terintegrasi dengan proyek utama, saya menambahkan 'main' ke dalam daftar INSTALLED_APPS di file settings.py. Dengan begitu, Django mengenali aplikasi main sebagai bagian dari proyek dan siap digunakan dalam pengembangan lebih lanjut.
   
   3. Melakukan routing pada proyek agar dapat menjalankan aplikasi main
      Pada file `urls.py` , saya menambahkan konfigurasi routing dengan mengimpor include dari django.urls. Setelah itu, saya menambahkan baris `path('', include('main.urls'))` sehingga setiap permintaan ke root URL diarahkan ke file urls.py milik aplikasi main. Dengan cara ini, rute utama proyek secara otomatis dipetakan ke dalam sistem routing aplikasi main.
   
   4. Membuat model pada aplikasi main dengan nama Product dan memiliki atribut wajib
      di models.py saya definisikan `Product(models.Model)` dengan atribut sebagai berikut:
      ```
      name = models.CharField(max_length=255)
      price = models.IntegerField()
      description = models.TextField()
      category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
      thumbnail = models.URLField(blank=True, null=True)
      is_featured = models.BooleanField(default=False)
      ```
      Lalu, Saya menjalankan perintah `python manage.py makemigrations` untuk membuat berkas migrasi berdasarkan model yang telah didefinisikan di aplikasi main. Setelah itu, saya mengeksekusi `python manage.py migrate` agar migrasi tersebut diterapkan ke database.

   5. Membuat fungsi pada views.py untuk dikembalikan ke template HTML yang menampilkan nama aplikasi serta nama dan kelas:
      Di main/views.py, buat fungsi show_main(request):
      ```
      from django.shortcuts import render
      
      def show_main(request):
          context = {
              'npm' : '2406436972',
              'name': 'Fakhri Husaini Romza',
              'class': 'PBP B'
          }

          return render(request, "main.html", context)
      ```

   6. Membuat sebuah routing pada urls.py aplikasi main
      ```
      from django.urls import path
      from main.views import show_main

      app_name = 'main'

      urlpatterns = [
          path('', show_main, name='show_main'),
      ]
      ```

  7. Melakukan deployment ke PWS
     ```
     git add .
     git commit -m "Tugas 2: Django MVT impementations"
     git push origin master
     git push pws master
     ```
## 2. Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.
   <img width="691" height="559" alt="image" src="https://github.com/user-attachments/assets/b0fcd570-1f6d-4437-b614-d48f540bff0a" />

1. User mengakses suatu URL tertentu pada browser (request).
2. Django akan memetakan URL (routing) tersebut ke View melalui urls.py.
3. View mengambil dan memproses data dari Model apabila dibutuhkan.
4. Output dari View ditampilkan ke pengguna dengan cara dikirim ke Template (html)

Referensi adalah PPT 03 - MTV Django Architecture:
https://drive.google.com/drive/folders/1St8NywVbAFIgZ1AWCbe6VMmZZj2_BzR_?usp=sharing 
   
## 3. Jelaskan peran settings.py dalam proyek Django!
   settings.py adalah file konfigurasi proyek Django. Peran-perannya adalah:
   1. Pengaturan database
   2. Static files dan template.
   3. Keamanan, seperti SECRET_KEY, DEBUG, ALLOWED_HOSTS
   4. Konfigurasi proyek, seperti nama aplikasi di INSTALLED_APPS, pengaturan middleware, dan pengaturan root URL

## 4. Bagaimana cara kerja migrasi database di Django?
   Migrasi database di Django adalah proses yang menghubungkan perubahan pada model di `models.py` dengan struktur database. Saat developer membuat atau mengubah model, perintah `python manage.py makemigrations` digunakan untuk menghasilkan file migrasi yang berisi instruksi perubahan skema database. Selanjutnya, perintah `python manage.py migrate` mengeksekusi file migrasi tersebut ke database sehingga struktur database selalu selaras dengan definisi model.

## 5. Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?
   1. Dengan pola MTV (Model-Template-View), Django memudahkan pemula memahami hubungan antara logika aplikasi, pengelolaan data, dan tampilan antarmuka.
   2. Django memiliki banyak fitur bawaan, seperti autentikasi, sistem admin, manajemen URL, dll.
   3. Dokumentasi lengkap.
   4. Django banyak digunakan di industri.

## 6. Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?
   Tutorial 1 sangat membantu. catatan-catatan yang ada juga sangat berguna ketika ada error. Penjelasan yang ada juga sudah sangat jelas.