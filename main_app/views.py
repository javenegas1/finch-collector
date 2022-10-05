from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .models import Car


class Home(TemplateView):
    template_name = 'home.html'

class About(TemplateView):
    template_name = 'about.html'

class CarsList(TemplateView):
    template_name = "cars_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        make = self.request.GET.get('make')

        if make != None:
            context["cars"] = Car.objects.filter(make__icontains=make)
            # We add a header context that includes the search param
            context["header"] = f"Searching for {make}"
        else:
            context["cars"] = Car.objects.all()
            # default header for not searching 
            context["header"] = "Classic Cars"
        return context

class CarCreate(CreateView):
    model = Car
    fields = ['make', 'model', 'image', 'bio']
    template_name = "car_create.html"
    success_url = "/cars/"