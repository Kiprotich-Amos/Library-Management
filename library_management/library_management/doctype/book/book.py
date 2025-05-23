# Copyright (c) 2025, Amos Kiprotich Rono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.docstatus import DocStatus
from frappe.model.document import Document

class Book(Document):
	def before_save(self):
		exist = frappe.db.exists("Book", {
			"book_id":self.book_id
		})
		if exist and (isinstance(exist, dict) and exist.get("name") != self.name):
			frappe.throw("A book with this Book ID already exists.")


