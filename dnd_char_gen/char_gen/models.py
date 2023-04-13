from django.db import models


class AbilityScore(models.Model):
    index = models.CharField(max_length=3)
    name = models.CharField(max_length=3)
    full_name = models.CharField(max_length=15)
    desc1 = models.TextField()
    desc2 = models.TextField()

    url = models.URLField()

    @staticmethod
    def from_json(json_obj):
        model = AbilityScore(
            index=json_obj.get('index', 'n/a'),
            name=json_obj.get('name', 'N/A'),
            full_name=json_obj.get('full_name', 'N/A'),
            desc1=json_obj.get('desc', ['None', 'None'])[0],
            desc2=json_obj.get('desc', ['None', 'None'])[1],
            url=json_obj.get('url')
        )
        return model

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    index = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    desc = models.TextField()
    ability_score = models.ForeignKey("AbilityScore", on_delete=models.CASCADE)

    url = models.URLField()

    @staticmethod
    def from_json(json_obj):
        model = Skill(
            index=json_obj.get('index', 'n/a'),
            name=json_obj.get('name', 'N/A'),
            desc=json_obj.get('desc', ['None'])[0],
            ability_score=AbilityScore.objects.get(
                index=json_obj.get('ability_score').get('index', None)),
            url=json_obj.get('url')
        )
        return model

    def __str__(self):
        return self.name


class Language(models.Model):
    index = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    language_type = models.CharField(max_length=20)
    typical_speakers = models.JSONField()
    script = models.CharField(max_length=20)

    url = models.URLField()

    @staticmethod
    def from_json(json_obj):
        model = Language(
            index=json_obj.get('index', 'n/a'),
            name=json_obj.get('name', 'N/A'),
            language_type=json_obj.get('type', 'None'),
            typical_speakers=json_obj.get('typical_speakers', []),
            script=json_obj.get('script', 'None'),
            url=json_obj.get('url')
        )
        return model

    def __str__(self):
        return self.name


class Proficiency(models.Model):
    index = models.CharField(max_length=30)
    proficiency_type = models.CharField(max_length=20)
    name = models.CharField(max_length=30)

    url = models.URLField()

    @staticmethod
    def from_json(json_obj):
        model = Proficiency(
            index=json_obj.get('index', 'n/a'),
            name=json_obj.get('name', 'N/A'),
            proficiency_type=json_obj.get('type', 'None'),
            url=json_obj.get('url')
        )
        return model

    def __str__(self):
        return self.name


class AbilityScoreBonus(models.Model):
    race = models.ForeignKey("Race", on_delete=models.CASCADE)
    ability_score = models.ForeignKey("AbilityScore", on_delete=models.CASCADE)
    bonus = models.IntegerField()


class ChoiceOptions(models.Model):
    desc = models.TextField()
    choose = models.IntegerField()
    choice_type = models.CharField(max_length=30)


class ProficiencyOptions(ChoiceOptions):
    options = models.ManyToManyField("Proficiency")

    def __str__(self):
        return f"{self.race.first()} options"


class LanguageOptions(ChoiceOptions):
    options = models.ManyToManyField("Language")

    def __str__(self):
        return f"{self.race.first()} options"


class Race(models.Model):
    index = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    speed = models.IntegerField()
    ability_bonuses = models.ManyToManyField(
        "AbilityScore", through="AbilityScoreBonus")
    alignment = models.TextField()
    age = models.TextField()
    size = models.CharField(max_length=20)
    size_desc = models.TextField()
    starting_proficiencies = models.ManyToManyField("Proficiency")
    starting_proficiency_options = models.ForeignKey(
        "ProficiencyOptions", on_delete=models.SET_NULL, null=True, related_name="race")
    languages = models.ManyToManyField("Language")
    language_options = models.ForeignKey(
        "LanguageOptions", on_delete=models.SET_NULL, null=True, related_name="race")
    language_desc = models.TextField()

    url = models.URLField()

    @staticmethod
    def from_json(json_obj):
        model = Race(
            index=json_obj.get('index', 'n/a'),
            name=json_obj.get('name', 'N/A'),
            speed=json_obj.get('speed', 0),
            alignment=json_obj.get('alignment', 'None'),
            age=json_obj.get('age', 'None'),
            size=json_obj.get('size', 'None'),
            size_desc=json_obj.get('size_desc', 'None'),
            language_desc=json_obj.get('language_desc', 'None'),
            url=json_obj.get('url')
        )
        return model

    def __str__(self):
        return self.name
