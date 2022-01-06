import frappe
from frappe.desk.reportview import get_match_cond

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def jewelry_items(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT name
        FROM `tabJewelry Items`
        WHERE docstatus < 2
            AND ({key} LIKE %(txt)s
            {mcond}
        ORDER BY
            IF(LOCATE(%(_txt)s, name), LOCATE(%(_txt)s, name), 99999),
            name
        LIMIT %(start)s, %(page_len)s
    """.format(**{
            'key': searchfield,
            'mcond':get_match_cond(doctype)
        }), {
        'txt': "%{}%".format(txt),
        '_txt': txt.replace("%", ""),
        'start': start,
        'page_len': page_len
    })