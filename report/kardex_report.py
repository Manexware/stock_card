import time
from openerp import api, models
from ..model import stock_card

class ReportKardex(models.AbstractModel):
    _name = 'report.stock_card.kardex'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        product = self.env['product.product'].browse(data['product_id'])
        stock_card = self.env['stock.card.product'].create({'product_id': product.id})
        # stock_card.product_id = product
        stock_card.stock_card_move_get()
        # stock_card.stock_card_move_get()
        report = report_obj._get_report_from_name('stock_card.kardex')
        docargs = {
            'doc_ids': self.ids,
            'product': product,
            'stock_card_move_ids': stock_card.stock_card_move_ids,
        }
        return report_obj.render('stock_card.kardex', docargs)