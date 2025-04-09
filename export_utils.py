import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from io import BytesIO
import xlsxwriter

class PDF(FPDF):
    def header(self):
        # Set up a logo
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'HKEPH Engineering Database Management System', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        # Add a footer with page numbers
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'R')

def generate_pdf_report(data, report_type, start_date, end_date):
    """
    Generate a PDF report based on the data and report type
    """
    pdf = PDF()
    pdf.add_page()
    
    # Add report title
    report_titles = {
        'soldering_tips': 'Soldering Tip Requisition Report',
        'machine_calibrations': 'Machine Calibration Scheduler Report',
        'overtime_logbook': 'Overtime Logbook Report',
        'equipment_downtime': 'Equipment Downtime Record Report'
    }
    
    title = report_titles.get(report_type, 'Report')
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, title, 0, 1, 'C')
    pdf.ln(5)
    
    # Add date range
    pdf.set_font('Arial', '', 12)
    date_range = f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    pdf.cell(0, 10, date_range, 0, 1)
    pdf.ln(5)
    
    # Add table headers based on report type
    pdf.set_font('Arial', 'B', 10)
    
    if report_type == 'soldering_tips':
        # Table header
        col_widths = [40, 40, 40, 30, 40]
        headers = ['Machine Name', 'Engineer Name', 'Personnel Name', 'Shift', 'Date']
        
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1, 0, 'C')
        pdf.ln()
        
        # Table data
        pdf.set_font('Arial', '', 10)
        for item in data:
            pdf.cell(col_widths[0], 10, item.machine_name, 1)
            pdf.cell(col_widths[1], 10, item.engineer_name, 1)
            pdf.cell(col_widths[2], 10, item.personnel_name, 1)
            pdf.cell(col_widths[3], 10, item.shift, 1)
            pdf.cell(col_widths[4], 10, item.date.strftime('%Y-%m-%d'), 1)
            pdf.ln()
    
    elif report_type == 'machine_calibrations':
        # Table header
        col_widths = [60, 40, 60, 40]
        headers = ['Machine Name', 'Days Per Calibration', 'Location/Line', 'Operator Name']
        
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1, 0, 'C')
        pdf.ln()
        
        # Table data
        pdf.set_font('Arial', '', 10)
        for item in data:
            pdf.cell(col_widths[0], 10, item.machine_name, 1)
            pdf.cell(col_widths[1], 10, str(item.days_per_calibration), 1)
            pdf.cell(col_widths[2], 10, item.location_line, 1)
            pdf.cell(col_widths[3], 10, item.operator_name, 1)
            pdf.ln()
    
    elif report_type == 'overtime_logbook':
        # Table header
        col_widths = [80, 50, 60]
        headers = ['Employee Name', 'Date', 'Hours']
        
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1, 0, 'C')
        pdf.ln()
        
        # Table data
        pdf.set_font('Arial', '', 10)
        for item in data:
            pdf.cell(col_widths[0], 10, item.employee_name, 1)
            pdf.cell(col_widths[1], 10, item.date.strftime('%Y-%m-%d'), 1)
            pdf.cell(col_widths[2], 10, str(item.hours), 1)
            pdf.ln()
    
    elif report_type == 'equipment_downtime':
        # Table header for first row
        col_widths = [50, 50, 40, 30, 20]
        headers = ['Equipment Name', 'Product Name', 'Date', 'Shift', 'Downtime (min)']
        
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1, 0, 'C')
        pdf.ln()
        
        # Table data
        pdf.set_font('Arial', '', 10)
        for item in data:
            pdf.cell(col_widths[0], 10, item.equipment_name, 1)
            pdf.cell(col_widths[1], 10, item.product_name, 1)
            pdf.cell(col_widths[2], 10, item.date.strftime('%Y-%m-%d'), 1)
            pdf.cell(col_widths[3], 10, item.shift, 1)
            pdf.cell(col_widths[4], 10, str(item.downtime_minutes), 1)
            pdf.ln()
            
            # Add issue and action taken with full width
            pdf.cell(0, 10, f"Issue: {item.issue}", 1, 1)
            pdf.cell(0, 10, f"Action Taken: {item.action_taken}", 1, 1)
            pdf.ln(5)
    
    # Add summary information
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Summary', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Total Records: {len(data)}', 0, 1)
    
    if report_type == 'overtime_logbook':
        total_hours = sum(item.hours for item in data)
        pdf.cell(0, 10, f'Total Hours: {total_hours}', 0, 1)
    
    elif report_type == 'equipment_downtime':
        total_downtime = sum(item.downtime_minutes for item in data)
        pdf.cell(0, 10, f'Total Downtime (minutes): {total_downtime}', 0, 1)
    
    # Save PDF to memory
    buffer = BytesIO()
    # For regular fpdf, use this method
    pdf.output(buffer, 'F')
    buffer.seek(0)
    return buffer

