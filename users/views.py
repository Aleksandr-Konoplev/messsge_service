import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy, reverse

from sending_messages.models import MailingAttempt
from users.forms import UserRegisterForm
from users.models import User
from config.settings import EMAIL_HOST_USER
from sending_messages.mixins import OwnerOrManagerMixin


#############################
### Создание пользователя ###
#############################
class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        send_mail(
            subject="Активация аккаунта",
            message=f"Перейдите по ссылке: {url} для регистрации аккаунта",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.is_email_verified = True
    user.save()
    return redirect(reverse("users:login"))


############################
### Профиль пользователя ###
############################
class ProfileView(OwnerOrManagerMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user_obj"] = user

        context["attempts"] = (
            MailingAttempt.objects
            .filter(mailing__owner=user)
            .select_related("mailing", "recipient")
            .order_by("-created_at")
        )

        return context