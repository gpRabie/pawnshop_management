import frappe
import math
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
	
	# phone = cellphones[1][6]
	# print(phone)
	loop_in_gadgets(cellphones, "Cellphone")
	loop_in_gadgets(tablets, "Tablet")
	loop_in_gadgets(laptops, "Laptop")
	loop_in_gadgets(cameras, "Camera")


def loop_in_gadgets(entry, gadget_type):
	if gadget_type == "Laptop":
		for entry_no in range(1, len(entry)):
			add_brands(entry[entry_no][0])
			if str(entry[entry_no][0]).title() == "Apple":
				add_models(entry[entry_no][1], gadget_type, entry[entry_no][3], entry[entry_no][4], entry[entry_no][5], entry[entry_no][0])
			else:
				add_models(entry[entry_no][1], gadget_type, entry[entry_no][3], entry[entry_no][4], entry[entry_no][5])
			assign_gadget_type(entry[entry_no][0], gadget_type)
	elif gadget_type == "Cellphone":
		for entry_no in range(1, len(entry)):
			add_brands(entry[entry_no][0])
			add_models(entry[entry_no][1], gadget_type, entry[entry_no][4], entry[entry_no][5], entry[entry_no][6], entry[entry_no][0])
			assign_gadget_type(entry[entry_no][0], gadget_type)
	elif gadget_type == "Tablet":
		for entry_no in range(1, len(entry)):
			add_brands(entry[entry_no][0])
			add_models(entry[entry_no][1], gadget_type, entry[entry_no][3], entry[entry_no][4], entry[entry_no][5], entry[entry_no][0])
			assign_gadget_type(entry[entry_no][0], gadget_type)
	elif gadget_type == "Camera":
		for entry_no in range(1, len(entry)):
			add_brands(entry[entry_no][0])
			add_models(entry[entry_no][1], gadget_type, entry[entry_no][2], entry[entry_no][3], entry[entry_no][4], entry[entry_no][0])
			assign_gadget_type(entry[entry_no][0], gadget_type)

def add_brands(brand_name):
	brand_name = str(brand_name).title()
	if frappe.db.exists('Brands', brand_name) != brand_name:
		if brand_name != "None":
			new_brand = frappe.new_doc('Brands')
			new_brand.brand = brand_name
			new_brand.save(ignore_permissions=True)

def add_models(model_name, gadget_type, defective_price, minimum_price, maximum_price, brand=None):
	model_name = str(model_name).title()
	gadget_type = str(gadget_type).title()
	brand = str(brand).title()
	if frappe.db.exists('Models', model_name) != model_name:
		if model_name != "None":
			if brand == None or brand == "None":
				new_model = frappe.new_doc('Models')
				new_model.model = model_name
				new_model.type = gadget_type
				new_model.defective = string_to_int_converter(defective_price)
				new_model.minimum = string_to_int_converter(minimum_price)
				new_model.maximum = string_to_int_converter(maximum_price)
				new_model.save(ignore_permissions=True)
			else:
				new_model = frappe.new_doc('Models')
				new_model.model = model_name
				new_model.type = gadget_type
				new_model.brand = brand
				new_model.defective = string_to_int_converter(defective_price)
				new_model.minimum = string_to_int_converter(minimum_price)
				new_model.maximum = string_to_int_converter(maximum_price)
				new_model.save(ignore_permissions=True)

def assign_gadget_type(brand, gadget_type):
	if frappe.db.exists('Brands', str(brand).title()) == str(brand).title():
		if gadget_type == "Cellphone":
			item = frappe.get_doc('Brands', str(brand).title())
			if item.cellphone != 1:
				item.cellphone = 1
				item.save(ignore_permissions=True)
		elif gadget_type == "Tablet":
			item = frappe.get_doc('Brands', str(brand).title())
			if item.tablet != 1:
				item.tablet = 1
				item.save(ignore_permissions=True)
		elif gadget_type == "Laptop":
			item = frappe.get_doc('Brands', str(brand).title())
			if item.laptop != 1:
				item.laptop = 1
				item.save(ignore_permissions=True)
		elif gadget_type == "Camera":
			item = frappe.get_doc('Brands', str(brand).title())
			if item.camera != 1:
				item.camera = 1
				item.save(ignore_permissions=True)

def delete_models(model_name):
	if model_name != None:
		if frappe.db.exists('Brands', str(model_name).title()) == str(model_name).title():
			frappe.delete_doc('Brands', str(model_name).title())

def check_model_status(model_name): 							# Check if model name is in the google sheets database
	model_list = frappe.db.get_list('Models', pluck='name')
	for models in model_list:
		if models == str(model_name).title():
			return True 										# Returns True if model name is found in both google sheets database and in erpnext database
	return False												# Returns False if model name is not found in both google sheets database and in erpnext database


def check_brand_status(brand_name):								# Check if brand name is in the google sheets database
	brands_list = frappe.db.get_list('Brands', pluck='name')
	for brands in brands_list:
		if brands == str(brand_name).title():
			return True											# Returns True if brand name is found in both google sheets database and in erpnext database
	return False												# Returns False if brand name is not found in both google sheets database and in erpnext database

def string_to_int_converter(number):
	if type(number) == str:
		if "," in number:
			prices = number.split(",")
			converted_number = prices[0] + prices[1]
			return int(converted_number)
		else:
			return int(number)
	else:
		return int(number)