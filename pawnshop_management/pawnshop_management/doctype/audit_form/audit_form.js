// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Audit Form', {
	refresh: function(frm) {
		frm.set_query('document_type', () => {
			return {
				filters: {
					'name':
					[
						'in',
						[
							"Pawn Ticket Jewelry",
							"Pawn Ticket Non Jewelry",
							"Provisional Receipt"
						]
					]
				}
			}
		})
	}
});
