from . import __version__ as app_version

app_name = "pawnshop_management"
app_title = "Pawnshop Management"
app_publisher = "Rabie Moses Santillan"
app_description = "Pawnshop Management System"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "gprabiemosessantillan@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/pawnshop_management/css/pawnshop_management.css"
# app_include_js = "/assets/pawnshop_management/js/pawnshop_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/pawnshop_management/css/pawnshop_management.css"
# web_include_js = "/assets/pawnshop_management/js/pawnshop_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "pawnshop_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "pawnshop_management.install.before_install"
# after_install = "pawnshop_management.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "pawnshop_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"pawnshop_management.tasks.all"
# 	],
# 	"daily": [
# 		"pawnshop_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"pawnshop_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"pawnshop_management.tasks.weekly"
# 	]
# 	"monthly": [
# 		"pawnshop_management.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "pawnshop_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "pawnshop_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "pawnshop_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"pawnshop_management.auth.validate"
# ]

# fixtures = [
# 	"Workflow State",
# 	"Role",
# 	"Role Profile",
# 	"DocPerm", 		# Role Permissions Manager
# 	"Workspace",
# 	"Print Settings", 		# Print Option will only be available after submit
# 	"Workflow",
# 	"Naming Series"
# ]

