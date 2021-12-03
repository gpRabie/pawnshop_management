// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sangla', {
	onload: function(frm){
		show_tracking_no();
	},

	// refresh: function(frm) {
	// },

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
			if (frm.doc.pawn_type == 'Jewelry') {
				set_series();
				show_tracking_no();
				frm.clear_table('non_jewelry_items');
				frm.set_df_property('jewelry_items', 'hidden', false);
				frm.set_df_property('non_jewelry_items', 'hidden', true);
			}
			else if (frm.doc.pawn_type == 'Non Jewelry'){
				frm.set_value('item_series', 'B');
				show_tracking_no();
				frm.clear_table('jewelry_items');
				frm.set_df_property('jewelry_items', 'hidden', true);
				frm.set_df_property('non_jewelry_items', 'hidden', false);
			}
		}, () => {
			// action to perform if No is selected
		})
	},

	desired_principal: function(frm) {
		set_series();
		show_tracking_no();
		frm.refresh_fields('pawn_ticket');
	}


});


function set_series(frm) {
	if (cur_frm.doc.desired_principal >= 1500 && cur_frm.doc.desired_principal <= 10000 && cur_frm.doc.pawn_type == 'Jewelry') {
		cur_frm.set_value('item_series', 'A');
		console.log(cur_frm.doc.item_series);
	} else if ((cur_frm.doc.desired_principal < 1500 || cur_frm.doc.desired_principal > 10000) && cur_frm.doc.pawn_type == 'Jewelry') {
		cur_frm.set_value('item_series', 'B');
		console.log(cur_frm.doc.item_series);
	}
}

function show_tracking_no(frm){
	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			'doctype': 'Pawnshop Management Settings',
			'fieldname': [
				'a_series_current_count',
				'b_series_current_count',
				'non_jewelry_inventory_count',
				'jewelry_inventory_count'
			]
		},

		callback: function(value){
			let tracking_no = value.message;
			if (cur_frm.doc.item_series == 'A') {
				let new_ticket_no = parseInt(tracking_no.a_series_current_count) + 1;
				cur_frm.set_value('pawn_ticket', new_ticket_no + cur_frm.doc.item_series);
			} else if (cur_frm.doc.item_series == 'B'){
				let new_ticket_no = parseInt(tracking_no.b_series_current_count) + 1;
				cur_frm.set_value('pawn_ticket', new_ticket_no + cur_frm.doc.item_series);
			}

			if (cur_frm.doc.pawn_type == 'Jewelry') {
				let jewelry_count = parseInt(tracking_no.jewelry_inventory_count)
				jewelry_count++;
				cur_frm.set_value('inventory_tracking_no', jewelry_count + 'J')
			} else if (cur_frm.doc.pawn_type == 'Non Jewelry'){
				let non_jewelry_count = parseInt(tracking_no.non_jewelry_inventory_count)
				non_jewelry_count++;
				cur_frm.set_value('inventory_tracking_no', non_jewelry_count + 'NJ')
			}
		},

		error: function(value){
			console.error('Error! Check show_tracking_no block');
		}
	});
	
}

