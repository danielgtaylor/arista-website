# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from forms import ContactForm

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
    return render(request, "presets/list.html")

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

