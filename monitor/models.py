# -*- coding: utf-8 -*-

from django.db import models
from django.utils.timezone import now


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.TextField(max_length=32)
    first_name = models.TextField(max_length=32)
    last_name = models.TextField(max_length=32)
    institution = models.TextField(blank=True, max_length=32)
    email = models.CharField(unique=True, blank=True, max_length=32)

    def __str__(self):
        return '(id=%s, username=%s)' % (self.id, self.username)

    def save(self, *args, **kwargs):
        print('Creating new user: %s' % self)
        super(User, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['id', 'first_name', 'last_name', 'email', 'institution']


class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    # session = models.CharField(max_length=32)

    def __str__(self):
        return '(user=%s, date=%s)' % (self.user, self.date)

    def save(self, *args, **kwargs):
        if self.date == None:
            self.date = now()
        try:
            last_visit = list(Visit.objects.filter(user=self.user))[-1]
            if ((self.date - last_visit.date).seconds / 60) < 1.0:
                print('Session already recorded')
                return
        except IndexError:
            pass
        print('Recording session...')
        super(Visit, self).save(*args, **kwargs)
        
        

