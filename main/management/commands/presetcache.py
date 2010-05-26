try:
    import json
except ImportError:
    import simplejson as json

import glob
import os
import subprocess

from django.core.management.base import BaseCommand, CommandError

import settings

class Command(BaseCommand):
    args = '[device_short_name]'
    help = 'Update the presets cache (tar archives and latest.txt)'
    search_path = os.path.join(settings.MEDIA_ROOT, "presets")

    def handle(self, *args, **options):
        if len(args):
            device = json.load(open(os.path.join(self.search_path, args[0] + ".json")))
            self.gentar(args[0], device)
        else:
            # All files
            latest = []
            
            for filename in glob.glob(os.path.join(self.search_path, "*.json")):
                device = json.load(open(filename))
                short_name = os.path.basename(filename)[:-5]
                latest.append("%s, %s" % (short_name, device["version"]))
                self.gentar(short_name, device)
            
            open(os.path.join(self.search_path, "latest.txt"), "w").write("\n".join(sorted(latest)))
    
    def gentar(self, short_name, device):
        images = []
        
        if "icon" in device:
            images.append(device["icon"][7:])
        
        for preset in device["presets"]:
            if "icon" in preset:
                images.append(preset["icon"][7:])
        
        os.chdir(self.search_path)
        archive = short_name + ".tar.bz2"
        files = " ".join([short_name + ".json"] + images)
        cmd = "tar -cjf %s %s" % (archive, files)
        print "Creating %s (version %s)" % (archive, device["version"])
        subprocess.call(cmd, shell=True)   

