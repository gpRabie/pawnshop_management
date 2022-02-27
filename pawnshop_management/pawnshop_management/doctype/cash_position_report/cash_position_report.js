// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cash Position Report', {
	refresh: function(frm) {
		get_provisional_receipts_of_the_day(frm, '2022-02-09');
		frm.add_custom_button('Test', () => {
			get_provisional_receipts_of_the_day(frm, '2022-02-09');
			get_non_jewelry_of_the_day(frm, '2022-02-27')
		})
	},

	provisional_receipts: function(frm){
		frm.set_value('total_in', 0.00);
		frm.set_value('total_in', + calculate_total_in());
		frm.refresh_field('total_in');
	},

	selling: function(frm){
		frm.set_value('total_in', 0.00);
		frm.set_value('total_in', + calculate_total_in());
		frm.refresh_field('total_in');
	},

	cash_from_vault: function(frm){
		frm.set_value('total_in', 0.00);
		frm.set_value('total_in', + calculate_total_in());
		frm.refresh_field('total_in');
	},

	jewelry_a: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	jewelry_b: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	non_jewelry: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	cash_to_vault: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	total_in: function(frm){
		frm.set_value('net_cash', 0.00);
		frm.set_value('net_cash', calculate_net_cash());
		frm.refresh_field('net_cash');
	},
	
	total_out: function(frm){
		frm.set_value('net_cash', 0.00);
		frm.set_value('net_cash', calculate_net_cash());
		frm.refresh_field('net_cash');
	},

	net_cash: function(frm){
		frm.set_value('ending_balance', 0.00);
		frm.set_value('ending_balance', calculate_ending_balance());
		frm.refresh_field('ending_balance');
	}
});

function calculate_total_in() {
	var total_in = parseFloat(cur_frm.doc.provisional_receipts) + parseFloat(cur_frm.doc.selling) + parseFloat(cur_frm.doc.cash_from_vault);
	return total_in;
}

function calculate_total_out(){
	var total_out = parseFloat(cur_frm.doc.jewelry_a) + parseFloat(cur_frm.doc.jewelry_b) + parseFloat(cur_frm.doc.cash_to_vault) + parseFloat(cur_frm.doc.non_jewelry);
	return total_out;
}

function calculate_net_cash() {
	var net_cash = calculate_total_in() - calculate_total_out();
	return net_cash;
}

function calculate_ending_balance() {
	var ending_balance = parseFloat(cur_frm.doc.beginning_balance) + calculate_net_cash();
	return ending_balance;
}
function get_provisional_receipts_of_the_day(frm, date_today = null) {
	console.log(date_today);
	frappe.db.get_list('Provisional Receipt', {
		fields: ['total'],
		filters: {
			date_issued: date_today
		}
	}).then(records => {
		let temp_total = 0.00;
		frm.set_value('provisional_receipts', 0.00);
		for (let index = 0; index < records.length; index++) {
			temp_total += parseFloat(records[index].total)
			console.log(temp_total);
		}
		frm.set_value('provisional_receipts', temp_total);
	})
}

function get_jewelry_a_of_the_day(frm, date_today=null) {
	frappe.db.get_list('Pawn Ticket Jewelry', {
		fields: ['net_proceeds'],
		filters: {
			date_loan_granted: date_today,
			item_series: 'A'
		}
	}).then(records => {
		let temp_total = 0.00;
		frm.set_value('jewelry_a', 0.00);
		for (let index = 0; index < records.length; index++) {
			temp_total += parseFloat(records[index].net_proceeds)
			console.log(temp_total);
		}
		frm.set_value('jewelry_a', temp_total);
	})
}

function get_jewelry_b_of_the_day(frm, date_today=null) {
	frappe.db.get_list('Pawn Ticket Jewelry', {
		fields: ['net_proceeds'],
		filters: {
			date_loan_granted: date_today,
			item_series: 'B'
		}
	}).then(records => {
		let temp_total = 0.00;
		frm.set_value('jewelry_b', 0.00);
		for (let index = 0; index < records.length; index++) {
			temp_total += parseFloat(records[index].net_proceeds)
			console.log(temp_total);
		}
		frm.set_value('jewelry_b', temp_total);
	})
}

function get_non_jewelry_of_the_day(frm, date_today=null) {
	frappe.db.get_list('Pawn Ticket Non Jewelry', {
		fields: ['net_proceeds'],
		filters: {
			date_loan_granted: date_today,
			workflow_state: 'Active'
		}
	}).then(records => {
		let temp_total = 0.00;
		frm.set_value('non_jewelry', 0.00);
		for (let index = 0; index < records.length; index++) {
			temp_total += parseFloat(records[index].net_proceeds)
			console.log(temp_total);
		}
		frm.set_value('non_jewelry', temp_total);
	})
}