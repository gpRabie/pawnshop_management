import frappe

@frappe.whitelist()
def change_role(email):
    # user_role = frappe.get_doc("User", email)
    # user_role.append('roles', {
    #     "doctype": "Has Role",
    #     "role": "Pawnshop Cashier"
    # })
    # user_role.save(ignore_permissions=True)
    remove_cashier_role()
    add_cashier_role(email)


def remove_cashier_role():
    users = frappe.db.get_list('User', pluck='name')
    for i in range(len(users)):
        if users[i] != "Administrator":
            user_role = frappe.get_doc("User", users[i])
            user_role.remove_roles("Pawnshop Cashier")
            user_role.save(ignore_permissions=True)


def add_cashier_role(email):
    user_role = frappe.get_doc("User", email)
    user_role.add_roles("Pawnshop Cashier")
    user_role.save(ignore_permissions=True)