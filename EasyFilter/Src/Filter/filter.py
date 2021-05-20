import subprocess
import json

class Filter:

    def extract_audio(self, input_file, output_file):
        command = 'ffmpeg -i {} -y -vcodec libx264 -preset ultrafast -ab 160k -ac 1 -ar 44100 {}'.format(input_file, output_file)
        subprocess.call(command, shell=True)
    

    def mute_word(self, start_s, end_s):
        mute = "\"volume=enable='between(t,{},{})':volume=0\",".format(start_s, end_s)
        return mute
    

    def filter_audio(self, transcript, words, profanity_file, input_audio, output_audio):
        self.write_profanity(words, profanity_file)
        self.open_profanity(profanity_file)
        profanity_list = self.static_words + self.dynamic_words
        prefix = "ffmpeg -i {} -y -af ".format(input_audio)
        mute = ''
        suffix = " {}".format(output_audio)
        filtered_count = 0
        for frame in transcript:
            if frame['word'] in profanity_list:
                mute += self.mute_word(start_s=frame['start'], end_s=frame['end'])
                filtered_count += 1
        if filtered_count == 0:
            prefix = "ffmpeg -i {} -y".format(input_audio)
            suffix = " {}".format(output_audio)
            command = prefix + suffix
        else:
            mute = mute[0:-1]
            command = prefix + mute + suffix
        subprocess.call(command)
        self.default_profanity(profanity_file)
    


    def open_profanity(self, file):
        with open(file) as prof_list:
            data = json.load(prof_list)
            self.static_words = data["static_words"]
            self.dynamic_words = data["dynamic_words"]
    

    def write_profanity(self, words, file):
        with open(file) as prof_list:
            data = json.load(prof_list)
            for word in words:
                data["dynamic_words"].append(word)
            prof_list.close()
        with open(file, "w") as prof_list:
            json.dump(data, prof_list, indent=4)
            prof_list.close()
    

    def default_profanity(self, file):
        with open(file) as prof_list:
            data = json.load(prof_list)
            data['dynamic_words'].clear()
            data['dynamic_words'].append('')
            prof_list.close()
        with open(file, "w") as prof_list:
            json.dump(data, prof_list, indent=4)
            prof_list.close()
    

    def get_video(self, input_video, input_audio, output_video):
        command = "ffmpeg -i {} -i {} -strict -2 -y -c copy -map 0:v:0 -map 1:a:0 {}".format(input_video, input_audio, output_video)
        subprocess.call(command, shell=True)
        return output_video
    
    