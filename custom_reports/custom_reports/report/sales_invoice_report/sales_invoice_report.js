// Copyright (c) 2025, future_support and contributors
// For license information, please see license.txt

frappe.query_reports["Sales_invoice_report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("من تاريخ"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
			"width": "50"
		},
		{
			"fieldname": "to_date",
			"label": __("إلى تاريخ"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"width": "50"
		},
		{
			"fieldname": "customer_name",
			"label": __("العميل"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": "80"
		},
		{
			"fieldname": "branch",
			"label": __("الفرع"),
			"fieldtype": "MultiSelectList",
			"options": [
				"الجموم",
				"الخضراء",
				"الراشدية",
				"الستين",
				"الشرائع",
				"العوالى",
				"المكتب الإداري",
				"النوارية",
				"ﻣﺬﺍﻕ ﺍﻟﻨﺒﻼﺀ ﻟﺨﺪﻣﺎﺕ ﺍﻻﻋﺎﺷﺔ"
			],
			"width": "80"
		},
		{
			"fieldname": "status",
			"label": __("الحالة"),
			"fieldtype": "MultiSelectList",
			"options": [
				"Return",
				"Credit Note Issued",
				"Submitted",
				"Paid",
				"Partly Paid",
				"Unpaid",
				"Unpaid and Discounted",
				"Partly Paid and Discounted",
				"Overdue and Discounted",
				"Overdue",
				"Internal Transfer"
			],
			"width": "80"
		},
		{
			"fieldname": "integration_status",
			"label": __("حالة الربط"),
			"fieldtype": "MultiSelectList",
			"options": [
				"Accepted",
				"Rejected",
				"Accepted with warnings"
			],
			"width": "80"
		}
	]
};

