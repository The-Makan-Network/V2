from django.contrib import admin

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ('userid', 'phoneno', 'password')
  
  fields = ['userid', 'phoneno', 'password']


admin.site.register(User, AuthorAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ('productid', 'name', 'description', 'minorder')


  
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
  list_filter = ('status')

