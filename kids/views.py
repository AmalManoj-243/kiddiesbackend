from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

@login_required
@csrf_protect
def complete_phonics_quiz(request, lesson_id):
    if request.method == 'POST':
        from .models import Lesson, LessonCompletion
        lesson = Lesson.objects.get(id=lesson_id)
        completion, created = LessonCompletion.objects.get_or_create(user=request.user, lesson=lesson)
        completion.completed_quiz = True
        completion.save()
        print(f"[DEBUG] PhonicsCompletion: user={request.user.id}, lesson={lesson.id}, completed_quiz={completion.completed_quiz}, created={created}")
        return redirect('lesson_detail', lesson_id=lesson.id)
    return redirect('lesson_detail', lesson_id=lesson_id)
def snakes_ladders_player_select(request):
    return render(request, 'kids/snakes_ladders_player_select.html')
def snakes_ladders_mode(request):
    return render(request, 'kids/snakes_ladders_mode.html')
def snakes_ladders_start(request):
    return render(request, 'kids/snakes_ladders_start.html')
def entertainment_snakes_ladders(request):
    return render(request, 'kids/entertainment_snakes_ladders.html')
def start_highscore(request):
    return render(request, 'kids/start_highscore.html')
def level_select(request):
    return render(request, 'kids/level_select.html')
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
# Mark alphabet quiz as complete for the user
@login_required
@csrf_protect
def complete_alphabet_quiz(request, lesson_id):
    if request.method == 'POST':
        from .models import Lesson, LessonCompletion
        lesson = Lesson.objects.get(id=lesson_id)
        completion, created = LessonCompletion.objects.get_or_create(user=request.user, lesson=lesson)
        completion.completed_quiz = True
        completion.save()
        print(f"[DEBUG] LessonCompletion: user={request.user.id}, lesson={lesson.id}, completed_quiz={completion.completed_quiz}, created={created}")
        # Redirect to lesson detail page (or course detail)
        return redirect('lesson_detail', lesson_id=lesson.id)
    return redirect('lesson_detail', lesson_id=lesson_id)
def lesson_alphabet_quiz(request, lesson_id):
    from .models import Lesson
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'kids/lessons/alphabet_quiz.html', {'lesson': lesson})

def alphabet_quiz(request):
    from .models import Lesson
    # Try to get lesson_id from GET params
    lesson_id = request.GET.get('lesson_id')
    lesson = None
    if lesson_id:
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            lesson = Lesson.objects.filter(lesson_type='alphabet').first()
    else:
        lesson = Lesson.objects.filter(lesson_type='alphabet').first()
    return render(request, 'kids/lessons/alphabet_quiz.html', {'lesson': lesson})

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Fill in the Blank Test Page
@login_required
def fill_blank_test(request, lesson_id):
    from .models import Lesson
    lesson = get_object_or_404(Lesson, id=lesson_id)
    # Use the same sentences as the simple sentences lesson
    import re
    class StaticSentence:
        def __init__(self, text):
            clean_text = re.sub(r'[^a-zA-Z ]', '', text)
            self.text = clean_text
            self.words = clean_text.split()
    sentence_pool = [
        'The monkey swings from the tree',
        'A rocket flies to the moon',
        'The chef bakes a yummy cake',
        'The puppy digs in the sand',
        'A rainbow appears after rain',
        'The robot can dance and sing',
        'The princess wears a golden crown',
        'The pirate finds a treasure chest',
        'The elephant splashes water',
        'The wizard casts a magic spell',
        'The astronaut floats in space',
        'The dragon breathes fire',
        'The clown juggles three balls',
        'The farmer plants seeds in spring',
        'The squirrel hides a nut',
        'The artist paints a bright picture',
        'The teacher reads a story',
        'The lion roars loudly',
        'The mouse runs into a hole',
        'The fox jumps over the fence',
        'The bee buzzes near the flower',
        'The turtle walks slowly',
        'The boy builds a tall tower',
        'The girl skips with a rope',
        'The fish swims in the pond',
        'The car drives down the road',
        'The bird pecks at the seed',
        'The baby laughs and claps',
        'The snowman wears a red scarf',
        'The frog leaps into the water',
        'The horse gallops fast',
        'The chef stirs the soup',
        'The owl hoots at night',
        'The child blows bubbles',
        'The duck waddles to the lake',
        'The star twinkles in the sky',
        'The apple falls from the tree',
        'The rabbit eats a carrot',
        'The dog catches the ball',
        'The cat naps on the sofa',
        'The girl draws a rainbow',
        'The boy rides his bike',
        'The sun rises in the morning',
        'The moon glows at night',
        'The flower blooms in spring',
        'The bear hugs its cub',
        'The penguin slides on ice',
        'The king sits on his throne',
        'The queen waves to the crowd',
    ]
    import random
    selected_texts = random.sample(sentence_pool, 25)
    sentences = [StaticSentence(text) for text in selected_texts]
    # Pass sentences to JS via context
    return render(request, 'kids/lessons/fill_blank_test.html', {
        'lesson': lesson,
        'blank_sentences': [s.text for s in sentences],
    })
