// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Provisional Receipt', {
	before_save: function(frm){
		if (frm.doc.transaction_type == "Renewal w/ Amortization" || frm.doc.transaction_type == "Amortization") {
			if (frm.doc.additional_amortization <= 0 || frm.doc.additional_amortization == null) {
				frappe.throw('Unable to proceed because Additional Amortization field is either empty or is equal to 0');
			}
		}
	},
	refresh: function(frm) {
		frm.set_query('pawn_ticket_type', () => {
			return {
				"filters": {
					"name": 
					[
						'in',
						[
							"Pawn Ticket Jewelry", 
							"Pawn Ticket Non Jewelry"
						]
					]
				}
			}
		})

		frm.set_query('pawn_ticket_no', () => {
			return {
				"filters": {
					"workflow_state": "Active"
				}
			}
		})

		frm.add_custom_button('Compute Interest', () => {
			show_payment_fields(frm)
			// calculate_interest(frm)
			// calculate_total_amortization(frm, frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
		})
	},

	date_issued: function(frm){
		if (frm.doc.date_issued > frm.doc.maturity_date) {
			frm.set_df_property('transaction_type', 'options', ['Renewal', 'Redemption', 'Interest Payment', 'Renewal w/ Amortization'])
		} else {
			frm.set_df_property('transaction_type', 'options', ['Renewal', 'Redemption', 'Interest Payment', 'Amortization', 'Renewal w/ Amortization'])
		}
		select_transaction_type(frm)
	},

	pawn_ticket_no: function(frm){
		frm.clear_table('items');
		show_items(frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
		frm.refresh_field('items');
		if (frm.doc.date_issued > frm.doc.maturity_date) {
			frm.set_df_property('transaction_type', 'options', ['Renewal', 'Redemption', 'Interest Payment', 'Renewal w/ Amortization'])
		} else {
			frm.set_df_property('transaction_type', 'options', ['Renewal', 'Redemption', 'Interest Payment', 'Amortization', 'Renewal w/ Amortization'])
		}
		select_transaction_type(frm)
	},

	transaction_type: function(frm){
		frm.toggle_display(['new_pawn_ticket_no'], frm.doc.transaction_type == 'Renewal w/ Amortization');
		frm.toggle_display(['additional_amortization'], frm.doc.transaction_type == 'Amortization');
		if (frm.doc.transaction_type == "Amortization") {
			clear_all_payment_fields();
			show_payment_fields(frm);
			frm.set_df_property('interest_payment', 'hidden', 1);
			frm.set_df_property('discount', 'hidden', 1);
			frm.set_df_property('new_pawn_ticket_no', 'hidden', 1);
			frm.set_df_property('advance_interest', 'hidden', 1);
			select_transaction_type(frm)
		} else if(frm.doc.transaction_type == "Interest Payment") {
			clear_all_payment_fields();
			show_payment_fields(frm);
			frm.set_df_property('discount', 'hidden', 1);
			frm.set_df_property('new_pawn_ticket_no', 'hidden', 1);
			frm.set_df_property('additional_amortization', 'hidden', 1);
			frm.set_df_property('advance_interest', 'hidden', 1);
			select_transaction_type(frm);
		} else if(frm.doc.transaction_type == "Redemption") {
			clear_all_payment_fields();
			show_payment_fields(frm);
			frm.set_df_property('additional_amortization', 'hidden', 1);
			frm.set_df_property('new_pawn_ticket_no', 'hidden', 1);
			frm.set_df_property('advance_interest', 'hidden', 1);
			select_transaction_type(frm);
		} else if (frm.doc.transaction_type == "Renewal") {
			clear_all_payment_fields();
			show_payment_fields(frm);
			frm.set_df_property('additional_amortization', 'hidden', 1);
			frm.set_df_property('advance_interest', 'hidden', 1);
			get_new_pawn_ticket_no(frm);
			select_transaction_type(frm);
		} else if (frm.doc.transaction_type == "Renewal w/ Amortization") {
			clear_all_payment_fields();
			show_payment_fields(frm);
			get_new_pawn_ticket_no(frm);
			select_transaction_type(frm);
		}
	},

	interest_payment: function(frm){
		frm.set_value('total', parseFloat(frm.doc.total) + parseFloat(frm.doc.interest_payment));
		frm.refresh_field('total');
	},

	discount: function(frm){
		frm.set_value('total', parseFloat(frm.doc.total) - parseFloat(frm.doc.discount));
		frm.refresh_field('total');
	},

	additional_amortization: function(frm){
		if (frm.doc.transaction_type == "Renewal w/ Amortization") {
			calculate_new_interest(frm);
		}
		frm.set_value('total', parseFloat(frm.doc.total) + parseFloat(frm.doc.additional_amortization));
		frm.refresh_field('total');
	},

	advance_interest: function(frm){
		frm.set_value('total', parseFloat(frm.doc.total) + parseFloat(frm.doc.advance_interest));
		frm.refresh_field('total');
	}
});


