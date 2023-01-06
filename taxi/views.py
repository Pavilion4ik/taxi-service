from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from taxi.models import Driver, Car, Manufacturer


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5
    queryset = Manufacturer.objects.all()


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer
    template_name = "taxi/cars_of_manufacturer.html"


class ManufacturerCreateView(
    SuccessMessageMixin, LoginRequiredMixin, generic.CreateView
):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Manufacturer wa added!"


class ManufacturerUpdateView(
    SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView
):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Manufacturer was updated!"


class ManufacturerDeleteView(
    SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView
):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Manufacturer was deleted!"

