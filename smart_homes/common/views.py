import base64
import logging
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from django.contrib import messages
from django.conf import settings
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from smart_homes.common.forms import ContactForm


# UserModel = get_user_model()

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
    success_url = "/contact/"

    def form_valid(self, form):
        data = form.cleaned_data

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        attachments = []
        plan = data.get("plan")
        if plan:
            try:
                file_content = plan.read()
                attachments.append({
                    "content": base64.b64encode(file_content).decode("utf-8"),
                    "name": plan.name
                })
                plan.seek(0)
            except Exception as e:
                messages.error(self.request, f"Error processing file: {str(e)}")
                return super().form_invalid(form)

        sender_name = "SmartHomes Contact Form"
        email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": settings.CONTACT_TO_EMAIL}],
            sender={"email": settings.CONTACT_TO_EMAIL, "name": sender_name},
            subject=f"Inquiry from {data['name']} for smart home system.",
            html_content=f"""
                <p><strong>Name:</strong> {data['name']}</p>
                <p><strong>Email:</strong> {data['email']}</p>
                <p><strong>Phone:</strong> {data.get('phone') or '-'}</p>
                <p><strong>Type:</strong> {data['type']}</p>
                <p><strong>Message:</strong><br>{data['message']}</p>
            """,
            attachment=attachments if attachments else None
        )

        try:
            response = api_instance.send_transac_email(email)
            messages.success(self.request, "Thank you! We will contact you soon.")
        except ApiException as e:
            messages.error(self.request, f"Error sending email: {e.body}")
            return super().form_invalid(form)

        return super().form_valid(form)