function show_payment_fields(frm) {
	frm.set_df_property('amortization', 'hidden', 0);
	frm.set_df_property('interest_payment', 'hidden', 0);
	frm.set_df_property('additional_amortization', 'hidden', 0);
	frm.set_df_property('discount', 'hidden', 0)
	frm.set_df_property('advance_interest', 'hidden', 0)
}

function calculate_interest(frm) {
	
	frm.set_value('interest_payment', 0.00);
	frm.refresh_field('interest_payment');
	var date_today = frm.doc.date_issued;											//frappe.datetime.get_today()
	if (date_today > frm.doc.maturity_date && date_today < frm.doc.expiry_date) {
		calculate_maturity_date_interest(frm);
	} else if (date_today >= frm.doc.expiry_date) {
		calculate_expiry_date_interest(frm);
	}
}

function calculate_maturity_date_interest(frm) {
	frappe.db.get_doc('Holiday List', 'No Operations').then(function(r){
		var holidays_list = r.holidays;
		var holidays_before_expiry_date = null;
		var temp_maturity_date = maturity_date_of_the_month(frm)
		var current_date = frm.doc.date_issued; 									//frappe.datetime.get_today().split("-");
		var maturity_date = temp_maturity_date
		var multiplier = maturity_interest_multiplier(frm);
		var temp_interest = frm.doc.interest;
		var date_today = frm.doc.date_issued; 										//frappe.datetime.get_today();

		for (let index = 0; index < holidays_list.length; index++) {				// Check if maturity date is a holiday
			if (holidays_list[index].holiday_date == temp_maturity_date.previous_maturity_date) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 1)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 2)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			}
		}


		if (date_today > frm.doc.maturity_date) {
			if (temp_maturity_date.previous_maturity_date == holidays_before_expiry_date) {
				console.log("SC1");
				if (date_today > frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3)) {
					temp_interest = temp_interest * multiplier;
				} else {
					temp_interest = temp_interest * (multiplier - 1);
					if (temp_interest < 0) {
						temp_interest = 0.00
					}
				}
			} else if (frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3) == holidays_before_expiry_date) {
				console.log("SC2");
				if (date_today > frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3)) {
					temp_interest = temp_interest * multiplier;
				} else {
					temp_interest = temp_interest * (multiplier - 1);
					if (temp_interest < 0) {
						temp_interest = 0.00
					}
				}
			} else if (frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 2) == holidays_before_expiry_date) {
				console.log("SC3");
				if (date_today > frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3)) {
					temp_interest = temp_interest * multiplier;
				} else {
					temp_interest = temp_interest * (multiplier - 1);
					if (temp_interest < 0) {
						temp_interest = 0.00
					}
				}
			} else if (frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 1) == holidays_before_expiry_date) {
				console.log("SC4");
				if (date_today > frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3)) {
					temp_interest = temp_interest * multiplier;
				} else {
					temp_interest = temp_interest * (multiplier - 1);
					if (temp_interest < 0) {
						temp_interest = 0.00
					}
				}
			} else {
				console.log("SC5");
				if (date_today > frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 2)) {
					console.log("SBC1");
					temp_interest = temp_interest * multiplier;
				} else {
					console.log("SCB2");
					temp_interest = temp_interest * (multiplier - 1);
					if (temp_interest < 0) {
						temp_interest = 0.00
					}
				}
			}
		} else {
			temp_interest = 0.00;
		}

		if (frm.doc.transaction_type == "Renewal") {
			temp_interest += parseFloat(frm.doc.interest)
		}

		frm.set_value('interest_payment', temp_interest);
		frm.refresh_field('interest_payment');
	});
}



