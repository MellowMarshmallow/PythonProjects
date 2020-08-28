#!/usr/bin/env python3


# Dependencies
import youtube_dl


class Logger:
    def debug(self, message):
        pass

    def error(self, message):
        print(f'[ERROR]: {message}')

    def warning(self, message):
        pass


class YouTubeDL:

    # constructor
    # hook
    # prompt(s)
    # validator(s)

    def __init__(self):
        self.audio_formats = {'aac', 'flac', 'mp3', 'm4a', 'opus', 'vorbis', 'wav'}
        self.default_audio_format = 'm4a'

        # to be determined/assigned
        self.youtube_url = ''
        self.audio_format = self.default_audio_format

    def post_transaction_hook(download):
        bytes_to_mb = lambda byte: round(download['total_bytes'] / 1000000, 2)
        print('Done downloading, printing information...',
              f'[FILENAME]: {download["filename"]}',
              f'[SIZE]: {bytes_to_mb(download["total_bytes"])}MB', sep='\n')

    def prompt_for_url(self):
        try:
            self.youtube_url = input('Enter complete (YouTube) URL to audio: ').strip()
        except EOFError:
            print('EOFError while getting user input for URL')
            self.youtube_url = ''

    def prompt_for_audio_format(self):
        try:
            self.audio_format = input('Enter preferred audio format: ').strip().lower()
        except EOFError:
            print('EOFError while getting user input for audio format')
            self.audio_format = self.default_audio_format

    def validate_audio_format(self):
        if self.audio_format not in self.audio_formats:
            self.audio_format = self.default_audio_format
