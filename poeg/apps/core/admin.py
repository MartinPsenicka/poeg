from django.contrib import admin

from .models import HomePageSlider

# Register your models here.


@admin.register(HomePageSlider)
class HomePageSliderAdmin(admin.ModelAdmin):
	list_display = ('name','is_active')
	list_filter = ('is_active',)
	search_fields = ('name','slider_content')


