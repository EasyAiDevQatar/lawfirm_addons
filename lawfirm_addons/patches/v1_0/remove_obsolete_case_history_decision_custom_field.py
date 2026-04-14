import frappe


def execute():
	name = "Case History-decision"
	if frappe.db.exists("Custom Field", name):
		frappe.delete_doc("Custom Field", name, force=True)
