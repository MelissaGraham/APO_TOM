from django.views.generic import TemplateView
from tom_targets.models import Target
from tom_observations.models import ObservationRecord


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        return {'targets': Target.objects.all(),'observations':ObservationRecord.objects.all()}
