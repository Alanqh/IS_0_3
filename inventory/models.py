from django.db import models


# 建立一个库存模型，这个模型中包含各种各样的库存产品，模型中需要给出每种产品的id，名称，类别，数量，价格，以及产品的描述
class ProductList(models.Model):
    product_id = models.AutoField(primary_key=True)
    CATEGORY_CHOICES = (
        ('engine', '发动机'),
        ('battery', '电池'),
        ('tire', '轮胎'),
        ('charging pile', '充电桩'),
        ('parts', '其他小配件'),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    # price价格应该是正数，可以有小数，小数点2位
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_list'


class InventoryProducts(models.Model):
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Inventory Products #{self.pk}"


class PurchaseOrder(models.Model):
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # 订单发生的日期和时间，自动添加
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"采购了{self.quantity}个{self.product.name}"


class InventoryChange(models.Model):
    product = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    change_amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"变化了{self.change_amount}个{self.product.name}"
