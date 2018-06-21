from django.contrib import admin
from blog import models
from django.utils.html import format_html

# def copy_one(self, request, queryset):
#     # 定义actions函数
#     # 判断用户选择了几条数据，如果是一条以上，则报错
#     if queryset.count() == 1:
#         old_data = queryset.values()[0]
#         old_data.pop('id')
#         self.message_user(request, "你选了一条没错")
#         # 将原数据复制并去掉id字段后，插入数据库，以实现复制数据功能，返回值即新数据的id（这是在model里__str__中定义的）
#         # r_pk = Record.objects.create(**old_data)
#         # # 修改数据后重定向url到新加数据页面
#         # return HttpResponseRedirect('{}{}/change'.format(request.path, r_pk))
#     else:
#         self.message_user(request, "只能选取一条数据！")
# copy_one.short_description = "判断是否只选了一条"

list_per_page = 50
ordering = ('-add_date',)

admin.site.site_header = '夏天浩 博客'
admin.site.site_title = '夏天浩 博客'


class ArticleInline(admin.TabularInline):
    model = models.Article
    extra = 5  # 默认显示条目的数量


class ArticleGroupAdmin(admin.ModelAdmin):
    inlines = [ArticleInline, ]  # Inline把BillSubInline关联进来
    list_display = ('name',)


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    def article_tags(self, obj):
        tags = ''
        for each in obj.tags.all():
            tags += each.name + "/"
        return format_html("%s" % tags)

    def copy_one(self, request, queryset):
        # 定义actions函数
        # 判断用户选择了几条数据，如果是一条以上，则报错
        if queryset.count() == 1:
            old_data = queryset.values()[0]
            old_data.pop('id')
            self.message_user(request, "你只选了一条没错！")
            # 将原数据复制并去掉id字段后，插入数据库，以实现复制数据功能，返回值即新数据的id（这是在model里__str__中定义的）
            # r_pk = Record.objects.create(**old_data)
            # # 修改数据后重定向url到新加数据页面
            # return HttpResponseRedirect('{}{}/change'.format(request.path, r_pk))
        else:
            self.message_user(request, "只能选取一条数据！")

    copy_one.short_description = "判断是否选了一条"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # change_obj = models.Article.objects.filter(pk=object_id)
        # self.get_readonly_fields(request, obj=change_obj) # 配合get_readonly_fields实现不同状态的数据不同的可修改字段
        return super(ArticleAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
            # self.readonly_fields = ['title', 'content']
        # elif hasattr(obj, 'is_sure'): # 用来判断如是否已经审批等状态
        #     if obj.is_sure:
        #         self.readonly_fields = ('project_name', 'to_mail', 'data_selected', 'frequency', 'start_date',
        #                                 'end_date')
        # else:
        #     self.readonly_fields = ('paper_num', 'is_sure', 'proposer', 'sql', 'commit_date')

        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        # 数据保存时进行一些额外的操作（通过重写ModelAdmin的save_model实现）
        # 通过change参数，可以判断是修改还是新增，同时做相应的操作
        # print(obj,form,change)
        pass
        super(ArticleAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        pass
        super(ArticleAdmin, self).delete_model(request, obj)

    # def more_than_100(self,obj):
    #     #自定义字段,要加到list_display中去
    #     if obj.read_times>100:
    #         return format_html('YES')
    #     else:
    #         return format_html('No')
    #
    # more_than_100.short_description = '阅读是否过百'#自定义表头
    # more_than_100.admin_order_field = 'read_times'  # 使自定义字段 可以通过单击进行排序
    actions = ('copy_one',)
    readonly_fields = ('title',)
    article_tags.short_description = '标签'
    # inlines = [StepInline, ]
    list_display = ('title', 'type', 'group', 'add_date', 'article_tags', 'read_times')
    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     ('Personal', {'fields': ('name',)}),
    #     ('Permissions', {'fields': ('is_admin',)}),
    # )  # 只显示和可编辑这些,字段集合fieldsets中每一个元组的第一个元素是该字段集合的标题
    filter_horizontal = ('tags',)
    search_fields = ('title', 'type__name')  # 添加搜索字段
    date_hierarchy = 'add_date'
    list_filter = ('type', 'group', 'tags', 'add_date')  # 添加按照字段过滤的关键字list_filter
    # list_editable = ('type',)  # 让后台界面上可以直接修改字段值的关键字定义list_editable,这里注意Django admin后台默认显示的第一个表字段是不能修改的.
    list_per_page = 10  # 让每页显示几条记录的设置

    # raw_id_fields = ('type',)    # 只针对外键的 即不显示对应的文章,类型而显示ID如 1
    # exclude = ('recommend',)  # 排除该字段
    # fields =  ('caption', 'author', 'tags', 'content')# 只显示
    # fieldsets = (
    #     ("base info", {'fields': ['caption', 'author', 'tags']}),
    #     ("Content", {'fields': ['content', 'recommend']})
    # )设置显示及分块


    ordering = ('-add_date',)


admin.site.register(models.UserProfile)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleTag)
admin.site.register(models.ArticleGroup, ArticleGroupAdmin)
admin.site.register(models.Comment)
admin.site.register(models.Visitor)
admin.site.register(models.ArticleType)
