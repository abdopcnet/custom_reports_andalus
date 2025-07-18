// Copyright (c) 2025, future_support and contributors
// For license information, please see license.txt

frappe.query_reports["sale_invoice_tax"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"), 
            "fieldtype": "Date",
            "default": frappe.datetime.month_start(), 
            "mandatory": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "mandatory": 1
        },
        {
            "fieldname": "customer_name",
            "label": __("Customer"), 
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname": "branch",
            "label": __("Branch"),
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
            "label": __("Status"),
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
};

