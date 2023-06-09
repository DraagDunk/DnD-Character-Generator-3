import requests
from django.db import migrations


def populate_races(apps, schema_editor):
    base_url = "https://www.dnd5eapi.co"

    Race = apps.get_model("char_gen", "Race")
    AbilityScoreBonus = apps.get_model("char_gen", "AbilityScoreBonus")
    AbilityScore = apps.get_model("char_gen", "AbilityScore")
    Proficiency = apps.get_model("char_gen", "Proficiency")
    Language = apps.get_model("char_gen", "Language")

    response = requests.get(base_url + "/api/races")

    par_obj = response.json()

    for obj in par_obj.get('results'):
        score_response = requests.get(base_url + obj.get("url"))
        json_obj = score_response.json()

        model = Race.objects.create(
            index=json_obj.get('index', 'n/a'),
            name=json_obj.get('name', 'N/A'),
            speed=json_obj.get('speed', 0),
            alignment=json_obj.get('alignment', 'None'),
            age=json_obj.get('age', 'None'),
            size=json_obj.get('size', 'None'),
            size_desc=json_obj.get('size_description', 'None'),
            language_desc=json_obj.get('language_desc', 'None'),
            url=json_obj.get('url')
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

        languages = json_obj.get('languages', [])
        for language in languages:
            model.languages.add(Language.objects.get(
                index=language.get('index')))


class Migration(migrations.Migration):

    dependencies = [
        ('char_gen', '0004_abilityscorebonus_choiceoptions_languageoptions_and_more'),
    ]

    operations = [

        migrations.RunPython(populate_races,
                             reverse_code=migrations.RunPython.noop),]
