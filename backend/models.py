from django.db import models

# Create your models here.
class Article(models.Model):
    aid = models.AutoField(primary_key=True,auto_created=True)
    title = models.CharField(null=False,max_length=100)
    content = models.TextField(max_length=100000)
    category = models.ForeignKey('Cattegory',to_field="cid")
    time = models.CharField(max_length=20,null=False,)
    status = models.IntegerField(null=False,default=1)
    like = models.IntegerField(default=0)

class Cattegory(models.Model):
    cid = models.IntegerField(primary_key=True,auto_created=True)
    cname = models.CharField(null=False,max_length=50)

class User(models.Model):
    uid = models.AutoField(auto_created=True,primary_key=True)
    username = models.CharField(max_length=64,null=False,unique=True)
    passwd = models.CharField(max_length=256,null=False)
    telphone = models.IntegerField(null=True)
    wechat = models.CharField(null=True,max_length=128)
    qq = models.IntegerField(null=True)
    email = models.CharField(null=True,max_length=32)