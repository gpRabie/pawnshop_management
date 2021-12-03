// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Non Jewelry Items', {
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
				'non_jewelry_inventory_count',
				'non_jewelry_count'
			]
		},

		callback: function(data) {
			let non_jewelry_inventory_count = parseInt(data.message.non_jewelry_inventory_count);
			let non_jewelry_count = parseInt(data.message.non_jewelry_count)
			non_jewelry_count++
			non_jewelry_inventory_count++
			
			cur_frm.set_value('item_no', '1-' + non_jewelry_inventory_count + '-' + non_jewelry_count)
		},

		error: function(data){
			console.error('Error! Check show_item_no block');
		}
	})
}