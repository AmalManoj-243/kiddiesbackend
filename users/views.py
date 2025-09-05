from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Redirect teachers to teacher dashboard after login
@login_required
def post_login_redirect(request):
    if hasattr(request.user, 'userprofile'):
            if request.user.userprofile.user_type == 'kid':
                return redirect('kids_home')
    return redirect('home')
from django.shortcuts import redirect

def switch_mode(request):
    from django.shortcuts import render
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_profile = getattr(request.user, 'userprofile', None)
            if user_profile:
                if user_profile.user_type == 'kid':
                    # Kid users must enter parental PIN to exit kids mode
                    pin = request.POST.get('parental_pin')
                    if pin is not None:
                        # Hardcoded demo PIN: 1234
                        if pin == '1234':
                            request.session['kids_mode'] = False
                            return redirect('/')
                        else:
                            return render(request, 'users/parental_pin.html', {'error': 'Incorrect PIN'})
                    # Show PIN entry form
                    request.session['kids_mode'] = True
                    return render(request, 'users/parental_pin.html')
                    # Removed normal user logic
                    kids_mode = request.session.get('kids_mode', False)
                    request.session['kids_mode'] = not kids_mode
                    if not kids_mode:
                        return redirect('/kids/')
                    else:
                        return redirect('/')
        # Fallback: redirect to homepage
        if request.session.get('kids_mode', False):
            return redirect('/kids/')
        else:
            return redirect('/')
    return redirect('/')
