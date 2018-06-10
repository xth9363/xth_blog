from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


import uuid

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
# Create your models here.
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class UserProfileManager(BaseUserManager):
    '''
    账号管理
    '''

    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        self.is_active = True

        user.set_password(password)  # 检测密码合理性
        user.save(using=self._db)  # 保存密码
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    """账号表"""

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    email = models.EmailField(
        verbose_name='邮箱',
        max_length=255,
        unique=True,
        null=True,
        # help_text=mark_safe('''<a href='password/'>修改密码</a>''')
    )
    # password = models.CharField(_('password'), max_length=128, )
    name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)

    # is_superuser = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    add_date = models.DateTimeField(auto_now_add=True)
    # 固定这写法
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'  # 决定登录名
    REQUIRED_FIELDS = ['name']  # 必须填写的数据

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser


class ArticleTag(models.Model):
    name = models.CharField(max_length=32, verbose_name="标签名", help_text="标签名", unique=True)
    details = models.TextField(verbose_name="说明", help_text="说明")
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = '文章标签'

    def __str__(self):
        return "%s" % (self.name)


class ArticleType(models.Model):
    class Meta:
        verbose_name = '文章类型'
        verbose_name_plural = '文章类型'

    name = models.CharField(max_length=32, verbose_name='文章类型', help_text='文章类型')

    def __str__(self):
        return '%s' % self.name


class Article(models.Model):
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

    auther = models.ForeignKey(UserProfile, verbose_name="作者", help_text='作者', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100, verbose_name="文章标题", help_text="文章标题")
    content = RichTextUploadingField(verbose_name="内容", help_text="内容")
    add_date = models.DateTimeField()
    read_times = models.IntegerField(default=0, verbose_name="阅读次数", help_text="所属系列")
    update_date = models.DateTimeField(auto_now_add=True, verbose_name="最后修改时间", help_text="最后修改时间")
    good = models.IntegerField(default=0, verbose_name="赞", help_text="赞")
    bad = models.IntegerField(default=0, verbose_name="踩", help_text="踩")
    group = models.ForeignKey(to="ArticleGroup", blank=True, null=True, verbose_name="所属系列", help_text="所属系列",
                              on_delete=models.CASCADE)
    type = models.ForeignKey(to="ArticleType", verbose_name="文章类型", help_text="文章类型",
                             on_delete=models.CASCADE)
    tags = models.ManyToManyField("ArticleTag", related_name="articles", blank=True, null=True, )

    def __str__(self):
        return "%s" % (self.title)


class ArticleGroup(models.Model):
    class Meta:
        verbose_name = '文章系列'
        verbose_name_plural = '文章系列'

    author = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, verbose_name="系列文章", help_text="系列文章")
    content = RichTextUploadingField(verbose_name="说明", help_text="说明")
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.name)


class Comment(models.Model):
    class Meta:
        verbose_name = '留言'
        verbose_name_plural = '留言'

    # user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, verbose_name="留言用户")
    commenter = models.CharField(max_length=32, null=True, blank=True)
    reply_to = models.CharField(max_length=32, null=True, blank=True, verbose_name="回复对象")
    article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name='留言文章')
    content = models.TextField(verbose_name="留言内容")
    add_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(to='Comment', related_name='childs', on_delete=models.CASCADE, verbose_name="父回复",
                               blank=True, null=True)

    def __str__(self):
        return "%d:%s:%s" % (self.id, self.commenter, self.content)


class Visitor(models.Model):
    class Meta:
        verbose_name = '访问者'
        verbose_name_plural = '访问者'

    ip = models.GenericIPAddressField(verbose_name='访问者Ip')
    url = models.TextField(verbose_name='访问地址',null=True,blank=True)
    user = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='用户', on_delete=models.CASCADE)
    visit_date = models.DateTimeField(auto_now_add=True, verbose_name='访问时间')
    location = models.CharField(max_length=64, verbose_name='访问者所在地', null=True, blank=True)

    def __str__(self):
        return "{}:{}:{}".format(self.id, self.ip, self.url)


