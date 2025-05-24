# Copyright (c) 2025, Amos Kiprotich Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LibraryMember(Document):
	def after_insert(self):
		self.create_customer()



	def create_customer(self):
		if frappe.db.exists("Customer", self.name):
			return
		customer = frappe.new_doc("Customer")
		customer.customer_name = self.name
		customer.customer_type = "Library Member"
		customer.customer_group = "Individual"
		customer.territory = "All Territories"
		customer.save()
