from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views import View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls import reverse

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

from .models import Car, Sale, Wishlist

class Signup(View):
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("artist_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wishlists"] = Wishlist.objects.all()
        return context


class About(TemplateView):
    template_name = 'about.html'

@method_decorator(login_required, name='dispatch')
class CarsList(TemplateView):
    template_name = "cars_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        make = self.request.GET.get('make')

        if make != None:
            context["cars"] = Car.objects.filter(make__icontains=make, user=self.request.user)
            # We add a header context that includes the search param
            context["header"] = f"Searching for {make}"
        else:
            context["cars"] = Car.objects.filter(user=self.request.user)
            # default header for not searching 
            context["header"] = "Classic Cars"
        return context

class CarDetail(DetailView):
    model = Car
    template_name = "car_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wishlists"] = Wishlist.objects.all()
        return context

class CarCreate(CreateView):
    model = Car
    fields = ['make', 'model', 'image', 'bio']
    template_name = "car_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CarCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('car_detail', kwargs={'pk': self.object.pk})

class CarUpdate(UpdateView):
    model = Car
    fields = ['make', 'model', 'image', 'bio']
    template_name = "car_update.html"

    def get_success_url(self):
        return reverse('car_detail', kwargs={'pk': self.object.pk})

class CarDelete(DeleteView):
    model = Car
    template_name = "car_delete_confirm.html"
    success_url = "/cars/"

#create sale
class SaleCreate(CreateView):

    def post(self, request, pk):
        owner = request.POST.get("owner")
        price = request.POST.get("price")
        make = Car.objects.get(pk=pk)
        Sale.objects.create(owner=owner, price=price, make=make)
        return redirect('car_detail', pk=pk)

#wishlist
class WishlistSaleAssoc(View):

    def get(self, request, pk, song_pk):
        # get the query param from the url
        assoc = request.GET.get("assoc")
        if assoc == "remove":
            # get the playlist by the id and
            # remove from the join table the given song_id
            Wishlist.objects.get(pk=pk).sales.remove(sale_pk)
        if assoc == "add":
            # get the playlist by the id and
            # add to the join table the given song_id
            Wishlist.objects.get(pk=pk).sales.add(sale_pk)
        return redirect('home')