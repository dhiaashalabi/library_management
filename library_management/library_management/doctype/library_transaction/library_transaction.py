# Copyright (c) 2022, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LibraryTransaction(Document):
	def before_submit(self):
		article = frappe.get_doc('Article', self.article)
		if self.type == 'Issue':
			self.validate_issue()
			self.validate_maximum_limit()
			article.status = 'Issued'
			article.save()
		elif self.type == 'Return':
			self.validate_return()
			article.status = 'Available'
			article.save()

	def validate_issue(self):
		self.validate_membership()
		article = frappe.get_doc('Article', self.article)
		if article.status == 'Issued':
			frappe.throw('Article is already issued by another member')

	def validate_return(self):
		article = frappe.get_doc('Article', self.article)
		if article.status == 'Available':
			frappe.throw('Article cannot be returned without being issued first')

	def validate_maximum_limit(self):
		# max_articles = frappe.db.get_single_value('Library Settings', 'max_articles')
		max_articles  = frappe.get_single('Library Settings').max_articles
		count = frappe.db.count(
            'Library Transaction',
            {'library_member': self.library_member, 'type': 'Issue', 'docstatus': 1},
        )
		if count >= max_articles:
			frappe.throw('Maximum limit reached for issuing articles')

	def validate_membership(self):
		valid_membership = frappe.db.exists(
			'Library Membership',
			{
				'library_member': self.library_member,
				'docstatus': 1,
				'from_date': ('<', self.date),
				'to_date': ('>', self.date),
			},
		)
		if not valid_membership:
			frappe.throw('The member does not have a valid membership')