function maturity_date_of_the_month(frm) {
	var current_date = frm.doc.date_issued.split("-");//frappe.datetime.get_today().split("-");
	var maturity_date = frm.doc.maturity_date.split("-");
	var expiry_date = frm.doc.expiry_date.split("-")
	var month_difference = 0;
	var previous_maturity_date = null;
	var current_maturity_date = frm.doc.maturity_date;
	var previous_maturity_date = frm.doc.maturity_date;
	
	if (parseInt(current_date[0]) > parseInt(maturity_date[0])) { //Calculate month difference if maturity date is for next year
		month_difference = Math.abs(parseInt(current_date[1]) - (12 - parseInt(maturity_date[1])));
	} else if(parseInt(current_date[0]) == parseInt(maturity_date[0])){ // Calculate month difference if maturity date is the same year
		month_difference = parseInt(current_date[1]) - parseInt(maturity_date[1]);
		if (month_difference < 0) {
			month_difference = 0;
		}
	}
	
	current_maturity_date = frappe.datetime.add_months(current_maturity_date, month_difference);
	var current_maturity_date_day = current_maturity_date.split("-");

	if (current_date[0] > maturity_date[0]){
		if (current_date[2] > maturity_date[2]) {
			current_maturity_date = frappe.datetime.add_months(frm.doc.maturity_date, month_difference);
			previous_maturity_date = frappe.datetime.add_months(current_maturity_date, -1);
		}
	} else if (current_date[0] == maturity_date[0]) {
		if (current_date[1] > maturity_date[1]) {
			if (current_date[2] > current_maturity_date_day[2]) {
				current_maturity_date = frappe.datetime.add_months(frm.doc.maturity_date, month_difference + 1);
				previous_maturity_date = frappe.datetime.add_months(current_maturity_date, -1);
			} else {
				current_maturity_date = frappe.datetime.add_months(frm.doc.maturity_date, month_difference);
				previous_maturity_date = frappe.datetime.add_months(current_maturity_date, -1);
			}
		} else if(current_date[1] == maturity_date[1]){
			if (current_date[2] > current_maturity_date_day[2]) {
				current_maturity_date = frappe.datetime.add_months(frm.doc.maturity_date, month_difference + 1);
				previous_maturity_date = frappe.datetime.add_months(current_maturity_date, -1);
			} 
		} 
	}

	
	if (current_maturity_date > cur_frm.doc.expiry_date) {
		current_maturity_date = frappe.datetime.add_days(current_maturity_date, parseInt(maturity_date[2])*-1)
		current_maturity_date = frappe.datetime.add_days(current_maturity_date, parseInt(expiry_date[2]))
	}
	return {
		'previous_maturity_date': previous_maturity_date,
		'current_maturity_date': current_maturity_date
	}
}


function maturity_interest_multiplier(frm) {
	var temp_maturity_date = maturity_date_of_the_month(frm).previous_maturity_date.split("-");
	var maturity_date = frm.doc.maturity_date.split("-");
	var multiplier = 0;
	var current_date = frm.doc.date_issued.split("-");//frappe.datetime.get_today().split("-");
	var actual_current_date = frm.doc.date_issued; //frappe.datetime.get_today();
	var actual_original_maturity_date = frm.doc.maturity_date;
	
	if (parseInt(temp_maturity_date[0]) > parseInt(maturity_date[0])) {
		console.log("A1");
		multiplier = parseInt(temp_maturity_date[1]) + (12 - parseInt(maturity_date[1]))
	} else if (parseInt(temp_maturity_date[0]) == parseInt(maturity_date[0])) {
		console.log("B1");
		if (parseInt(temp_maturity_date[1]) == parseInt(maturity_date[1])) {
			console.log("B1-1");
			if (actual_current_date > actual_original_maturity_date) {
				console.log("B1-2");
				multiplier = 1;
			} 
		}else if (parseInt(temp_maturity_date[1]) > parseInt(maturity_date[1])) {
			console.log("B2");
			if (actual_current_date > actual_original_maturity_date) {
				console.log("B2-1");
				multiplier = Math.abs(parseInt(temp_maturity_date[1]) - parseInt(maturity_date[1])) + 1;
			} else {
				console.log("B2-2");
				multiplier = Math.abs(parseInt(temp_maturity_date[1]) - parseInt(maturity_date[1]));
			}
		}
	}
	return multiplier;
}

