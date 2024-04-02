from copy import copy

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View

from fajne_dane.consts import Platform
from users.exceptions import PasswordsNotMatch, EmailUsed, ObjectNotFound, ActivationTokenUsed, ActivationTokenExpired, \
    UserAlreadyActive
from users.models import User, ActivationToken
from users.serializers import UserRegistrationSerializer, ActivationTokenSerializer, PasswordResetSerializer


def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
    return None


def index_view(request):
    return render(request, 'users/index.html')


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate_user(email, password)

        context = {"errors": []}

        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect(self.request.GET.get('next', '/'))
            else:
                context['errors'].append("To konto nie zostało jeszcze aktywowane.")
        else:
            context['errors'].append("Wpisano niepoprawny email lub hasło.")

        return render(request, self.template_name, context)


class ExamplesView(View):
    template_name = 'examples/index.html'

    def get(self, request):
        return render(request, self.template_name)


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        context = {'errors': []}

        data = copy(request.POST)
        name_parts = data['name'].split()
        data['first_name'] = name_parts[0]
        data['last_name'] = " ".join(name_parts[1:])

        serializer = UserRegistrationSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                user = serializer.instance
                user.send_registration_email(Platform.API)
                return redirect('/')
            else:
                print(serializer.errors)

        except (PasswordsNotMatch, EmailUsed) as e:
            context['errors'].append(str(e))
        return render(request, self.template_name, context)




class ResetPasswordView(View):
    template_name = 'users/reset-password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        context = {'errors': []}
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        platform = request.GET.get("platform", Platform.API)
        if user:
            user.send_reset_password_email(platform=platform)
            return redirect(request.GET.get('next', '/'))
        else:
            context['errors'].append("Nie znaleziono użytkownika.")
        return render(request, self.template_name, context)


class ChangePasswordView(View):
    template_name = 'users/change-password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        context = {'errors': []}
        if 'token' in request.POST:
            context['token'] = request.POST['token']

        try:
            serializer = PasswordResetSerializer(data=request.POST)
            if serializer.is_valid():
                token = ActivationToken.objects.get(token=request.POST['token'])
                token.use()
                serializer.update(token.user, serializer.validated_data)
                return redirect(request.GET.get('next', '/'))
            else:
                context['errors'].append("Wypełnij wszystkie wymagane pola formularza.")
        except PasswordsNotMatch as e:
            context['errors'].append("Podane hasła są różne.")
        except ActivationTokenUsed as e:
            context['errors'].append("Ten token został już wykorzystany.")

        return render(request, self.template_name, context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(request.GET.get('next', '/'))



class ActivateView(View):
    template_name = 'users/activate.html'

    def get(self, request):
        context = {'errors': []}
        serializer = ActivationTokenSerializer(data=request.GET)
        try:
            if serializer.is_valid():
                token = serializer.retrieve()
                token.activate()
            else:
                context['errors'].append("Token aktywacyjny nie może być pusty.")
        except ObjectNotFound as e:
            context['errors'].append("Przekazany token aktywacyjny jest niepoprawny.")
        except UserAlreadyActive as e:
            context['errors'].append("Ten użytkownik został już aktywwowany.")
        except ActivationTokenUsed as e:
            context['errors'].append("Przekazany token aktywacyjny został już wykorzystany.")
        except ActivationTokenExpired as e:
            context['errors'].append("Przekazany token aktywacyjny wygasł.")
        return render(request, self.template_name, context)
