from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.views import View

from analytics.models import ClickEvent
from .forms import SubmitUrlForm
from .models import KirrURL

# Create your views here.

def home_view_fbv(request,*args,**kwargs):
    if request.method =="POST":
        print(request.POST)
    return render(request,'shortener/home.html',context)

class HomeView(View):
    def get(self,request,*arg,**kwargs):
        the_form = SubmitUrlForm()
        context = {
            "title":"Kirr.co",
            "form":the_form
        }
        return render(request,"shortner/home.html",context)

    def post(self,request,*arg,**kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "title":"Kirr.co",
            "form":form
        }
        template = 'shortener/home.html'
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj,created = KirrURL.objects.get_or_create(url=new_url)
            context = {
                "object": obj,
                "created": created,
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"
        return render(request,template,context)



class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = KirrURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)