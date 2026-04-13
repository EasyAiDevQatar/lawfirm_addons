import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = []
	values = {}

	if filters.get("from_date"):
		conditions.append("ch.case_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]

	if filters.get("to_date"):
		conditions.append("ch.case_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	if filters.get("court"):
		conditions.append("ch.court = %(court)s")
		values["court"] = filters["court"]

	where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

	columns = [
		{"label": "Case", "fieldname": "case_name", "fieldtype": "Link", "options": "Case", "width": 140},
		{"label": "Registration No", "fieldname": "registration_no", "fieldtype": "Data", "width": 120},
		{"label": "Litigation Degree", "fieldname": "litigation_degree", "fieldtype": "Data", "width": 130},
		{"label": "Case Number", "fieldname": "case_number", "fieldtype": "Data", "width": 120},
		{"label": "Lawsuit Date", "fieldname": "lawsuit_date", "fieldtype": "Date", "width": 110},
		{"label": "Court", "fieldname": "court", "fieldtype": "Data", "width": 120},
		{"label": "Chamber", "fieldname": "chamber", "fieldtype": "Data", "width": 120},
		{"label": "Opponent", "fieldname": "opponent", "fieldtype": "Data", "width": 130},
		{"label": "Opponent Capacity", "fieldname": "opponent_capacity", "fieldtype": "Data", "width": 140},
		{"label": "Session Date", "fieldname": "session_date", "fieldtype": "Date", "width": 110},
		{"label": "Decision", "fieldname": "decision", "fieldtype": "Text", "width": 150},
		{"label": "Facts Summary", "fieldname": "facts_summary", "fieldtype": "Small Text", "width": 150},
		{"label": "Defense Summary", "fieldname": "defense_summary", "fieldtype": "Small Text", "width": 150},
	]

	data = frappe.db.sql(
		f"""
		SELECT
			ch.parent AS case_name,
			ch.registration_no,
			ch.litigation_degree,
			ch.case_number,
			ch.lawsuit_date,
			ch.court,
			ch.chamber,
			ch.opponent,
			ch.opponent_capacity,
			ch.case_date AS session_date,
			ch.decision,
			ch.facts_summary,
			ch.defense_summary
		FROM `tabCase History` ch
		{where_clause}
		ORDER BY ch.case_date DESC, ch.modified DESC
		""",
		values,
		as_dict=True,
	)

	return columns, data
