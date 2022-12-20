from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SkypeUserModel(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    other_user = models.ForeignKey(User, related_name='other_user', on_delete=models.CASCADE)

class SkypeMyNameModel(models.Model):
    user = models.OneToOneField(User, related_name='user_skype_id', on_delete=models.CASCADE)
    skype_id = models.CharField(max_length=100)

####################################################stripe####################################################
# 商品マスタ
class Product(models.Model):
    # 商品名
    name = models.CharField(max_length=100)
    # 商品概要
    description = models.CharField(max_length=255, blank=True, null=True)
    # 商品ID（★stripeの商品IDを値に用いる）
    stripe_product_id = models.CharField(max_length=100)
    # 商品写真登録用のファイル
    file = models.FileField(upload_to="product_files/", blank=True, null=True)
    # 商品詳細ページのリンク
    url  = models.URLField()

    # admin画面で商品名表示
    def __str__(self):
        return self.name

# 価格マスタ
class Price(models.Model):
    # 外部キーで商品マスタを紐付け
    product = models.ForeignKey(Product, related_name='Prices', on_delete=models.CASCADE)
    # 価格ID（★stripeの価格IDを値に用いる）
    stripe_price_id = models.CharField(max_length=100)
    # 価格
    price = models.IntegerField(default=0)

    # Django画面に表示する価格
    def get_display_price(self):
        return self.price

# トランザクションマスタ
class Transaction(models.Model):
    # 購入日
    date   = models.CharField(max_length=100)
    # 購入者
    customer_name = models.CharField(max_length=100)
    # 購入者のメールアドレス
    email  = models.EmailField(max_length=100)
    # 購入商品名
    product_name = models.CharField(max_length=100)
    # 支払い金額
    product_amount = models.IntegerField()

    # admin画面で商品名表示
    def __str__(self):
        return self.date + '_' + self.product_name  + '_' + self.customer_name

#20221213
class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    stripe = models.CharField(verbose_name='Stripe Session', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_date = models.DateField(null=True, blank=True)
########################################################################################################