from __future__ import annotations

from frappe.utils import getdate, nowdate


def _build_history_signature(row) -> tuple:
	return (
		getattr(row, "registration_no", None),
		getattr(row, "business_on_date", None) or getattr(row, "case_date", None),
		getattr(row, "case_number", None),
		getattr(row, "decision", None),
	)


def move_due_sessions_to_history(doc, method=None):
	"""Move Case Sessions rows to Case History when next_date is today."""
	today = getdate(nowdate())
	session_rows = list(doc.get("case_sessions") or [])
	history_rows = doc.get("case_history") or []

	existing_signatures = {_build_history_signature(row) for row in history_rows}
	rows_to_remove = []

	for row in session_rows:
		if not row.get("next_date"):
			continue

		if getdate(row.next_date) != today:
			continue

		signature = (
			row.get("registration_no"),
			row.get("business_on_date"),
			row.get("case_number"),
			row.get("decision"),
		)
		if signature in existing_signatures:
			rows_to_remove.append(row)
			continue

		doc.append(
			"case_history",
			{
				"registration_no": row.get("registration_no"),
				"case_date": row.get("business_on_date"),
				"litigation_degree": row.get("litigation_degree"),
				"case_number": row.get("case_number"),
				"lawsuit_date": row.get("business_on_date"),
				"court": row.get("court"),
				"chamber": row.get("chamber"),
				"case_subject": row.get("case_subject"),
				"client": row.get("client"),
				"client_capacity": row.get("client_capacity"),
				"opponent": row.get("opponent"),
				"opponent_capacity": row.get("opponent_capacity"),
				"previous_decision": row.get("previous_decision"),
				"decision": row.get("decision"),
				"business_details": row.get("attachments_note"),
				"facts_summary": row.get("facts_summary"),
				"defense_summary": row.get("defense_summary"),
			},
		)
		existing_signatures.add(signature)
		rows_to_remove.append(row)

	for row in rows_to_remove:
		doc.remove(row)
