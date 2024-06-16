from django.contrib import admin
from .models import *


admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(PromotionProfile)
admin.site.register(SubStatus)
