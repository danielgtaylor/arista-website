import os

from django import forms
from django.forms import widgets

import settings

REGEX_RANGE = "[0-9]+,\s?[0-9]+"
REGEX_RANGE_FLOAT = "[0-9.]+,\s?[0-9.]+"

class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField()
    message = forms.CharField(widget=widgets.Textarea())

class SubmitForm(forms.Form):
    email = forms.EmailField()
    preset_file = forms.FileField()

class PresetForm(forms.Form):
    template = unicode(open(os.path.join(settings.PROJECT_ROOT, "media", "template.json")).read())

    author_name = forms.CharField()
    author_email = forms.EmailField()
    short_name = forms.CharField(help_text="A short, one-word, unique identifier")
    make = forms.CharField(help_text="The manufacturer of this device, e.g. 'Apple'", initial="Generic")
    model = forms.CharField(help_text="The model of this device, e.g. 'iPhone'")
    description = forms.CharField(help_text="A short description, e.g. 'H.264/AAC in MP4 for iPhones")
    icon = forms.FileField(help_text="An SVG or PNG file")
    container = forms.ChoiceField(choices = [
        ("qtmux", "MP4"),
        ("webmmux", "WebM"),
        ("matroskamux", "Matroska"),
        ("avimux", "AVI"),
        ("mpegtsmux", "MPEG-TS"),
        ("ffmux_dvd", "DVD"),
        ("oggmux", "Ogg"),
    ])
    video_codec = forms.ChoiceField(choices = [
        ("x264enc", "H.264"),
        ("vp8enc", "VP8"),
        ("xvidenc", "MPEG4"),
        ("mpeg2enc", "MPEG2 DVD"),
        ("theoraenc", "Theora"),
    ])
    video_quality = forms.ChoiceField(choices = [
        ("worst", "Worst (small files)"),
        ("worse", "Worse"),
        ("good", "Good"),
        ("better", "Better"),
        ("best", "Best (large files)"),
    ], help_text="Visual quality where bitrate is automatically determined", initial="good")
    video_bitrate = forms.IntegerField(help_text="The video bitrate in kbps", initial=4000)
    width = forms.RegexField(regex=REGEX_RANGE, help_text="Range of allowed widths, like 'min, max'", initial="120, 1280")
    height = forms.RegexField(regex=REGEX_RANGE, help_text="Range of allowed heights, like 'min, max'", initial="120, 720")
    framerate = forms.RegexField(regex=REGEX_RANGE_FLOAT, help_text="Range of allowed framerates, like 'min, max'", initial="1, 30")
    audio_codec = forms.ChoiceField([
        ("faac", "AAC"),
        ("lame", "MP3"),
        ("vorbisenc", "Vorbis"),
        ("ffenc_ac3", "AC3"),
    ])
    audio_bitrate = forms.IntegerField(help_text="The audio bitrate in kbps", initial=128)
    audio_channels = forms.RegexField(regex=REGEX_RANGE, help_text="Range of allowed channels, like 'min, max'", initial="1, 2")
    
    def clean_icon(self):
        data = self.cleaned_data["icon"]
        
        if data.size > 1024 ** 2:
            raise forms.ValidationError("File size must be under 1 MiB")
        
        return data
    
    @property
    def extension(self):
        return {
            "qtmux": "mp4",
            "matroskamux": "mkv",
            "avimux": "avi",
            "ffmux_dvd": "mpg",
            "oggmux": "ogg",
            "webmmux": "webm",
        }.get(self.cleaned_data["container"], "mp4")
    
    @property
    def x264_video_quality(self):
        return {
            "worst": 27.0,
            "worse": 24.0,
            "good": 21.0,
            "better": 19.0,
            "best": 18.0,
        }.get(self.cleaned_data["video_quality"], 21.0)
    
    @property
    def vp8_video_quality(self):
        return {
            "worst": 2,
            "worse": 4,
            "good": 5,
            "better": 6,
            "best": 8,
        }.get(self.cleaned_data["video_quality"], 5)
    
    @property
    def xvid_video_quality(self):
        return {
            "worst": 10.0,
            "worse": 8.0,
            "good": 5.0,
            "better": 3.0,
            "best": 2.0,
        }.get(self.cleaned_data["video_quality"], 5)
    
    @property
    def theora_video_quality(self):
        return {
            "worst": 15,
            "worse": 30,
            "good": 40,
            "better": 60,
            "best": 80,
        }.get(self.cleaned_data["video_quality"], 40)
    
    @property
    def video_pass(self):
        cleaned = self.cleaned_data
        
        return {
            "x264enc": "pass=qual quantizer=%d subme=6 cabac=0 threads=0" % self.x264_video_quality,
            "vp8enc": "quality=%d threads=%%(threads)s speed=2" % self.vp8_video_quality,
            "xvidenc": "pass=quant quantizer=%d max-bframes=0 trellis=true" % self.xvid_video_quality,
            "mpeg2enc": "format=9 bitrate=%s" % self.cleaned_data["video_bitrate"],
            "theoraenc": "border=0 quality=%d keyframe-freq=30" % self.theora_video_quality,
        }.get(cleaned["video_codec"], "")
    
    @property
    def audio_pass(self):
        cleaned = self.cleaned_data
        
        return {
            "faac": "bitrate=%d profile=LC" % (int(cleaned["audio_bitrate"]) * 1024),
            "lame": "bitrate=%s" % cleaned["audio_bitrate"],
            "vorbisenc": "bitrate=%d" % (int(cleaned["audio_bitrate"]) * 1024),
            "ffenc_ac3": "bitrate=%d" % (int(cleaned["audio_bitrate"]) * 1024),
        }.get(cleaned["audio_codec"], "")
    
    @property
    def audio_container(self):
        cleaned = self.cleaned_data
        return {
            "lame": "",
        }.get(cleaned["audio_codec"], cleaned["container"])
    
    @property
    def preset_json(self):
        cleaned = self.cleaned_data
        return self.template % {
            "make": cleaned["make"],
            "model": cleaned["model"],
            "description": cleaned["description"],
            "version": "1.0",
            "author_name": cleaned["author_name"],
            "author_email": cleaned["author_email"],
            "icon": cleaned["icon"].name,
            "extension": self.extension,
            "container": cleaned["container"],
            "video_name": cleaned["video_codec"],
            "video_container": cleaned["container"],
            "width": cleaned["width"],
            "height": cleaned["height"],
            "rate": cleaned["framerate"],
            "video_pass": self.video_pass,
            "audio_name": cleaned["audio_codec"],
            "audio_container": self.audio_container,
            "audio_pass": self.audio_pass,
            "audio_channels": cleaned["audio_channels"],
        }
    

