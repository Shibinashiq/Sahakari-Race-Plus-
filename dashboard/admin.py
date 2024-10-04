from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Batch)
admin.site.register(Subscription)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(PDFNote)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(TalentHunt)
admin.site.register(TalentHuntSubject)
admin.site.register(Level) 
admin.site.register(Schedule) 
# admin.site.register(SuccessStory) 
admin.site.register(Folder) 
admin.site.register(BatchLesson) 
admin.site.register(TempUser) 
admin.site.register(Otp) 


