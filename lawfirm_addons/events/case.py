from __future__ import annotations

# Fields aligned with Case Sessions; next_date is intentionally excluded.
_SESSION_TO_HISTORY_FIELDS = (
	"registration_no",
	"business_on_date",
	"court",
	"litigation_degree",
	"case_number",
	"chamber",
	"case_subject",
	"client",
	"client_capacity",
	"opponent",
	"opponent_capacity",
	"previous_decision",
	"decision",
	"facts_summary",
	"defense_summary",
	"attachments_note",
	"agent",
)


def sync_case_history_from_sessions(doc, method=None):
	"""Mirror Case Sessions into Case History (same fields as sessions; excludes next session date)."""
	if doc.doctype != "Case":
		return

	sessions = doc.get("case_sessions") or []
	if not sessions:
		return

	doc.set("case_history", [])

	for row in sessions:
		entry = {fieldname: row.get(fieldname) for fieldname in _SESSION_TO_HISTORY_FIELDS}
		doc.append("case_history", entry)
