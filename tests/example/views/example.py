from django.views.generic.base import TemplateView


class ExampleView(TemplateView):
    template_name = 'example.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.request.session.get('count', 0)
        context['otherCount'] = self.request.session.get('otherCount', 0)
        return context


class ParamView(TemplateView):
    template_name = 'param.html'

    def get(self, request, *args, **kwargs):
        kwargs.update(dict(self.request.GET.items()))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class TagExampleView(TemplateView):
    template_name = 'tag_example.html'

    def get(self, request, *args, **kwargs):
        kwargs.update({"parameter": "I am a parameter"})
        kwargs.update(dict(self.request.GET.items()))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class SecondTagExampleView(TemplateView):
    template_name = 'second_tag_example.html'

    def get(self, request, *args, **kwargs):
        kwargs.update({"parameter": "I am a parameter"})
        kwargs.update({"object_definition": {"controller": "abc", "reflex": "increment", "other_param": 123}})
        kwargs.update(dict(self.request.GET.items()))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
