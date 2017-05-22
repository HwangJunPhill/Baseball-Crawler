# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DailyRecord(models.Model):
    no = models.IntegerField(db_column='No', primary_key=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=50, blank=True, null=True)  # Field name made lowercase.
    opponent = models.CharField(db_column='Opponent', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pa = models.IntegerField(db_column='PA', blank=True, null=True)  # Field name made lowercase.
    ab = models.IntegerField(db_column='AB', blank=True, null=True)  # Field name made lowercase.
    h = models.IntegerField(db_column='H', blank=True, null=True)  # Field name made lowercase.
    number_2b = models.IntegerField(db_column='2B', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_3b = models.IntegerField(db_column='3B', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    hr = models.IntegerField(db_column='HR', blank=True, null=True)  # Field name made lowercase.
    rbi = models.IntegerField(db_column='RBI', blank=True, null=True)  # Field name made lowercase.
    r = models.IntegerField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    sb = models.IntegerField(db_column='SB', blank=True, null=True)  # Field name made lowercase.
    bb = models.IntegerField(db_column='BB', blank=True, null=True)  # Field name made lowercase.
    so = models.IntegerField(db_column='SO', blank=True, null=True)  # Field name made lowercase.
    avg = models.FloatField(db_column='AVG', blank=True, null=True)  # Field name made lowercase.
    oba = models.FloatField(db_column='OBA', blank=True, null=True)  # Field name made lowercase.
    sa = models.FloatField(db_column='SA', blank=True, null=True)  # Field name made lowercase.
    ops = models.FloatField(db_column='OPS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'daily_record'

class Profile(models.Model):
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    team = models.CharField(db_column='Team', max_length=50)  # Field name made lowercase.
    number = models.CharField(db_column='Number', max_length=50)  # Field name made lowercase.
    debut = models.CharField(db_column='Debut', max_length=50, blank=True, null=True)  # Field name made lowercase.
    born = models.CharField(db_column='Born', max_length=50, blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=50, blank=True, null=True)  # Field name made lowercase.
    body = models.CharField(db_column='Body', max_length=50, blank=True, null=True)  # Field name made lowercase.
    photo = models.CharField(db_column='Photo', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile'


class SeasonRecord(models.Model):
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.
    g = models.IntegerField(db_column='G', blank=True, null=True)  # Field name made lowercase.
    pa = models.IntegerField(db_column='PA', blank=True, null=True)  # Field name made lowercase.
    ab = models.IntegerField(db_column='AB', blank=True, null=True)  # Field name made lowercase.
    h = models.IntegerField(db_column='H', blank=True, null=True)  # Field name made lowercase.
    number_2b = models.IntegerField(db_column='2B', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_3b = models.IntegerField(db_column='3B', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    hr = models.IntegerField(db_column='HR', blank=True, null=True)  # Field name made lowercase.
    rbi = models.IntegerField(db_column='RBI', blank=True, null=True)  # Field name made lowercase.
    r = models.IntegerField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    sb = models.IntegerField(db_column='SB', blank=True, null=True)  # Field name made lowercase.
    bb = models.IntegerField(db_column='BB', blank=True, null=True)  # Field name made lowercase.
    so = models.IntegerField(db_column='SO', blank=True, null=True)  # Field name made lowercase.
    avg = models.FloatField(db_column='AVG', blank=True, null=True)  # Field name made lowercase.
    oba = models.FloatField(db_column='OBA', blank=True, null=True)  # Field name made lowercase.
    sa = models.FloatField(db_column='SA', blank=True, null=True)  # Field name made lowercase.
    ops = models.FloatField(db_column='OPS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'season_record'


class TotalRecord(models.Model):
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.
    g = models.IntegerField(db_column='G', blank=True, null=True)  # Field name made lowercase.
    pa = models.CharField(db_column='PA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ab = models.IntegerField(db_column='AB', blank=True, null=True)  # Field name made lowercase.
    h = models.IntegerField(db_column='H', blank=True, null=True)  # Field name made lowercase.
    number_2b = models.IntegerField(db_column='2B', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    number_3b = models.IntegerField(db_column='3B', blank=True, null=True)  # Field name made lowercase. Field renamed because it wasn't a valid Python identifier.
    hr = models.IntegerField(db_column='HR', blank=True, null=True)  # Field name made lowercase.
    rbi = models.IntegerField(db_column='RBI', blank=True, null=True)  # Field name made lowercase.
    r = models.IntegerField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    sb = models.IntegerField(db_column='SB', blank=True, null=True)  # Field name made lowercase.
    bb = models.IntegerField(db_column='BB', blank=True, null=True)  # Field name made lowercase.
    so = models.IntegerField(db_column='SO', blank=True, null=True)  # Field name made lowercase.
    avg = models.FloatField(db_column='AVG', blank=True, null=True)  # Field name made lowercase.
    oba = models.FloatField(db_column='OBA', blank=True, null=True)  # Field name made lowercase.
    sa = models.FloatField(db_column='SA', blank=True, null=True)  # Field name made lowercase.
    ops = models.FloatField(db_column='OPS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'total_record'


class Smelt(models.Model):
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    leftgame = models.IntegerField()
    h = models.IntegerField()
    hr = models.IntegerField()
    avg = models.FloatField()
    rbi = models.IntegerField()
    sb = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'smelt'

class Stat(models.Model):
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.
    contact = models.IntegerField(db_column='Contact', blank=True, null=True)  # Field name made lowercase.
    power = models.IntegerField(db_column='Power', blank=True, null=True)  # Field name made lowercase.
    speed = models.IntegerField(db_column='Speed', blank=True, null=True)  # Field name made lowercase.
    eye = models.IntegerField(db_column='Eye', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stat'


class Pitprofile(models.Model):
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    team = models.CharField(db_column='Team', max_length=50)  # Field name made lowercase.
    number = models.CharField(db_column='Number', max_length=50)  # Field name made lowercase.
    debut = models.CharField(db_column='Debut', max_length=50, blank=True, null=True)  # Field name made lowercase.
    born = models.CharField(db_column='Born', max_length=50, blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=50, blank=True, null=True)  # Field name made lowercase.
    body = models.CharField(db_column='Body', max_length=50, blank=True, null=True)  # Field name made lowercase.
    photo = models.CharField(db_column='Photo', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pitprofile'

class PitdailyRecord(models.Model):
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=50, blank=True, null=True)  # Field name made lowercase.
    opponent = models.CharField(db_column='Opponent', max_length=50, blank=True, null=True)  # Field name made lowercase.
    w = models.IntegerField(db_column='W', blank=True, null=True)  # Field name made lowercase.
    l = models.IntegerField(db_column='L', blank=True, null=True)  # Field name made lowercase.
    s = models.IntegerField(db_column='S', blank=True, null=True)  # Field name made lowercase.
    hld = models.IntegerField(db_column='HLD', blank=True, null=True)  # Field name made lowercase.
    ip = models.IntegerField(db_column='IP', blank=True, null=True)  # Field name made lowercase.
    np = models.IntegerField(db_column='NP', blank=True, null=True)  # Field name made lowercase.
    h = models.IntegerField(db_column='H', blank=True, null=True)  # Field name made lowercase.
    hr = models.IntegerField(db_column='HR', blank=True, null=True)  # Field name made lowercase.
    k = models.IntegerField(db_column='K', blank=True, null=True)  # Field name made lowercase.
    bb = models.IntegerField(db_column='BB', blank=True, null=True)  # Field name made lowercase.
    r = models.IntegerField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    er = models.IntegerField(db_column='ER', blank=True, null=True)  # Field name made lowercase.
    whip = models.FloatField(db_column='WHIP', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pitdaily_record'


class PitseasonRecord(models.Model):
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.
    g = models.IntegerField(db_column='G', blank=True, null=True)  # Field name made lowercase.
    w = models.IntegerField(db_column='W', blank=True, null=True)  # Field name made lowercase.
    l = models.IntegerField(db_column='L', blank=True, null=True)  # Field name made lowercase.
    s = models.IntegerField(db_column='S', blank=True, null=True)  # Field name made lowercase.
    hld = models.IntegerField(db_column='HLD', blank=True, null=True)  # Field name made lowercase.
    ip = models.FloatField(db_column='IP', blank=True, null=True)  # Field name made lowercase.
    np = models.IntegerField(db_column='NP', blank=True, null=True)  # Field name made lowercase.
    h = models.IntegerField(db_column='H', blank=True, null=True)  # Field name made lowercase.
    hr = models.IntegerField(db_column='HR', blank=True, null=True)  # Field name made lowercase.
    k = models.IntegerField(db_column='K', blank=True, null=True)  # Field name made lowercase.
    bb = models.IntegerField(db_column='BB', blank=True, null=True)  # Field name made lowercase.
    r = models.IntegerField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    er = models.IntegerField(db_column='ER', blank=True, null=True)  # Field name made lowercase.
    era = models.FloatField(db_column='ERA', blank=True, null=True)  # Field name made lowercase.
    whip = models.FloatField(db_column='WHIP', blank=True, null=True)  # Field name made lowercase.
    qs = models.IntegerField(db_column='QS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pitseason_record'


class PittotalRecord(models.Model):
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.
    g = models.IntegerField(db_column='G', blank=True, null=True)  # Field name made lowercase.
    w = models.IntegerField(db_column='W', blank=True, null=True)  # Field name made lowercase.
    l = models.IntegerField(db_column='L', blank=True, null=True)  # Field name made lowercase.
    s = models.IntegerField(db_column='S', blank=True, null=True)  # Field name made lowercase.
    hld = models.IntegerField(db_column='HLD', blank=True, null=True)  # Field name made lowercase.
    ip = models.FloatField(db_column='IP', blank=True, null=True)  # Field name made lowercase.
    np = models.IntegerField(db_column='NP', blank=True, null=True)  # Field name made lowercase.
    h = models.IntegerField(db_column='H', blank=True, null=True)  # Field name made lowercase.
    hr = models.IntegerField(db_column='HR', blank=True, null=True)  # Field name made lowercase.
    k = models.IntegerField(db_column='K', blank=True, null=True)  # Field name made lowercase.
    bb = models.IntegerField(db_column='BB', blank=True, null=True)  # Field name made lowercase.
    r = models.IntegerField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    er = models.IntegerField(db_column='ER', blank=True, null=True)  # Field name made lowercase.
    era = models.FloatField(db_column='ERA', blank=True, null=True)  # Field name made lowercase.
    whip = models.FloatField(db_column='WHIP', blank=True, null=True)  # Field name made lowercase.
    qs = models.IntegerField(db_column='QS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pittotal_record'


class Pitsmelt(models.Model):
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    leftgame = models.IntegerField()
    w = models.IntegerField()
    l = models.IntegerField()
    s = models.IntegerField()
    h = models.IntegerField()
    ip = models.FloatField()
    k = models.IntegerField()
    era = models.FloatField()
    qs = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pitsmelt'


class Pitstat(models.Model):
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.
    control = models.IntegerField(db_column='Control', blank=True, null=True)  # Field name made lowercase.
    power = models.IntegerField(db_column='Power', blank=True, null=True)  # Field name made lowercase.
    physical = models.IntegerField(db_column='Physical', blank=True, null=True)  # Field name made lowercase.
    def_field = models.IntegerField(db_column='Def', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'pitstat'
