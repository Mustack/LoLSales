from django.views.generic import TemplateView


class ChampionView(TemplateView):

    template_name = "champions/champion.html"

    def get_context_data(self, **kwargs):
        context = super(ChampionView, self).get_context_data(**kwargs)
        return context
