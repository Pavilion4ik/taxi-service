from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Driver, Car, Manufacturer, Comment, Rating
from .forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm,
    CommentForm,
    DriverAvatarUpdateForm,
    CarImageUpdateForm,
    SignUpForm,
    LoginForm,
)


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ManufacturerListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = ManufacturerSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)
        return self.queryset


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer
    template_name = "taxi/cars_of_manufacturer.html"


class ManufacturerCreateView(
    SuccessMessageMixin, LoginRequiredMixin, generic.CreateView
):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Manufacturer was added!"


class ManufacturerUpdateView(
    SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView
):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")
    fields = "__all__"
    template_name = "taxi/manufacturer_form.html"
    success_message = "Manufacturer was updated!"


class ManufacturerDeleteView(
    SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView
):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Manufacturer was deleted!"


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = (
        Car.objects.all()
        .prefetch_related("comments")
        .prefetch_related("drivers")
        .select_related("manufacturer")
    )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)

        model = self.request.GET.get("model", "")

        context["search_form"] = CarSearchForm(initial={"model": model})

        return context

    def get_queryset(self):
        model = self.request.GET.get("model")

        if model:
            return self.queryset.filter(model__icontains=model)
        return self.queryset


class CarDetailView(SuccessMessageMixin, LoginRequiredMixin, generic.DetailView):
    model = Car
    form = CommentForm
    success_message = "Comment was added!"
    queryset = Car.objects.all().prefetch_related("comments").all()

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            car = self.get_object()
            form.instance.user = request.user
            form.instance.car = car
            form.save()
            return redirect(reverse_lazy("taxi:car-detail", args=[str(car.id)]))

    def get_context_data(self, **kwargs):
        context = super(CarDetailView, self).get_context_data(**kwargs)
        num_comments = Comment.objects.all().filter(car=self.object.id).count()
        car_comments = Comment.objects.all().filter(car=self.object.id)
        context.update(
            {
                "comment_form": self.form,
                "car_comments": car_comments,
                "num_comments": num_comments,
            }
        )
        return context


class CarCreateView(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    success_message = "Car was created!"


class CarUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_message = "Car was successfully updated!"

    def get_success_url(self, **kwargs):
        return reverse_lazy("taxi:car-detail", kwargs={"pk": self.get_object().id})


class CarDeleteView(SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    success_message = "Car was successfully deleted!"


class CarImageUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarImageUpdateForm
    template_name = "taxi/car_image_update.html"
    success_message = "Image was successfully updated!"

    def get_success_url(self, **kwargs):
        return reverse_lazy("taxi:car-detail", kwargs={"pk": self.get_object().id})


class CommentDeleteView(SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView):
    model = Comment
    success_url = reverse_lazy("")
    success_message = "Comment successfully deleted!"

    def get_success_url(self, **kwargs):
        return reverse_lazy("taxi:car-detail", kwargs={"pk": self.get_object().car.id})


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5
    queryset = Driver.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DriverListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = DriverSearchForm(initial={"username": username})

        return context

    def get_queryset(self):
        username = self.request.GET.get("username")

        if username:
            return self.queryset.filter(username__icontains=username)
        return self.queryset


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    success_message = "Driver was successfully created!"


class DriverLicenseUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    success_message = "License number was successfully updated!"
    template_name = "taxi/driver_license_update.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy("taxi:driver-detail", kwargs={"pk": self.get_object().id})


class DriverAvatarUpdateView(
    SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView
):
    model = Driver
    form_class = DriverAvatarUpdateForm
    template_name = "taxi/avatar_update.html"
    success_message = "Avatar was successfully updated!"

    def get_success_url(self, **kwargs):
        return reverse_lazy("taxi:driver-detail", kwargs={"pk": self.get_object().id})


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")


@login_required
def toggle_assign_to_car(request, pk):
    driver = Driver.objects.get(id=request.user.id)
    if Car.objects.get(id=pk) in driver.cars.all():
        driver.cars.remove(pk)
    else:
        driver.cars.add(pk)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))


class RegisterCreateView(SuccessMessageMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:index")
    template_name = "registration/register.html"
    success_message = "Now you can login!"


def rate(request: HttpRequest, car_id: int, rating: int) -> HttpResponse:
    car = Car.objects.get(id=car_id)
    Rating.objects.filter(car=car, user=request.user).delete()
    car.rating_set.create(user=request.user, rating=rating)
    return index(request)


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = "Invalid credentials"
        else:
            msg = "Error validating the form"

    return render(request, "registration/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = "Account created successfully."
            success = True

            # return redirect("/login/")

        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(
        request,
        "registration/register.html",
        {"form": form, "msg": msg, "success": success},
    )
