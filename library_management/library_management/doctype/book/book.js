// Copyright (c) 2025, Amos Kiprotich Rono and contributors
// For license information, please see license.txt

frappe.ui.form.on('Book', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Book',{
	after_submit: function(frm){
		if(frm.doc.docstatus===1){
			frappe.set_route('List', 'Book');
		}
	}
});
