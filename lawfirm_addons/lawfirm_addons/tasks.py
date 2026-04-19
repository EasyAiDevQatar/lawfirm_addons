import frappe

from lawfirm_addons.events.case import sync_case_history_from_sessions


def migrate_case_history_from_sessions_bulk() -> None:
	"""One-off maintenance: resync Case History from Case Sessions for all cases."""
	for name in frappe.get_all("Case", pluck="name"):
		doc = frappe.get_doc("Case", name)
		sync_case_history_from_sessions(doc)
		doc.save(ignore_permissions=True)


# Backwards compatibility
migrate_due_case_sessions_to_history = migrate_case_history_from_sessions_bulk
