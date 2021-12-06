// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Jewelry Items', {
	onload: function(frm) {
		show_item_no();
	}

});

function show_item_no(frm) {
	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			'doctype': 'Pawnshop Management Settings',
			'fieldname': [
				'jewelry_inventory_count',
				'jewelry_count'
			]
		},

		callback: function(data) {
			let jewelry_inventory_count = parseInt(data.message.jewelry_inventory_count);
			let jewelry_count = parseInt(data.message.jewelry_count)
			jewelry_count++
			jewelry_inventory_count++
			cur_frm.set_value('batch_number', jewelry_inventory_count)
			cur_frm.set_value('item_no', '1-' + jewelry_inventory_count + '-' + jewelry_count)
		},

		error: function(data){
			console.error('Error! Check show_item_no block');
		}
	})
}