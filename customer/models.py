from django.db import models

from register.models import User, Car


class ServiceType(models.Model):
    service_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'service_type'  # 指定数据库表名
    # 添加其他服务类型相关的字段


class ServiceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    description = models.TextField()
    service_state = models.IntegerField(default=0)  # 0:未处理 1:已处理

    # 添加其他服务记录相关的字段
    class Meta:
        db_table = 'service_record'  # 指定数据库表名

    def __str__(self):
        return self.service_type.name + ' | ' + self.user.last_name + self.user.first_name + "的" + self.car.car_name
