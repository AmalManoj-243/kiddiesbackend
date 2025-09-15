
from django.contrib import admin
from .models import AgeGroup, Subject, Course, Lesson, KidsMovie, ColorImage, Story, LessonCompletion, LessonVideo, LessonPoster, LessonImage

class LessonPosterInline(admin.TabularInline):
    model = LessonPoster
    extra = 1

class LessonVideoInline(admin.TabularInline):
    model = LessonVideo
    extra = 1

class ColorImageInline(admin.TabularInline):
    model = ColorImage
    extra = 1

class LessonImageInline(admin.TabularInline):
    model = LessonImage
    extra = 1

class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonPosterInline, LessonVideoInline, ColorImageInline, LessonImageInline]
    fields = ('course', 'title', 'lesson_type', 'content', 'order', 'video_url', 'poster_image')

admin.site.register(LessonPoster)
admin.site.register(Story)
admin.site.register(AgeGroup)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonImage)
admin.site.register(KidsMovie)
admin.site.register(ColorImage)

class LessonCompletionAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed_learned', 'completed_activity', 'completed_game', 'completed_quiz', 'teacher_approved', 'completed_at', 'teacher')
    list_filter = ('teacher_approved', 'lesson')
    search_fields = ('user__username', 'lesson__title')
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        queryset.update(teacher_approved=True)
    approve_selected.short_description = "Mark selected completions as approved"

admin.site.register(LessonCompletion, LessonCompletionAdmin)
