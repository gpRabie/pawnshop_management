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
	}
});
