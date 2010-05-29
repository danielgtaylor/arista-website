try:
    import json
except ImportError:
    import simplejson as json

import os
import time

from django.core.management.base import BaseCommand, CommandError

from github2.client import Github

import settings

class Command(BaseCommand):
    args = ''
    help = 'Update the downloads cache (used to render the downloads page)'

    def handle(self, *args, **options):
        github = Github()
        
        data = []
        
        tags = github.repos.tags("danielgtaylor/arista")
        
        for tag_name in sorted(tags.keys(), reverse=True):
            commit = github.commits.show("danielgtaylor/arista", tags[tag_name])
            data.append([tag_name, time.mktime(commit.authored_date.timetuple()), commit.id])
        
        open(os.path.join(settings.MEDIA_ROOT, "downloads.json"), "w").write(json.dumps(data, indent=4))
        
        print "Downloads cache updated."

