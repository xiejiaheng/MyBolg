from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

# Create your models here.
#文章分类
class Article_Kind(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,null=False)

    def __str__(self):
        return "%s" %self.name

#博客文章
class Article(models.Model):
    title = models.CharField(max_length=50)
    content =  RichTextUploadingField()
    created_time = models.DateTimeField(auto_now_add=True)
    kind = models.ForeignKey("Article_Kind",on_delete=models.CASCADE)

    def __str__(self):
        return "<Articlename;%s>" %self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telephone = models.CharField('Telephone', max_length=50, blank=True)
    class Meta:
        verbose_name = 'User Profile'
    def __str__(self):
        return self.user.__str__()

class About(models.Model):
    id = models.AutoField(primary_key=True)
    tit = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.tit
