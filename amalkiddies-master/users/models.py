# Move imports to the top
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# User-uploaded music track model
class MusicTrack(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='music_tracks')
	title = models.CharField(max_length=100)
	artist = models.CharField(max_length=100)
	album = models.CharField(max_length=100, blank=True, null=True)
	genre = models.CharField(max_length=50, blank=True, null=True)
	audio_file = models.FileField(upload_to='music/')
	cover_image = models.ImageField(upload_to='music/covers/', blank=True, null=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.title} by {self.artist}"

# Game attempt tracking and leaderboard
class GameAttempt(models.Model):
	GAME_CHOICES = [
		('movie_quiz', 'Movie Quiz'),
		('scratch_card', 'Scratch Card'),
		('spin_wheel', 'Spin Wheel'),
		('lucky_draw', 'Lucky Draw'),
		('daily_challenge', 'Daily Challenge'),
		# Add other games as needed
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.CharField(max_length=32, choices=GAME_CHOICES)
	attempted_at = models.DateTimeField(auto_now_add=True)
	score = models.IntegerField(default=0)



class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
	mobile_number = models.CharField(max_length=15, blank=True, null=True)
	accept_gifts = models.BooleanField(default=True)
	gift_permission_mode = models.CharField(max_length=16, choices=[('auto','Auto'),('with_permission','With Permission')], default='auto')
	referral_code = models.CharField(max_length=32, unique=True, blank=True, null=True)
	coins = models.PositiveIntegerField(default=0)
	USER_TYPE_CHOICES = [
		('kid', 'Kid'),
	]

	user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='kid')
	courses = models.ManyToManyField('kids.Course', blank=True, related_name='students', help_text='Courses the student is enrolled in')

	def __str__(self):
		return f"Profile for {self.user.username}"

# Auto-generate referral code on profile creation
@receiver(post_save, sender=UserProfile)
def generate_referral_code(sender, instance, created, **kwargs):
	if created and not instance.referral_code:
		instance.referral_code = str(uuid.uuid4())[:8]
		instance.save()


# Loyalty/Rewards Program
class LoyaltyPoint(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loyalty_points')
	points = models.PositiveIntegerField(default=0)

	def __str__(self):
		return f"{self.user.username}: {self.points} points"


# Leaderboard Model
class Leaderboard(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard')
	total_score = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.user.username}: {self.total_score} points"

