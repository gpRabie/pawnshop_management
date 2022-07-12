# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

from pydoc import doc
import frappe
from frappe.model.document import Document

class AuditForm(Document):
	def on_submit(self):
		if frappe.db.exists(self.document_type, self.document_name) == self.document_name:
			try:
				journal_entry = frappe.db.get_value('Journal Entry', {'reference_document': self.document_name}, 'name')
				doc1 = frappe.get_doc('Journal Entry', journal_entry)
				try:
					doc1.workflow_state = "Audited"
					doc1.save(ignore_permissions=True)
				except:
					print("Journal Entry didn't save")
			except:
				print("Journal Entry doesn't exist or document isn't linked to any journal entry")
	
	def on_cancel(self):
		if frappe.db.exists(self.document_type, self.document_name) == self.document_name:
			journal_entry = frappe.db.get_value('Journal Entry', {'reference_document': self.document_name}, 'name')
			doc1 = frappe.get_doc('Journal Entry', journal_entry)
			if doc1.docstatus != 1:
				doc1.workflow_state = "Draft"
				doc1.save(ignore_permissions=True)
				