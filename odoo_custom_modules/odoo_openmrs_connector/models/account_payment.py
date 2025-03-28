from itertools import groupby
from odoo import models, fields, api
import logging
logger = logging.getLogger(__name__)

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def get_invoice_lines(self):
        provider_name = []
        provider_namet = ""
        taxes = 0.0
        amount_untaxed = 0.0
        discount = 0.0
        bill_amount = 0.0
        invoice_data = {'taxes': 0.0,
                        'amount_untaxed': 0.0,
                        'discount': 0.0,
                        'net_amount': 0.0,
                        'previous_balance': 0.0,
                        'bill_amount': 0.0,
                        'paid_amount': 0.0,
                        'outstanding_balance': 0.0}
        invoice_lines = []
        for inv in self.invoice_ids:
            sale_order = self.env['sale.order'].search([('name', '=', inv.origin)])
            if sale_order.provider_name:
                provider_name.append(sale_order.provider_name.name)
                provider_namet=sale_order.provider_name.name
            taxes += inv.amount_tax
            amount_untaxed += inv.amount_untaxed
            discount += inv.discount
            bill_amount += inv.amount_total
            for line in inv.invoice_line_ids:
                invoice_lines.append({'product_name': line.product_id.name,
                                      'expiry_date': line.expiry_date,
                                      'quantity': line.quantity,
                                      'price_unit': line.price_unit,
                                      'price_subtotal': line.price_subtotal})
        invoice_data['invoice_lines'] = invoice_lines
        if provider_name:
            print "provider_name:", provider_name
            invoice_data['provider_name'] = ','.join(str(provider_name))
            invoice_data['provider_namet'] = provider_namet
        else:
            invoice_data['provider_name'] = ''
        invoice_data['taxes'] = taxes
        invoice_data['amount_untaxed'] = amount_untaxed
        invoice_data['discount'] = discount
        invoice_data['net_amount'] = invoice_data['taxes'] + invoice_data['amount_untaxed'] - invoice_data['discount']
        invoice_data['outstanding_balance'] = self.partner_id.credit or self.partner_id.debit
        invoice_data['paid_amount'] = self.amount
        invoice_data['previous_balance'] = invoice_data['outstanding_balance'] - (bill_amount - invoice_data['paid_amount'])
        invoice_data['bill_amount'] = invoice_data['net_amount'] + invoice_data['previous_balance']
        return invoice_data