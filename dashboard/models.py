
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class MyUserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", 1)
        extra_fields.setdefault("name", "Superuser")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("user_type") != 1:
            raise ValueError("Superuser must have user_type=1.")
        return self._create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
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
    
    district = models.CharField(max_length=2, choices=DISTRICT_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    objects = MyUserManager()

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username
        
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
    def save(self, *args, **kwargs):
   
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
        
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)




class Batch(models.Model):
    batch_expiry = models.DateField()
    batch_price = models.DecimalField(max_digits=10, decimal_places=2)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Batch for {self.course.course_name}, {self.batch_expiry}, {self.batch_price}"

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Subscription of {self.user.username} to batch {self.batch.batch_expiry}"

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.course_name

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    subject_name = models.CharField(max_length=200)
    image=models.ImageField(upload_to='subject_images/', null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.subject_name  


class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    chapter_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='chapter_images/', null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.chapter_name} - {self.subject.subject_name}"

class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    lesson_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='lesson_images/', null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.lesson_name

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    url = models.URLField()
    is_downloadable = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title 

class PDFNote(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='pdf_notes')
    title = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='pdf_notes/')
    is_downloadable = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title 

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    pdf_note = models.ForeignKey(PDFNote, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"Comment by {self.user.username}"

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
            return f"{self.user.username} liked video: {self.video.title}"
        elif self.pdf_note:
            return f"{self.user.username} liked PDF: {self.pdf_note.title}"

            
