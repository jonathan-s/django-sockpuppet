from django.views.generic.base import TemplateView


class {{ class_name }}View(TemplateView):
    template_name = '{{ reflex_name|lower }}.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = 0
        return context
