from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    
    body = forms.CharField(label='Punya pertanyaan seputar produk?', widget=forms.Textarea, min_length=10, max_length=450)
    
    class Meta:
        model = Comment
        fields = ('body',)
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ajukan pertanyaan ..', 'rows': '5'})
