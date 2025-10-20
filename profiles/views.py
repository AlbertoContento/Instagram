from django.urls import reverse_lazy
from django.views.generic import UpdateView
from profiles.models import UserProfile
from .forms import ProfileUpdateForm

class ProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = ProfileUpdateForm
    template_name = 'profiles/profile_update.html'
    success_url = reverse_lazy('profile_detail')