from django import forms
from .models import Book, Author, Publisher

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','publisher', 'publication_date', 'isbn', 'author']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [ 'first_name', 'last_name', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PublisherForm(forms.ModelForm): 
    class Meta:
        model = Publisher
        fields = ['name', 'address', 'city', 'state_province', 'country', 'website']

class BookFormwithoutauthor(forms.ModelForm):
    class Meta:
        model= Book
        exclude= ['author']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BookFormwithoutauthorandpublisher(forms.ModelForm):
    class Meta:
        model= Book
        exclude= ['author','publisher']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }