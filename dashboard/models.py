
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from ckeditor.fields import RichTextField
class MyUserManager(BaseUserManager):
    def _create_user(self, email, name, phone_number, district,  **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone_number=phone_number, district=district, **extra_fields)
      
        user.save(using=self._db)
        return user

    def create_user(self, email, name, phone_number, district, **extra_fields):
        return self._create_user(email, name, phone_number, district, **extra_fields)

    def create_superuser(self, email, name, phone_number, district,  **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, name, phone_number, district, **extra_fields)

class CustomUser(AbstractBaseUser):
    DISTRICT_CHOICES = [
        ('0', 'Thiruvananthapuram'),
        ('1', 'Kollam'),
        ('2', 'Pathanamthitta'),
        ('3', 'Alapuzha'),
        ('4', 'Kottayam'),
        ('5', 'Idukki'),
        ('6', 'Eranakulam'),
        ('7', 'Thrissur'),
        ('8', 'Palakkad'),
        ('9', 'Malappuaram'),
        ('10', 'Kozhikode'),
        ('11', 'Wayanad'),
        ('12', 'Kannur'),
        ('13', 'Kasargode'),
    ]

    email = models.EmailField(null=True,blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    district = models.CharField(max_length=2, choices=DISTRICT_CHOICES)
    created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'district']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text="Groups this user belongs to.",
        related_query_name='customuser'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name='customuser'
    )




class Batch(models.Model):
    start_date = models.DateField()
    batch_expiry = models.DateField()
    batch_price = models.DecimalField(max_digits=10, decimal_places=2)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Batch for {self.course.course_name}, {self.batch_expiry}, {self.batch_price}"

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    batch = models.ManyToManyField(Batch)
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Subscription of {self.user.name} "

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.course_name  or 'No title'

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    subject_name = models.CharField(max_length=200)
    image=models.ImageField(upload_to='subject_images/', null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.subject_name  or 'No title'


class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    chapter_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='chapter_images/', null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.chapter_name  or 'No title'

class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    lesson_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='lesson_images/', null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.lesson_name  or 'No title'

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    url = models.URLField()
    is_downloadable = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title  or 'No title'

class PDFNote(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='pdf_notes')
    title = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='pdf_notes/')
    is_downloadable = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title  or 'No title'

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    pdf_note = models.ForeignKey(PDFNote, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"Comment by {self.user.name}"

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    pdf_note = models.ForeignKey(PDFNote, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'video', 'pdf_note') 

    def __str__(self):
        if self.video:
            return f"{self.user.name} liked video: {self.video.title}"
        elif self.pdf_note:
            return f"{self.user.name} liked PDF: {self.pdf_note.title}"

class TalentHunt(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    # subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title or 'No title'
    
class TalentHuntSubject(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    talentHunt = models.ForeignKey(TalentHunt, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title or 'No title'

class Level(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField( blank=True, null=True)
    talenthuntsubject = models.ForeignKey(TalentHuntSubject, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title or 'No title'

class Exam(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    duration = models.TimeField(null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title or 'No title'

class Question(models.Model):
    QUESTION_TYPES = (
        (1, 'Text'),
        (2, 'Image'),
    )
  
    question_type = models.PositiveIntegerField(choices=QUESTION_TYPES, default=1)
    question_description = RichTextField()
    hint = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    options = models.JSONField(default=list, null=True, blank=True)
    right_answers = models.JSONField(default=list, null=True, blank=True)  
    master_question = models.IntegerField(null=True, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True)
    talenthunt = models.ForeignKey(TalentHunt, on_delete=models.SET_NULL, null=True, blank=True)
    level=models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.question_description or 'No question type'



class Schedule(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title or 'No title'