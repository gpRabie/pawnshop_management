// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Jewelry Items', {
	refresh: function(frm) {
		show_item_no();
	},

	new_batch: function(frm){
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
			if (jewelry_inventory_count == 0) {
				cur_frm.set_value('new_batch', 1)
				jewelry_inventory_count++;
				jewelry_count++;
			} else if (cur_frm.doc.new_batch == true) {
				jewelry_inventory_count++;
				jewelry_count = 1;
			} else {
				jewelry_count++;
			}
			cur_frm.set_value('item_no', 'CC-' + jewelry_inventory_count + '-' + jewelry_count)
			cur_frm.refresh_fields();
		}
	})
}