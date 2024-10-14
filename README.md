# django-task
KURULUM
Proje docker üzerinden çalıştırmak için:

    1. Başlangıçta Docker-compose bilgisayarınızda kurulu olduğuna emin olunuz. İndirmek için 
     https://docs.docker.com/compose/install/ linkinden faydalanabilirsiniz.
    2. Projeyi githubdan klonlayınız.
    3.Proje dosyasını klonladıktan sonra,  "docker-compose up --build" komutu ile çalıştırabilirsiniz.(Bundan sonraki komutlarda permission hatası alıyorsanız sudo ile çalıştırabilirsiniz)
    4.Sonrasında açacağınız yeni bir terminalde " docker-compose exec web python manage.py migrate"  komutu ile migration dosyasındaki tabloları, db'ye ekliyoruz.
    5.Daha sonra " docker-compose exec web python manage.py loaddata mockdata.json" komutu ile mockdatayı db'ye eklemiş oluyoruz.
    6. Unit Testleri çalıştırmak için  " docker-compose exec web python manage.py test"  komutuyla var olan bütün unit testleri çalıştırabilirsiniz.
    7.Aşağıdaki kullanıcı adı ve şifrelerle giriş yapabilirsiniz. http://127.0.0.1:8000/ dan erişebilirsiniz.
    8. http://127.0.0.1:8000/api/swagger/'dan ve http://127.0.0.1:8000/api/redoc/ 'dan swagger ui'da bulunan API dokümantasyonuna göz atabilirsiniz.
    

    username:tail password:baykartail ->tail ekibinde
    username:avionics password:baykaravionics ->avionics ekibinde
    username:fuselage password:baykarfuselage ->fuselage ekibinde
    username:wing password:baykarwing ->wing ekibinde
    username:assembly password:baykarassembly -> assembly ekibinde

DOSYA YAPISI
Uygulamada api ve pages adlı iki app bulunmaktador.Pages app klasörü içerisinde MVT tasarım deseni kullanılarak dört farklı sayfa oluşturulmuştur. Template dili olarak jinja kullanılmıştır.

Api app klasörü içeriisnde ise kullanılan apilar mevcuttur.Get, Update, Create,Delete(CRUD) operasyonlarının gerçekleştiği ve db tablolarının bulunduğu yerdir.

Test dosyları hem api hem de pages app klasörlerinde mevcuttur. 

```bash
.   
├── api
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_initial.py
│   │   ├── 0003_remove_part_aircraft_remove_part_is_used_and_more.py
│   │   ├── 0004_rename_user_producedpart_producer_and_more.py
│   │   ├── 0005_producedpart_produced_time_production_produced_time.py
│   │   └── __init__.py
│   ├── models.py
│   ├── serializer
│   │   ├── aircraftserializer.py
│   │   ├── __init__.py
│   │   ├── partserializer.py
│   │   ├── producedpartserializer.py
│   │   ├── productionserializer.py
│   │   └── userserializer.py
│   ├── tests
│   │   ├── dashboardapitest.py
│   │   ├── dbtest.py
│   │   ├── deleteandupdateapitest.py
│   │   ├── __init__.py
│   │   └── logintest.py
│   ├── urls.py
│   └── views
│       ├── dashboardapi.py
│       ├── deleteandupdateapi.py
│       ├── __init__.py
│       └── loginapi.py
├── baykar
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── mockdata.json
├── pages
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── __init__.py
│   │  
│   ├── models.py
│   ├── static
│   │   ├── css
│   │   │   ├── add.css
│   │   │   ├── dashboard.css
│   │   │   ├── login-static.css
│   │   │   └── update.css
│   │   └── js
│   │       ├── add.js
│   │       ├── dashboard.js
│   │       ├── login.js
│   │       └── update.js
│   ├── templates
│   │   ├── add.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   └── update.html
│   ├── tests
│   │   ├── addpagetest.py
│   │   ├── dashboardpagetest.py
│   │   ├── __init__.py
│   │   ├── loginpagetest.py
│   │   └── updatepagetest.py
│   ├── urls.py
│   └── views
│       ├── addpage.py
│       ├── dashboard.py
│       ├── __init__.py
│       ├── loginpage.py
│       └── updatepage.py
└── requirements.txt
```
Çalışma Yapısı
Kullanıcıların her biri django'da bulunan groups (authorization) tablosunda bir ekibe dahil.5 ekip mevcut (tail, wing, fuselage, assembly,avionics). Arayüz olarak request atan kullanıcının ekibine göre dashboard değişmektedir. Ekleme, güncelleme ve çıkarma api'larında işlemler view üzerinden gerçekleşmektedir. Login yapıldıktan sonra token iletilir.API iletilen token üzerinden çalışır. Kullanıcı değiştirileceği zaman login ekranına gelip giriş yapılacak kişinin kullanıcı adı ve şifresi girilebilir. Dashboard ekranında bulunan datatable'ın her bir sırasına tıkladığınızda onu güncellemeniz için başka bir sayfaya yönlendirecektir. O sayfada sadece güncelleme değil, silme işlemi de gerçekleştirebilirsiniz.

Fotoğraflar
![login](<Screenshot from 2024-10-14 22-30-55.png>)
![dashboard](<Screenshot from 2024-10-14 22-27-02.png>)
![create](<Screenshot from 2024-10-14 22-27-09.png>)
![create](<Screenshot from 2024-10-14 22-27-11.png>)
![update](<Screenshot from 2024-10-14 22-27-18.png>)
![dashboard](<Screenshot from 2024-10-14 22-27-40.png>)
![create](<Screenshot from 2024-10-14 22-27-46.png>)

