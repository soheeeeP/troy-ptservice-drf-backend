from django.db import models
from django.contrib.gis.db.models import PointField


class Center(models.Model):
    # psql의 공간 데이터 column postgis 사용
    location = PointField(
        db_index=True,
        verbose_name='위치',
        default=None
    )
    name = models.CharField(
        max_length=50,
        verbose_name='장소명'
    )
    full_address = models.CharField(
        max_length=100,
        verbose_name='도로명 주소'
    )
    city = models.CharField(
        max_length=50,
        verbose_name='시/도',
        null=True
    )
    district = models.CharField(
        max_length=50,
        verbose_name='시/군/구',
        null=True
    )
    town = models.CharField(
        max_length=50,
        verbose_name='읍/면/동',
        null=True
    )

    class Meta:
        db_table = 'center'
        verbose_name = '센터'
        verbose_name_plural = verbose_name
