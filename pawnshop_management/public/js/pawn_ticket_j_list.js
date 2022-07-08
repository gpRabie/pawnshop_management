frappe.listview_settings['Pawn Ticket Jewelry'] = {
    // filters: [
    //     ['branch', '=', "Garcia's Pawnshop - CC"]
    // ],

    onload: function(){
        // if (listview.page.fields_dict.branch) {
        //     listview.page.fields_dict.branch.get_query = function(){
        //         return {
        //             "filters": {
        //                 "branch": "Garcia's Pawnshop - CC"
        //             }
        //         }
        //     }
        // }
        // listview.page.fields_dict.branch.set_input("Garcia's Pawnshop - CC")
        // listview.page.fields_dict.branch.read_only
        return [__("Branch"), "branch,=,Garcia's Pawnshop - CC"]
    }
}

// frappe.listview_settings['Pawn Ticket Jewelry'].formatters = {
//     branch(value){
//         return value ? "Garcia's Pawnshop - CC" : "Garcia's Pawnshop - POB"
//     }
// }