from django.conf import settings
import os

BASE_DIR = settings.BASE_DIR
MEDIA_ROOT = settings.MEDIA_ROOT
SAMPLE_INPUTS = os.path.join(MEDIA_ROOT, 'sample_inputs')
SAMPLE_OUTPUTS = os.path.join(MEDIA_ROOT, 'sample_outputs')
PROFANITY_PATH = os.path.join(BASE_DIR, 'profanity')