def blending_sounds_lesson(request):
    return render(request, 'kids/lessons/blending_sounds_lesson.html')

def blending_sounds_quiz_game(request):
    return render(request, 'kids/lessons/blending_sounds_quiz_game.html')
def phonics_quiz_game(request):
    # Renders the interactive phonics quiz game template
    from .models import Lesson
    lesson = Lesson.objects.filter(lesson_type='phonics').first()
    return render(request, 'kids/phonics_quiz_game.html', {'lesson': lesson})
def phonics_quiz(request):
    # Simple placeholder view for phonics quiz
    return render(request, 'kids/phonics_quiz.html', {})
def shape_matching_game(request):
    return render(request, 'kids/shape_matching_game.html')
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Drawing, AgeGroup, Subject, Course, Lesson, KidsMovie, Story, LessonCompletion
from .forms import DrawingForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods

@login_required
def performance(request):
    # Get all courses student is enrolled in
    userprofile = getattr(request.user, 'userprofile', None)
    courses = userprofile.courses.all() if userprofile else []
    selected_course_id = request.GET.get('course')
    selected_course = None
    if selected_course_id:
        try:
            selected_course = courses.get(id=selected_course_id)
        except Exception:
            selected_course = None
    # Filter drawings by course
    drawings = Drawing.objects.filter(user=request.user)
    if selected_course:
        drawings = drawings.filter(lesson__course=selected_course)
    total_drawings = drawings.count()
    graded_drawings = drawings.exclude(mark__isnull=True).exclude(mark__exact='')
    grades = [d.mark for d in graded_drawings]
    feedbacks = [d.feedback for d in graded_drawings if d.feedback]
    # Aggregate quiz/game scores
    from users.models import GameAttempt, Leaderboard
    game_attempts = GameAttempt.objects.filter(user=request.user)
    if selected_course:
        game_attempts = game_attempts.filter(game__icontains=selected_course.name.lower().replace(' ', '_'))
    total_game_score = sum([a.score for a in game_attempts])
    leaderboard_score = None
    try:
        leaderboard_score = Leaderboard.objects.get(user=request.user).total_score
    except Leaderboard.DoesNotExist:
        leaderboard_score = 0
    return render(request, 'kids/performance.html', {
        'courses': courses,
        'selected_course': selected_course,
        'drawings': drawings,
        'total_drawings': total_drawings,
        'grades': grades,
        'feedbacks': feedbacks,
        'game_attempts': game_attempts,
        'total_game_score': total_game_score,
        'leaderboard_score': leaderboard_score,
    })

# Teacher dashboard: list lessons and link to marking galleries
@login_required
def teacher_dashboard(request):
    # Only allow teachers (user_type == 'teacher')
    # Removed teacher user logic
    lessons = Lesson.objects.all().order_by('course__name', 'order')
    return render(request, 'kids/teacher_dashboard.html', {'lessons': lessons})

