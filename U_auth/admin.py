from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Country_codes)
admin.site.register(languages)
admin.site.register(OTP)

admin.site.register(UserPersonalDetails)
admin.site.register(Pictures)
admin.site.register(Hobbies)
admin.site.register(Intrestes)
admin.site.register(Job_Details)
admin.site.register(Relationship_Goals)
admin.site.register(AdditionalDetails)
admin.site.register(UserDisabilities)



