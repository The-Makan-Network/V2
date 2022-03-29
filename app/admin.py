from django.contrib import admin

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ('userid', 'phoneno', 'password')
  
  fields = ['userid', 'phoneno', 'password']
    pass

admin.site.register(User, AuthorAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ('productid', 'name', 'description', 'minorder')
    pass

  
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
  list_filter = ('status')
    pass
