from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Predicted_Schedule, Schedule
from django.forms import modelformset_factory

from .models import Item





class ScheduleForm(forms.ModelForm):
    
    week_etb_cgp = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Wk/ETB CGP", "class":"form-control"}), label="")
    service = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Service", "class":"form-control"}), label="")
    vessel = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Vessel", "class":"form-control"}), label="")
    voyage_s = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Voyage-S", "class":"form-control"}), label="")
    
    eta_cgp = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder":"ETA CGP", "class":"form-control"}), label="")
    etb_cgp = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder":"ETB CGP", "class":"form-control"}), label="")
    etd_cgp = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder":"ETD CGP", "class":"form-control"}), label="")
    
    voyage_n = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Voyage-N", "class":"form-control"}), label="")
    
    eta_cmb = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder":"ETA CMB", "class":"form-control"}), label="")
    etb_cmb = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder":"ETB CMB", "class":"form-control"}), label="")
    etd_cmb = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder":"ETD CMB", "class":"form-control"}), label="")
    
    eta_cgp_2 = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder":"ETA CGP-2", "class":"form-control"}), label="")
    etb_cgp_2 = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder":"ETB CGP-2", "class":"form-control"}), label="")
    etd_cgp_2 = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={"placeholder":"ETD CGP-2", "class":"form-control"}), label="")

    class Meta:
        model = Schedule
        fields = "__all__"







class PredictedScheduleForm(forms.ModelForm):
    class Meta:
        model = Predicted_Schedule
        fields = [
            'week_etb_cgp', 'service', 'vessel', 'voyage_s', 
            'eta_cgp', 'etb_cgp', 'etd_cgp', 
            'voyage_n', 
            'eta_cmb', 'etb_cmb', 'etd_cmb', 
            'eta_cgp_2', 'etb_cgp_2', 'etd_cgp_2'
        ]





class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity']