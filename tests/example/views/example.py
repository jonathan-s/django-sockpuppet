from django.views.generic.base import TemplateView


class ExampleView(TemplateView):
    template_name = 'example.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.request.session.get('count', 0)
        return context
