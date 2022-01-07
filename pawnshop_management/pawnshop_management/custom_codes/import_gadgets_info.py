import frappe
import json
from frappe.utils.csvutils import read_csv_content, get_csv_content_from_google_sheets

def get_data(url):
	content = get_csv_content_from_google_sheets(url)
	raw_data = read_csv_content(content)
	data = json.dumps(raw_data)
	new_data = json.loads(data)
	return new_data

@frappe.whitelist()
def update_gadgets_data():
	cellphones = get_data('https://docs.google.com/spreadsheets/d/1KnKfUxhLcJQzjLR3ZbbN3viqgAChvk3NziK6u3dwD7I/edit#gid=1409266298')
	tablets = get_data('https://docs.google.com/spreadsheets/d/1KnKfUxhLcJQzjLR3ZbbN3viqgAChvk3NziK6u3dwD7I/edit#gid=1127836523')
	laptops = get_data('https://docs.google.com/spreadsheets/d/1KnKfUxhLcJQzjLR3ZbbN3viqgAChvk3NziK6u3dwD7I/edit#gid=1918171614')
	cameras = get_data('https://docs.google.com/spreadsheets/d/1KnKfUxhLcJQzjLR3ZbbN3viqgAChvk3NziK6u3dwD7I/edit#gid=622869103')
	laptop_brands = laptops[1][0].split()
	# return cellphones[1][0].title()
	for entry_no in range(1, len(cellphones)):
		if frappe.db.exists('Brands', str(cellphones[entry_no][0]).title()) != str(cellphones[entry_no][0]).title():
			new_brand = frappe.new_doc('Brands')
			new_brand.brand = str(cellphones[entry_no][0]).title()
			new_brand.save(ignore_permissions=True)

		# if frappe.db.exists()