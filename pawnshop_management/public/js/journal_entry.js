frappe.ui.form.on("Journal Entry", {
    refresh:function(frm){
        // frm.add_custom_button('Import Data', () =>{
        //     frappe.call({
        //         // method: 'fx.foreign_exchange.test.hello',

        //         // callback: function(r){
        //         //     frappe.msgprint(r)
        //         // },

        //         method: 'fx.foreign_exchange_management.custom_codes.journal_entry_import.create_new_journal_entry',
        //         callback: function(r){
        //             frappe.show_alert({
        //                 message: 'Import Succesful',
        //                 indicator: 'green'
        //             })
        //         },

        //         error: function(r){
        //             frappe.show_alert({
        //                message: 'Import failed',
        //                indicator: 'red'
        //             })
        //         }
        //     })
        // })

        frm.set_query('reference_doctype', () => {
			return {
				"filters": {
					"name":
					[
						'in',
						[
							"Pawn Ticket Jewelry",
							"Pawn Ticket Non Jewelry",
                            "Provisional Receipt",
                            "Cash Position Report"
						]
					]
				}
			}
		})
    }
})