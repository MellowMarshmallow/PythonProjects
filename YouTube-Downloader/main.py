#!/usr/bin/env python3


# dependencies
import argparse
from shutil import which
import sys
import validators
import youtube_dl


class Logger:

    def debug(self, message):
        pass

    def error(self, message):
        print(f'[error] {message}')

    def warning(self, message):
        pass


class App:

    DEFAULT_FORMAT = 'm4a'
    ALLOWED_FORMATS = ('aac', 'flac', 'mp3', 'm4a', 'opus', 'vorbis', 'wav')

    def __init__(self, argument):
        parsed_argument = self.parse_arguments(argument)

        # set instance variables
        self.file_format = parsed_argument.file_format
        self.urls = parsed_argument.urls

        self.ydl_options = {
            'format': f'bestaudio[ext={App.DEFAULT_FORMAT}]',
            'outtmpl': '%(title)s.%(ext)s',
            'logger': Logger(),
            'progress_hooks': [self.post_transaction_hook],
        }

    def parse_arguments(self, argument):
        parser = argparse.ArgumentParser(description='Audio downloader for YouTube.')

        # optional argument
        parser.add_argument('-f', '--format', nargs=1, default=App.DEFAULT_FORMAT,
                            choices=App.ALLOWED_FORMATS, help='File format of the download(s).',
                            dest='file_format')

        # position argument (required)
        parser.add_argument('urls', nargs='+', help='Complete URL(s) to YouTube video(s).',
                            metavar='URL')

        return parser.parse_args(argument)

    def post_transaction_hook(self, download):
        bytes_to_mb = lambda byte: round(download['total_bytes'] / 1_000_000, 2)

        if download['status'] == 'finished':
            print('Done downloading, now converting...',
                  f'\t[FILENAME]: {download["filename"]}',
                  f'\t[SIZE]: {bytes_to_mb(download["total_bytes"])} MB', sep='\n')

    def validate_urls(self):
        for url in self.urls:
            if not validators.url(url):
                return False
        return True

    def is_extract_audio_supported(self):
        is_tool = lambda tool: which(tool) is not None

        # extract audio requires `ffmpeg` and `ffprobe`
        # or `avconv` and `avprobe`, but the last two
        # are not currently supported by this program
        return is_tool('ffmpeg') and is_tool('ffprobe')

    def download(self):
        with youtube_dl.YoutubeDL(self.ydl_options) as ydl:
            ydl.download(self.urls)


if __name__ == '__main__':
    instance = App(sys.argv[1:])

    if not instance.validate_urls():
        print('[error] Invalid web address(es).')
        sys.exit(2)
    elif instance.file_format != App.DEFAULT_FORMAT:
        if not instance.is_extract_audio_supported():
            print('[error] File format not supported (missing tools)')
            sys.exit(2)
        else:
            instance.ydl_options['format'] = 'bestaudio/best'
            instance.ydl_options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': instance.file_format[0],
                'preferredquality': '192',
            }]

    instance.download()
