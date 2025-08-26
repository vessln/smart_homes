from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.conf import settings

from smart_homes.common.forms import ContactForm

UserModel = get_user_model()


# class HomePageView(generic_views.TemplateView):
#     template_name = "common/index.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # TODO add best sellers (products):
#         # context["best_sellers"] = ProductModel.objects.order_by("-sales_count")[:3]
#
#         return context


class ContactView(FormView):
    template_name = "common/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("common:contact")

    def form_valid(self, form):
        data = form.cleaned_data
        subject = f"[Contact] {data['type'].title()} inquiry from {data['name']}"
        body = (
            f"Name: {data['name']}\n"
            f"Email: {data['email']}\n"
            f"Phone: {data.get('phone') or '-'}\n"
            f"Type: {data['type']}\n\n"
            f"Message:\n{data['message']}"
        )
        to_addr = getattr(settings, "CONTACT_TO_EMAIL", None) or settings.DEFAULT_FROM_EMAIL

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_addr],
            reply_to=[data["email"]],
        )

        plan = data.get("plan")
        if plan:
            email.attach(plan.name, plan.read(), "application/pdf")
            plan.seek(0)

        email.send(fail_silently=False)
        messages.success(self.request, "Thanks! Your message has been sent.")
        return super().form_valid(form)

