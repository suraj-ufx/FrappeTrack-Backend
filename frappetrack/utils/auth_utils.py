import frappe

def get_logged_in_user():
    if frappe.session.user == "Guest":
        frappe.throw("Unauthorized", frappe.PermissionError)
    return frappe.session.user