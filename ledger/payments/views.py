import json
from datetime import date
from django.views import generic
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse
from ledger.payments.pdf import create_invoice_pdf_bytes
from ledger.payments.utils import checkURL
from ledger.payments.cash.models import REGION_CHOICES
#
from ledger.payments.models import Invoice
#

class InvoicePDFView(generic.View):
    def get(self, request, *args, **kwargs):
        invoice = get_object_or_404(Invoice, reference=self.kwargs['reference'])
        response = HttpResponse(content_type='application/pdf')
        response.write(create_invoice_pdf_bytes('invoice.pdf',invoice))

        return response

class InvoiceDetailView(generic.DetailView):
    model = Invoice
    template_name = 'dpaw_payments/invoice/invoice.html'
    context_object_name = 'invoice'

    def get_object(self):
        invoice = get_object_or_404(Invoice, reference=self.kwargs['reference'])
        return invoice

class PaymentErrorView(generic.TemplateView):
    template_name = 'dpaw_payments/payment_error.html'

class InvoiceSearchView(generic.TemplateView):

    template_name = 'dpaw_payments/invoice/invoice_search.html'

class InvoicePaymentView(generic.DetailView):
    template_name = 'dpaw_payments/invoice/payment.html'
    num_years = 10
    context_object_name = 'invoice'

    def get_object(self):
        invoice = get_object_or_404(Invoice, reference=self.kwargs['reference'])
        return invoice

    def month_choices(self):
        return ["%.2d" %x for x in range(1,13)]

    def year_choices(self):
        return [x for x in range(
            date.today().year,
            date.today().year + self.num_years
        )]

    def get_context_data(self, **kwargs):
        ctx = super(InvoicePaymentView, self).get_context_data(**kwargs)
        ctx['months'] = self.month_choices
        ctx['years'] = self.year_choices
        ctx['regions'] = list(REGION_CHOICES)
        if self.request.GET.get('amountProvided') == 'true':
            ctx['amountProvided'] = True
        if self.request.GET.get('redirect_url'):
            try:
                checkURL(self.request.GET.get('redirect_url'))
                ctx['redirect_url'] = self.request.GET.get('redirect_url')
            except:
                pass
        if self.request.GET.get('custom_template'):
            try:
                ctx['custom_block'] = get_template(self.request.GET.get('custom_template'))
            except TemplateDoesNotExist as e:
                pass
        return ctx
