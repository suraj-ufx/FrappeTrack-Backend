import frappe
from frappe import _

@frappe.whitelist(allow_guest=False)
def get_projects_list():
    """
    Endpoint to get the list of projects with filter status equal to 'Open'.
    Returns a dictionary with status, data, and message.
    """
    try:
        user = frappe.session.user
        
        projects = frappe.db.get_list("Project", 
            fields=["name", "project_name"], 
            filters={"status": "Open"}
        )

        if projects:
            return {
                "status": "success",
                "data": projects,
                "message": _("{0} Open projects found.").format(len(projects))
            }
        else:
            return {
                "status": "success",
                "data": [],
                "message": _("No open projects found.")
            }

    except Exception as e:
        return {
            "status": "failed",
            "message": _("An error occurred while fetching projects: {0}").format(str(e))
        }