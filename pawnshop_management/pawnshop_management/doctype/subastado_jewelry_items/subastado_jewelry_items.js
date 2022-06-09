// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Subastado Jewelry Items', {
	refresh: function(frm) {
		frm.set_query('item_no', () => {
			return {
				filters: {
					workflow_state: "Pulled Out",
					branch: frm.doc.branch
				}
			}
		})
	}
});
