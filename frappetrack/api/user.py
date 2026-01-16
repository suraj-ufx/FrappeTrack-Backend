import frappe
from frappe import _
import jwt
import responses
apiKeyEnv = "dshafjdjkfjewoirfj"
apiSecretEnv = "kdjkfjasdoifjierfalkew"

import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def login_with_email(email: str, password: str):
    """
    Login using email and password.
    Creates a session and sends sid cookie automatically.
    """

    # 1️⃣ Get user by email
    user = frappe.db.get_value("User", {"name": email}, "name")
    print(f"printing user: {user}")
    if not user:
        frappe.throw(_("Invalid email or password"), frappe.AuthenticationError)

    # 2️⃣ Authenticate
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=user, pwd=password)
        login_manager.post_login()
    except frappe.AuthenticationError:
        frappe.throw(_("Invalid email or password"), frappe.AuthenticationError)

    # 3️⃣ Return success (cookie already set)
    return {
        "success": True,
        "message": "Login successful",
        "user": frappe.session.user
    }



@frappe.whitelist()
def get_employee_profile():
    """
    Returns the employee details of the logged-in user.
    """
    try:
        # Guest check
        if frappe.session.user == "Guest":
            frappe.throw(
                "Unauthorized: Please login first",
                frappe.PermissionError
            )

        user = frappe.session.user
        print(f"this is user from session: {user}")
        employee = frappe.db.get_value(
            "Employee",
            {"user_id": user},
            ["name", "designation", "image"],
            as_dict=True
        )
        print(f"this is employee from db: {employee}")

        if employee and employee.get("image"):
            employee["image"] = frappe.utils.get_url(employee["image"])


        return {
            "success": True,
            "user": {
                "name": frappe.get_value("User", user, "full_name"),
                "email": frappe.get_value("User", user, "email"),
                "employee": employee
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Unable to fetch profile",
            "error": str(e)
        }
# @frappe.whitelist()
# def get_employee_profile():
#     """
#     Returns the employee details of the logged-in user.
#     """
#     try:
#         # Guest check
#         if frappe.session.user == "Guest":
#             frappe.throw("Unauthorized: Please login first", frappe.PermissionError)
       
#         headers = frappe.get_request_header("Authorization")
#         if headers and headers.startswith("token"):
#             token = headers[5:]
#             if ":" in token:
#                 apiKey, apiSecret = token.split(":", 1)

#         print(f"headers{headers}, apiKey- {apiKey}, apiSecret- {apiSecret}")

#         apiKeyToken = jwt.encode({"apiKey":apiKey}, apiKeyEnv, algorithm="HS256")
#         apiSecretToken = jwt.encode({"apiSecret":apiSecret}, apiSecretEnv, algorithm="HS256")

#         # frappe.
#         # response._HeaderSet("Set-Cookie", {apiKeyToken: apiSecretToken})
#         # setHeader("Set-Cookie", {apiKeyToken: apiSecretToken})

#         user = frappe.session.user
#         employee = frappe.db.get_value(
#             "Employee",
#             {"user_id": user},
#             ["name", "designation", "image"],
#             as_dict=True,
#         )

#         if employee and employee.get("image"):
#             employee["image"] = frappe.utils.get_url(employee["image"])

#         return {
#             "success": True,
#             "user": {
#                 "name": frappe.get_value("User", user, "full_name"),
#                 "email": frappe.get_value("User", user, "email"),
#                 "employee": employee,
#             },
#             "token": f"{apiKeyToken}:{apiSecretToken}"
#         }

#     except Exception as e:
#         return {"success": False, "message": "Unable to fetch profile", "error": str(e)}
