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
					frappe.throw("Member has Outstanding Debt over 500 KSH")

				if book.quantity < 1:
					frappe.throw("Book not available")

				days = date_diff(self.return_date, self.issue_date)
				if days < 1:
					frappe.throw("Return Date must be after Issue Date")

				rent = book.rent_fee * days
				self.rent_fee = rent
				new_outstanding = member.outstanding + rent

				try:
					invoice = frappe.new_doc("Sales Invoice")
					invoice.customer = self.member
					invoice.due_date = self.return_date
					invoice.append("items", {
						"item_name": book.title,
						"description": f"Rental for '{book.title}' for {days} day(s)",
						"qty": 1,
						"rate": book.rent_fee,
						"amount": rent
					})
					invoice.insert()
					frappe.msgprint(f"Sales Invoice {invoice.name} created for {self.member}")

					self.invoice = invoice.name

					# Update outstanding and book quantity
					frappe.db.set_value("Library Member", self.member, "outstanding", new_outstanding)
					frappe.db.set_value("Book", self.book, "quantity", book.quantity - 1)

				except Exception as e:
					frappe.throw(f"Failed to create invoice: {e}")


		
		if self.transaction_type == "Return":
			if self.book and self.member:
				book = frappe.get_doc("Book", self.book)
				member = frappe.get_doc("Library Member", self.member)

				debt_fee = member.outstanding or 0
				amount = self.amount_paid or 0

				# Ensure amount is numeric
				try:
					amount = float(amount)
				except (TypeError, ValueError):
					frappe.throw("Amount Paid must be a valid number")

				new_outstanding = debt_fee - amount

				# Update member's outstanding and set balance
				if new_outstanding >= 0:
					member.outstanding = new_outstanding
					self.balance = 0
					self.remarks = f"Remaining outstanding is KSH {new_outstanding}"
				else:
					overpaid = abs(new_outstanding)
					member.outstanding = 0
					self.balance = overpaid
					self.remarks = f"Overpaid KSH {overpaid} — please refund or carry forward"

				# Update book quantity
				book.quantity += 1

				# Save updates
				member.save()
				book.save()
