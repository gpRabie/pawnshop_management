// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Provisional Receipt', {

	validate: function(frm){
		if (frm.doc.total > frm.doc.interest_payment && frm.doc.transaction_type == "Interest Payment") {
			frm.set_value('number_of_months_to_pay_in_advance', 0);
			frm.refresh_field('number_of_months_to_pay_in_advance');
			frappe.throw('Payment should not exceed accrued interest amount');
		}

		if (frm.doc.transaction_type == "Renewal w/ Amortization" || frm.doc.transaction_type == "Amortization") {
			if (frm.doc.additional_amortization <= 0 || frm.doc.additional_amortization == null) {
				frappe.throw('Unable to proceed because Additional Amortization field is either empty or is equal to 0');
			}
		}
	},

	before_submit: function(frm){
		if (frm.doc.transaction_type != "Interest Payment") {
			check_creditted_interest_payments(frm);
		}
	},

	refresh: function(frm) {
		// frm.toggle_display(['new_pawn_ticket_no'], (frm.doc.docstatus == 1 && frm.doc.new_pawn_ticket_no != "") || frm.doc.transaction_type == "Renewal" || frm.doc.transaction_type == "Renewal w/ Amortization")
		if (frm.is_new()) {
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.get_ip.get_ip',
				callback: function(data){
					let current_ip = data.message
					frappe.call({
						method: 'pawnshop_management.pawnshop_management.custom_codes.get_ip.get_ip_from_settings',
						callback: (result) => {
							let ip = result.message;
							if (current_ip == ip["cavite_city"]) {
								frm.set_value('branch', "Garcia's Pawnshop - CC");
								frm.refresh_field('branch');
							} else if (current_ip == ip["poblacion"]) {
								frm.set_value('branch', "Garcia's Pawnshop - POB");
								frm.refresh_field('branch');
							} else if (current_ip == ip["molino"]) {
								frm.set_value('branch', "Garcia's Pawnshop - MOL");
								frm.refresh_field('branch');
							} else if (current_ip == ip["gtc"]) {
								frm.set_value('branch', "Garcia's Pawnshop - GTC");
								frm.refresh_field('branch');
							} else if (current_ip == ip["tanza"]) {
								frm.set_value('branch', "Garcia's Pawnshop - TNZ");
								frm.refresh_field('branch');
							} else if (current_ip == ip["rabies_house"]) {
								frm.set_value('branch', "Rabie's House");
								frm.refresh_field('branch');
							}
						}
					})
				}
			})
		}
		frm.add_custom_button('Skip PR No', () => {
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.update_pr.increment_pr_no',
				args: {
					prefix: frm.doc.naming_series
				},
				callback: function(data){
					console.log(data.message);
				}
			})
		})
		frm.toggle_display(['creditted'], frm.doc.transaction_type == 'Interest Payment');
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
					"workflow_state": 
					[
						'in',
						[
							'Active',
							'Returned',
							'Expired'
						]
					]
				}
			}
		})

		frm.add_custom_button('Test Button', () => {
			frappe.call('pawnshop_management.pawnshop_management.custom_codes.update_pawn_ticket.change_pawn_ticket_nj_status_to_expire', {
			}).then(r => {
				
			})
		})
	},

	branch: function(frm){
		select_naming_series(frm);
	},

	date_issued: function(frm){
		if (frm.doc.date_issued > frm.doc.maturity_date && frm.doc.interest_payment > 0) {
			frm.set_df_property('transaction_type', 'options', ['---Select Transaction Type---', 'Renewal', 'Redemption', 'Interest Payment', 'Renewal w/ Amortization']);
			frm.refresh_field('transaction_type');
			console.log("Hi");
		} else if (frm.doc.date_issued > frm.doc.maturity_date) {
			frm.set_df_property('transaction_type', 'options', ['---Select Transaction Type---', 'Renewal', 'Redemption', 'Renewal w/ Amortization']);
			frm.refresh_field('transaction_type');
			console.log("Hello");
		} else {
			frm.set_df_property('transaction_type', 'options', ['---Select Transaction Type---', 'Renewal', 'Redemption', 'Interest Payment', 'Amortization', 'Renewal w/ Amortization']);
			frm.refresh_field('transaction_type');
			console.log("Welcome");
		}
		select_transaction_type(frm);
		calculate_interest(frm);
	},

	pawn_ticket_no: function(frm){
		frm.clear_table('items');
		show_items(frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
		frm.refresh_field('items');
		if (frm.doc.date_issued > frm.doc.maturity_date && frm.doc.interest_payment > 0) {
			frm.set_df_property('transaction_type', 'options', ['Renewal', 'Redemption', 'Interest Payment', 'Renewal w/ Amortization']);
			frm.refresh_field('transaction_type');
			console.log("Hi");
		} else if (frm.doc.date_issued > frm.doc.maturity_date) {
			frm.set_df_property('transaction_type', 'options', ['Renewal', 'Redemption', 'Renewal w/ Amortization']);
			frm.refresh_field('transaction_type');
			console.log("Hello");
		} else {
			frm.set_df_property('transaction_type', 'options', ['Renewal', 'Redemption', 'Amortization', 'Renewal w/ Amortization']);
			frm.refresh_field('transaction_type');
			console.log("Welcome");
		}
		calculate_total_amortization(frm, frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
		show_previous_interest_payment(frm);
		select_transaction_type(frm)
		calculate_interest(frm);
	},

	transaction_type: function(frm){
		if (frm.doc.transaction_type == "Amortization") {
			clear_all_payment_fields();
			show_payment_fields(frm);
			frm.set_df_property('interest_payment', 'hidden', 1);
			frm.set_df_property('discount', 'hidden', 1);
			frm.set_df_property('advance_interest', 'hidden', 1);
			frm.set_df_property('number_of_months_to_pay_in_advance', 'hidden', 1);
			select_transaction_type(frm)
		} else if(frm.doc.transaction_type == "Interest Payment") {
			clear_all_payment_fields();
			show_payment_fields(frm);
			// frm.set_df_property('interest_payment', 'hidden', 1);
			frm.set_df_property('discount', 'hidden', 1);
			frm.set_df_property('additional_amortization', 'hidden', 1);
			frm.set_df_property('advance_interest', 'hidden', 1);
			select_transaction_type(frm);
		} else if(frm.doc.transaction_type == "Redemption") {
			clear_all_payment_fields();
			show_payment_fields(frm);
			frm.set_df_property('additional_amortization', 'hidden', 1);
			frm.set_df_property('advance_interest', 'hidden', 1);
			frm.set_df_property('number_of_months_to_pay_in_advance', 'hidden', 1);
			select_transaction_type(frm);

		} else if (frm.doc.transaction_type == "Renewal") {
			clear_all_payment_fields();
			show_payment_fields(frm);
			frm.set_df_property('additional_amortization', 'hidden', 1);
			frm.toggle_display(['new_pawn_ticket_no'], frm.doc.transaction_type == 'Renewal' || frm.doc.transaction_type == 'Renewal w/ Amortization');
			// frm.set_df_property('advance_interest', 'hidden', 1);
			frm.set_df_property('number_of_months_to_pay_in_advance', 'hidden', 1);
			get_new_pawn_ticket_no(frm);
			select_transaction_type(frm);
		} else if (frm.doc.transaction_type == "Renewal w/ Amortization") {
			frm.toggle_display(['new_pawn_ticket_no'], frm.doc.transaction_type == 'Renewal' || frm.doc.transaction_type == 'Renewal w/ Amortization');
			clear_all_payment_fields();
			show_payment_fields(frm);
			get_new_pawn_ticket_no(frm);
			frm.set_df_property('number_of_months_to_pay_in_advance', 'hidden', 1);
			select_transaction_type(frm);
		}
	},

	mode_of_payment: function(frm){
		frm.toggle_display(['bank'], frm.doc.mode_of_payment === 'Bank Transfer');
	},

	discount: function(frm){
		frm.set_value('total', parseFloat(frm.doc.total) - parseFloat(frm.doc.discount));
		frm.refresh_field('total');
	},

	additional_amortization: function(frm){
		if (frm.doc.transaction_type == "Renewal w/ Amortization") {
			calculate_new_interest(frm);
			// console.log(parseFloat(frm.doc.additional_amortization) + parseFloat(frm.doc.interest_payment) + parseFloat(frm.doc.advance_interest) - parseFloat(frm.doc.discount));
			frm.set_value('total', (parseFloat(frm.doc.additional_amortization) + parseFloat(frm.doc.interest_payment) + parseFloat(frm.doc.advance_interest)) - parseFloat(frm.doc.discount));
			frm.refresh_field('total');
		} else if (frm.doc.transaction_type == "Amortization") {
			frm.set_value('total', parseFloat(frm.doc.additional_amortization));
			frm.refresh_field('total');
		}
		
	},

	advance_interest: function(frm){
		frm.set_value('total', (parseFloat(frm.doc.additional_amortization) + parseFloat(frm.doc.interest_payment)) - parseFloat(frm.doc.discount) + parseFloat(frm.doc.advance_interest));
		frm.refresh_field('total');
	},

	number_of_months_to_pay_in_advance: function(frm){
		calculate_advance_interest_payment(frm);
	},

	interest_payment: function(frm){
		if (frm.doc.transaction_type == "Amortization" || frm.doc.transaction_type == "Renewal w/ Amortization") {
			frm.set_value('total', (parseFloat(frm.doc.additional_amortization) + parseFloat(frm.doc.interest_payment)) - parseFloat(frm.doc.discount) + parseFloat(frm.doc.advance_interest));
			frm.refresh_field('total');
		} else if (frm.doc.transaction_type == "Redemption") {
			frm.set_value('total', (parseFloat(frm.doc.principal_amount) + parseFloat(frm.doc.interest_payment)) - parseFloat(frm.doc.discount) + parseFloat(frm.doc.advance_interest));
			frm.refresh_field('total');
		} else if (frm.doc.transaction_type == "Renewal") {
			frm.set_value('total', (parseFloat(frm.doc.interest_payment) + parseFloat(frm.doc.advance_interest)) - parseFloat(frm.doc.discount));
			frm.refresh_field('total');
		}

		if (frm.doc.date_issued > frm.doc.maturity_date && frm.doc.interest_payment > 0) {
			frm.set_df_property('transaction_type', 'options', ['Renewal', 'Redemption', 'Interest Payment', 'Renewal w/ Amortization']);
		} else if (frm.doc.date_issued > frm.doc.maturity_date) {
			frm.set_df_property('transaction_type', 'options', ['Renewal', 'Redemption', 'Renewal w/ Amortization']);
		} else {
			frm.set_df_property('transaction_type', 'options', ['Renewal', 'Redemption', 'Interest Payment', 'Amortization', 'Renewal w/ Amortization']);
		}
	},

	number_of_months_to_pay_in_advance: function(frm){
		frm.set_value('total', frm.doc.number_of_months_to_pay_in_advance * frm.doc.interest);
		frm.refresh_field('total');
	}
});


