import frappe
from frappe import _


@frappe.whitelist(allow_guest=False)
def get_task_list()-> dict:
    """
    Returns a list of open tasks.
    """
    try:
        user = frappe.session.user

        tasks = frappe.db.get_list("Task", 
            fields=["name", "subject"], 
            filters={"status": "Open"}
        )

        if tasks:
            return {
                "status": "success",
                "data": tasks,
                "message": _("{0} Open tasks found.").format(len(tasks))
            }
        else:
            return {
                "status": "success",
                "data": [],
                "message": _("No open tasks found.")
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist(allow_guest=False)
def get_task_by_project(project_id: str):
    """
    Fetches a list of 'Open' tasks associated with a specific Project ID.
    """
    try:
        user = frappe.session.user

        tasks = frappe.db.get_list(
            "Task",
            fields=["name", "subject", "status"],
            filters={
                "project": project_id,
                "status": "Open"
            }
        )

        if tasks:
            return {
                "status": "success",
                "data": tasks,
                "message": _("{0} tasks found for project {1}.")
                .format(len(tasks), project_id)
            }
        else:
            return {
                "status": "success",
                "data": [],
                "message": _("No tasks found for this project.")
            }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_task_by_project failed")
        return {
            "status": "failed",
            "message": str(e)
        }


@frappe.whitelist(allow_guest=False)
def create_task(project_id: str, subject: str, priority: str):
    try:
        pass

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "create_task failed")
        return {
            "status": "failed",
            "message": str(e)
        }