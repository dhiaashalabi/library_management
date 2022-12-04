# Copyright (c) 2022, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LibraryMembership(Document):
	def before_submit(self):
		exists = frappe.db.exists(
			'Library Membership',
			{
				'library_member': self.library_member,
				'docstatus':1,
				'to_date': ('>', self.from_date),
			},
		)
		if exists:
			frappe.throw('Cannot have overlapping memberships')
		# loan_period = frappe.db.get_single_value('Library Settings', 'loan_period')
		loan_period = frappe.get_single('Library Settings').loan_period
		self.to_date = frappe.utils.add_days(self.from_date, loan_period)
