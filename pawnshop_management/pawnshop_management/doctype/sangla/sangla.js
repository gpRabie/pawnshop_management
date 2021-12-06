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

frappe.ui.form.on('Jewelry List', {
	item_no: function(frm, cdt, cdn){
		let table_length = parseInt(frm.doc.jewelry_items.length)
		if (frm.doc.jewelry_items.length > 1) {
			for (let index = 0; index < table_length - 1; index++) {
				if (frm.doc.jewelry_items[table_length-1].item_no == frm.doc.jewelry_items[index].item_no) {
					console.log(frm.doc.jewelry_items.pop(table_length-1));
					frm.refresh_field('jewelry_items');
					frappe.msgprint({
						title:__('Notification'),
						indicator:'red',
						message: __('Added item is already in the list. Item removed.')
					})
					// console.log("Pasok!");
				}
				// console.log(frm.doc.jewelry_items[index].item_no);
				// console.log(frm.doc.jewelry_items[table_length - 1].item_no);
			}
		}
	},

	suggested_appraisal_value: function(frm, cdt, cdn){
		set_total_appraised_amount(frm,cdt, cdn);
	},

	jewelry_items_remove: function(frm, cdt, cdn){ //calculate appraisal value when removing items
		set_total_appraised_amount(frm, cdt, cdn);
	}

});

frappe.ui.form.on('Non Jewelry List', {
	suggested_appraisal_value: function(frm, cdt, cdn){
		set_total_appraised_amount(frm,cdt, cdn);
	},

	non_jewelry_items_remove: function(frm, cdt, cdn){
		set_total_appraised_amount(frm, cdt, cdn);
	}
	

});


function set_series(frm) {
	if (cur_frm.doc.desired_principal >= 1500 && cur_frm.doc.desired_principal <= 10000 && cur_frm.doc.pawn_type == 'Jewelry') {
		cur_frm.set_value('item_series', 'A');
	} else if ((cur_frm.doc.desired_principal < 1500 || cur_frm.doc.desired_principal > 10000) && cur_frm.doc.pawn_type == 'Jewelry') {
		cur_frm.set_value('item_series', 'B');
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
			items_filter(cur_frm.doc.pawn_type, jewelry_count, non_jewelry_count) // filters items with the same batch
			let tracking_no = value.message;
			let jewelry_count = parseInt(tracking_no.jewelry_inventory_count)
			let non_jewelry_count = parseInt(tracking_no.non_jewelry_inventory_count)
			if (cur_frm.doc.item_series == 'A') {
				let new_ticket_no = parseInt(tracking_no.a_series_current_count) + 1;
				cur_frm.set_value('pawn_ticket', new_ticket_no + cur_frm.doc.item_series);
			} else if (cur_frm.doc.item_series == 'B'){
				let new_ticket_no = parseInt(tracking_no.b_series_current_count) + 1;
				cur_frm.set_value('pawn_ticket', new_ticket_no + cur_frm.doc.item_series);
			}

			if (cur_frm.doc.pawn_type == 'Jewelry') {
				jewelry_count++;
				cur_frm.set_value('inventory_tracking_no', jewelry_count + 'J')
			} else if (cur_frm.doc.pawn_type == 'Non Jewelry'){
				non_jewelry_count++;
				cur_frm.set_value('inventory_tracking_no', non_jewelry_count + 'NJ')
			}

		},

		error: function(value){
			console.error('Error! Check show_tracking_no block');
		}
	});
	
}


function set_total_appraised_amount(frm, cdt, cdn) { // Calculate Principal Amount
	let temp_principal = 0.00;
	if (cur_frm.doc.pawn_type == 'Jewelry') {
		$.each(cur_frm.doc.jewelry_items, function(index, item){
			temp_principal += parseFloat(item.suggested_appraisal_value);
		});
		cur_frm.set_value('desired_principal', temp_principal)
		set_item_interest(frm, temp_principal)
	} else {
		$.each(cur_frm.doc.non_jewelry_items, function(index, item){
			temp_principal += parseFloat(item.suggested_appraisal_value);
		});
		cur_frm.set_value('desired_principal', temp_principal);
		set_item_interest(frm, temp_principal)
	}
}

function set_item_interest(frm, temp_principal) {
	var interest = 0.00;
	var net_proceeds = 0.00;
	if (cur_frm.doc.pawn_type == 'Jewelry') {
		frappe.db.get_single_value('Pawnshop Management Settings', 'jewelry_interest_rate').then(value => {
			interest = parseFloat(value)/100 * temp_principal;
			cur_frm.set_value('interest', interest);
			net_proceeds = temp_principal - interest;
			cur_frm.set_value('net_proceeds', net_proceeds)
		});
	} else {
		frappe.db.get_single_value('Pawnshop Management Settings', 'gadget_interest_rate').then(value => {
			interest = parseFloat(value)/100 * temp_principal;
			cur_frm.set_value('interest', interest);
			net_proceeds = temp_principal - interest;
			cur_frm.set_value('net_proceeds', net_proceeds)
		});
	}
}

function items_filter(pawn_type, jewelry_batch, non_jewelry_batch){
	if (pawn_type == 'Jewelry') {
		cur_frm.set_query("sangla", "jewelry_items", function(){
			return {
				"filters": {
					"batch_number": jewelry_batch
				}
			}
		})
	} else if (pawn_type == 'Non Jewelry'){
		cur_frm.set_query("sangla", "non_jewelry_items", function(){
			return {
				"filters": {
					"batch_number": non_jewelry_batch
				}
			}
		})
	}
}


