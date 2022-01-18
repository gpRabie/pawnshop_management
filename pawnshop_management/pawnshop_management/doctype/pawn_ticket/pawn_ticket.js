// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pawn Ticket', {
	validate: function(frm, cdt, cdn){
		let temp_principal = 0.0;
		if (frm.doc.type == "Non Jewelry") {
			$.each(frm.doc.non_jewelry_items, function(index, item){
				temp_principal += parseFloat(item.suggested_appraisal_value);
			});
		} else {
			$.each(frm.doc.jewelry_items, function(index, item){
				temp_principal += parseFloat(item.suggested_appraisal_value);
			});
		}

		if (frm.doc.desired_principal > temp_principal) {
			frappe.throw(__('Desired Principal is greater than the total value of items'));
		}
	},
	refresh: function(frm){
		// show_tracking_no();
		let today = frappe.datetime.now_datetime().split(" ");
		frm.set_value('date_loan_granted', today[0]);
		frappe.call({
			method: 'frappe.client.get_value',
			args: {
				'doctype': 'Pawnshop Management Settings',
				'fieldname': [
					'non_jewelry_inventory_count',
					'jewelry_inventory_count'
				]
			},
			callback: function(r){
				let inventory_count = r.message
				frm.set_query('item_no', 'jewelry_items', function(){
					return {
						"filters": {
							"batch_number": String(parseInt(inventory_count.jewelry_inventory_count) + 1)
						}
					};
				});

				frm.set_query('item_no', 'non_jewelry_items', function(){
					return {
						"filters": {
							"batch_number": String(parseInt(inventory_count.non_jewelry_inventory_count) + 1)
						}
					};
				});
			}

		})
	},

	date_loan_granted: function(frm){
		let default_maturity_date = frappe.datetime.add_days(cur_frm.doc.date_loan_granted, 30);
		cur_frm.set_value('maturity_date', default_maturity_date);

		let defaul_expiry_date = frappe.datetime.add_days(cur_frm.doc.date_loan_granted, 120);
		cur_frm.set_value('expiry_date', defaul_expiry_date);
	},

	pawn_type: function(frm){
		let previous_pawn_type = frm.doc.pawn_type;
		frappe.confirm('Pawn item list will be cleared, are you sure you want to proceed?', 
		() => {
			// action to perform if Yes is selected
			if (frm.doc.pawn_type == 'Jewelry') {
				set_series();
				show_tracking_no();
				frm.clear_table('non_jewelry_items');
				frm.set_value('desired_principal', 0);
				frm.set_df_property('jewelry_items', 'hidden', false);
				frm.set_df_property('non_jewelry_items', 'hidden', true);
			}
			else if (frm.doc.pawn_type == 'Non Jewelry'){
				frm.set_value('item_series', 'B');
				show_tracking_no();
				frm.clear_table('jewelry_items');
				frm.set_value('desired_principal', 0);
				frm.set_df_property('jewelry_items', 'hidden', true);
				frm.set_df_property('non_jewelry_items', 'hidden', false);
			}
		}, () => {
			frm.set_value('pawn_type', previous_pawn_type);
		})
	},

	desired_principal: function(frm, cdt, cdn) {
		set_series();
		show_tracking_no();
		frm.refresh_fields('pawn_ticket');
		set_item_interest()
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
					});
					set_total_appraised_amount(frm, cdt, cdn);
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
	item_no: function(frm, cdt, cdn){
		let table_length = parseInt(frm.doc.non_jewelry_items.length)
		if (frm.doc.non_jewelry_items.length > 1) {
			for (let index = 0; index < table_length - 1; index++) {
				if (frm.doc.non_jewelry_items[table_length-1].item_no == frm.doc.non_jewelry_items[index].item_no) {
					console.log(frm.doc.non_jewelry_items.pop(table_length-1));
					frm.refresh_field('jewelry_items');
					frappe.msgprint({
						title:__('Notification'),
						indicator:'red',
						message: __('Added item is already in the list. Item removed.')
					});
					set_total_appraised_amount(frm, cdt, cdn);
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

	non_jewelry_items_remove: function(frm, cdt, cdn){
		set_total_appraised_amount(frm, cdt, cdn);
	}
	

});


function set_series(frm) { //Set the pawn ticket series
	if (cur_frm.doc.desired_principal >= 1500 && cur_frm.doc.desired_principal <= 10000 && cur_frm.doc.pawn_type == 'Jewelry') {
		cur_frm.set_value('item_series', 'A');
	} else if ((cur_frm.doc.desired_principal < 1500 || cur_frm.doc.desired_principal > 10000) && cur_frm.doc.pawn_type == 'Jewelry') {
		cur_frm.set_value('item_series', 'B');
	}
}

function show_tracking_no(frm){ //Sets inventory tracking number
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

			// items_filter(cur_frm.doc.pawn_type, jewelry_count, non_jewelry_count) // filters items with the same batch

		},

		error: function(value){
			console.error('Error! Check show_tracking_no block');
		}
	});
	
}


function set_total_appraised_amount(frm, cdt, cdn) { // Calculate Principal Amount
	let temp_principal = 0.00;
	var interest = 0.00;
	var net_proceeds = 0.00;
	if (cur_frm.doc.pawn_type == 'Jewelry') {
		$.each(cur_frm.doc.jewelry_items, function(index, item){
			temp_principal += parseFloat(item.suggested_appraisal_value);
		});
		cur_frm.set_value('desired_principal', temp_principal)
		set_item_interest()
	} else {
		$.each(cur_frm.doc.non_jewelry_items, function(index, item){
			temp_principal += parseFloat(item.suggested_appraisal_value);
		});
		cur_frm.set_value('desired_principal', temp_principal);
		set_item_interest()
	}
	return temp_principal
}

function set_item_interest() {
	var principal = parseFloat(cur_frm.doc.desired_principal);
	var interest = 0.00;
	var net_proceeds = 0.00;

	if (cur_frm.doc.pawn_type == 'Jewelry') {
		frappe.db.get_single_value('Pawnshop Management Settings', 'jewelry_interest_rate').then(value => {
			interest = (parseFloat(value)/100) * (parseFloat(principal));
			cur_frm.set_value('interest', interest);
			net_proceeds = principal - interest;
			cur_frm.set_value('net_proceeds', net_proceeds)
		});
	} else {
		frappe.db.get_single_value('Pawnshop Management Settings', 'gadget_interest_rate').then(value => {
			interest = parseFloat(value)/100 * principal;
			cur_frm.set_value('interest', interest);
			net_proceeds = principal - interest;
			cur_frm.set_value('net_proceeds', net_proceeds)
		});
	}
}

function null_checker(number) {
	if (number == null) {
		number = 0;
	}
	return parseInt(number)
}