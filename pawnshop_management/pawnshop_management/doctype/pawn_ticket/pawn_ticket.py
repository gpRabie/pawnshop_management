# Copyright (c) 2021, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class Sangla(Document):
	# def autoname(self):
	# 	self.name = self.pawn_ticket
		
	def before_save(self):
		settings = frappe.get_doc('Pawnshop Management Settings')
		if self.pawn_ticket != frappe.db.exists('Pawn Ticket', self.pawn_ticket):
			if self.pawn_type == 'Jewelry':
				settings.jewelry_inventory_count += 1
				settings.jewelry_count = 0
			elif self.pawn_type == 'Non Jewelry':
				settings.non_jewelry_inventory_count += 1
				settings.non_jewelry_count = 0

			if self.item_series == 'A':
				settings.a_series_current_count += 1
			elif self.item_series == 'B':
				settings.b_series_current_count += 1
		settings.save(ignore_permissions=True)


