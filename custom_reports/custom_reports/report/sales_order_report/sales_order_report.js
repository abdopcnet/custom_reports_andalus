// Copyright (c) 2025, future_support and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Order Report"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("الشركة"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_default("company"),
			"width": "80",
		},
		{
			"fieldname": "from_date",
			"label": __("من تاريخ"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.month_start(),
		},
		{
			"fieldname": "to_date",
			"label": __("إلى تاريخ"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "branch",
			"label": __("الفرع"),
			"fieldtype": "Link",
			"options": "Branch",
			"width": "80",
		},
		{
			"fieldname": "status",
			"label": __("الحالة"),
			"fieldtype": "MultiSelectList",
			"options": ["Draft", "On Hold", "To Deliver and Bill", "To Bill", "To Deliver", "Completed", "Cancelled", "Closed"],
			"width": "80",
		},
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname == "delay_days" && data && data.delay_days > 0) {
			value = "<span style='color:red;'>" + value + "</span>";
		}
		return value;
	},
};