function expiry_interest_multiplier(frm) {
	var temp_expiry_date = expiry_date(frm).previous_expiry_date.split("-");
	var original_expiry_date = frm.doc.expiry_date;
	var actual_current_date = frm.doc.date_issued; //frappe.datetime.get_today();
	var split_current_date = frm.doc.date_issued.split("-"); //frappe.datetime.get_today().split("-")
	var split_original_expiry_date = frm.doc.expiry_date.split("-")
	var multiplier = 0;

	if (parseInt(temp_expiry_date[0]) > parseInt(split_original_expiry_date[0])) {
		console.log("A1");
		multiplier = parseInt(temp_expiry_date[1]) + (12 - parseInt(split_original_expiry_date[1]))
	} else if (parseInt(temp_expiry_date[0]) == parseInt(split_original_expiry_date[0])) {
		console.log("B1");
		if (parseInt(temp_expiry_date[1]) == parseInt(split_original_expiry_date[1])) {
			console.log("B1-1");
			if (actual_current_date > original_expiry_date) {
				console.log("B1-2");
				multiplier = 1;
			} 
		}else if (parseInt(temp_expiry_date[1]) > parseInt(split_original_expiry_date[1])) {
			console.log("B2");
			if (actual_current_date > original_expiry_date) {
				console.log("B2-1");
				multiplier = Math.abs(parseInt(temp_expiry_date[1]) - parseInt(split_original_expiry_date[1])) + 1;
			} else {
				console.log("B2-2");
				multiplier = Math.abs(parseInt(temp_expiry_date[1]) - parseInt(split_original_expiry_date[1]));
			}
		}
	}
	return multiplier
}

function expiry_date(frm) {
	var actual_current_date = frm.doc.date_issued; //frappe.datetime.get_today();
	var actual_previous_expiry_date = frm.doc.expiry_date;
	var actual_current_expiry_date = frm.doc.expiry_date;
	var previous_expiry_date = actual_previous_expiry_date.split("-");
	var current_expiry_date = actual_current_expiry_date.split("-");
	var current_date = actual_current_date.split("-");
	var month_difference = 0;
	

	if (actual_current_date > actual_previous_expiry_date) {
		if (parseInt(current_date[0]) > parseInt(previous_expiry_date[0])) {
			month_difference = parseInt(current_date[1]) + (12 - parseInt(previous_expiry_date[1]))
		} else if (parseInt(current_date[0]) == parseInt(previous_expiry_date[0])) {
			month_difference = parseInt(current_date[1]) - parseInt(previous_expiry_date[1]);
			if (month_difference < 0) {
				month_difference = 0;
			}
		}
	}

	if (current_date[0] > previous_expiry_date[0]){
		if (current_date[2] > previous_expiry_date[2]) {
			actual_current_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, month_difference);
			actual_previous_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, -1);
		}
	} else if (current_date[0] == previous_expiry_date[0]) {
		if (current_date[1] > previous_expiry_date[1]) {
			if (current_date[2] > previous_expiry_date[2]) {
				actual_current_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, month_difference + 1);
				actual_previous_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, -1);
			} else {
				actual_current_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, month_difference);
				actual_previous_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, -1);
			}
		} else if(current_date[1] == previous_expiry_date[1]){
			if (current_date[2] > previous_expiry_date[2]) {
				actual_current_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, month_difference + 1);
				actual_previous_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, -1);
			}
		}
	}
	return {
		'previous_expiry_date': actual_previous_expiry_date,
		'current_expiry_date': actual_current_expiry_date
	}
}