def memory_match(request):
    return render(request, 'users/memory_match.html')
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
@csrf_exempt
def dart_throw(request):
    # Only allow game to load if user is eligible for a new attempt
    error_message = None
    wait_time = None
    attempts_list = []
    if request.user.is_authenticated:
        from django.utils import timezone
        from users.models import GameAttempt
        now = timezone.now()
        # Count all attempts for today (score >= 0)
        today_attempts = GameAttempt.objects.filter(user=request.user, game='dart_throw', attempted_at__date=now.date()).order_by('-attempted_at')
        attempt_count = today_attempts.count()
        attempts_list = list(today_attempts.values_list('attempted_at', flat=True))
        if attempt_count >= 3:
            error_message = 'You can only play Dart Throw 3 times per day.'
        elif attempt_count > 0:
            last_attempt = today_attempts.first().attempted_at
            seconds_since_last = (now - last_attempt).total_seconds()
            if seconds_since_last < 8 * 3600:
                seconds_left = 8 * 3600 - seconds_since_last
                hours = int(seconds_left // 3600)
                minutes = int((seconds_left % 3600) // 60)
                error_message = 'You must wait 8 hours for your next Dart Throw attempt.'
                wait_time = f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
        # Only create a new attempt if eligible and not already created for this session
        if not error_message:
            # If no attempts today, or last attempt was more than 8 hours ago
            if attempt_count == 0 or (attempt_count > 0 and seconds_since_last >= 8 * 3600):
                # Check if last attempt is score=0 and was just created (avoid duplicate on reload)
                if attempt_count == 0 or today_attempts.first().score != 0:
                    GameAttempt.objects.create(user=request.user, game='dart_throw', score=0)
                    # Refresh attempts after creation
                    today_attempts = GameAttempt.objects.filter(user=request.user, game='dart_throw', attempted_at__date=now.date()).order_by('-attempted_at')
                    attempt_count = today_attempts.count()
                    attempts_list = list(today_attempts.values_list('attempted_at', flat=True))
    attempt_count = len(attempts_list) if attempts_list else 0
    return render(request, 'users/dart_throw.html', {
        'error_message': error_message,
        'wait_time': wait_time,
        'attempts_list': attempts_list,
        'attempt_count': attempt_count
    })
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def update_coins(request):
    if request.method == 'POST' and request.user.is_authenticated:
        from django.utils import timezone
        from users.models import UserProfile, GameAttempt
        import logging
        logger = logging.getLogger('dart_throw_debug')
        now = timezone.now()
        # Only count attempts that have coins > 0 (i.e., completed games)
        today_attempts = GameAttempt.objects.filter(user=request.user, game='dart_throw', attempted_at__date=now.date(), score__gt=0).order_by('-attempted_at')
        attempt_count = today_attempts.count()
        logger.info(f"[DART THROW] User: {request.user.username}, Attempts today: {attempt_count}, POST coins: {request.POST.get('coins')}")
        if attempt_count >= 3:
            logger.warning(f"[DART THROW] User {request.user.username} blocked: 3 attempts reached.")
            error_message = 'You can only play Dart Throw 3 times per day.'
            return render(request, 'users/quiz_error.html', {'error_message': error_message, 'wait_time': None})
        elif attempt_count > 0:
            last_attempt = today_attempts.first().attempted_at
            seconds_since_last = (now - last_attempt).total_seconds()
            logger.info(f"[DART THROW] User {request.user.username} last attempt: {last_attempt}, seconds since: {seconds_since_last}")
            if seconds_since_last < 8 * 3600:
                seconds_left = 8 * 3600 - seconds_since_last
                hours = int(seconds_left // 3600)
                minutes = int((seconds_left % 3600) // 60)
                error_message = 'You must wait 8 hours for your next Dart Throw attempt.'
                wait_time = f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
                logger.warning(f"[DART THROW] User {request.user.username} blocked: must wait {wait_time}.")
                return render(request, 'users/quiz_error.html', {'error_message': error_message, 'wait_time': wait_time})
        coins = int(request.POST.get('coins', 0))
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.coins += coins
        profile.save()
        ga = GameAttempt.objects.create(user=request.user, game='dart_throw', score=coins)
        logger.info(f"[DART THROW] GameAttempt created for user {request.user.username}: score={coins}, attempted_at={ga.attempted_at}")
        # Redirect to leaderboard after successful attempt
        from django.shortcuts import redirect
        return redirect('/users/leaderboard/')
def leaderboard(request):
    from users.models import UserProfile
    top_users = UserProfile.objects.select_related('user').order_by('-coins')[:20]
    return render(request, 'users/leaderboard.html', {'leaderboard': top_users})
from django.utils import timezone
from users.models import GameAttempt
from django.shortcuts import render
def scratch_card(request):
    import random
    reward = None
    if request.method == 'POST':
        rewards = ['Free Ticket', '50% Off', 'Popcorn Combo']
        reward = random.choice(rewards)
        if request.user.is_authenticated:
            from users.models import Leaderboard, LoyaltyPoint, UserProfile
            GameAttempt.objects.create(user=request.user, game='scratch_card', score=1)
            leaderboard, _ = Leaderboard.objects.get_or_create(user=request.user)
            leaderboard.total_score += 1
            leaderboard.save()
            loyalty, _ = LoyaltyPoint.objects.get_or_create(user=request.user)
            loyalty.points += 10
            loyalty.save()
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.coins += 5
            profile.save()
    else:
        # Always set a reward for GET requests for demo/testing
        reward = random.choice(['Free Ticket', '50% Off', 'Popcorn Combo', 'Movie Merchandise'])
    return render(request, 'users/scratch_card.html', {'reward': reward})
def games(request):
    return render(request, 'users/games.html')
def spin_wheel(request):
    if request.user.is_authenticated:
        from users.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.coins += 3
        profile.save()
    return render(request, 'users/spin_wheel.html')
def box_office_prediction(request):
    actual_collection = 157  # Example: Avengers Endgame opening weekend in India (crores)
    result = None
    if request.method == 'POST':
        try:
            prediction = float(request.POST.get('prediction', 0))
            diff = abs(prediction - actual_collection)
            if diff <= 10:
                result = f"Excellent! Your prediction was very close. Actual: {actual_collection} crores."
            elif diff <= 25:
                result = f"Good try! Actual collection was {actual_collection} crores."
            else:
                result = f"Keep trying! Actual collection was {actual_collection} crores."
        except ValueError:
            result = "Please enter a valid number."
    # Daily Challenge: reward can be coins or other items
    if request.method == 'POST' and request.user.is_authenticated:
        from users.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        import random
        possible_rewards = [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Snack Coupon', 'Badge', 'Discount']
        reward = random.choice(possible_rewards)
        if isinstance(reward, int) and reward > 0:
            profile.coins += reward
            profile.save()
        # Optionally, pass reward to template for display
    return render(request, 'users/box_office_prediction.html', {'result': result})
def emoji_guess(request):
    emoji = "🎬🦁👑"  # The Lion King
    result = None
    if request.method == 'POST':
        answer = request.POST.get('answer', '').strip().lower()
        if answer in ['the lion king', 'lion king']:
            result = "Correct! It's The Lion King."
        else:
            result = "Try again!"
    # Daily Challenge: reward can be coins or other items
    if request.user.is_authenticated:
        from users.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        import random
        possible_rewards = [2, 0, 0, 0, 0, 0, 'Snack Coupon', 'Badge', 'Discount']
        reward = random.choice(possible_rewards)
        if isinstance(reward, int) and reward > 0:
            profile.coins += reward
            profile.save()
    return render(request, 'users/emoji_guess.html', {'result': result})

def movie_trivia(request):
    pass
# Movie Quiz Game View
 # ...removed stray import...

def movie_quiz(request):
    from django.utils import timezone
    from django.shortcuts import redirect
    from django.contrib import messages
    from users.models import GameAttempt, Leaderboard
    if request.user.is_authenticated:
        now = timezone.now()
        today_attempts = GameAttempt.objects.filter(user=request.user, game='movie_quiz', attempted_at__date=now.date()).order_by('-attempted_at')
        if today_attempts.count() >= 3:
            error_message = 'You can only attempt the Movie Quiz 3 times per day.'
            return render(request, 'users/quiz_error.html', {'error_message': error_message, 'wait_time': None})
        if today_attempts.exists():
            last_attempt = today_attempts.first().attempted_at
            seconds_left = 8 * 3600 - (now - last_attempt).total_seconds()
            if seconds_left > 0:
                hours = int(seconds_left // 3600)
                minutes = int((seconds_left % 3600) // 60)
                error_message = 'You must wait 8 hours between quiz attempts.'
                wait_time = f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
                return render(request, 'users/quiz_error.html', {'error_message': error_message, 'wait_time': wait_time})
    import random
    # ...removed movie quiz view...
from django.shortcuts import redirect, get_object_or_404
from .models import UserProfile

# Referral invite view
def invite_referral(request, referral_code):
    # Store referral code in session
    request.session['referral_code'] = referral_code
    # Optionally, you can show a landing page here
    return redirect('register')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
@login_required
def share_and_earn(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    gifts = GiftedTicket.objects.filter(recipient_email=request.user.email, accepted=True).order_by('-sent_at')
    userprofile = getattr(request.user, 'userprofile', None)
    return render(request, 'users/share_and_earn.html', {
        'bookings': bookings,
        'gifts': gifts,
        'userprofile': userprofile,
    })
# Social sharing endpoint
from django.contrib import messages
@login_required
def award_share_points(request):
    if request.method == 'POST':
        from users.models import LoyaltyPoint
        loyalty, _ = LoyaltyPoint.objects.get_or_create(user=request.user)
        loyalty.points += 3
        loyalty.save()
        messages.success(request, f'You earned 3 loyalty points for sharing! Total points: {loyalty.points}')
        return redirect('share_and_earn')
    return redirect('share_and_earn')
from .models import UserProfile
from django.contrib import messages
from .forms import UserEditForm, UserProfileForm
from .forms import UserProfileForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
 # ...removed movies app import...
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings

def home(request):
    # ...removed movies queryset...
    if request.user.is_authenticated:
        from users.models import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        # Reset kids_mode session variable based on user type
        if hasattr(profile, 'user_type') and profile.user_type == 'kid':
            request.session['kids_mode'] = True
            from django.shortcuts import redirect
            return redirect('kids_home')
        else:
            request.session['kids_mode'] = False
    # Always return a response
    return render(request, 'home.html')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            if not user_type:
                user_type = 'normal'
            from users.models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.user_type = user_type
            profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Award referral points if referral_code in session
            referral_code = request.session.get('referral_code')
            if referral_code:
                ref_profile = UserProfile.objects.filter(referral_code=referral_code).first()
                if ref_profile:
                    from users.models import LoyaltyPoint
                    loyalty, _ = LoyaltyPoint.objects.get_or_create(user=ref_profile.user)
                    loyalty.points += 20
                    loyalty.save()
                    # Optionally, clear referral_code from session
                    del request.session['referral_code']
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_login_redirect')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    from users.models import LoyaltyPoint
    loyalty, _ = LoyaltyPoint.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserEditForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # Award loyalty points for first profile completion
            from users.models import LoyaltyPoint
            loyalty, _ = LoyaltyPoint.objects.get_or_create(user=request.user)
            if loyalty.points == 0:
                loyalty.points += 10
                loyalty.save()
                messages.success(request, 'Profile updated! You earned 10 loyalty points for completing your profile.')
            else:
                messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        u_form = UserEditForm(instance=request.user)
        p_form = UserProfileForm(instance=profile)
    return render(request, 'users/profile.html', {'u_form': u_form, 'form': p_form, 'loyalty_points': loyalty.points, 'profile': profile})
    bookings= Booking.objects.filter(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'u_form': u_form,'bookings':bookings})

@login_required
def reset_password(request):
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'users/reset_password.html',{'form':form})

@login_required
def my_bookings(request):
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related('movie', 'show')
        .prefetch_related('seats')
        .order_by('-booked_at')
    )
    return render(request, 'users/my_bookings.html', {'bookings': bookings})

@login_required
def view_ticket(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        # Check if user is recipient of a GiftedTicket for this booking
        gifted = GiftedTicket.objects.filter(booking_id=booking_id, recipient_email=request.user.email, accepted=True).first()
        if not gifted:
            from django.http import Http404
            raise Http404("No Booking matches the given query.")
        booking = gifted.booking
    return render(request, 'users/view_ticket.html', {'booking': booking})

@login_required
def my_gifts(request):
    gifts = GiftedTicket.objects.filter(recipient_email=request.user.email).select_related('booking', 'sender').order_by('-sent_at')
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'users/my_gifts.html', {'gifts': gifts, 'bookings': bookings})

@login_required
def gift_settings(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        mode = request.POST.get('accept_gifts', 'auto')
        if mode == 'auto':
            profile.accept_gifts = True
            profile.gift_permission_mode = 'auto'
        elif mode == 'with_permission':
            profile.accept_gifts = True
            profile.gift_permission_mode = 'with_permission'
        else:
            profile.accept_gifts = False
            profile.gift_permission_mode = 'auto'
        profile.save()
        messages.success(request, 'Gift settings updated!')
        return redirect('gift_settings')
    # For display, set selected_mode
    if not profile.accept_gifts:
        selected_mode = 'no'
    else:
        selected_mode = profile.gift_permission_mode
    return render(request, 'users/gift_settings.html', {
        'selected_mode': selected_mode
    })

def gift_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        # Check recipient's gift acceptance
        try:
            recipient_profile = UserProfile.objects.get(user__email=recipient_email)
            if not recipient_profile.accept_gifts:
                # Optionally, show a message or redirect
                return render(request, 'users/view_ticket.html', {
                    'booking': booking,
                    'gift_error': 'Recipient is not accepting gifts at this time.'
                })
        except UserProfile.DoesNotExist:
            pass  # Allow gifting to non-registered emails
        # ...existing code for gifting...
        recipient_name = request.POST.get('recipient_name')
        message = request.POST.get('message')
        unique_code = get_random_string(32)
        gift = GiftedTicket.objects.create(
            booking=booking,
            sender=request.user,
            recipient_name=recipient_name,
            recipient_email=recipient_email,
            message=message,
            unique_code=unique_code
        )
        send_mail(
            subject=f"You've received a movie ticket gift!",
            message=f"Hi {recipient_name},\n\n{request.user.username} has gifted you a movie ticket for {booking.movie.name}.\nMessage: {message}\nView your ticket: {request.build_absolute_uri('/gifts/')}",
            from_email=None,
            recipient_list=[recipient_email],
            fail_silently=True,
        )
        return redirect('view_ticket', booking_id=booking.id)
    return redirect('view_ticket', booking_id=booking.id)

@csrf_exempt
@login_required
def send_gift(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        recipient_name = request.POST.get('recipient_name')
        recipient_email = request.POST.get('recipient_email')
        message = request.POST.get('message')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        try:
            recipient_profile = UserProfile.objects.get(user__email=recipient_email)
            if not recipient_profile.accept_gifts:
                return render(request, 'users/my_gifts.html', {
                    'gifts': GiftedTicket.objects.filter(recipient_email=request.user.email),
                    'bookings': Booking.objects.filter(user=request.user),
                    'gift_error': 'Recipient is not accepting gifts at this time.'
                })
            if recipient_profile.gift_permission_mode == 'with_permission':
                accepted = False
            else:
                accepted = True
            recipient_mobile = recipient_profile.mobile_number
        except UserProfile.DoesNotExist:
            accepted = True
            recipient_mobile = None
        unique_code = get_random_string(32)
        gift = GiftedTicket.objects.create(
            booking=booking,
            sender=request.user,
            recipient_name=recipient_name,
            recipient_email=recipient_email,
            message=message,
            unique_code=unique_code,
            accepted=accepted
        )
        # Send notification email and SMS for permission
        sms_body = None
        if not accepted:
            send_mail(
                subject=f"Gift acceptance required!",
                message=f"Hi {recipient_name},\n\n{request.user.username} wants to gift you a movie ticket for {booking.movie.name}.\nMessage: {message}\nPlease log in and accept the gift in your Gifts section.",
                from_email=None,
                recipient_list=[recipient_email],
                fail_silently=True,
            )
            if recipient_mobile:
                sms_body = f"{request.user.username} wants to gift you a ticket for {booking.movie.name}. Please log in and accept the gift in your Gifts section."
        else:
            send_mail(
                subject=f"You've received a movie ticket gift!",
                message=f"Hi {recipient_name},\n\n{request.user.username} has gifted you a movie ticket for {booking.movie.name}.\nMessage: {message}\nView your ticket: {request.build_absolute_uri('/gifts/')}",
                from_email=None,
                recipient_list=[recipient_email],
                fail_silently=True,
            )
            if recipient_mobile:
                sms_body = f"{request.user.username} has gifted you a ticket for {booking.movie.name}. View your ticket in your Gifts section."
        # Send SMS if mobile number and Twilio settings are available
        if sms_body and recipient_mobile and settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_PHONE_NUMBER:
            try:
                # ...removed movies.views import...
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                client.messages.create(
                    body=sms_body,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=recipient_mobile
                )
            except Exception as e:
                print(f"Twilio SMS error for gift notification: {e}")
        return redirect('my_gifts')
    return redirect('my_gifts')

@login_required
def accept_gift(request, gift_id):
    gift = get_object_or_404(GiftedTicket, id=gift_id, recipient_email=request.user.email)
    if request.method == 'POST' and not gift.accepted:
        gift.accepted = True
        gift.accepted_at = timezone.now()
        gift.save()
    return redirect('my_gifts')
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
@require_POST
def update_coins(request):
    coins = int(request.POST.get('coins', 0))
    user_profile = request.user.userprofile
    user_profile.coins += coins  # Add to current coins
    user_profile.save()
    return redirect('leaderboard')
def music_lounge(request):
    return render(request, 'users/music.html')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MusicTrackUploadForm
from .models import MusicTrack

@login_required
def upload_music(request):
    if request.method == 'POST':
        form = MusicTrackUploadForm(request.POST, request.FILES)
        if form.is_valid():
            music = form.save(commit=False)
            music.owner = request.user
            music.save()
            return redirect('music-upload')
    else:
        form = MusicTrackUploadForm()
    user_tracks = MusicTrack.objects.filter(owner=request.user)
    return render(request, 'users/music_upload.html', {'form': form, 'user_tracks': user_tracks})

def music_lounge(request):
    from django.core.cache import cache
    user_tracks = MusicTrack.objects.filter(owner=request.user) if request.user.is_authenticated else []
    query = request.GET.get('query')
    import os
    from googleapiclient.discovery import build
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []
    # Cache YouTube search results for 6 hours
    if query:
        cache_key = f'youtube_search_{query}'
        videos = cache.get(cache_key)
        if videos is None:
            try:
                search_response = youtube.search().list(
                    q=query,
                    part='id,snippet',
                    maxResults=15,
                    type='video'
                ).execute()
                video_ids = [item['id']['videoId'] for item in search_response.get('items', []) if item.get('id', {}).get('videoId')]
                videos = []
                if video_ids:
                    video_details = youtube.videos().list(
                        part='status,snippet,contentDetails',
                        id=','.join(video_ids)
                    ).execute()
                    for item in video_details.get('items', []):
                        status = item.get('status', {})
                        privacy = status.get('privacyStatus')
                        upload_status = status.get('uploadStatus')
                        content_details = item.get('contentDetails', {})
                        embeddable = content_details.get('embeddable', True)
                        if privacy == 'public' and upload_status == 'processed' and embeddable:
                            videos.append({
                                'id': item['id'],
                                'title': item['snippet']['title']
                            })
                cache.set(cache_key, videos, 6*60*60)
            except Exception as e:
                videos = []
    # Cache popular Tamil songs for 6 hours
    tamil_cache_key = 'popular_tamil_songs'
    popular_tamil_songs = cache.get(tamil_cache_key)
    if popular_tamil_songs is None:
        try:
            tamil_response = youtube.search().list(
                q='popular tamil songs',
                part='id,snippet',
                maxResults=15,
                type='video',
                regionCode='IN'
            ).execute()
            tamil_video_ids = [item['id']['videoId'] for item in tamil_response.get('items', []) if item.get('id', {}).get('videoId')]
            popular_tamil_songs = []
            if tamil_video_ids:
                tamil_video_details = youtube.videos().list(
                    part='status,snippet,contentDetails',
                    id=','.join(tamil_video_ids)
                ).execute()
                for item in tamil_video_details.get('items', []):
                    status = item.get('status', {})
                    privacy = status.get('privacyStatus')
                    upload_status = status.get('uploadStatus')
                    content_details = item.get('contentDetails', {})
                    embeddable = content_details.get('embeddable', True)
                    if privacy == 'public' and upload_status == 'processed' and embeddable:
                        popular_tamil_songs.append({
                            'id': item['id'],
                            'title': item['snippet']['title'],
                            'thumbnail': item['snippet']['thumbnails']['medium']['url']
                        })
            cache.set(tamil_cache_key, popular_tamil_songs, 6*60*60)
        except Exception as e:
            popular_tamil_songs = []
    return render(request, 'users/music.html', {'user_tracks': user_tracks, 'videos': videos, 'popular_tamil_songs': popular_tamil_songs})