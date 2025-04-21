from django.db import models
from accounts.models import CustomUser


class Taux(models.Model):
    euro = models.IntegerField(verbose_name="Euro",default=1)
    gnf = models.IntegerField(verbose_name="GNF")
    date_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    author=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.euro

    class Meta:
        db_table = "tauxs"
        ordering = ['-id']
    