# Upload drawing for a lesson
@login_required
def upload_drawing(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.method == 'POST':
        form = DrawingForm(request.POST, request.FILES)
        if form.is_valid():
            drawing = form.save(commit=False)
            drawing.user = request.user
            drawing.lesson = lesson
            drawing.save()
            return HttpResponseRedirect(reverse('drawing_gallery', args=[lesson_id]))
    else:
        form = DrawingForm()
    return render(request, 'kids/upload_drawing.html', {'form': form, 'lesson': lesson})

# Kids' gallery: show only their own drawings for a lesson
@login_required
def drawing_gallery(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    drawings = Drawing.objects.filter(lesson=lesson, user=request.user).order_by('-uploaded_at')
    return render(request, 'kids/drawing_gallery.html', {'drawings': drawings, 'lesson': lesson})

# Teacher gallery: show all drawings for a lesson, allow marking/feedback
@login_required
def teacher_drawing_gallery(request, lesson_id):
    # Only allow teachers (user_type == 'teacher')
    # Removed teacher user logic
    lesson = Lesson.objects.get(id=lesson_id)
    if request.method == 'POST':
        drawing_id = request.POST.get('drawing_id')
        mark = request.POST.get('mark')
        feedback = request.POST.get('feedback')
        if drawing_id:
            try:
                drawing = Drawing.objects.get(id=drawing_id, lesson=lesson)
                drawing.mark = mark
                drawing.feedback = feedback
                drawing.save()
            except Drawing.DoesNotExist:
                pass
    drawings = Drawing.objects.filter(lesson=lesson).order_by('-uploaded_at')
    return render(request, 'kids/teacher_drawing_gallery.html', {'drawings': drawings, 'lesson': lesson})

def lesson_by_order(request, order):
    from .models import Lesson, QuizQuestion
    import random
    try:
        lesson = Lesson.objects.select_related('course').get(order=order)
    except Lesson.DoesNotExist:
        return render(request, 'kids/lesson_not_found.html', {})
    quiz_questions = list(QuizQuestion.objects.filter(lesson=lesson))
    random_question = random.choice(quiz_questions) if quiz_questions else None
    video_embed_url = ""
    if lesson.video_url:
        if "youtu.be/" in lesson.video_url:
            video_embed_url = lesson.video_url.replace("https://youtu.be/", "https://www.youtube.com/embed/")
        elif "youtube.com/watch?v=" in lesson.video_url:
            video_embed_url = lesson.video_url.replace("watch?v=", "embed/")
        else:
            video_embed_url = lesson.video_url

    # Group shape images by label for shapes lesson
    shape_images_by_label = {}
    if lesson.order == 2:
        for img in lesson.lesson_images.all():
            if img.image_type == "shape":
                shape_images_by_label.setdefault(img.label, []).append(img)
        template_name = 'kids/lessons/shape_lesson_detail.html'
    else:
        template_name = 'kids/lesson_detail.html'

    # Get stories for this lesson, filtered by type
    stories = lesson.stories.all().order_by('-created_at')
    return render(request, template_name, {
        'lesson': lesson,
        'quiz_question': random_question,
        'video_embed_url': video_embed_url,
        'shape_images_by_label': shape_images_by_label,
        'stories': stories,
    })
# Lesson detail view for rich lesson modules
@login_required
def lesson_detail(request, lesson_id):
    from kids.models import LessonCompletion
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    userprofile = getattr(request.user, 'kids_userprofile', None)
    if userprofile is None:
        from kids.models import UserProfile
        userprofile, created = UserProfile.objects.get_or_create(user=request.user)
    enrolled = course in userprofile.courses.all()
    if not enrolled:
        return redirect('course_detail', course_id=course.id)
    completion = LessonCompletion.objects.filter(user=request.user, lesson=lesson).first()
    video_embed_url = ""
    if lesson.video_url:
        if "youtu.be/" in lesson.video_url:
            video_embed_url = lesson.video_url.replace("https://youtu.be/", "https://www.youtube.com/embed/")
        elif "youtube.com/watch?v=" in lesson.video_url:
            video_embed_url = lesson.video_url.replace("watch?v=", "embed/")
        else:
            video_embed_url = lesson.video_url
    # Find next lesson in the course
    next_lesson = Lesson.objects.filter(course=course, order__gt=lesson.order).order_by('order').first()
    # Choose template based on lesson type
    if lesson.lesson_type == 'alphabet':
        # ...existing code for alphabet lesson...
        alphabet_words = {
            'A': 'Apple', 'B': 'Ball', 'C': 'Cat', 'D': 'Dog', 'E': 'Elephant', 'F': 'Fish', 'G': 'Goat',
            'H': 'Hat', 'I': 'Icecream', 'J': 'Jug', 'K': 'Kite', 'L': 'Lion', 'M': 'Monkey', 'N': 'Nest',
            'O': 'Orange', 'P': 'Pig', 'Q': 'Queen', 'R': 'Rabbit', 'S': 'Sun', 'T': 'Tiger', 'U': 'Umbrella',
            'V': 'Violin', 'W': 'Wolf', 'X': 'Xylophone', 'Y': 'Yak', 'Z': 'Zebra'
        }
        alphabet_images = {
            'A': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756897998/media/movies/i4oczrducxr2t5qbrbfu.png',
            'B': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898010/media/movies/i1fqxpcn3bldkw8ulsio.webp',
            'C': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898005/media/movies/x3agqhuwtfagt68hanwd.png',
            'D': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898011/media/movies/o7hrufhngj8f9hxsajsj.jpg',
            'E': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898011/media/movies/s9ctpql1wycxwbsj4lpq.avif',
            'F': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898027/media/movies/zbf0yrgo0zy9rqcfyn48.webp',
            'G': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898018/media/movies/yi4fm9p514fad7rezunq.jpg',
            'H': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898019/media/movies/tlkkyxbmxhbu6qzu7qfj.jpg',
            'I': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898021/media/movies/wy537j26inkld2p6b5x2.png',
            'J': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898023/media/movies/bh3vnwskzqulfnqckxam.avif',
            'K': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898023/media/movies/cn28mvhevguscg0vjntf.png',
            'L': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898025/media/movies/iuo7nebclrypfzqdcrsa.webp',
            'M': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898025/media/movies/lpgdyr3vsirvaiw14vrc.jpg',
            'N': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898000/media/movies/mpnm1aus5ya5tfh0pq36.avif',
            'O': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898027/media/movies/mecsar9knhpbcc3mdllu.webp',
            'P': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898030/media/movies/xzjqurvs0wljhrtshyfk.png',
            'Q': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898033/media/movies/ntoskuxdsc5xylvehhxd.jpg',
            'R': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898031/media/movies/skkshefanbml3rmqnsva.png',
            'S': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898003/media/movies/bc6pvssiund7iqo9xnpv.jpg',
            'T': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898035/media/movies/t8wetww5upa60dxjaw0c.jpg',
            'U': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898044/media/movies/cuwl7lb0mc2o7dg6rqql.jpg',
            'V': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898044/media/movies/eobgwabd9sc7bqctlkfz.avif',
            'W': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898012/media/movies/yquxjntuydpmftb3yaqc.avif',
            'X': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898040/media/movies/hh9rp22seid9kpdhp8pd.jpg',
            'Y': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898013/media/movies/pxxebjccqxidetww4oke.jpg',
            'Z': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898014/media/movies/likwz6y1fn3jj3kxzbjw.jpg',
        }
        template_name = 'kids/lessons/alphabet_lesson_detail.html'
        lesson_videos = []
        for video in lesson.videos.all().order_by('order'):
            url = video.video_url
            embed_url = url
            if url:
                if 'youtu.be/' in url:
                    embed_url = url.replace('https://youtu.be/', 'https://www.youtube.com/embed/')
                elif 'youtube.com/watch?v=' in url:
                    embed_url = url.replace('watch?v=', 'embed/')
            video.video_embed_url = embed_url
            lesson_videos.append(video)
        return render(request, template_name, {
            'lesson': lesson,
            'completion': completion,
            'video_embed_url': video_embed_url,
            'next_lesson': next_lesson,
            'alphabet_words': alphabet_words,
            'alphabet_images': alphabet_images,
            'lesson_videos': lesson_videos,
        })
    elif lesson.lesson_type == 'words':
        # Render the Simple Words lesson template
        template_name = 'kids/lessons/simple_words_lesson.html'
        return render(request, template_name, {
            'lesson': lesson,
            'completion': completion,
            'video_embed_url': video_embed_url,
            'next_lesson': next_lesson,
        })
    elif lesson.lesson_type == 'blending':
        # Render the Blending Sounds & Word Building lesson template
        template_name = 'kids/lessons/blending_sounds_lesson.html'
        return render(request, template_name, {
            'lesson': lesson,
            'completion': completion,
            'video_embed_url': video_embed_url,
            'next_lesson': next_lesson,
        })
    elif lesson.lesson_type == 'simple_sentences':
        # Render the Simple Sentences lesson template with static sentences and word list
        import re
        class StaticSentence:
            def __init__(self, text, image=None):
                # Remove all non-alphabetic characters except spaces for display and game
                clean_text = re.sub(r'[^a-zA-Z ]', '', text)
                self.text = clean_text
                self.words = clean_text.split()
                self.image = None
        import random
        sentence_pool = [
            'The monkey swings from the tree',
            'A rocket flies to the moon',
            'The chef bakes a yummy cake',
            'The puppy digs in the sand',
            'A rainbow appears after rain',
            'The robot can dance and sing',
            'The princess wears a golden crown',
            'The pirate finds a treasure chest',
            'The elephant splashes water',
            'The wizard casts a magic spell',
            'The astronaut floats in space',
            'The dragon breathes fire',
            'The clown juggles three balls',
            'The farmer plants seeds in spring',
            'The squirrel hides a nut',
            'The artist paints a bright picture',
            'The teacher reads a story',
            'The lion roars loudly',
            'The mouse runs into a hole',
            'The fox jumps over the fence',
            'The bee buzzes near the flower',
            'The turtle walks slowly',
            'The boy builds a tall tower',
            'The girl skips with a rope',
            'The fish swims in the pond',
            'The car drives down the road',
            'The bird pecks at the seed',
            'The baby laughs and claps',
            'The snowman wears a red scarf',
            'The frog leaps into the water',
            'The horse gallops fast',
            'The chef stirs the soup',
            'The owl hoots at night',
            'The child blows bubbles',
            'The duck waddles to the lake',
            'The star twinkles in the sky',
            'The apple falls from the tree',
            'The rabbit eats a carrot',
            'The dog catches the ball',
            'The cat naps on the sofa',
            'The girl draws a rainbow',
            'The boy rides his bike',
            'The sun rises in the morning',
            'The moon glows at night',
            'The flower blooms in spring',
            'The bear hugs its cub',
            'The penguin slides on ice',
            'The king sits on his throne',
            'The queen waves to the crowd',
        ]
        selected_texts = random.sample(sentence_pool, 25)
        sentences = [StaticSentence(text) for text in selected_texts]
        template_name = 'kids/lessons/simple_sentences_lesson.html'
        return render(request, template_name, {
            'lesson': lesson,
            'completion': completion,
            'video_embed_url': video_embed_url,
            'next_lesson': next_lesson,
            'sentences': sentences,
        })
    elif lesson.lesson_type == 'sight_words':
        # Render the Sight Words lesson template
        template_name = 'kids/lessons/sight_words_lesson.html'
        return render(request, template_name, {
            'lesson': lesson,
            'completion': completion,
            'video_embed_url': video_embed_url,
            'next_lesson': next_lesson,
        })
    elif lesson.lesson_type == 'phonics' or lesson.order == 4:
        # Example context, replace with your actual phonics data
        phonics_sounds = {
            'A': 'a (as in apple)', 'B': 'b (as in ball)', 'C': 'k (as in cat)', 'D': 'd (as in dog)',
            'E': 'e (as in elephant)', 'F': 'f (as in fish)', 'G': 'g (as in goat)', 'H': 'h (as in hat)',
            'I': 'i (as in ice)', 'J': 'j (as in jug)', 'K': 'k (as in kite)', 'L': 'l (as in lion)',
            'M': 'm (as in monkey)', 'N': 'n (as in nest)', 'O': 'o (as in orange)', 'P': 'p (as in pig)',
            'Q': 'kw (as in queen)', 'R': 'r (as in rabbit)', 'S': 's (as in sun)', 'T': 't (as in tiger)',
            'U': 'u (as in umbrella)', 'V': 'v (as in violin)', 'W': 'w (as in wolf)', 'X': 'ks (as in xylophone)',
            'Y': 'y (as in yak)', 'Z': 'z (as in zebra)'
        }
        phonics_example_words = {
            'A': 'apple', 'B': 'ball', 'C': 'cat', 'D': 'dog',
            'E': 'elephant', 'F': 'fish', 'G': 'goat', 'H': 'hat',
            'I': 'ice', 'J': 'jug', 'K': 'kite', 'L': 'lion',
            'M': 'monkey', 'N': 'nest', 'O': 'orange', 'P': 'pig',
            'Q': 'queen', 'R': 'rabbit', 'S': 'sun', 'T': 'tiger',
            'U': 'umbrella', 'V': 'violin', 'W': 'wolf', 'X': 'xylophone',
            'Y': 'yak', 'Z': 'zebra'
        }
        phonics_images = {
            'A': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756897998/media/movies/i4oczrducxr2t5qbrbfu.png',
            'B': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898010/media/movies/i1fqxpcn3bldkw8ulsio.webp',
            'C': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898005/media/movies/x3agqhuwtfagt68hanwd.png',
            'D': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898011/media/movies/o7hrufhngj8f9hxsajsj.jpg',
            'E': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898011/media/movies/s9ctpql1wycxwbsj4lpq.avif',
            'F': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898027/media/movies/zbf0yrgo0zy9rqcfyn48.webp',
            'G': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898018/media/movies/yi4fm9p514fad7rezunq.jpg',
            'H': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898019/media/movies/tlkkyxbmxhbu6qzu7qfj.jpg',
            'I': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898021/media/movies/wy537j26inkld2p6b5x2.png',
            'J': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898023/media/movies/bh3vnwskzqulfnqckxam.avif',
            'K': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898023/media/movies/cn28mvhevguscg0vjntf.png',
            'L': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898025/media/movies/iuo7nebclrypfzqdcrsa.webp',
            'M': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898025/media/movies/lpgdyr3vsirvaiw14vrc.jpg',
            'N': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898000/media/movies/mpnm1aus5ya5tfh0pq36.avif',
            'O': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898027/media/movies/mecsar9knhpbcc3mdllu.webp',
            'P': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898030/media/movies/xzjqurvs0wljhrtshyfk.png',
            'Q': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898033/media/movies/ntoskuxdsc5xylvehhxd.jpg',
            'R': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898031/media/movies/skkshefanbml3rmqnsva.png',
            'S': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898003/media/movies/bc6pvssiund7iqo9xnpv.jpg',
            'T': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898035/media/movies/t8wetww5upa60dxjaw0c.jpg',
            'U': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898044/media/movies/cuwl7lb0mc2o7dg6rqql.jpg',
            'V': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898044/media/movies/eobgwabd9sc7bqctlkfz.avif',
            'W': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898012/media/movies/yquxjntuydpmftb3yaqc.avif',
            'X': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898040/media/movies/hh9rp22seid9kpdhp8pd.jpg',
            'Y': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898013/media/movies/pxxebjccqxidetww4oke.jpg',
            'Z': 'https://res.cloudinary.com/djc3qirsl/image/upload/v1756898014/media/movies/likwz6y1fn3jj3kxzbjw.jpg',
        }
        template_name = 'kids/phonics_and_letter_sounds.html'
        lesson_videos = []
        if hasattr(lesson, 'videos'):
            for video in lesson.videos.all().order_by('order'):
                url = video.video_url
                embed_url = url
                if url:
                    if 'youtu.be/' in url:
                        embed_url = url.replace('https://youtu.be/', 'https://www.youtube.com/embed/')
                    elif 'youtube.com/watch?v=' in url:
                        embed_url = url.replace('watch?v=', 'embed/')
                video.video_embed_url = embed_url
                lesson_videos.append(video)
        # Build completion_map for current user
        completion_map = {}
        if request.user.is_authenticated:
            from kids.models import LessonCompletion
            completions = LessonCompletion.objects.filter(user=request.user)
            for comp in completions:
                completion_map[comp.lesson_id] = comp
        # Get the phonics lesson id for badge lookup
        phonics_lesson = Lesson.objects.filter(lesson_type='phonics').first()
        phonics_lesson_id = phonics_lesson.id if phonics_lesson else None
        return render(request, template_name, {
            'lesson': lesson,
            'completion': completion,
            'video_embed_url': video_embed_url,
            'next_lesson': next_lesson,
            'phonics_sounds': phonics_sounds,
            'phonics_images': phonics_images,
            'phonics_example_words': phonics_example_words,
            'lesson_videos': lesson_videos,
            'completion_map': completion_map,
            'phonics_lesson_id': phonics_lesson_id,
        })
    elif lesson.order == 2:
        template_name = 'kids/lessons/shape_lesson_detail.html'
        return render(request, template_name, {
            'lesson': lesson,
            'completion': completion,
            'video_embed_url': video_embed_url,
                'X': '/media/movies/the-illustration-of-xylophone-vector.jpg',
        })
    elif lesson.lesson_type == 'activities':
        template_name = 'kids/lessons/activities_lesson.html'
        return render(request, template_name, {
            'lesson': lesson,
            'completion': completion,
            'video_embed_url': video_embed_url,
            'next_lesson': next_lesson,
        })
    else:
        template_name = 'kids/lesson_detail.html'
        return render(request, template_name, {
            'lesson': lesson,
            'completion': completion,
            'video_embed_url': video_embed_url,
            'next_lesson': next_lesson,
        })


from django.shortcuts import render

# Main platform views
def online_platform(request):
    age_groups = AgeGroup.objects.all().order_by('min_age')
    subjects = Subject.objects.all().order_by('name')
    courses = Course.objects.select_related('age_group', 'subject').order_by('age_group__min_age', 'order')
    return render(request, 'kids/onlineplatform.html', {
        'age_groups': age_groups,
        'subjects': subjects,
        'courses': courses,
    })

# Stories page view
def stories(request):
    lesson_id = request.GET.get('lesson_id')
    if lesson_id:
        stories = Story.objects.filter(lesson_id=lesson_id).order_by('-created_at')
    else:
        stories = []
    for story in stories:
        if story.video_url:
            if "youtu.be/" in story.video_url:
                story.video_embed_url = story.video_url.replace("https://youtu.be/", "https://www.youtube.com/embed/")
            elif "youtube.com/watch?v=" in story.video_url:
                story.video_embed_url = story.video_url.replace("watch?v=", "embed/")
            else:
                story.video_embed_url = story.video_url
        else:
            story.video_embed_url = ""
    return render(request, 'kids/stories.html', {'stories': stories})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('order')
    userprofile = getattr(request.user, 'kids_userprofile', None)
    if userprofile is None:
        if request.user.is_authenticated:
            from kids.models import UserProfile
            userprofile, created = UserProfile.objects.get_or_create(user=request.user)
        else:
            userprofile = None
    enrolled = userprofile and course in userprofile.courses.all() if userprofile else False
    if request.method == 'POST' and not enrolled and userprofile:
        userprofile.courses.add(course)
        enrolled = True
    name = course.name.strip().lower().replace('&', 'and').replace('  ', ' ')
    if name == 'colors and shapes':
        template_name = 'kids/colorsandshapes.html'
    else:
        template_name = 'kids/course_detail.html'
    # Build completion map for current user
    completion_map = {}
    if request.user.is_authenticated:
        from kids.models import LessonCompletion
        completions = LessonCompletion.objects.filter(user=request.user, lesson__in=lessons)
        for comp in completions:
            completion_map[comp.lesson_id] = comp
    return render(request, template_name, {
        'course': course,
        'lessons': lessons,
        'enrolled': enrolled,
        'completion_map': completion_map,
    })

# Game and utility views
def puzzle_game(request):
    return render(request, 'kids/puzzle_game.html')

def arrow_throw(request):
    return render(request, 'kids/arrow_throw.html')

def brain_games(request):
    return render(request, 'kids/pattern_sequence.html')

def home(request):
    movies = KidsMovie.objects.all()
    return render(request, 'kids/home.html', {'movies': movies})

def funny_runner(request):
    return render(request, 'kids/funny_runner.html')

def funny_runner_phaser(request):
    return render(request, 'kids/funny_runner_phaser.html')

def space_shooter(request):
    return render(request, 'kids/space_shooter.html')

def platformer_adventure(request):
    return render(request, 'kids/platformer_adventure.html')

def digital_drawing(request):
    return render(request, 'kids/digital_drawing.html')

def painting_game(request):
    return render(request, 'kids/painting_game.html')

def art_puzzle(request):
    return render(request, 'kids/art_puzzle.html')

# Color Mixing Game view
def color_mixing_game(request):
    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'kids/color_mixing_game.html', {'username': username})

def leaderboard(request):
    return render(request, 'kids/leaderboard.html')

def play_screen(request):
    username = request.user.username if request.user.is_authenticated else ''
    return render(request, 'kids/play_screen.html', {'username': username})

def alphabet_lesson_detail(request):
    alphabet_words = {
        'A': 'Apple', 'B': 'Ball', 'C': 'Cat', 'D': 'Dog', 'E': 'Elephant', 'F': 'Fish', 'G': 'Goat',
        'H': 'Hat', 'I': 'Ice', 'J': 'Jug', 'K': 'Kite', 'L': 'Lion', 'M': 'Monkey', 'N': 'Nest',
        'O': 'Orange', 'P': 'Pig', 'Q': 'Queen', 'R': 'Rabbit', 'S': 'Sun', 'T': 'Tiger', 'U': 'Umbrella',
        'V': 'Violin', 'W': 'Wolf', 'X': 'Xylophone', 'Y': 'Yak', 'Z': 'Zebra'
    }
    alphabet_images = {
        'A': 'https://cdn.pixabay.com/photo/2016/03/31/19/56/apple-1295556_1280.png',
        'B': 'https://cdn.pixabay.com/photo/2013/07/12/15/37/ball-150935_1280.png',
        'C': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/cat-1296275_1280.png',
        'D': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/dog-1296276_1280.png',
        'E': 'https://cdn.pixabay.com/photo/2017/01/06/19/15/elephant-1957747_1280.png',
        'F': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/fish-1296277_1280.png',
        'G': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/goat-1296278_1280.png',
        'H': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/hat-1296279_1280.png',
        'I': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/ice-1296280_1280.png',
        'J': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/jug-1296281_1280.png',
        'K': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/kite-1296282_1280.png',
        'L': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/lion-1296283_1280.png',
        'M': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/monkey-1296284_1280.png',
        'N': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/nest-1296285_1280.png',
        'O': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/orange-1296286_1280.png',
        'P': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/pig-1296287_1280.png',
        'Q': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/queen-1296288_1280.png',
        'R': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/rabbit-1296289_1280.png',
        'S': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/sun-1296290_1280.png',
        'T': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/tiger-1296291_1280.png',
        'U': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/umbrella-1296292_1280.png',
        'V': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/violin-1296293_1280.png',
        'W': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/wolf-1296294_1280.png',
        'X': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/xylophone-1296295_1280.png',
        'Y': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/yak-1296296_1280.png',
        'Z': 'https://cdn.pixabay.com/photo/2016/03/31/20/11/zebra-1296297_1280.png',
    }
    from kids.models import Lesson, LessonPoster
    # Get the current lesson (alphabet lesson)
    lesson = Lesson.objects.filter(lesson_type='Alphabet').first()
    posters = lesson.posters.all() if lesson else []
    return render(request, 'kids/lessons/alphabet_lesson_detail.html', {
        'alphabet_words': alphabet_words,
        'alphabet_images': alphabet_images,
        'lesson': lesson,
        'posters': posters,
    })

def simple_words_quiz_game(request):
    return render(request, 'kids/lessons/simple_words_quiz_game.html')
def sight_words_quiz_game(request):
    return render(request, 'kids/lessons/sight_words_quiz_game.html')
def virtual_pet(request):
    return render(request, 'kids/pet/virtualpet.html')