function show_payment_fields(frm) {
	frm.set_df_property('amortization', 'hidden', 0);
	frm.set_df_property('interest_payment', 'hidden', 0);
	frm.set_df_property('additional_amortization', 'hidden', 0);
	frm.set_df_property('discount', 'hidden', 0)
	frm.set_df_property('advance_interest', 'hidden', 0)
	frm.set_df_property('number_of_months_to_pay_in_advance', 'hidden', 0)
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

		frm.set_value('interest_payment', temp_interest - frm.doc.previous_interest_payment);
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
		// if (frm.doc.transaction_type == "Renewal") {
		// 	temp_interest += parseFloat(frm.doc.interest)
		// }
		frm.set_value('interest_payment', temp_interest - frm.doc.previous_interest_payment)
		frm.refresh_field('interest_payment')
	});
}

function show_items(doctype, doc_name, doc_table_name = null) {
	frappe.db.get_doc(doctype, doc_name).then(function(r){
		if (doctype == "Pawn Ticket Non Jewelry") {
			var item_list = r.non_jewelry_items
			for (let index = 0; index < item_list.length; index++) {
				let childTable = cur_frm.add_child("items");
				childTable.item_code = item_list[index].item_no;
				childTable.description = item_list[index].model + ", " + item_list[index].model_number
			}
			cur_frm.refresh_field('items')
		} else if (doctype == "Pawn Ticket Jewelry") {
			var item_list = r.jewelry_items
			for (let index = 0; index < item_list.length; index++) {
				let childTable = cur_frm.add_child("items");
				childTable.item_code = item_list[index].item_no;
				childTable.description = item_list[index].type + ", " + item_list[index].karat + ", " + item_list[index].karat_category + ", " + item_list[index].color;
			}
			cur_frm.refresh_field('items')
		}
		
	})
}

