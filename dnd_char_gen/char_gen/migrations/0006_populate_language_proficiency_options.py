import requests
from django.db import migrations


def populate_languages_and_proficiencies(apps, schema_editor):
    base_url = "https://www.dnd5eapi.co"

    Race = apps.get_model("char_gen", "Race")
    AbilityScoreBonus = apps.get_model("char_gen", "AbilityScoreBonus")
    ProficiencyOptions = apps.get_model("char_gen", "ProficiencyOptions")
    LanguageOptions = apps.get_model("char_gen", "LanguageOptions")
    AbilityScore = apps.get_model("char_gen", "AbilityScore")
    Proficiency = apps.get_model("char_gen", "Proficiency")
    Language = apps.get_model("char_gen", "Language")

    response = requests.get(base_url + "/api/races")

    par_obj = response.json()

    for obj in par_obj.get('results'):
        score_response = requests.get(base_url + obj.get("url"))
        json_obj = score_response.json()

        model = Race.objects.get(index=json_obj.get('index'))

        spo = json_obj.get('starting_proficiency_options', {})
        if spo:
            prof_option = ProficiencyOptions.objects.create(
                desc=spo.get('desc', 'None'),
                choose=spo.get('choose', 0),
                choice_type=spo.get('type', 'none')
            )
            model.starting_proficiency_options = prof_option
            model.save()

            for option in spo.get('from', {}).get('options', []):
                prof_option.options.add(
                    Proficiency.objects.get(index=option.get('item', {}).get('index')))

        lo = json_obj.get('language_options', {})
        if lo:
            lang_option = LanguageOptions.objects.create(
                desc=lo.get('desc', 'None'),
                choose=lo.get('choose', 0),
                choice_type=lo.get('type', 'none')
            )
            model.language_options = lang_option
            model.save()

            for option in lo.get('from', {}).get('options', []):
                lang_option.options.add(
                    Language.objects.get(index=option.get('item', {}).get('index')))

        ability_bonuses = json_obj.get('ability_bonuses')
        for bonus in ability_bonuses:
            AbilityScoreBonus.objects.create(
                race=model,
                ability_score=AbilityScore.objects.get(
                    index=bonus.get('ability_score').get('index')),
                bonus=bonus.get('bonus')
            )

        starting_proficiencies = json_obj.get('starting_proficiencies')
        for prof in starting_proficiencies:
            model.starting_proficiencies.add(
                Proficiency.objects.get(index=prof.get('index')))

        languages = json_obj.get('languages', [])
        for language in languages:
            model.languages.add(Language.objects.get(
                index=language.get('index')))


class Migration(migrations.Migration):

    dependencies = [
        ('char_gen', '0005_populate_races'),
    ]

    operations = [

        migrations.RunPython(populate_languages_and_proficiencies,
                             reverse_code=migrations.RunPython.noop),]
