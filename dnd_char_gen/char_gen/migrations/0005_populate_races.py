import requests
from django.db import migrations


def populate_races(apps, schema_editor):
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

        spo = obj.get('starting_proficiency_options', {})
        prof_option = ProficiencyOptions.objects.create(
            desc=spo.get('desc', 'None'),
            choose=spo.get('choose', 0),
            choice_type=spo.get('type', 'none')
        )

        for option in spo.get('from', {}).get('options', []):
            prof_option.options.add(
                Proficiency.objects.get(index=option.get('index')))
        prof_option.save()

        lo = obj.get('language_options', {})
        lang_option = LanguageOptions.objects.create(
            desc=lo.get('desc', 'None'),
            choose=lo.get('choose', 0),
            choice_type=lo.get('type', 'none')
        )

        for option in lo.get('from', {}).get('options', []):
            print(Language.objects.get(index=option.get('index')))
            lang_option.options.add(
                Language.objects.get(index=option.get('index')))
        lang_option.save()

        model = Race.objects.create(
            index=json_obj.get('index', 'n/a'),
            name=json_obj.get('name', 'N/A'),
            speed=json_obj.get('speed', 0),
            alignment=json_obj.get('alignment', 'None'),
            age=json_obj.get('age', 'None'),
            size=json_obj.get('size', 'None'),
            size_desc=json_obj.get('size_description', 'None'),
            language_desc=json_obj.get('language_desc', 'None'),
            url=json_obj.get('url'),

            starting_proficiency_options=prof_option,
            language_options=lang_option
        )

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

        languages = obj.get('languages', [])
        for language in languages:
            model.languages.add(Language.objects.get(
                index=language.get('index')))
        model.save()


class Migration(migrations.Migration):

    dependencies = [
        ('char_gen', '0004_abilityscorebonus_choiceoptions_languageoptions_and_more'),
    ]

    operations = [

        migrations.RunPython(populate_races,
                             reverse_code=migrations.RunPython.noop),]
