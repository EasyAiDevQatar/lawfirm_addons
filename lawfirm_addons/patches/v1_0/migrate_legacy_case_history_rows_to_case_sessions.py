"""Move rows from legacy tabCase History (casecentral schema) into tabCase Sessions with parentfield=case_sessions.

Placing them under Case Sessions lets the normal validate hook mirror them into Case History on save.
"""

from __future__ import annotations

import frappe


def execute():
	if not frappe.db.has_table("tabCase History"):
		return
	if not frappe.db.has_table("tabCase Sessions"):
		return

	legacy = frappe.db.sql(
		"""
		SELECT name, creation, modified, owner, modified_by, docstatus, idx,
			parent, parentfield, parenttype,
			judge, business_on_date, purpose_of_hearing, business_details, hearing_date
		FROM `tabCase History`
		WHERE parenttype = 'Case' AND parentfield = 'case_history'
		""",
		as_dict=True,
	)
	if not legacy:
		return

	for row in legacy:
		if frappe.db.exists("Case Sessions", row.name):
			continue

		attachments = row.get("business_details") or None

		frappe.db.sql(
			"""
			INSERT INTO `tabCase Sessions` (
				name, creation, modified, owner, modified_by, docstatus, idx,
				parent, parentfield, parenttype,
				registration_no, business_on_date, court, litigation_degree, case_number,
				chamber, case_subject, client, client_capacity, opponent, opponent_capacity,
				previous_decision, decision, next_date, facts_summary, defense_summary,
				attachments_note, agent
			) VALUES (
				%(name)s, %(creation)s, %(modified)s, %(owner)s, %(modified_by)s, %(docstatus)s, %(idx)s,
				%(parent)s, 'case_sessions', 'Case',
				NULL, %(business_on_date)s, NULL, NULL, NULL,
				%(chamber)s, %(case_subject)s, NULL, NULL, NULL, NULL,
				NULL, NULL, %(next_date)s, NULL, NULL,
				%(attachments_note)s, NULL
			)
			""",
			{
				"name": row.name,
				"creation": row.creation,
				"modified": row.modified,
				"owner": row.owner,
				"modified_by": row.modified_by,
				"docstatus": row.docstatus or 0,
				"idx": row.idx or 0,
				"parent": row.parent,
				"business_on_date": row.business_on_date,
				"chamber": row.judge,
				"case_subject": row.purpose_of_hearing,
				"next_date": row.hearing_date,
				"attachments_note": attachments or None,
			},
		)

	frappe.db.sql(
		"DELETE FROM `tabCase History` WHERE parenttype = 'Case' AND parentfield = 'case_history'"
	)
