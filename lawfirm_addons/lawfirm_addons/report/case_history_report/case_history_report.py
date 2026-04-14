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

	if filters.get("customer_name"):
		conditions.append("c.customer_name LIKE %(customer_name)s")
		values["customer_name"] = f"%{filters['customer_name']}%"

	if filters.get("case_number"):
		conditions.append("ch.case_number LIKE %(case_number)s")
		values["case_number"] = f"%{filters['case_number']}%"

	where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

	columns = [
		{"label": "Case", "fieldname": "case_name", "fieldtype": "Link", "options": "Case", "width": 140},
		{"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "width": 140},
		{"label": "Registration No", "fieldname": "registration_no", "fieldtype": "Data", "width": 120},
		{"label": "Session Date", "fieldname": "session_date", "fieldtype": "Date", "width": 110},
		{"label": "Court", "fieldname": "court", "fieldtype": "Data", "width": 120},
		{"label": "Litigation Degree", "fieldname": "litigation_degree", "fieldtype": "Data", "width": 130},
		{"label": "Case Number", "fieldname": "case_number", "fieldtype": "Data", "width": 120},
		{"label": "Chamber", "fieldname": "chamber", "fieldtype": "Data", "width": 120},
		{"label": "Case Subject", "fieldname": "case_subject", "fieldtype": "Data", "width": 140},
		{"label": "Client", "fieldname": "client", "fieldtype": "Data", "width": 120},
		{"label": "Client Capacity", "fieldname": "client_capacity", "fieldtype": "Data", "width": 120},
		{"label": "Opponent", "fieldname": "opponent", "fieldtype": "Data", "width": 130},
		{"label": "Opponent Capacity", "fieldname": "opponent_capacity", "fieldtype": "Data", "width": 140},
		{"label": "Previous Decision", "fieldname": "previous_decision", "fieldtype": "Small Text", "width": 150},
		{"label": "Decision", "fieldname": "decision", "fieldtype": "Text", "width": 150},
		{"label": "Lawsuit Date", "fieldname": "lawsuit_date", "fieldtype": "Date", "width": 110},
		{"label": "Facts Summary", "fieldname": "facts_summary", "fieldtype": "Small Text", "width": 150},
		{"label": "Defense Summary", "fieldname": "defense_summary", "fieldtype": "Small Text", "width": 150},
	]

	data = frappe.db.sql(
		f"""
		SELECT
			ch.parent AS case_name,
			c.customer_name,
			ch.registration_no,
			ch.case_date AS session_date,
			ch.court,
			ch.litigation_degree,
			ch.chamber,
			ch.case_number,
			ch.case_subject,
			ch.client,
			ch.client_capacity,
			ch.opponent,
			ch.opponent_capacity,
			ch.previous_decision,
			ch.decision,
			ch.lawsuit_date,
			ch.facts_summary,
			ch.defense_summary
		FROM `tabCase History` ch
		INNER JOIN `tabCase` c ON c.name = ch.parent
		{where_clause}
		ORDER BY ch.case_date DESC, ch.modified DESC
		""",
		values,
		as_dict=True,
	)

	return columns, data
