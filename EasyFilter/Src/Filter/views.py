from re import sub
from django.db.models import fields
from django.shortcuts import render, redirect

from .forms import TranscribeForm
from .models import TranscribeModel

from .transcribe import Transcribe
from .filter import Filter

from .conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS, PROFANITY_PATH
import os
import subprocess

# Create your views here.
def home_view(request, *args, **kwargs):
    # delete database objects
    db = TranscribeModel.objects.all()
    db.delete()
    ## delete files
    del_inp = os.path.join(SAMPLE_INPUTS, '*')
    del_out = os.path.join(SAMPLE_OUTPUTS, '*')
    subprocess.call('del /Q ' + del_inp, shell=True)
    subprocess.call('del /Q ' + del_out, shell=True)
    form = TranscribeForm(request.POST, request.FILES)
    if form.is_valid():
        profanity_words = form.cleaned_words()
        file_name = form.cleaned_video()
        form.save()
        extracted_audio = os.path.join(SAMPLE_INPUTS, 'extracted_audio.flac')
        profanity_file = os.path.join(PROFANITY_PATH, 'prof_en.json')
        filtered_audio = os.path.join(SAMPLE_OUTPUTS, 'filtered_audio.flac')
        txt_file = os.path.join(PROFANITY_PATH, 'transcript_text.txt')
        transcribe = Transcribe()
        censor = Filter()
        if file_name[1] == 'video':
            file_name = file_name[0]
            video_file = os.path.join(SAMPLE_INPUTS, file_name)
            censor.extract_audio(video_file, extracted_audio)
            transcript, transcript_txt = transcribe.transcript(extracted_audio)
            transcribe.write_txt(transcript_txt, txt_file)
            censor.filter_audio(transcript, profanity_words, profanity_file, extracted_audio, filtered_audio)
            output_video = os.path.join(SAMPLE_OUTPUTS, file_name)
            output_video = censor.get_video(video_file, filtered_audio, output_video)
        if file_name[1] == 'audio':
            file_name = file_name[0]
            extracted_audio = os.path.join(SAMPLE_INPUTS, file_name)
            transcript, transcript_txt = transcribe.transcript(extracted_audio)
            transcribe.write_txt(transcript_txt, txt_file)
            output_audio = os.path.join(SAMPLE_OUTPUTS, file_name)
            censor.filter_audio(transcript, profanity_words, profanity_file, extracted_audio, output_audio)
        return redirect('download-view')
    else:
        form = TranscribeForm()
    return render(request, 'home.html', {'form':form})


def download_view(request, *args, **kwargs):
    form = TranscribeModel.objects.all()
    for item in form:
        name = item.video.name
        name = name.replace('sample_inputs', 'sample_outputs')
        item.video.name = name
    return render(request, 'download.html', {"form":form})