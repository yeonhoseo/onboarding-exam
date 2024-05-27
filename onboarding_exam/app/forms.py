from django import forms 

class LeadForm(forms.Form) :    
    FirstName = forms.CharField(max_length=100)
    LastName = forms.CharField(max_length=100)
    Company = forms.CharField(max_length=100)
    Phone = forms.CharField(max_length=100)
    Email = forms.EmailField()
