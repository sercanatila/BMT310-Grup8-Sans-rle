from .models import TranscribeModel
from django import forms
import re

class TranscribeForm(forms.ModelForm):
    words = forms.CharField(max_length=100, required=False)
    class Meta:
        model = TranscribeModel
        fields = [
            'words',
            'video'
        ]
    

    def cleaned_words(self):
        data = self.cleaned_data.get('words')
        data = str(data).split()
        invalid_chars = re.compile(r"[<>/{}[\]~`]*,.0123456789")
        for words in data:
            if invalid_chars.search(words):
                raise forms.ValidationError("separate words with space and don't use special characters")
        return data

    def cleaned_video(self):
        file_name = self.cleaned_data.get('video').name
        valid_video_ext = ['mp4', 'mkv', 'flv', '3gp']
        valid_audio_ext = ['mp3', 'flac', 'aac', 'wav']
        file_ext = file_name.rsplit('.')
        for ext in valid_video_ext:
            if file_ext[1].endswith(ext):
                return file_name, 'video'
        for ext in valid_audio_ext:
            if file_ext[1].endswith(ext):
                return file_name, 'audio'
        raise forms.ValidationError("upload a supported file")