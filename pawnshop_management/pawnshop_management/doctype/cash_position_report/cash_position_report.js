// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cash Position Report', {
	refresh: function(frm) {
		if (frm.is_new()) {
			get_provisional_receipts_of_the_day(frm, frm.doc.date);
			get_non_jewelry_of_the_day(frm, frm.doc.date)
			frappe.db.get_list('Cash Position Report', {
				fields: ['ending_balance', 'date', 'creation'],
				filters: {
					date: frappe.datetime.add_days(frm.doc.date, -1)
				}
			}).then(records => {
				let latest_record = records[0]
				for (let index = 0; index < records.length; index++) {
					if (latest_record.creation < records[index].creation) {
						latest_record = records[index]
						console.log(latest_record);
					}
				}
				console.log(latest_record.ending_balance == null);
				frm.set_value('beginning_balance', latest_record.ending_balance)
				frm.refresh_field('beginning_balance')
			})
		}
		// frm.set_value('date', frappe.datetime.now_date())
		frm.add_custom_button('Test', () => {
			get_provisional_receipts_of_the_day(frm, '2022-02-09');
			get_non_jewelry_of_the_day(frm, '2022-02-27')
			frappe.db.get_list('Cash Position Report', {
				fields: ['ending_balance', 'date', 'creation'],
				filters: {
					date: frm.doc.date
				}
			}).then(records => {
				// for (let index = 0; index < records.length; index++) {
				// 	console.log(records[index]);
				// 	frm.set_value('beginning_balance',records[index].ending_balance);
				// 	frm.refresh_field('beginning_balance');
				// }
				console.log(records[0]);
			})
		})
	},

	date: function(frm){
		get_provisional_receipts_of_the_day(frm, frm.doc.date);
		get_non_jewelry_of_the_day(frm, frm.doc.date)
		frappe.db.get_list('Cash Position Report', {
			fields: ['ending_balance', 'date', 'creation'],
			filters: {
				date: frappe.datetime.add_days(frm.doc.date, -1)
			}
		}).then(records => {
			let latest_record = records[0]
			for (let index = 0; index < records.length; index++) {
				if (latest_record.creation < records[index].creation) {
					latest_record = records[index]
				}
			}
			frm.set_value('beginning_balance', latest_record.ending_balance)
			frm.refresh_field('beginning_balance')
		})
	},

	validate: function(frm){
		if (frm.doc.total_cash != frm.doc.ending_balance) {
			frappe.throw("Cash on hand is not equal to the Ending Balance")
		}
	},


	beginning_balance: function(frm){
		frm.set_value('ending_balance', 0.00);
		frm.set_value('ending_balance', calculate_ending_balance());
		frm.refresh_field('ending_balance');
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
	},

	one_thousand_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	five_hundred_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	two_hundred_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	one_hundred_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	fifty_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	twenty_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	ten_php_coin: function(frm){
		total_cash_breakdown(frm);
	},

	five_php_coin: function(frm){
		total_cash_breakdown(frm);
	},

	peso_php_coin: function(frm){
		total_cash_breakdown(frm);
	},

	twenty_five_cent_php_coin: function(frm){
		total_cash_breakdown(frm);
	},

	shortage_overage: function(frm){
		total_cash_breakdown(frm);
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
			date_issued: date_today,
			docstatus: 1
		}
	}).then(records => {
		let temp_total = 0.00;
		frm.set_value('provisional_receipts', 0.00);
		for (let index = 0; index < records.length; index++) {
			temp_total += parseFloat(records[index].total)
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
		}
		frm.set_value('jewelry_b', temp_total);
	})
}

function get_non_jewelry_of_the_day(frm, date_today=null) {
	frappe.db.get_list('Pawn Ticket Non Jewelry', {
		fields: ['net_proceeds'],
		filters: {
			date_loan_granted: date_today
		}
	}).then(records => {
		let temp_total = 0.00;
		frm.set_value('non_jewelry', 0.00);
		for (let index = 0; index < records.length; index++) {
			temp_total += parseFloat(records[index].net_proceeds)
		}
		frm.set_value('non_jewelry', temp_total);
	})
}

function total_cash_breakdown(frm) {
	let thousand_bill = parseFloat(frm.doc.one_thousand_php_bills);
	let five_hundred_bill = parseFloat(frm.doc.five_hundred_php_bills);
	let two_hundred_bill = parseFloat(frm.doc.two_hundred_php_bills);
	let one_hundred_bill = parseFloat(frm.doc.one_hundred_php_bills);
	let fifty_bill = parseFloat(frm.doc.fifty_php_bills);
	let twenty_bill = parseFloat(frm.doc.twenty_php_bills);
	let ten_peso_coin = parseFloat(frm.doc.ten_php_coin);
	let five_peso_coin = parseFloat(frm.doc.five_php_coin);
	let one_peso_coin = parseFloat(frm.doc.peso_php_coin);
	let twenty_five_cents = parseFloat(frm.doc.twenty_five_cent_php_coin);
	let total_cash_breakdown = (thousand_bill + five_hundred_bill + two_hundred_bill + one_hundred_bill + fifty_bill + twenty_bill + ten_peso_coin + five_peso_coin + one_peso_coin + twenty_five_cents) - parseFloat(frm.doc.shortage_overage);

	frm.set_value('total_cash', 0.00);
	frm.set_value('total_cash', total_cash_breakdown);
	frm.refresh_field('total_cash');
}
