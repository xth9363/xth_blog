from django.contrib import admin
from blog import models
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    # inlines = [StepInline, ]
    filter_horizontal = ('tags',)

admin.site.register(models.UserProfile)
admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.ArticleTag)
admin.site.register(models.ArticleGroup)
admin.site.register(models.Comment)
admin.site.register(models.Visitor)
admin.site.register(models.ArticleType)
