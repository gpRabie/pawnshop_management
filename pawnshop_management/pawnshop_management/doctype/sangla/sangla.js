// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sangla', {
	refresh: function(frm) {
		show_pawn_ticket();
	},

	date_loan_granted: function(frm){
		let default_maturity_date = frappe.datetime.add_days(cur_frm.doc.date_loan_granted, 30);
		cur_frm.set_value('maturity_date', default_maturity_date);

		let defaul_expiry_date = frappe.datetime.add_days(cur_frm.doc.date_loan_granted, 120);
		cur_frm.set_value('expiry_date', defaul_expiry_date);
	},

	pawn_type: function(frm){
		frappe.confirm('Pawn item list will be cleared, are you sure you want to proceed?', 
		() => {
			// action to perform if Yes is selected
			if (frm.doc.pawn_type == 'Non Jewelry'){
				cur_frm.set_value('item_series', 'B');
			} else {
				cur_frm.set_value('item_series', 'A');
			}
			frm.clear_table('pawn_items');
			frm.refresh();
		}, () => {
			// action to perform if No is selected
		})
	}


});

function show_pawn_ticket(frm){
	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			'doctype': 'Pawnshop Management Settings',
			'fieldname': [
				'a_series_current_count',
				'b_series_current_count'
			]
		},

		callback: function(value){
			let previous_ticket_no = value.message;
			if (cur_frm.doc.item_series == 'A') {
				let new_ticket_no = parseInt(previous_ticket_no.a_series_current_count) + 1;
				cur_frm.set_value('pawn_ticket', new_ticket_no + cur_frm.doc.item_series);
			} else {
				let new_ticket_no = parseInt(previous_ticket_no.b_series_current_count) + 1;
				cur_frm.set_value('pawn_ticket', new_ticket_no + cur_frm.doc.item_series);
			}
			cur_frm.refresh_fields();
		}
	});
	
}