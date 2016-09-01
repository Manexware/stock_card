import time
from openerp import api, models
from ..model import stock_card

class ReportKardex(models.AbstractModel):
    _name = 'report.stock_card.kardex'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        # product = self.env['product.product'].browse(data['product_id'])
        stock_cards = []
        if data['all']:
            products = self.env['product.product'].search([])
            for record in products:
                stock_card = self.env['stock.card.product'].create({'product_id': record.id,
                                                                    'start_date': data['start_date'],
                                                                    'end_date': data['end_date']})
                stock_card.stock_card_move_get()
                stock_cards.append(stock_card)
        else:
            for record in data['product_ids']:
                stock_card = self.env['stock.card.product'].create({'product_id': record,
                                                                    'start_date':data['start_date'],
                                                                    'end_date': data['end_date']})
                stock_card.stock_card_move_get()
                stock_cards.append(stock_card)
        report = report_obj._get_report_from_name('stock_card.kardex')
        elaborado = self.env.user.partner_id.name
        employee = self.env['hr.employee'].search([('user_id','=',self.env.user.id)])
        docargs = {
            'doc_ids': self.ids,
            # 'product': product,
            # 'stock_card_move_ids': stock_card.stock_card_move_ids,
            'stock_cards':stock_cards,
            'elaborado': elaborado,
            'responsable': employee.parent_id.name,
            'departamento': employee.department_id.name,
            'start_date': data['start_date'],
            'end_date': data['end_date']
        }
        return report_obj.render('stock_card.kardex', docargs)