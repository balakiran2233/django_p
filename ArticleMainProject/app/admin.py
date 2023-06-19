from django.contrib import admin
from .models import Post, Profile

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','author')
    prepopulated_fields = {'slug':('title',)}

class AdminProfile(admin.ModelAdmin):
    list_display = ['user','dob','photo']


admin.site.register(Post,PostAdmin)
admin.site.register(Profile, AdminProfile)
