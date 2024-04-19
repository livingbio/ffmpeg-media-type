# ffmpeg-media-type

`ffmpeg-media-type` is a Python library that utilizes FFmpeg to detect various media file information, such as duration, width, and height. This library provides an easy-to-use interface for extracting essential details from media files by leveraging the powerful capabilities of FFmpeg.

[![CI](https://github.com/livingbio/ffmpeg-media-type/workflows/python-unittest/badge.svg?branch=main)](https://github.com/livingbio/ffmpeg-media-type/actions?query=workflow%3Apython-unittest++branch%3Amain++)
[![codecov](https://codecov.io/gh/livingbio/ffmpeg-media-type/graph/badge.svg?token=B95PR629LP)](https://codecov.io/gh/livingbio/ffmpeg-media-type)
[![pypi](https://img.shields.io/pypi/v/ffmpeg-media-type.svg)](https://pypi.python.org/pypi/ffmpeg-media-type)
[![downloads](https://pepy.tech/badge/ffmpeg-media-type/month)](https://pepy.tech/project/ffmpeg-media-type)
[![versions](https://img.shields.io/pypi/pyversions/ffmpeg-media-type.svg)](https://github.com/livingbio/ffmpeg-media-type)
[![license](https://img.shields.io/github/license/livingbio/ffmpeg-media-type.svg)](https://github.com/livingbio/ffmpeg-media-type/blob/main/LICENSE)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)



### Table of Contents

- [Documentation](https://livingbio.github.io/ffmpeg-media-type/)




## Installation

You can install `ffmpeg-media-type` via pip:

```bash
pip install ffmpeg-media-type
```

Note: FFmpeg must be installed on your system for this library to function correctly. Make sure you have FFmpeg installed and added to your system's PATH.



## Usage

To use `ffmpeg-media-type`, first import the library:



```python
import ffmpeg_media_type
```


### Detecting Media File Information

To detect media file information, use the `detect` function, providing the path to the media file as a parameter:



```python

media_info = ffmpeg_media_type.detect('https://raw.githubusercontent.com/livingbio/ffmpeg-media-type/main/docs/media/overlay.png')
media_info
```




    MediaInfo(type='image', width=163, height=117, duration=None, format='png_pipe', size=2212, suggest_ext='png')




The `detect` function returns a model containing the following information:

- `type`: The type of media file (e.g. `video`, `audio`, `image`, etc.).
- `duration`: The duration of the media file in seconds.
- `width`: The width of the media file in pixels.
- `height`: The height of the media file in pixels.
- `format`: The format of the media file (e.g. `mp4`, `mp3`, `png`, etc.).
- `size`: The size of the media file in bytes.
- `suggest_ext`: The suggested file extension for the media file (e.g. `mp4`, `mp3`, `png`, etc.).

Here's an example of how to access these details:



```python
duration = media_info.duration
width = media_info.width
height = media_info.height
```

### Example



```python
import ffmpeg_media_type

# Specify the path to the media file
file_path = 'https://raw.githubusercontent.com/livingbio/ffmpeg-media-type/main/docs/media/SampleVideo_1280x720_1mb.mp4'

# Detect media file information
media_info = ffmpeg_media_type.detect(file_path)

# Extract information from the media_info dictionary
duration = media_info.duration
width = media_info.width
height = media_info.height

# Print the extracted information
print(f"Duration: {duration} seconds")
print(f"Width: {width} pixels")
print(f"Height: {height} pixels")
```

    Duration: 5.312 seconds
    Width: 1280 pixels
    Height: 720 pixels



### Enhancing Accuracy in Guessing Media File Extensions with FFmpeg

- Typically, the media file's extension is utilized to determine its file type. Nevertheless, this approach may not always yield accurate results. For instance, a file bearing the `.mp4` extension could, in reality, be an audio file.
- The `ffmpeg-media-type` tool enhances the precision of media file extension guessing by leveraging the built-in format functionality of FFmpeg through the command `ffmpeg -formats`.

check [cache](https://github.com/livingbio/ffmpeg-media-type/tree/main/src/ffmpeg_media_type/cache) for details.

### Access ffprobe output

If you need to access the raw ffprobe output, you can use the `ffprobe` function:



```python
ffprobe_output = ffmpeg_media_type.ffprobe('https://raw.githubusercontent.com/livingbio/ffmpeg-media-type/main/docs/media/SampleVideo_1280x720_1mb.mp4')

ffprobe_output
```




    FFProbeInfo(format=FFProbeFormat(filename='https://raw.githubusercontent.com/livingbio/ffmpeg-media-type/main/docs/media/SampleVideo_1280x720_1mb.mp4', duration='5.312000', format_name='mov,mp4,m4a,3gp,3g2,mj2', format_long_name='QuickTime / MOV', start_time='0.000000', size='1055736', probe_score=100), streams=(FFProbeStream(index=0, width=1280, height=720, codec_type='video', codec_name='h264', codec_long_name='H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10', profile='Main', pix_fmt='yuv420p', r_frame_rate='25/1', tags=FFProbeStreamTags(rotate=0)), FFProbeStream(index=1, width=None, height=None, codec_type='audio', codec_name='aac', codec_long_name='AAC (Advanced Audio Coding)', profile='LC', pix_fmt=None, r_frame_rate='0/0', tags=FFProbeStreamTags(rotate=0))))



## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/livingbio/ffmpeg-media-type/issues). If you would like to contribute code, please fork the repository and submit a pull request.

Before submitting a pull request, make sure to run the tests using the following command:

```bash
poetry install --with dev
py.test src
```

Please ensure that your code follows the established coding style and passes all tests.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/livingbio/ffmpeg-media-type/blob/main/LICENSE) file for more information.
