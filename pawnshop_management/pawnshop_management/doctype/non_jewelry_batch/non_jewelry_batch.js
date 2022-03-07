// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Non Jewelry Batch', {
	refresh: function(frm) {
		if (frm.is_new) {
			frappe.db.get_single_value('Pawnshop Management Settings', 'non_jewelry_inventory_count')
			.then(inventory_count => {
				frm.set_value('inventory_tracking_no', inventory_count + "NJ")
				frm.refresh_field('inventory_tracking_no')
			})
		}

		frappe.db.get_single_value('Pawnshop Management Settings', 'non_jewelry_inventory_count')
			.then(inventory_count => {
				frm.set_query('item_no', 'items', () => {
					return {
						"filters": {
							"batch_number": String(inventory_count)
						}
					}
				})
			})
		frm.fields_dict["items"].grid.grid_buttons.find(".grid-add-row")[0].innerHTML = "Add Item"	//Change "Add Row" button of jewelry_items table into "Add Item"

		frm.add_custom_button('Test', () => {
			console.log(frm.doc.inventory_tracking_no);
			console.log(get_inventory_batch(frm));
		})
	}
});

function get_inventory_batch(frm) {
	var inventory_tracking_no = frm.doc.inventory_tracking_no;
	var batch_number = "";
	for (let index = 0; index < inventory_tracking_no.length; index++) {
		if (!isNaN(inventory_tracking_no[index])) {
			batch_number += inventory_tracking_no[index];
		}
	}
	return batch_number
}
