import frappe
from frappe import _

@frappe.whitelist(allow_guest=False)
def get_activity_type()-> dict:
    """
    This endpoint returns activity type's list.
    """
    try:
        # user = frappe.session.user
        acitvity_types = frappe.db.get_list(
            "Activity Type",
            fields=["name"],
            filters={
                "disabled": 0
            }, 
            order_by="name asc",
        )

        return {
            "status": "success",
            "data": acitvity_types
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_activity_type failed")
        return {
            "status": "failed",
            "message": str(e)
        }