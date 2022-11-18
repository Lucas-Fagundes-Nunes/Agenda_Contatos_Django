from contatos.models import Contato  # importando class agenda
from django import forms
from django.db import models

# Create your models here.

class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        exclude = ('mostrar',)
