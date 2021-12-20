# Copyright (c) 2021, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.auth import LoginManager

class JewelryItems(Document):	
	def before_save(self):
		doc = frappe.get_doc('Pawnshop Management Settings')
		if self.item_no != frappe.db.exists('Jewelry Items', self.item_no):
			doc.jewelry_count += 1
		doc.save(ignore_permissions=True)

	def validate(self):
		login_manager = LoginManager()
		login_manager.check_password(user=self.assistant_appraiser, pwd = self.password)