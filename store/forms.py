from django import forms

from .models import Comment, Reply

class CommentForm(forms.ModelForm):
    
    body = forms.CharField(label='Punya pertanyaan seputar produk?', widget=forms.Textarea, min_length=10, max_length=450)
    
    class Meta:
        model = Comment
        fields = ('body',)
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ajukan pertanyaan ..', 'rows': '5'})

class ReplyForm(forms.ModelForm):
    
    comment = forms.CharField(widget=forms.HiddenInput())
    body = forms.CharField(widget=forms.Textarea, min_length=10, max_length=450)
    
    class Meta:
        model = Reply
        fields = ('comment', 'body',)
    
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        try:
            obj = Comment.objects.get(id=comment)
        except Comment.DoesNotExist:
            raise forms.ValidationError("Comment not found")
        
        return obj
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'rows': '3'})
