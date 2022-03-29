import frappe
from frappe.utils import flt
from frappe.utils import today

@frappe.whitelist()
def create_journal_entry_nj(desired_principal):
    doc1 = frappe.new_doc('Journal Entry')
    doc1.voucher_type = 'Journal Entry'
    doc1.company = 'TEST Garcia\'s Pawnshop'
    doc1.posting_date = today()

    row_values1 = doc1.append('accounts', {})
    row_values1.account = "Inventory in Transit - NJ - TGP"
    row_values1.debit_in_account_currency = flt(desired_principal)
    row_values1.credit_in_account_currency = flt(0)

    row_values1 = doc1.append('accounts', {})
    row_values1.account = "Pawned Items Inventory - NJ - TGP"
    row_values1.debit_in_account_currency = flt(0)
    row_values1.credit_in_account_currency = flt(desired_principal)

    doc1.save(ignore_permissions=True)
    doc1.submit()
