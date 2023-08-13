from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = get_user_model().objects.filter(email=email).first()
        if user is not None and user.check_password(password):
            print(f'username: {user.username}, email: {user.email}')
            login(request, user)
            # Replace 'home' with the name of your desired redirect URL
            return redirect('home')
        else:
            print(f'FAILED --  email: {email}')
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


@login_required
def home_view(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'home.html', context)
