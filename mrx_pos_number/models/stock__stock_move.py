# -*- coding: utf-8 -*-

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Add some extra fields to the model
    mrx_pos_number_delivery = fields.Integer(related='sale_line_id.mrx_pos_number', string='Pos.')
    mrx_pos_number_receipt = fields.Integer(related='purchase_line_id.mrx_pos_number', string='Pos.')


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    ## Override original function from: ../addons/stock/models/stock_move_line.py
    # 1. 'pos' has been added to the dictionary
    # 2. last 3 lines have been added to the end
    def _get_aggregated_product_quantities(self, **kwargs):
        """ Returns a dictionary of products (key = id+name+description+uom) and corresponding values of interest.

        Allows aggregation of data across separate move lines for the same product. This is expected to be useful
        in things such as delivery reports. Dict key is made as a combination of values we expect to want to group
        the products by (i.e. so data is not lost). This function purposely ignores lots/SNs because these are
        expected to already be properly grouped by line.

        returns: dictionary {product_id+name+description+uom: {product, name, description, qty_done, product_uom}, ...}
        """
        aggregated_move_lines = {}
        for move_line in self:
            name = move_line.product_id.display_name
            description = move_line.move_id.description_picking
            if description == name or description == move_line.product_id.name:
                description = False
            uom = move_line.product_uom_id
            line_key = str(move_line.product_id.id) + "_" + name + (description or "") + "uom " + str(uom.id)

            if line_key not in aggregated_move_lines:
                aggregated_move_lines[line_key] = {'pos': str(move_line.move_id.mrx_pos_number_delivery) + ".",
                                                   'name': name,
                                                   'description': description,
                                                   'qty_done': move_line.qty_done,
                                                   'product_uom': uom.name,
                                                   'product': move_line.product_id}
            else:
                aggregated_move_lines[line_key]['qty_done'] += move_line.qty_done
                aggregated_move_lines[line_key]['pos'] = str(aggregated_move_lines[line_key]['pos']) + "," + str(move_line.mrx_pos_number_delivery) + "."
        sorted_tuples = sorted(aggregated_move_lines.items(), key=lambda x: x[1]['pos'])
        res = {k: v for k, v in sorted_tuples} # Convert back to dictionary
        return res
