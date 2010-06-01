# Create your views here.

try:
    import json
except ImportError:
    import simplejson as json

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import datetime
import glob
import os
import tarfile

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect

import settings

from forms import ContactForm, SubmitForm, PresetForm

def render(request, template, params = {}, mimetype = 'text/html'):
    """
        Render a response with the proper request context so that all
        variables expected in templates are indeed there from installed
        apps and middleware.
    """
    return render_to_response(template, params, mimetype = mimetype,
                               context_instance = RequestContext(request))

def about(request):
    return render(request, "about.html")

def presets(request):
    presets = []
    
    search_path = os.path.join(settings.MEDIA_ROOT, "presets", "*.json")
    
    for filename in glob.glob(search_path):
        presets.append(json.load(open(filename)))
        presets[-1]["name"] = os.path.basename(filename)[:-5]
        if presets[-1]["make"] != "Generic":
            presets[-1]["display_name"] = presets[-1]["make"] + " " + presets[-1]["model"]
        else:
            presets[-1]["display_name"] = presets[-1]["model"]

    return render(request, "presets/list.html", {
        "presets": sorted(presets, lambda x,y: cmp(x["display_name"], y["display_name"])),
    })

def preset_submit(request):
    if request.method == "POST":
        form = SubmitForm(request.POST, request.FILES)
        
        if form.is_valid():
            preset = request.FILES["preset_file"]
            message = EmailMessage(**{
                "subject": "[Arista] Preset for %s" % preset.name[:-5],
                "body": "A user has uploaded a new preset!",
                "from_email": form.cleaned_data["email"],
                "to": [x[1] for x in settings.ADMINS],
                "attachments": [
                    (preset.name, preset.read(), "application/x-bzip-compressed-tar"),
                ],
            })
            
            message.send()
        
            return HttpResponseRedirect("/presets/?thanks=1")
    else:
        form = SubmitForm()
    
    return render(request, "presets/submit.html", {
        "form": form,
    })

def preset_create(request):
    if request.method == "POST":
        form = PresetForm(request.POST, request.FILES)
        
        if form.is_valid():
            response = HttpResponse(mimetype="application/x-bzip-compressed-tar")
            response["Content-Disposition"] = "attachment; filename=%s.tar.bz2" % form.cleaned_data["short_name"]
            
            tar = tarfile.open(fileobj=response, mode="w:bz2")
            
            json = StringIO.StringIO()
            json.write(form.preset_json)
            json.seek(0)
            info = tarfile.TarInfo(name=form.cleaned_data["short_name"] + ".json")
            info.size = len(json.getvalue())
            tar.addfile(info, fileobj=json)
            
            icon = StringIO.StringIO()
            icon.write(request.FILES["icon"].read())
            icon.seek(0)
            info = tarfile.TarInfo(name=request.FILES["icon"].name)
            info.size = request.FILES["icon"].size
            tar.addfile(info, fileobj=icon)
            
            tar.close()
            
            return response
    else:
        form = PresetForm()
    
    return render(request, "presets/create.html", {
        "form": form,
    })

def screenshots(request):
    return render(request, "screenshots.html")

def downloads(request):
    data = json.loads(open(os.path.join(settings.MEDIA_ROOT, "downloads.json")).read())
    
    for release in data:
        release[1] = datetime.datetime.fromtimestamp(release[1])
    
    return render(request, "downloads.html", {
        "data": data,
    })

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        
        if form.is_valid():
            send_mail("[Arista] " + form.cleaned_data["title"], form.cleaned_data["message"], form.cleaned_data["email"], [x[1] for x in settings.ADMINS])
            
            return HttpResponseRedirect("/contact/thanks")
    else:
        form = ContactForm()

    return render(request, "contact.html", {
        "form": form,
    })

def thanks(request):
    return render(request, "thanks.html")

