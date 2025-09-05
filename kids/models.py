from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kids_userprofile')
    courses = models.ManyToManyField('Course', related_name='enrolled_users', blank=True)

    def __str__(self):
        return self.user.username
from django.db import models
class LessonPoster(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='posters')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='lesson_posters/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"
from django.db import models
class LessonVideo(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100, help_text="Title or heading for the video")
    video_url = models.URLField(help_text="YouTube or video embed URL for the video")
    order = models.IntegerField(default=0, help_text="Order for displaying videos")
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"
from django.db import models
from django.conf import settings

# Drawing model for kids' activity uploads
class Drawing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='drawings')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='drawings')
    image = models.ImageField(upload_to='drawings/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    mark = models.CharField(max_length=20, blank=True, null=True, help_text="Teacher's mark (e.g. A+, Good, etc.)")
    feedback = models.TextField(blank=True, null=True, help_text="Teacher's feedback or comments")

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({self.uploaded_at:%Y-%m-%d})"
from django.db import models
# Story model for adding more stories

class Story(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='stories', null=True, blank=True, help_text="Link this story to a specific lesson")
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="YouTube or video embed URL for the story")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.CharField(max_length=255)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100, blank=True)
    option_d = models.CharField(max_length=100, blank=True)
    correct_option = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

    def __str__(self):
        return f"{self.question} ({self.lesson.title})"

# Age group for courses
class AgeGroup(models.Model):
    name = models.CharField(max_length=50)
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    def __str__(self):
        return self.name

# Subject for courses
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Course model
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    level = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0, help_text="Order for displaying courses (lower comes first)")

    def __str__(self):
        return self.name

# Lesson model
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    LESSON_TYPE_CHOICES = [
        ('color', 'Color'),
        ('shape', 'Shape'),
        ('animal', 'Animal'),
        ('number', 'Number'),
        ('alphabet', 'Alphabet'),
        ('phonics', 'Phonics'),
        ('vowel', 'Vowel'),
        ('consonant', 'Consonant'),
        ('words', 'Simple Words'),
        ('sight_words', 'Sight Words'),
        ('blending', 'Blending Sounds'),
        ('word_building', 'Word Building'),
        ('blending_quiz', 'Blending Quiz'),
        ('simple_sentences', 'Simple Sentences'),
        ('activities', 'Activities'),
        # Add more types as needed
    ]
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='color', help_text="Type of lesson (color, shape, etc.)")
    content = models.TextField()
    order = models.IntegerField(default=0)
    video_url = models.URLField(blank=True, null=True, help_text="YouTube or video embed URL for the lesson")
    poster_image = models.ImageField(upload_to='lesson_posters/', blank=True, null=True, help_text="Upload a poster for this lesson")
    def __str__(self):
        return f"{self.course.name} - {self.title}"

class ColorImage(models.Model):
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('yellow', 'Yellow'),
        ('green', 'Green'),
        ('orange', 'Orange'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
        ('brown', 'Brown'),
        ('black', 'Black'),
        ('white', 'White'),
    ]
    lesson = models.ForeignKey(Lesson, related_name='color_images', on_delete=models.CASCADE)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    image = models.ImageField(upload_to='lessons/colors/')

    def __str__(self):
        return f"{self.lesson.title} - {self.color}"
    

class LessonImage(models.Model):
    IMAGE_TYPE_CHOICES = [
        ('color', 'Color'),
        ('shape', 'Shape'),
        ('animal', 'Animal'),
        ('number', 'Number'),
        # Add more types as needed
    ]
    lesson = models.ForeignKey(Lesson, related_name='lesson_images', on_delete=models.CASCADE)
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES)
    label = models.CharField(max_length=50, help_text="Name of the color, shape, animal, etc.")
    image = models.ImageField(upload_to='lessons/images/')

    def __str__(self):
        return f"{self.lesson.title} - {self.image_type} - {self.label}"

# Example: KidsMovie model for kids movies
class KidsMovie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to='kids/movies/', blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True)
    genre = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

class LessonCompletion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_completions')
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='completions')
    completed_learned = models.BooleanField(default=False)
    completed_activity = models.BooleanField(default=False)
    completed_game = models.BooleanField(default=False)
    completed_quiz = models.BooleanField(default=False)
    teacher_approved = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_completions')

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} completion"
