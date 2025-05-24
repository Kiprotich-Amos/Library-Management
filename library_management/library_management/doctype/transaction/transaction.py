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

				days = date_diff(self.return_date, self.issue_date)
				if days <1:
					frappe.throw("Return Date must Be after issue date")

				rent = book.rent_fee * days
				self.rent_fee = rent
				new_outstanding = member.outstanding + self.rent_fee
				# creating invoice
				invoice = frappe.new_doc("Sales Invoice")
				invoice.customer = self.member
				invoice.due_date = self.return_date
				invoice.append("items", {
					"item_name": book.title,
					"description": f"Rental for '{book.title}' for {days} day(s)",
					"qty": 1,
					"rate":book.rent_fee,
					"amount": new_outstanding
				})
				invoice.insert()
				frappe.msgprint(f"Sales Invoice{invoice.name} created for {self.member}")
				self.invoice = invoice.name
				frappe.db.set_value("Library Member",self.member, "outstanding", new_outstanding)				
				frappe.db.set_value("Book", self.book, "quantity", book.quantity - 1)


		
		if self.transaction_type == "Return":
			if self.book and self.member:
				book = frappe.get_doc("Book", self.book)
				member = frappe.get_doc("Library Member", self.member)

				debt_fee = member.outstanding or 0	
				amount = self.amount_paid or 0
				new_outstanding = debt_fee - amount

            # Update member's outstanding
			if new_outstanding >= 0:
				member.outstanding = new_outstanding
				self.balance = 0
				self.remarks = f"Remaining outstanding is KSH {new_outstanding}"
			else:
                # Overpayment
				overpaid = abs(new_outstanding)
				member.outstanding = 0
				self.balance = overpaid
				self.remarks = f"Overpaid KSH {overpaid} — please refund or carry forward"

            # Update book quantity
			book.quantity += 1
			member.save()
			book.save()
			frappe.db.set_value("Book", self.book, "quantity", book.quantity + 1)
			frappe.db.set_value("Library Member",self.member, "outstanding", new_outstanding)



				