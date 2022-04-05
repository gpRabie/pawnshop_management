import frappe
from frappe.utils import flt
from frappe.utils import today

@frappe.whitelist()
def create_journal_entry_nj_sales_cash(date, for_cash_on_hand_account, for_prendas_dispaly, for_gains_loss):
    doc1 = frappe.new_doc('Journal Entry')
    doc1.voucher_type = 'Journal Entry'
    doc1.company = 'TEST Garcia\'s Pawnshop'
    doc1.posting_date = date
    row_values1 = doc1.append('accounts', {})
    row_values1.account = "Cash on Hand - Pawnshop - NJ - TGP"
    row_values1.debit_in_account_currency = flt(for_cash_on_hand_account)
    row_values1.credit_in_account_currency = flt(0)

    row_values2 = doc1.append('accounts', {})
    row_values2.account = "Prendas Display - NJ - TGP"
    row_values2.debit_in_account_currency = flt(0)
    row_values2.credit_in_account_currency = flt(for_prendas_dispaly)

    row_values3 = doc1.append('accounts', {})
    row_values3.account = "Gains/Loss on Rematada Sale - NJ - TGP"
    row_values3.debit_in_account_currency = flt(0)
    row_values3.credit_in_account_currency = flt(for_gains_loss)

    doc1.save(ignore_permissions=True)
    doc1.submit()
    return "Success"


@frappe.whitelist()
def create_journal_entry_nj_sales_gcash(date, total, for_prendas_dispaly, for_gains_loss):
    doc1 = frappe.new_doc('Journal Entry')
    doc1.voucher_type = 'Journal Entry'
    doc1.company = 'TEST Garcia\'s Pawnshop'
    doc1.posting_date = date

    row_values1 = doc1.append('accounts', {})
    row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
    row_values1.debit_in_account_currency = flt(total) - (flt(total) * 0.02)
    row_values1.credit_in_account_currency = flt(0)

    row_values2 = doc1.append('accounts', {})
    row_values2.account = "Merchant Fee - COS - Gcash - TGP"
    row_values2.debit_in_account_currency = (flt(total) * 0.02)
    row_values2.credit_in_account_currency = flt(0)

    row_values3 = doc1.append('accounts', {})
    row_values3.account = "Withholding Tax Expense - Expanded - TGP"
    row_values3.debit_in_account_currency = ((flt(total) * 0.02) / 1.12) * 0.02
    row_values3.credit_in_account_currency = flt(0)

    row_values2 = doc1.append('accounts', {})
    row_values2.account = "Prendas Display - NJ - TGP"
    row_values2.debit_in_account_currency = flt(0)
    row_values2.credit_in_account_currency = flt(for_prendas_dispaly)

    row_values3 = doc1.append('accounts', {})
    row_values3.account = "Gains/Loss on Rematada Sale - NJ - TGP"
    row_values3.debit_in_account_currency = flt(0)
    row_values3.credit_in_account_currency = flt(for_gains_loss)

    row_values7 = doc1.append('accounts', {})
    row_values7.account = "Withholding Tax Payable - Expanded - TGP"
    row_values7.debit_in_account_currency = flt(0)
    row_values7.credit_in_account_currency = ((flt(total) * 0.02) / 1.12) * 0.02

    doc1.save(ignore_permissions=True)
    doc1.submit()
    return "Success"

@frappe.whitelist()
def create_journal_entry_nj_sales_bank_transfer(date, bank, total, for_prendas_dispaly, for_gains_loss):
    doc1 = frappe.new_doc('Journal Entry')
    doc1.voucher_type = 'Journal Entry'
    doc1.company = 'TEST Garcia\'s Pawnshop'
    doc1.posting_date = date
    row_values1 = doc1.append('accounts', {})
    if bank == "BDO":
        row_values1.account = "Cash in Bank - BDO - TGP"
    elif bank == "BPI":
        row_values1.account = "Cash in Bank - BPI - TGP"
    elif bank == "EASTWEST":
        row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
    row_values1.debit_in_account_currency = flt(total)
    row_values1.credit_in_account_currency = flt(0)

    row_values2 = doc1.append('accounts', {})
    row_values2.account = "Prendas Display - NJ - TGP"
    row_values2.debit_in_account_currency = flt(0)
    row_values2.credit_in_account_currency = flt(for_prendas_dispaly)

    row_values3 = doc1.append('accounts', {})
    row_values3.account = "Gains/Loss on Rematada Sale - NJ - TGP"
    row_values3.debit_in_account_currency = flt(0)
    row_values3.credit_in_account_currency = flt(for_gains_loss)

    doc1.save(ignore_permissions=True)
    doc1.submit()
    return "Success"


@frappe.whitelist()
def create_journal_entry_nj_funds_from_VC(date, for_cash_on_hand_account, for_cash_in_vault):
    doc1 = frappe.new_doc('Journal Entry')
    doc1.voucher_type = 'Journal Entry'
    doc1.company = 'TEST Garcia\'s Pawnshop'
    doc1.posting_date = date

    row_values1 = doc1.append('accounts', {})
    row_values1.account = "Cash on Hand - Pawnshop - NJ - TGP"
    row_values1.debit_in_account_currency = flt(for_cash_on_hand_account)
    row_values1.credit_in_account_currency = flt(0)

    row_values2 = doc1.append('accounts', {})
    row_values2.account = "Cash in Vault - NJ - TGP"
    row_values2.debit_in_account_currency = flt(0)
    row_values2.credit_in_account_currency = flt(for_cash_in_vault)

    doc1.save(ignore_permissions=True)
    doc1.submit()
    return "Success"