# Copyright (c) 2025, Amos Kiprotich Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff, nowdate
from frappe.model.document import Document

class Transaction(Document):
	def validate(self):
		if self.transaction_type == "Issue":
			if self.book and self.member:
				book = frappe.get_doc("Book", self.book)
				member = frappe.get_doc("Library Member", self.member)
				if member.outstanding > 500:
					frappe.throw("Member has Outstanding Debt over 500 KSH ")
				if book.quantity <1 :
					frappe.throw("Book not available")
				frappe.db.set_value("Book", self.book, "quantity", book.quantity - 1)
		
		if self.transaction_type == "Return":
			if self.book and self.member:
				book = frappe.get_doc("Book", self.book)
				member = frappe.get_doc("Library Member", self.member)
				rent = book.rent_fee
				self.rent_fee = rent
				member.outstanding += rent
				book.quantity += 1
				member.save()
				frappe.db.set_value("Book", self.book, "quantity", book.quantity + 1)




				