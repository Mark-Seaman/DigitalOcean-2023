from django.views.generic import CreateView, TemplateView, UpdateView

from course.course import course_settings
from course.models import UrlGame
from course.urlgame import check_answer, generate_url_question


class UrlGameStart(CreateView):
    template_name = "urlgame-start.html"
    model = UrlGame
    fields = ['name']

    def get_success_url(self):
        return f'url-question/{self.object.pk}'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(course_settings(**self.kwargs))
        return kwargs

    def form_valid(self, form):
        name = form.cleaned_data['name']
        UrlGame.objects.filter(name=name).delete()
        return super().form_valid(form)


class UrlGameQuestion(UpdateView):
    template_name = "urlgame.html"
    model = UrlGame
    fields = ['answer']

    def get_context_data(self, **kwargs):
        game = UrlGame.objects.get(pk=self.kwargs.get('pk'))
        game.question  = generate_url_question()
        game.answer = None
        game.save()
        kwargs.update(course_settings(**self.kwargs))

        done = self.object.left < 1
        kwargs.update(dict(q=game.question, game=game, all_done=done))
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        game = UrlGame.objects.get(pk=self.kwargs.get('pk'))
        check_answer(game)
        return response

    def get_success_url(self):
        return f'../url-answer/{self.object.pk}'


class UrlGameAnswer(TemplateView):
    template_name = "urlgame.html"

    def get_context_data(self, **kwargs):
        game = UrlGame.objects.get(pk=self.kwargs.get('pk'))
        kwargs.update(course_settings(**self.kwargs))
        done = game.left < 1
        kwargs.update(dict(object=game, q=eval(game.question), a=game.answer, all_done=done))
        # game.answer = None
        # game.save()
        return kwargs


