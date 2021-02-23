from django.db import models
from django.db.models.fields.related import ForeignKey
import discord
# Create your models here.


class Guild(models.Model):
    """The Guild being used"""
    discord_id = models.BigIntegerField()

    def get_id(guild: discord.Guild):
        return guild.id


class Complex(models.Model):
    """The game being played"""
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    CLASSIC = "CLS"
    STRAIGHT = "STR"
    ZAP = "ZAP"
    game_style_choices = [
        (CLASSIC, 'Classic'),
        (STRAIGHT, 'Straight'),
        (ZAP, "Zap")
    ]
    game_style = models.CharField(null=True, 
        max_length=3, choices=game_style_choices, default=CLASSIC)


class User(models.Model):
    """A user of discord"""
    discord_id = models.BigIntegerField()

    def get_id(user: discord.User):
        return user.id

    class Meta:
        abstract = True


class Player(User, models.Model):
    """A player in a Complex"""
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    pass


class GM(User, models.Model):
    """A Gamemaster of a Complex"""
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)


class Troubleshooter(models.Model):
    "Player Character"
    class Clearance(models.IntegerChoices):
        INFRARED = 0
        RED = 1
        ORANGE = 2
        YELLOW = 3
        GREEN = 4
        BLUE = 5
        INDIGO = 6
        VIOLET = 7
        ULTRAVIOLET = 8

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=100),
    clearance = models.IntegerField(choices=Clearance.choices, default=Clearance.RED)
    management = models.IntegerField(null=True)
    stealth = models.IntegerField(null=True)
    violence = models.IntegerField(null=True)
    hardware = models.IntegerField(null=True)
    software = models.IntegerField(null=True)
    wetware = models.IntegerField(null=True)
    credits = models.BigIntegerField()
    mbd = models.CharField(null=True)
    perversity = models.IntegerField(null=True)



class Skill(models.Model):
    "Skills a character may have"
    MANAGEMENT = 'MAN'
    STEALTH = "STL"
    VIOLENCE = "VIO"
    HARDWARE = "HDW"
    SOFTWARE = "SFW"
    WETWARE = "WTW"

    type_choices = [
        (MANAGEMENT, 'Management'),
        (STEALTH, 'Stealth'),
        (VIOLENCE, 'Violence'),
        (HARDWARE, 'Hardware'),
        (SOFTWARE, 'Software'),
        (WETWARE, 'Wetware')
    ]
    type = models.CharField(max_length=3, choices=type_choices)
    is_common = models.BooleanField(default=False)
    is_narrow = models.BooleanField(default=False)
    is_weak = models.BooleanField(default=False)
    mod = models.IntegerField(null=True)

    troubleshooter = models.ForeignKey(
        Troubleshooter, on_delete=models.CASCADE)

    def return_value(self, troubleshooter: Troubleshooter):
        type_dict = {
            self.MANAGEMENT: troubleshooter.management,
            self.STEALTH: troubleshooter.stealth,
            self.VIOLENCE: troubleshooter.violence,
            self.HARDWARE: troubleshooter.hardware,
            self.SOFTWARE: troubleshooter.software,
            self.WETWARE: troubleshooter.wetware
        }
        value = type_dict[self.type] + self.mod
        if self.is_common:
            value += 4
        if self.is_narrow:
            value += 6
        if self.is_weak:
            value = 1
        return value
    
class Tics(models.Model):
    troubleshooter = models.ForeignKey(Troubleshooter, on_delete=models.CASCADE)
    description = models.CharField(null=True, max_length=500)
