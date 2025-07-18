// Copyright (c) 2025, future_support and contributors
// For license information, please see license.txt

frappe.query_reports["Sales_totals"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("من تاريخ"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_start()
        },
        {
            "fieldname": "to_date",
            "label": __("إلى تاريخ"),
            "fieldtype": "Date",
            "default": frappe.datetime.now_date()
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
            ]
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
            ]
        }
    ]
}