def generate_excel_report(data, report_type, start_date, end_date):
    """
    Generate an Excel report based on the data and report type
    """
    # Create a Pandas Excel writer using XlsxWriter as the engine
    buffer = BytesIO()
    
    # Initialize variables to avoid "possibly unbound" errors
    df = None
    df_summary = None
    
    # Different worksheets for different data types
    if report_type == 'soldering_tips':
        # Convert to pandas dataframe
        df = pd.DataFrame([{
            'Machine Name': item.machine_name,
            'Engineer Name': item.engineer_name,
            'Personnel Name': item.personnel_name,
            'Shift': item.shift,
            'Date': item.date,
            'Status': item.status,
            'Approval Date': item.approval_date
        } for item in data])
        
    elif report_type == 'machine_calibrations':
        df = pd.DataFrame([{
            'Machine Name': item.machine_name,
            'Days Per Calibration': item.days_per_calibration,
            'Location/Line': item.location_line,
            'Operator Name': item.operator_name,
            'Status': item.status,
            'Approval Date': item.approval_date
        } for item in data])
        
    elif report_type == 'overtime_logbook':
        df = pd.DataFrame([{
            'Employee Name': item.employee_name,
            'Date': item.date,
            'Hours': item.hours,
            'Status': item.status,
            'Approval Date': item.approval_date
        } for item in data])
        
        # Add a row with total hours
        total_hours = sum(item.hours for item in data)
        df_summary = pd.DataFrame([{'Employee Name': 'TOTAL', 'Hours': total_hours}])
        
    elif report_type == 'equipment_downtime':
        df = pd.DataFrame([{
            'Equipment Name': item.equipment_name,
            'Product Name': item.product_name,
            'Issue': item.issue,
            'Downtime (minutes)': item.downtime_minutes,
            'Shift': item.shift,
            'Action Taken': item.action_taken,
            'Date': item.date,
            'Status': item.status,
            'Approval Date': item.approval_date
        } for item in data])
        
        # Add a row with total downtime
        total_downtime = sum(item.downtime_minutes for item in data)
        df_summary = pd.DataFrame([{'Equipment Name': 'TOTAL', 'Downtime (minutes)': total_downtime}])
    
    # If we have valid data, create the Excel report
    if df is not None and not df.empty:
        # Create a Pandas Excel writer using XlsxWriter as the engine
        writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
        
        # Convert the dataframe to an XlsxWriter Excel object
        df.to_excel(writer, sheet_name='Report', index=False)
        
        # Add summary sheet for reports that have summaries
        if report_type in ['overtime_logbook', 'equipment_downtime'] and df_summary is not None:
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
        
        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Report']
        
        # Add a title with merged cells
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        report_titles = {
            'soldering_tips': 'Soldering Tip Requisition Report',
            'machine_calibrations': 'Machine Calibration Scheduler Report',
            'overtime_logbook': 'Overtime Logbook Report',
            'equipment_downtime': 'Equipment Downtime Record Report'
        }
        
        title = report_titles.get(report_type, 'Report')
        date_range = f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        
        # Merge cells for the title
        worksheet.merge_range('A1:H1', title, title_format)
        worksheet.merge_range('A2:H2', date_range, title_format)
        
        # Start writing the dataframe content from row 4
        worksheet.write('A4', f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        
        # Add autofilter and auto-size columns if we have data
        if len(df) > 0:
            # Add autofilter
            worksheet.autofilter(5, 0, 5 + len(df), len(df.columns) - 1)
            
            # Auto-size columns
            for i, col in enumerate(df.columns):
                column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, column_width)
        
        # Close the Pandas Excel writer and output the Excel file
        writer.close()
    else:
        # Create a simple Excel file with a message for no data
        writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
        empty_df = pd.DataFrame({'No Data': ['No records found for the selected date range.']})
        empty_df.to_excel(writer, sheet_name='Report', index=False)
        
        # Add a title for empty report
        workbook = writer.book
        worksheet = writer.sheets['Report']
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center'
        })
        
        report_titles = {
            'soldering_tips': 'Soldering Tip Requisition Report',
            'machine_calibrations': 'Machine Calibration Scheduler Report',
            'overtime_logbook': 'Overtime Logbook Report',
            'equipment_downtime': 'Equipment Downtime Record Report'
        }
        
        title = report_titles.get(report_type, 'Report')
        date_range = f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        
        worksheet.merge_range('A1:C1', title, title_format)
        worksheet.merge_range('A2:C2', date_range, title_format)
        worksheet.merge_range('A3:C3', 'No records found for the selected date range.', title_format)
        
        # Close the Pandas Excel writer
        writer.close()
    
    buffer.seek(0)
    return buffer