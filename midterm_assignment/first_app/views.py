from django.shortcuts import render,redirect
from . import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import  logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.urls import reverse_lazy
from . import models
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.utils.decorators import method_decorator

# Create your views here.
def profile(request):
    if request.user.is_authenticated:
        orders = models.Order.objects.filter(user=request.user)
        return render(request, 'profile.html', {'orders' : orders})
    else:
        return redirect('registerpage')

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account Created Successfully')
                return redirect('loginpage')
        else:
            form = forms.RegisterForm()
        return render(request, 'register.html', {'form' : form, 'type' : 'Register'})
    else:
        return redirect('profilepage')


class UserLogin(LoginView):
    template_name = 'register.html'
    # success_url = reverse_lazy('profilepage')
    def get_success_url(self):
        return reverse_lazy('profilepage')

    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request, 'Information incorrcet')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context

def user_logout(request):
    logout(request)
    return redirect('loginpage')

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = forms.ChangeUseraData(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profilepage')
    else:
        form = forms.ChangeUseraData(instance = request.user)   
        return render(request, 'edit_profile.html', {'form' : form})
    
@method_decorator(login_required, name = 'dispatch')
class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profilepage')
    template_name = 'pass_change.html'
    def form_valid(self, form):
        messages.success(self.request, 'Password updated successfully')
        return super().form_valid(form)

class CarDetailView(DetailView):
    model = models.Car
    template_name = 'car_details.html'
    pk_url_kwarg = 'id'
    context_object_name = 'car'


    def post(self, request, *args, **kwargs):
        car = self.get_object()
        form = forms.CommentForm(data = self.request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.car = car
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object
        comments = car.comments.all()
        form = forms.CommentForm()
        context['comments'] = comments
        context['form'] = form

        return context
@login_required
def buy_car(request, id):
    car = models.Car.objects.get(pk=id)

    if car.quantity > 0:
        models.Order.objects.create(user=request.user, car=car)
        car.quantity -= 1
        car.save()
        messages.success(request, 'Car purchased successfully')
    else:
        messages.warning(request, 'This car is not available')
    return redirect('profilepage')