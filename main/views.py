# Create your views here.

import json
import glob
import os

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect

import settings

from forms import ContactForm, SubmitForm

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
    print search_path
    for filename in sorted(glob.glob(search_path)):
        presets.append(json.load(open(filename)))
        presets[-1]["name"] = os.path.basename(filename)[:-5]

    return render(request, "presets/list.html", {
        "presets": presets,
    })

def preset_submit(request):
    if request.method == "POST":
        form = SubmitForm(request.POST, request.FILES)
        
        if form.is_valid():
            preset = request.FILES["preset_file"]
            icon = request.FILES["icon_file"]
            message = EmailMessage(**{
                "subject": "[Arista] Preset for %s" % preset.name[:-5],
                "body": "A user has uploaded a new preset!",
                "from_email": form.cleaned_data["email"],
                "to": settings.ADMINS,
                "attachments": [
                    (preset.name, preset.read(), "text/javascript"),
                    (icon.name, icon.read(), icon.name.endswith("svg") and "image/svg" or "image/png"),
                ],
            })
            
            message.send()
        
            return HttpResponseRedirect("/presets/?thanks=1")
    else:
        form = SubmitForm()
    
    return render(request, "presets/submit.html", {
        "form": form,
    })

def screenshots(request):
    return render(request, "screenshots.html")

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        
        if form.is_valid():
            send_mail("[Arista] " + form.cleaned_data["title"], form.cleaned_data["message"], form.cleaned_data["email"], settings.ADMINS)
            
            return HttpResponseRedirect("/contact/thanks")
    else:
        form = ContactForm()

    return render(request, "contact.html", {
        "form": form,
    })

