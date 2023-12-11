from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import user_passes_test

from djangoBookstoreFinal.settings import BASE_DIR


# Registration (Signup) View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')  # Redirect to a page of your choice
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
# Login View
def login_view(request):
    def login_view(request):
        print("Looking for template in:", BASE_DIR / 'templates' / 'accounts' / 'login.html')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('book_list')  # Redirect to a page of your choice
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('book_list')  # Redirect to a suitable page after logout