function select_naming_series(frm) { //Select naming series with regards to the branch
	if (frm.doc.branch == "Rabie's House") {
		frm.set_value('naming_series', "No-20-.######")
	} else if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frm.set_value('naming_series', "No-1-.######")
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frm.set_value('naming_series', "No-4-.######")
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frm.set_value('naming_series', "No-6-.######")
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frm.set_value('naming_series', "No-3-.######")
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frm.set_value('naming_series', "No-5-.######")
	}
}

function get_new_pawn_ticket_no(frm) {
	if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_value("Pawn Ticket Jewelry", frm.doc.pawn_ticket_no, "item_series")
		.then(data => {
			console.log(data.message.item_series);
			if (data.message.item_series == "A") {
				frappe.db.get_value("Pawnshop Naming Series", "Rabie's House", "a_series")
				.then(r => {
					let current_count = r.message.a_series;
					new_pawn_ticket_no(frm, "20-", current_count, 'A');
				})
			} else if (data.message.item_series == "B") {
				console.log(data.message.item_series);
				frappe.db.get_value("Pawnshop Naming Series", "Rabie's House", "b_series")
				.then(r => {
					let current_count = r.message.b_series;
					new_pawn_ticket_no(frm, "20-", current_count, 'B');
				})
			}
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frappe.db.get_value("Pawn Ticket Jewelry", frm.doc.pawn_ticket_no, "item_series")
		.then(data => {
			if (data.message.item_series == "A") {
				frappe.db.get_value("Pawnshop Naming Series", "Garcia's Pawnshop - CC", "a_series")
				.then(r => {
					let current_count = r.message.a_series;
					new_pawn_ticket_no(frm, "1-", current_count, 'A');
				})
			} else if (data.message.item_series == "B") {
				frappe.db.get_value("Pawnshop Naming Series", "Garcia's Pawnshop - CC", "b_series")
				.then(r => {
					let current_count = r.message.b_series;
					new_pawn_ticket_no(frm, "1-", current_count, 'B');
				})
			}
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frappe.db.get_value("Pawn Ticket Jewelry", frm.doc.pawn_ticket_no, "item_series")
		.then(data => {
			if (data.message.item_series == "A") {
				frappe.db.get_value("Pawnshop Naming Series", "Garcia's Pawnshop - GTC", "a_series")
				.then(r => {
					let current_count = r.message.a_series;
					new_pawn_ticket_no(frm, "4-", current_count, 'A');
				})
			} else if (data.message.item_series == "B") {
				frappe.db.get_value("Pawnshop Naming Series", "Garcia's Pawnshop - GTC", "b_series")
				.then(r => {
					let current_count = r.message.b_series;
					new_pawn_ticket_no(frm, "4-", current_count, 'B');
				})
			}
		})

	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frappe.db.get_value("Pawn Ticket Jewelry", frm.doc.pawn_ticket_no, "item_series")
		.then(data => {
			if (data.message.item_series == "A") {
				frappe.db.get_value("Pawnshop Naming Series", "Garcia's Pawnshop - MOL", "a_series")
				.then(r => {
					let current_count = r.message.a_series;
					new_pawn_ticket_no(frm, "6-", current_count, 'A');
				})
			} else if (data.message.item_series == "B") {
				frappe.db.get_value("Pawnshop Naming Series", "Garcia's Pawnshop - MOL", "b_series")
				.then(r => {
					let current_count = r.message.b_series;
					new_pawn_ticket_no(frm, "6-", current_count, 'B');
				})
			}
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frappe.db.get_value("Pawn Ticket Jewelry", frm.doc.pawn_ticket_no, "item_series")
		.then(data => {
			if (data.message.item_series == "A") {
				frappe.db.get_value("Pawnshop Naming Series", "Garcia's Pawnshop - POB", "a_series")
				.then(r => {
					let current_count = r.message.a_series;
					new_pawn_ticket_no(frm, "3-", current_count, 'A');
				})
			} else if (data.message.item_series == "B") {
				frappe.db.get_value("Pawnshop Naming Series", "Garcia's Pawnshop - POB", "b_series")
				.then(r => {
					let current_count = r.message.b_series;
					new_pawn_ticket_no(frm, "3-", current_count, 'B');
				})
			}
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frappe.db.get_value("Pawn Ticket Jewelry", frm.doc.pawn_ticket_no, "item_series")
		.then(data => {
			if (data.message.item_series == "A") {
				frappe.db.get_value("Pawnshop Naming Series", "Garcia's Pawnshop - TNZ", "a_series")
				.then(r => {
					let current_count = r.message.a_series;
					new_pawn_ticket_no(frm, "5-", current_count, 'A');
				})
			} else if (data.message.item_series == "B") {
				frappe.db.get_value("Pawnshop Naming Series", "Garcia's Pawnshop - TNZ", "b_series")
				.then(r => {
					let current_count = r.message.b_series;
					new_pawn_ticket_no(frm, "5-", current_count, 'B');
				})
			}
		})
	}
}

function new_pawn_ticket_no(frm, prefix, series_count, item_series) {
	// frm.set_df_property('new_pawn_ticket_no', 'hidden', 0);
	frm.set_value('new_pawn_ticket_no', prefix + series_count + item_series)
	frm.refresh_field('new_pawn_ticket_no')
	// if (frm.doc.pawn_ticket_type == "Pawn Ticket Non Jewelry" && frm.doc.transaction_type == "Renewal") {
	// 	frm.set_value('new_pawn_ticket_no', prefix + series_count + item_series)
	// 	frm.refresh_field('new_pawn_ticket_no')
	// } else if (frm.doc.pawn_ticket_type == "Pawn Ticket Jewelry" && (frm.doc.principal_amount >= 1500 && frm.doc.principal_amount <= 10000) && frm.doc.transaction_type == "Renewal") {
	// 	frm.set_value('new_pawn_ticket_no',  prefix + series_count + "A")
	// 	frm.refresh_field('new_pawn_ticket_no')
	// } else if(frm.doc.transaction_type == "Renewal"){
	// 	frm.set_value('new_pawn_ticket_no', prefix + series_count + "B")
	// 	frm.refresh_field('new_pawn_ticket_no')
	// } else if (frm.doc.pawn_ticket_type == "Pawn Ticket Non Jewelry" && frm.doc.transaction_type == "Renewal w/ Amortization") {
	// 	frm.set_value('new_pawn_ticket_no', prefix + series_count + "B")
	// 	frm.refresh_field('new_pawn_ticket_no')
	// } else if (frm.doc.pawn_ticket_type == "Pawn Ticket Jewelry" && (frm.doc.principal_amount >= 1500 && frm.doc.principal_amount <= 10000) && frm.doc.transaction_type == "Renewal w/ Amortization") {
	// 	frm.set_value('new_pawn_ticket_no', prefix + series_count + "A")
	// 	frm.refresh_field('new_pawn_ticket_no')
	// } else if(frm.doc.transaction_type == "Renewal w/ Amortization"){
	// 	frm.set_value('new_pawn_ticket_no', prefix + series_count + "B")
	// 	frm.refresh_field('new_pawn_ticket_no')
	// }
}

function select_transaction_type(frm) {					// Sets all field values calculations
	clear_all_payment_fields();
	frm.set_value('new_pawn_ticket_no', "");
	frm.refresh_field('new_pawn_ticket_no');
	if (frm.doc.transaction_type == "Redemption") {
		var total = 0.00;
		calculate_interest(frm);
		calculate_total_amortization(frm, frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
		show_previous_interest_payment(frm);
		total = parseFloat(frm.doc.interest_payment) + parseFloat(frm.doc.principal_amount) - parseFloat(frm.doc.discount);
		frm.set_value('total', total);
		frm.refresh_field('total');
	} else if (frm.doc.transaction_type == "Amortization") {
		calculate_total_amortization(frm, frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
		show_previous_interest_payment(frm);
	} else if (frm.doc.transaction_type == "Renewal w/ Amortization") {
		if (frm.doc.additional_amortization == 0) {
			frm.set_value('advance_interest', frm.doc.interest);
			frm.refresh_field('advance_interest');
		}
		calculate_interest(frm);
		calculate_total_amortization(frm, frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
		show_previous_interest_payment(frm);
	} else if(frm.doc.transaction_type == "Renewal"){
		calculate_interest(frm);
		calculate_total_amortization(frm, frm.doc.pawn_ticket_type, frm.doc.pawn_ticket_no);
		frm.set_value('interest_payment', parseFloat(frm.doc.interest_payment));
		frm.refresh_field('interest_payment');
		frm.set_value('advance_interest', parseFloat(frm.doc.interest));
		frm.refresh_field('advance_interest');
		show_previous_interest_payment(frm);
		frm.set_value('total', parseFloat(frm.doc.interest_payment) + parseFloat(frm.doc.advance_interest));
		frm.refresh_field('total');
		console.log(parseFloat(frm.doc.interest_payment));
	} else if (frm.doc.transaction_type == "Interest Payment") {
		calculate_interest(frm);
		calculate_advance_interest_payment(frm)
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
			let new_interest = (parseFloat(frm.doc.principal_amount) - parseFloat(frm.doc.additional_amortization)) * (rate/100);
			frm.set_value('advance_interest', new_interest);
			frm.refresh_field('advance_interest');
		})
	}
}

function calculate_advance_interest_payment(frm) { 			//For "Interest Payment" transaction
	let advance_interest_payment = parseFloat(frm.doc.interest) * parseInt(frm.doc.number_of_months_to_pay_in_advance);
	frm.set_value('total', advance_interest_payment);
	frm.refresh_field('total');
}

function show_previous_interest_payment(frm) {			// Gathers every provisional receipt that has the same pawn ticket, transaction type is "Interest Payment", and creditted checkbox is unchecked
	frappe.db.get_list('Provisional Receipt', {
		fields: ['total'],
		filters: {
			transaction_type: 'Interest Payment',
			creditted: 0,
			pawn_ticket_no: frm.doc.pawn_ticket_no,
			docstatus: 1
		} 
	}).then(records => {
		console.log(records);
		let temp_previous_interest_payment = 0.00
		for (let index = 0; index < records.length; index++) {
			console.log(records[index].total);
			temp_previous_interest_payment += parseFloat(records[index].total)
		}
		// console.log(temp_previous_interest_payment);
		frm.set_value('previous_interest_payment', temp_previous_interest_payment);
		frm.refresh_field('previous_interest_payment');
	})
}

function check_creditted_interest_payments(frm) {			//Check the checkbox "Creditted" in 
	frappe.db.get_list('Provisional Receipt', {
		fields: ['name'],
		filters: {
			transaction_type: 'Interest Payment',
			creditted: 0,
			pawn_ticket_no: frm.doc.pawn_ticket_no,
			docstatus: 1
		} 
	}).then(records => {
		for (let index = 0; index < records.length; index++) {
			frappe.db.set_value('Provisional Receipt', records[index].name, 'creditted', 1);
		}
	})
}

function subtract_previous_interest_payment(frm) {
	frm.set_value('interest_payment', parseFloat(frm.doc.interest_payment) - parseFloat(frm.doc.previous_interest_payment));
	frm.refresh_field('interest_payment');
}