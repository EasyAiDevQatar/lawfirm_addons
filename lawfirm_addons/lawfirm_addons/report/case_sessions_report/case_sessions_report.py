import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = []
	values = {}

	if filters.get("from_date"):
		conditions.append("cs.business_on_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]

	if filters.get("to_date"):
		conditions.append("cs.business_on_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	if filters.get("court"):
		conditions.append("cs.court = %(court)s")
		values["court"] = filters["court"]

	where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

	columns = [
		{"label": "Case", "fieldname": "case_name", "fieldtype": "Link", "options": "Case", "width": 140},
		{"label": "Registration No", "fieldname": "registration_no", "fieldtype": "Data", "width": 120},
		{"label": "Session Date", "fieldname": "session_date", "fieldtype": "Date", "width": 100},
		{"label": "Court", "fieldname": "court", "fieldtype": "Data", "width": 130},
		{"label": "Chamber", "fieldname": "chamber", "fieldtype": "Data", "width": 120},
		{"label": "Case Number", "fieldname": "case_number", "fieldtype": "Data", "width": 120},
		{"label": "Case Subject", "fieldname": "case_subject", "fieldtype": "Data", "width": 140},
		{"label": "Opponent", "fieldname": "opponent", "fieldtype": "Data", "width": 130},
		{"label": "Agent", "fieldname": "agent", "fieldtype": "Data", "width": 120},
		{"label": "Opponent Capacity", "fieldname": "opponent_capacity", "fieldtype": "Data", "width": 140},
		{"label": "Previous Decision", "fieldname": "previous_decision", "fieldtype": "Small Text", "width": 150},
		{"label": "Session Decision", "fieldname": "decision", "fieldtype": "Text", "width": 150},
		{"label": "Next Session Date", "fieldname": "next_date", "fieldtype": "Date", "width": 120},
	]

	data = frappe.db.sql(
		f"""
		SELECT
			cs.parent AS case_name,
			cs.registration_no,
			cs.business_on_date AS session_date,
			cs.court,
			cs.chamber,
			cs.case_number,
			cs.case_subject,
			cs.opponent,
			cs.agent,
			cs.opponent_capacity,
			cs.previous_decision,
			cs.decision,
			cs.next_date
		FROM `tabCase Sessions` cs
		{where_clause}
		ORDER BY cs.business_on_date DESC, cs.modified DESC
		""",
		values,
		as_dict=True,
	)

	return columns, data
