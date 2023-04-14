from django.contrib import admin

from .models import AbilityScore, Skill, Language, Proficiency, Race, ProficiencyOptions, LanguageOptions


@admin.register(AbilityScore)
class AbilityScoreAdmin(admin.ModelAdmin):
    list_display = ('full_name', )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'ability_score')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'language_type', 'script')


@admin.register(Proficiency)
class ProficiencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency_type')


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'size')


@admin.register(ProficiencyOptions)
class ProficiencyOptionsAdmin(admin.ModelAdmin):
    pass


@admin.register(LanguageOptions)
class LanguageOptionsAdmin(admin.ModelAdmin):
    pass
