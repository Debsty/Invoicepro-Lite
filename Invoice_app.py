import streamlit as st
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Alignment

# Streamlit App Title
st.title("📄 Invoice Generator App")

# Business Information Inputs
st.header("Business Information")
business_name = st.text_input("Business Name", "BrightTech Solutions")
business_address = st.text_input("Address", "123 Innovation Drive, Lagos, Nigeria")
business_phone = st.text_input("Phone", "+234-800-123-4567")
business_email = st.text_input("Email", "billing@brighttech.ng")

# Invoice Info
st.header("Invoice Details")
invoice_number = st.text_input("Invoice Number", "INV-2025-001")
invoice_date = st.date_input("Invoice Date")
due_date = st.date_input("Due Date")

# Client Information
st.header("Client Information (Billed To)")
client_name = st.text_input("Client Name", "Greenline Ventures")
client_address = st.text_input("Client Address", "45 Eco Avenue, Abuja, Nigeria")

# Invoice Items
st.header("Invoice Items")
items = st.text_area("Enter items (format: Item,Quantity,Unit Price):",
                     "Website Development,1,150000\nDomain Registration,1,10000\nHosting (12 months),1,30000")

# Process Items
invoice_data = []
for line in items.split("\n"):
    if line.strip():
        item, qty, price = line.split(",")
        qty = int(qty)
        price = float(price)
        invoice_data.append([item.strip(), qty, price, qty * price])

invoice_df = pd.DataFrame(invoice_data, columns=["Item", "Quantity", "Unit Price (₦)", "Amount (₦)"])
subtotal = invoice_df["Amount (₦)"].sum()
vat = subtotal * 0.075
total = subtotal + vat

st.subheader("Invoice Preview")
st.dataframe(invoice_df)
st.write(f"**Subtotal:** ₦{subtotal:,.2f}")
st.write(f"**VAT (7.5%):** ₦{vat:,.2f}")
st.write(f"**Total Amount:** ₦{total:,.2f}")

# Generate Excel
if st.button("Generate Invoice (Excel)"):
    business_info = [
        [business_name],
        [business_address],
        [f"Phone: {business_phone}"],
        [f"Email: {business_email}"],
        [""],
        ["INVOICE"],
        ["Invoice Number:", invoice_number],
        ["Invoice Date:", invoice_date.strftime("%b %d, %Y")],
        ["Due Date:", due_date.strftime("%b %d, %Y")],
        [""],
        ["Billed To:"],
        [client_name],
        [client_address],
        [""]
    ]

    totals = [
        ["", "", "Subtotal:", subtotal],
        ["", "", "VAT (7.5%):", vat],
        ["", "", "Total Amount:", total],
        [""],
        ["Payment Terms:"],
        ["Please make payment to the following account within 7 days:"],
        ["Bank: First Bank Nigeria"],
        ["Account Name: BrightTech Solutions"],
        ["Account Number: 1234567890"],
        [""],
        ["Thank you for your business!"]
    ]

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        pd.DataFrame(business_info).to_excel(writer, index=False, header=False, sheet_name="Invoice", startrow=0)
        invoice_df.to_excel(writer, index=False, sheet_name="Invoice", startrow=len(business_info) + 1)
        pd.DataFrame(totals).to_excel(writer, index=False, header=False, sheet_name="Invoice",
                                      startrow=len(business_info) + len(invoice_df) + 4)

    st.success("Invoice generated successfully!")
    st.download_button(
        label="📥 Download Invoice",
        data=output.getvalue(),
        file_name=f"{invoice_number}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
