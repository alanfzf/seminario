from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
class Dashboard(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('authenticate:login')
    template_name = 'start.html'

class AboutView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('authenticate:login')
    template_name = 'about.html'
