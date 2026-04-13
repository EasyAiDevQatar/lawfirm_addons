import frappe
from frappe.utils import getdate, nowdate


def _get_case_table_fieldname(child_doctype: str) -> str | None:
	case_meta = frappe.get_meta("Case")
	for field in case_meta.fields:
		if field.fieldtype == "Table" and field.options == child_doctype:
			return field.fieldname
	return None


def _build_history_signature(row) -> tuple:
	return (
		getattr(row, "registration_no", None),
		getattr(row, "business_on_date", None) or getattr(row, "case_date", None),
		getattr(row, "case_number", None),
		getattr(row, "decision", None),
	)


def migrate_due_case_sessions_to_history() -> None:
	"""Move due session rows into case history rows."""
	session_fieldname = _get_case_table_fieldname("Case Sessions")
	history_fieldname = _get_case_table_fieldname("Case History")

	if not session_fieldname or not history_fieldname:
		frappe.log_error(
			"Could not detect Case child table fields for Case Sessions/Case History",
			"Lawfirm Addons Session Migration",
		)
		return

	today = getdate(nowdate())
	case_names = frappe.get_all("Case", pluck="name")

	for case_name in case_names:
		case_doc = frappe.get_doc("Case", case_name)
		session_rows = list(case_doc.get(session_fieldname) or [])
		history_rows = case_doc.get(history_fieldname) or []

		existing_signatures = {_build_history_signature(row) for row in history_rows}
		rows_to_remove = []
		changed = False

		for row in session_rows:
			if not row.get("next_date"):
				continue

			if getdate(row.next_date) > today:
				continue

			signature = (
				row.get("registration_no"),
				row.get("business_on_date"),
				row.get("case_number"),
				row.get("decision"),
			)
			if signature in existing_signatures:
				rows_to_remove.append(row)
				changed = True
				continue

			case_doc.append(
				history_fieldname,
				{
					"registration_no": row.get("registration_no"),
					"case_date": row.get("business_on_date"),
					"case_number": row.get("case_number"),
					"lawsuit_date": row.get("business_on_date"),
					"court": row.get("court"),
					"chamber": row.get("chamber"),
					"opponent": row.get("opponent"),
					"opponent_capacity": row.get("opponent_capacity"),
					"decision": row.get("decision"),
					"facts_summary": row.get("facts_summary"),
					"defense_summary": row.get("defense_summary"),
				},
			)
			existing_signatures.add(signature)
			rows_to_remove.append(row)
			changed = True

		for row in rows_to_remove:
			case_doc.remove(row)

		if changed:
			case_doc.save(ignore_permissions=True)
