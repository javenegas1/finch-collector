from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from django.urls import reverse

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

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

class CarDetail(DetailView):
    model = Car
    template_name = "car_detail.html"

class CarCreate(CreateView):
    model = Car
    fields = ['make', 'model', 'image', 'bio']
    template_name = "car_create.html"

    def get_success_url(self):
        return reverse('car_detail', kwargs={'pk': self.object.pk})

class CarUpdate(CreateView):
    model = Car
    fields = ['make', 'model', 'image', 'bio']
    template_name = "car_update.html"

    def get_success_url(self):
        return reverse('car_detail', kwargs={'pk': self.object.pk})

class CarDelete(DeleteView):
    model = Car
    template_name = "car_delete_confirm.html"
    success_url = "/cars/"