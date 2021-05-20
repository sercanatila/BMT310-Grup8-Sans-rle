from google.cloud import speech_v1 as speech
import io

class Transcribe:
    audio = None
    config = None
    config = speech.RecognitionConfig(
        encoding = speech.RecognitionConfig.AudioEncoding.FLAC,
        language_code = 'en-US',
        sample_rate_hertz = 44100,
        audio_channel_count = 1,
        profanity_filter = False,
        enable_word_time_offsets = True
    )

    def load_audio(self, file):
        with io.open(file, "rb") as audio_file:
            audio = audio_file.read()
            self.audio = speech.RecognitionAudio(content=audio)
    
    

    def transcript(self, audio):
        self.load_audio(audio)
        client = speech.SpeechClient()
        operation = client.long_running_recognize(config=self.config, audio=self.audio)
        response = operation.result(timeout=160)
        output_transcript = []
        output_txt = []
        for result in response.results:
            best_alternative = result.alternatives[0]
            for word in best_alternative.words:
                start_s = word.start_time.total_seconds()
                end_s = word.end_time.total_seconds()
                word = word.word
                output_transcript.append({
                    "word": word,
                    "start": start_s,
                    "end": end_s
                })
                output_txt.append(word)
        return output_transcript, output_txt
    

    def write_txt(self, input_list, file):
        with open(file, 'w') as prof_list:
            for i in input_list:
                prof_list.write(i + ' ')
            prof_list.close()