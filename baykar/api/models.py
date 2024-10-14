from django.db import models
from django.contrib.auth.models import User

#uçak parçalarının adlarını barındıran tablo
class Part(models.Model):
    # parts = (
    #     ("Wing", "Wing"),
    #     ("Fuselage", "Fuselage"),
    #     ("Tail", "Tail"),
    #     ("Avionics", "Avionics"),
    # )
    part_id = models.AutoField(primary_key=True)
    #uçak parça isimlerinin bulunduğu yer, sonradan eklenerek sayısı arttırılabilir
    part_name= models.CharField(max_length=20, null=False, blank=False)
    
    def __str__(self):
        return self.part_name
    
#db de bulunan tablolar
class ProducedPart(models.Model):
   
    produced_part_id = models.AutoField(primary_key=True)
    # parçaların isimlerinin bulunudurulacağı yer
    part= models.ForeignKey("Part", on_delete=models.CASCADE)
    # parçanın kullanılıp kullanılmadığı ile ilgili alan
    is_used = models.BooleanField(default=False)
    # parça hangi uçağa ait onun ile ilgili alan
    aircraft = models.ForeignKey("Aircraft", on_delete=models.CASCADE)
    #üreten kişi
    producer = models.ForeignKey(User, on_delete=models.CASCADE)
    #üretildiği zaman
    produced_time=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.part.part_name


    
#var olan uçakları adlarını barındıran tablo
class Aircraft(models.Model):
    # aircrafts = (
    #     ("TB2", "TB2"),
    #     ("TB3", "TB3"),
    #     ("AKINCI", "AKINCI"),
    #     ("KIZILELMA", "KIZILELMA"),
    # )
    aircraft_id = models.AutoField(primary_key=True)
    # uçakların isimleri bu kısımda tutuluyor.Sonradan eklenerek sayısı arttırılabilir.
    aircraft_name = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.aircraft_name

#üretilen uçakların bulunduğu tablo
class Production(models.Model):
    product_id = models.AutoField(primary_key=True)
    # üretilen uçak modeli
    aircraft = models.ForeignKey("Aircraft", on_delete=models.CASCADE)
    # uçak üretiminde kullanılan kanat
    used_wing = models.ForeignKey(
        "ProducedPart", on_delete=models.CASCADE, related_name="wing")
    # uçak üretiminde kullanılan gövde
    used_fuselage = models.ForeignKey(
        "ProducedPart", on_delete=models.CASCADE, related_name="fuselage")
    # uçak üretiminde kullanılan kuyruk
    used_tail = models.ForeignKey(
        "ProducedPart", on_delete=models.CASCADE, related_name="tail")
    # uçak üretiminde kullanılan gövde
    used_avionics = models.ForeignKey(
        "ProducedPart", on_delete=models.CASCADE, related_name="avionics")
    #uçağın üretilip üretilmediğini kontrol edilir
    is_produced = models.BooleanField(default=False)
    #üreten kişi
    producer=models.ForeignKey(User,  on_delete=models.CASCADE)
    #üretildiği zaman
    produced_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_id}ID'li üretilen {self.aircraft}"
