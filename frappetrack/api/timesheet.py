import frappe
from frappe import _
import base64
from frappe.utils.file_manager import save_file
from frappe.utils import flt

@frappe.whitelist(allow_guest=False)
def get_timesheet_by_task(task_id: str):
    """
    Fetch UNIQUE Draft Timesheets linked to a specific Task
    """
    try:
        # Step 1: Get unique Timesheet names from child table
        timesheet_names = frappe.db.get_all(
            "Timesheet Detail", filters={"task": task_id}, pluck="parent", distinct=True
        )

        if not timesheet_names:
            return {
                "status": "success",
                "data": [],
                "message": _("No draft timesheets found for this task."),
            }

        # Step 2: Fetch draft Timesheets only once
        timesheets = frappe.db.get_all(
            "Timesheet",
            filters={"name": ["in", timesheet_names], "status": "Draft"},
            fields=["name", "parent_project", "employee", "employee_name", "status"],
        )

        return {
            "status": "success",
            "data": timesheets,
            "message": _("{0} unique draft timesheets found for task {1}.").format(
                len(timesheets), task_id
            ),
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Timesheet By Task API Error")
        return {"status": "error", "message": str(e)}



@frappe.whitelist(allow_guest=False)
def create_timesheet(employee: str, parent_project: str, activity_type: str, taskByProject: str, descriptionStore: str):
    try:
        ts = frappe.new_doc("Timesheet")
        ts.employee = employee
        ts.parent_project = parent_project

        # REQUIRED: add at least one time log
        ts.append(
            "time_logs",
            {
                "activity_type": activity_type,
                "from_time": frappe.utils.now_datetime(),
                "to_time": frappe.utils.now_datetime(),
                "hours": 0,
                "project": parent_project,
                "task": taskByProject,
                "description": descriptionStore,
                "completed": 1
            },
        )

        ts.insert(ignore_permissions=True)
        # ts.db_set("title", ts.name)
        frappe.db.commit()

        # ✅ Return full object for frontend dropdown
        return {
            "status": "success",
            "data": {
                "name": ts.name,
                "title": ts.title,
                "project": parent_project,
                "task": taskByProject,
                "activity_type": activity_type
            }
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Timesheet API Error")
        return {"status": "error", "message": str(e)}
    
    
# @frappe.whitelist(allow_guest=False)
# def create_timesheet(
#     employee: str,
#     parent_project: str,
#     activity_type: str,
#     taskByProject: str,
#     descriptionStore: str,
# ):
#     try:
#         ts = frappe.new_doc("Timesheet")
#         ts.employee = employee
#         ts.parent_project = parent_project

#         print(f"logs: {employee}: {activity_type}: {parent_project}")
#         # REQUIRED: add at least one time log
#         ts.append(
#             "time_logs",
#             {
#                 "activity_type": activity_type,
#                 "from_time": frappe.utils.now_datetime(),
#                 "to_time": frappe.utils.now_datetime(),
#                 "hours": 0,
#                 "project": parent_project,
#                 "task": taskByProject,
#                 "description": descriptionStore,
#                 "completed":1
#             },
#         )

#         ts.insert(ignore_permissions=True)
#         frappe.db.commit()
        

#         return {"status": "success", "timesheet": ts.name}

#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Create Timesheet API Error")
#         return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=False)
def add_time_log(timesheet, time_log):
    """
    Append a new Time Log row to an existing Timesheet
    and set employee from the JSON payload
    """

    try:
        # Parse JSON if needed
        if isinstance(time_log, str):
            time_log = frappe.parse_json(time_log)

        # If employee is passed in JSON, use it
        employee = time_log.get("employee")
        if not employee:
            # Fallback: derive from session user (optional)
            employee = frappe.get_all(
                "Employee",
                filters={"user_id": frappe.session.user},
                limit=1,
                pluck="name",
            )
            employee = employee[0] if employee else None

        if not employee:
            frappe.throw("Employee must be specified or mapped to session user")

        # Get Timesheet
        ts = frappe.get_doc("Timesheet", timesheet)

        # Set employee
        ts.employee = employee

        # Set parent project
        ts.parent_project = time_log.get("project")
        # print(f"logs:, {time_log.get("hours"), time_log.get("completed")}")
        # Append time log
        row = ts.append(
            "time_logs",
            {
                "activity_type": time_log.get("activity_type"),
                "from_time": time_log.get("from_time"),
                "to_time": time_log.get("to_time"),
                "hours": time_log.get("hours"),
                "completed": 1,
                "project": time_log.get("project"),
                "task": time_log.get("task"),
                "is_billable": time_log.get("is_billable", 0),
                "billing_hours": time_log.get("billing_hours", 0),
                "billing_rate": time_log.get("billing_rate", 0),
                "costing_rate": time_log.get("costing_rate", 0),
                "description": time_log.get("description"),
            },
        )

        ts.save(ignore_permissions=True)
        frappe.db.set_value(
            "Timesheet Detail",
            row.name,
            "hours",
            time_log.get("hours"),
            update_modified=False
        )        
        frappe.db.commit()

        return {
            "status": "success",
            "timesheet": ts.name,
            "employee": ts.employee,
            "total_hours": ts.total_hours,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Add Time Log Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=False)
def upload_screenshot(file_name: str, file_data: str, mime_type: str, timesheet_id: str):
    try:
        content = base64.b64decode(file_data)
    
        # map mime → extension
        ext_map = {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
        }

        extension = ext_map.get(mime_type, "")

        full_name = f"{file_name}{extension}"

        file_doc = save_file(
            fname=full_name,
            content=content,
            dt="Timesheet",
            dn=timesheet_id,
            is_private=0,
        )

        return {
            "status": "success",
            "file_name": file_doc.file_name,
            "file_url": file_doc.file_url,
            "file_id": file_doc.name,
        }

    except Exception:
        frappe.log_error(
            title="Upload Screenshot Error",
            message=frappe.get_traceback(),
        )
        return {"status": "error"}
    
def clean_time_logs_before_submit(doc, method):
    """
    Remove invalid Time Logs (0 or None hours) before submitting Timesheet.
    Ensures at least one valid log exists.
    """
    if not doc.time_logs:
        frappe.throw("Timesheet cannot be submitted without Time Logs.")

    valid_logs = []

    for row in doc.time_logs:
        hours = flt(row.hours)
        if hours > 0:
            valid_logs.append(row)

    # Reassign filtered logs
    doc.time_logs = valid_logs

    # ✅ FIX: Reset idx (serial number)
    for i, row in enumerate(doc.time_logs, start=1):
        row.idx = i

    # Safety check
    if not doc.time_logs:
        frappe.throw("Cannot submit Timesheet without valid Time Logs.")