function calculate_expiry_date_interest(frm) {
	frappe.db.get_doc('Holiday List', 'No Operations').then(function(r){
		var holidays_list = r.holidays;
		var holidays_before_expiry_date = null;
		var initial_interest = parseFloat(frm.doc.interest) * 3;
		var temp_expiry_date = expiry_date(frm)
		var multiplier = expiry_interest_multiplier(frm);
		var temp_interest = frm.doc.interest
		var date_today = frm.doc.date_issued; //frappe.datetime.get_today();

		for (let index = 0; index < holidays_list.length; index++) {
			
			if (holidays_list[index].holiday_date == temp_expiry_date.previous_expiry_date) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 1)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 2)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			}
		}

		if (date_today > frm.doc.expiry_date) {
			if (temp_expiry_date.previous_expiry_date == holidays_before_expiry_date) {
				console.log("A1");
				if (date_today > frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3)) {
					temp_interest = initial_interest + (temp_interest * multiplier);
				} else {
					multiplier = multiplier - 1;
					if (multiplier < 0) {
						multiplier = 0;
					}
					temp_interest = initial_interest + (temp_interest * (multiplier));
				}
			} else if(frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3) == holidays_before_expiry_date){
				console.log("B1");
				if (date_today > frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3)) {
					temp_interest = initial_interest + (temp_interest * multiplier);
				} else {
					multiplier = multiplier - 1;
					if (multiplier < 0) {
						multiplier = 0;
					}
					temp_interest = initial_interest + (temp_interest * (multiplier));
				}
			} else if (frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 2) == holidays_before_expiry_date) {
				console.log("C1");
				if (date_today > frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3)) {
					temp_interest = initial_interest + (temp_interest * multiplier);
				} else {
					multiplier = multiplier - 1;
					if (multiplier < 0) {
						multiplier = 0;
					}
					temp_interest = initial_interest + (temp_interest * (multiplier));
				}
			} else if (frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 1) == holidays_before_expiry_date) {
				console.log("D1");
				if (date_today > frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3)) {
					console.log("D1-1");
					temp_interest = initial_interest + (temp_interest * multiplier);
				} else {
					multiplier = multiplier - 1;
					console.log("D1-2");
					if (multiplier < 0) {
						multiplier = 0;
					}
					temp_interest = initial_interest + (temp_interest * (multiplier));
				}
			} else {
				console.log("E1");
				if (date_today > frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 2)) {
					console.log("E1-1");
					temp_interest = initial_interest + (temp_interest * (multiplier));
				} else {
					multiplier = multiplier - 1;
					console.log("E1-2");
					if (multiplier < 0) {
						multiplier = 0;
					}
					temp_interest = initial_interest + (temp_interest * multiplier);
				}
			}
		} else {
			temp_interest = initial_interest;
		}
		if (frm.doc.transaction_type == "Renewal") {
			temp_interest += parseFloat(frm.doc.interest)
		}
		frm.set_value('interest_payment', temp_interest)
		frm.refresh_field('interest_payment')
	});
}

function show_items(doctype, doc_name, doc_table_name = null) {
	frappe.db.get_doc(doctype, doc_name).then(function(r){
		var item_list = r.non_jewelry_items
		for (let index = 0; index < item_list.length; index++) {
			let childTable = cur_frm.add_child("items");
			childTable.item_code = item_list[index].item_no;
			childTable.description = item_list[index].model + ", " + item_list[index].model_number
		}
		cur_frm.refresh_field('items')
	})
}

function get_new_pawn_ticket_no(frm) {
	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			'doctype': 'Pawnshop Management Settings',
			'fieldname': [
				'a_series_current_count', 
				'b_series_current_count'
			]
		},
		callback: function(r){
			frm.set_df_property('new_pawn_ticket_no', 'hidden', 0);
			let new_pawn_ticket_no = r.message
			if (frm.doc.pawn_ticket_type == "Pawn Ticket Non Jewelry" && frm.doc.transaction_type == "Renewal") {
				frm.set_value('new_pawn_ticket_no', new_pawn_ticket_no.b_series_current_count + "B")
				frm.refresh_field('new_pawn_ticket_no')
			} else if (frm.doc.pawn_ticket_type == "Pawn Ticket Jewelry" && (frm.doc.principal_amount >= 1500 && frm.doc.principal_amount <= 10000) && frm.doc.transaction_type == "Renewal") {
				frm.set_value('new_pawn_ticket_no', new_pawn_ticket_no.a_series_current_count + "A")
				frm.refresh_field('new_pawn_ticket_no')
			} else if(frm.doc.transaction_type == "Renewal"){
				frm.set_value('new_pawn_ticket_no', new_pawn_ticket_no.b_series_current_count + "B")
				frm.refresh_field('new_pawn_ticket_no')
			} else if (frm.doc.pawn_ticket_type == "Pawn Ticket Non Jewelry" && frm.doc.transaction_type == "Renewal w/ Amortization") {
				frm.set_value('new_pawn_ticket_no', new_pawn_ticket_no.b_series_current_count + "B")
				frm.refresh_field('new_pawn_ticket_no')
			} else if (frm.doc.pawn_ticket_type == "Pawn Ticket Jewelry" && (frm.doc.principal_amount >= 1500 && frm.doc.principal_amount <= 10000) && frm.doc.transaction_type == "Renewal w/ Amortization") {
				frm.set_value('new_pawn_ticket_no', new_pawn_ticket_no.a_series_current_count + "A")
				frm.refresh_field('new_pawn_ticket_no')
			} else if(frm.doc.transaction_type == "Renewal w/ Amortization"){
				frm.set_value('new_pawn_ticket_no', new_pawn_ticket_no.b_series_current_count + "B")
				frm.refresh_field('new_pawn_ticket_no')
			}
		}
	})
}

