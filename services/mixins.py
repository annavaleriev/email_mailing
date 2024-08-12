from django.forms import inlineformset_factory

from services.forms import MessageForm
from services.models import Message


class CreateViewMixin:
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class SendMailFormsetMixin:
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessagesFormSet = inlineformset_factory(self.model, Message, form=MessageForm, extra=1)  # Создание формсета
        if self.request.POST:
            formset = MessagesFormSet(self.request.POST, instance=self.object)
        else:
            formset = MessagesFormSet(instance=self.object)
        context_data["formset"] = formset
        return context_data