function select_transaction_type(frm) {
	clear_all_payment_fields();
	frm.set_value('new_pawn_ticket_no', "");
	frm.refresh_field('new_pawn_ticket_no');
	if (frm.doc.transaction_type == "Redemption") {
		calculate_interest(frm);
		calculate_total_amortization(frm, frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
		frm.set_value('total', parseFloat(frm.doc.total) + parseFloat(frm.doc.principal_amount));
		frm.refresh_field('total');
	} else if (frm.doc.transaction_type == "Amortization") {
		calculate_total_amortization(frm, frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
	} else if (frm.doc.transaction_type == "Renewal w/ Amortization") {
		if (frm.doc.additional_amortization == 0) {
			frm.set_value('advance_interest', frm.doc.interest);
			frm.refresh_field('advance_interest');
		}
		calculate_interest(frm);
		calculate_total_amortization(frm, frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
	} else if(frm.doc.transaction_type == "Renewal"){
		calculate_interest(frm);
		calculate_total_amortization(frm, frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
		frm.set_value('interest_payment', parseFloat(frm.doc.interest) + parseFloat(frm.doc.interest_payment));
		frm.refresh_field('interest_payment');
	} 
}

function clear_all_payment_fields() {
	cur_frm.set_value('interest_payment', 0);
	cur_frm.refresh_field('interest_payment');
	cur_frm.set_value('discount', 0);
	cur_frm.refresh_field('discount');
	cur_frm.set_value('additional_amortization', 0);
	cur_frm.refresh_field('additional_amortization');
	cur_frm.set_value('advance_interest', 0)
	cur_frm.refresh_field('advance_interest')
	cur_frm.set_value('total', 0);
	cur_frm.refresh_field('total');
}

function calculate_total_amortization(frm, doctype, docname) {
	frappe.db.get_list("Provisional Receipt", {
		fields: ['additional_amortization'],
		filters: {
			docstatus: 1,
			pawn_ticket_type: doctype,
			pawn_ticket_no: docname,
			transaction_type: 'Amortization'
		}
	}).then(previous_amortizations => {
		let total_amortizations = 0.00;
		for (let index = 0; index < previous_amortizations.length; index++) {
			total_amortizations += parseFloat(previous_amortizations[index].additional_amortization);
		}
		frm.set_value('amortization', total_amortizations);
		frm.refresh_field('amortization');
	})
}

function calculate_new_interest(frm) {
	frm.set_value('advance_interest', 0.00);
	frm.refresh_field('advance_interest');
	if (frm.doc.pawn_ticket_type == "Pawn Ticket Non Jewelry") {
		frappe.db.get_single_value('Pawnshop Management Settings', 'gadget_interest_rate')
		.then(rate => {
			let new_interest = (parseFloat(frm.doc.principal_amount) - parseFloat(frm.doc.additional_amortization)) * (rate/100);
			frm.set_value('advance_interest', new_interest);
			frm.refresh_field('advance_interest');
		})
	} else {
		frappe.db.get_single_value('Pawnshop Management Settings', 'jewelry_interest_rate')
		.then(rate => {
			// let new_interest = (parseFloat(frm.doc.principal_amount) - parseFloat(frm.doc.additional_amortization)) * (rate/100);
			// frm.set_value('advance_interest', new_interest);
			// frm.refresh_field('advance_interest');
		})
	}
}