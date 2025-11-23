import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from .models import Equipment
from django.db import models
from datetime import datetime


def smart_detect_columns(df):
    columns = df.columns.tolist()
    
    patterns = {
        'name': ['name', 'equipment', 'item', 'machine', 'device', 'unit'],
        'type': ['type', 'category', 'class', 'kind', 'classification'],
        'numeric': ['flow', 'rate', 'pressure', 'temp', 'temperature', 'value', 'reading']
    }
    
    detected = {
        'name_column': None,
        'type_column': None,
        'numeric_columns': []
    }
    
    for col in columns:
        col_lower = col.lower()
        if any(pattern in col_lower for pattern in patterns['name']):
            detected['name_column'] = col
            break
    
    if not detected['name_column']:
        detected['name_column'] = columns[0]
    
    for col in columns:
        col_lower = col.lower()
        if col != detected['name_column'] and any(pattern in col_lower for pattern in patterns['type']):
            detected['type_column'] = col
            break
    
    if not detected['type_column']:
        for col in columns:
            if col != detected['name_column'] and df[col].dtype == 'object':
                if df[col].nunique() < len(df) * 0.5:
                    detected['type_column'] = col
                    break
    
    if not detected['type_column'] and len(columns) > 1:
        detected['type_column'] = columns[1] if columns[1] != detected['name_column'] else None
    
    for col in columns:
        if col not in [detected['name_column'], detected['type_column']]:
            try:
                pd.to_numeric(df[col], errors='raise')
                detected['numeric_columns'].append(col)
            except (ValueError, TypeError):
                pass
    
    return detected


def process_csv_file(csv_file):
    try:
        df = pd.read_csv(csv_file)
        
        if df.empty:
            return False, "CSV file is empty"
        
        detected_cols = smart_detect_columns(df)
        
        name_col = detected_cols['name_column']
        type_col = detected_cols['type_column']
        numeric_cols = detected_cols['numeric_columns']
        
        if not name_col:
            return False, "Could not detect equipment name column"
        
        if len(numeric_cols) < 1:
            return False, "No numeric data columns found. CSV must contain at least one numeric column."
        
        total_equipment = len(df)
        
        averages = {}
        ranges = {}
        
        for col in numeric_cols:
            try:
                numeric_data = pd.to_numeric(df[col], errors='coerce')
                averages[col] = float(numeric_data.mean())
                ranges[col] = {
                    'min': float(numeric_data.min()),
                    'max': float(numeric_data.max()),
                    'std': float(numeric_data.std()),
                }
            except Exception as e:
                print(f"Error processing column {col}: {e}")
                continue
        
        type_distribution = {}
        if type_col:
            type_distribution = df[type_col].value_counts().to_dict()
        else:
            type_distribution = {'Equipment': total_equipment}
        
        equipment_list = []
        for idx, row in df.iterrows():
            equipment_data = {
                'name': str(row[name_col]),
                'type': str(row[type_col]) if type_col else 'Equipment',
                'numeric_data': {}
            }
            
            for col in numeric_cols:
                try:
                    equipment_data['numeric_data'][col] = float(pd.to_numeric(row[col], errors='coerce'))
                except:
                    equipment_data['numeric_data'][col] = 0.0
            
            equipment_list.append(equipment_data)
        
        column_summary = {
            'total_columns': len(df.columns),
            'name_column': name_col,
            'type_column': type_col,
            'numeric_columns': numeric_cols,
            'all_columns': df.columns.tolist()
        }
        
        data = {
            'total_equipment': total_equipment,
            'averages': averages,
            'ranges': ranges,
            'type_distribution': type_distribution,
            'equipment_list': equipment_list,
            'column_summary': column_summary,
            'detected_structure': detected_cols
        }
        
        return True, data
        
    except Exception as e:
        return False, f"Error processing CSV: {str(e)}"


def save_equipment_data(dataset, equipment_list, column_summary):
    equipment_objects = []
    
    numeric_cols = column_summary['numeric_columns']
    
    flowrate_sum = 0
    pressure_sum = 0
    temperature_sum = 0
    count = len(equipment_list)
    
    for item in equipment_list:
        equipment_data = {
            'dataset': dataset,
            'equipment_name': item['name'],
            'equipment_type': item['type'],
        }
        
        if len(numeric_cols) > 0:
            val = item['numeric_data'].get(numeric_cols[0], 0.0)
            equipment_data['flowrate'] = val
            flowrate_sum += val
        else:
            equipment_data['flowrate'] = 0.0
            
        if len(numeric_cols) > 1:
            val = item['numeric_data'].get(numeric_cols[1], 0.0)
            equipment_data['pressure'] = val
            pressure_sum += val
        else:
            equipment_data['pressure'] = 0.0
            
        if len(numeric_cols) > 2:
            val = item['numeric_data'].get(numeric_cols[2], 0.0)
            equipment_data['temperature'] = val
            temperature_sum += val
        else:
            equipment_data['temperature'] = 0.0
        
        equipment = Equipment(**equipment_data)
        equipment_objects.append(equipment)
    
    Equipment.objects.bulk_create(equipment_objects)
    
    if count > 0:
        dataset.avg_flowrate = round(flowrate_sum / count, 2)
        dataset.avg_pressure = round(pressure_sum / count, 2)
        dataset.avg_temperature = round(temperature_sum / count, 2)
        dataset.save()


def create_chart_images(dataset):
    plt.style.use('seaborn-v0_8-darkgrid')
    colors_palette = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']
    
    chart_images = {}
    
    type_dist = dataset.equipment.values('equipment_type').annotate(
        count=models.Count('id')
    )
    types = [item['equipment_type'] for item in type_dist]
    counts = [item['count'] for item in type_dist]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(types, counts, color=colors_palette[:len(types)], edgecolor='white', linewidth=2)
    ax.set_xlabel('Equipment Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Equipment Distribution by Type', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    buf1 = BytesIO()
    plt.savefig(buf1, format='png', dpi=150, bbox_inches='tight')
    buf1.seek(0)
    chart_images['bar_chart'] = buf1
    plt.close()
    
    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        counts, 
        labels=types, 
        autopct='%1.1f%%',
        colors=colors_palette[:len(types)],
        startangle=90,
        textprops={'fontsize': 11, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
    
    ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    buf2 = BytesIO()
    plt.savefig(buf2, format='png', dpi=150, bbox_inches='tight')
    buf2.seek(0)
    chart_images['pie_chart'] = buf2
    plt.close()
    
    equipment_data = dataset.equipment.all()[:15]
    names = [eq.equipment_name[:15] for eq in equipment_data]
    param1 = [eq.flowrate for eq in equipment_data]
    param2 = [eq.pressure for eq in equipment_data]
    param3 = [eq.temperature for eq in equipment_data]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(names, param1, marker='o', linewidth=2.5, label='Parameter 1', color='#2563eb', markersize=8)
    ax.plot(names, param2, marker='s', linewidth=2.5, label='Parameter 2', color='#10b981', markersize=8)
    ax.plot(names, param3, marker='^', linewidth=2.5, label='Parameter 3', color='#f59e0b', markersize=8)
    
    ax.set_xlabel('Equipment Name', fontsize=12, fontweight='bold')
    ax.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax.set_title('Parameter Trends Across Equipment (First 15 Items)', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', frameon=True, shadow=True, fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.tight_layout()
    
    buf3 = BytesIO()
    plt.savefig(buf3, format='png', dpi=150, bbox_inches='tight')
    buf3.seek(0)
    chart_images['line_chart'] = buf3
    plt.close()
    
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    all_flowrates = [eq.flowrate for eq in dataset.equipment.all()]
    all_pressures = [eq.pressure for eq in dataset.equipment.all()]
    all_temperatures = [eq.temperature for eq in dataset.equipment.all()]
    
    axes[0].boxplot(all_flowrates, vert=True, patch_artist=True,
                    boxprops=dict(facecolor='#93c5fd', color='#2563eb'),
                    medianprops=dict(color='#1e40af', linewidth=2))
    axes[0].set_title('Parameter 1\nDistribution', fontweight='bold')
    axes[0].set_ylabel('Value', fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)
    
    axes[1].boxplot(all_pressures, vert=True, patch_artist=True,
                    boxprops=dict(facecolor='#86efac', color='#10b981'),
                    medianprops=dict(color='#059669', linewidth=2))
    axes[1].set_title('Parameter 2\nDistribution', fontweight='bold')
    axes[1].set_ylabel('Value', fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)
    
    axes[2].boxplot(all_temperatures, vert=True, patch_artist=True,
                    boxprops=dict(facecolor='#fcd34d', color='#f59e0b'),
                    medianprops=dict(color='#d97706', linewidth=2))
    axes[2].set_title('Parameter 3\nDistribution', fontweight='bold')
    axes[2].set_ylabel('Value', fontweight='bold')
    axes[2].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    buf4 = BytesIO()
    plt.savefig(buf4, format='png', dpi=150, bbox_inches='tight')
    buf4.seek(0)
    chart_images['box_plot'] = buf4
    plt.close()
    
    return chart_images


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.grey)
        page_num = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 50, 30, page_num)
        self.drawString(50, 30, "Chemical Equipment Visualizer - Analysis Report")


def calculate_quartiles(values):
    if not values or len(values) == 0:
        return None
    
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    
    q1_idx = n // 4
    q2_idx = n // 2
    q3_idx = (3 * n) // 4
    
    q1 = sorted_vals[q1_idx]
    median = sorted_vals[q2_idx]
    q3 = sorted_vals[q3_idx]
    iqr = q3 - q1
    
    return {
        'q1': q1,
        'median': median,
        'q3': q3,
        'iqr': iqr
    }


def generate_pdf_report_with_charts(dataset):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=50, 
        leftMargin=50, 
        topMargin=50, 
        bottomMargin=50
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#6b7280'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#374151'),
        spaceAfter=10,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    note_style = ParagraphStyle(
        'NoteStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        leading=16,
        alignment=TA_JUSTIFY
    )
    
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("Chemical Equipment Analysis", title_style))
    elements.append(Paragraph("Comprehensive Data Analysis Report", subtitle_style))
    elements.append(Spacer(1, 0.5*inch))
    
    cover_info_data = [
        ['Dataset Name:', dataset.name],
        ['Generated On:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
        ['Uploaded By:', dataset.uploaded_by.username],
        ['Upload Date:', dataset.uploaded_at.strftime('%B %d, %Y')],
        ['Total Equipment:', str(dataset.total_equipment)],
    ]
    
    cover_table = Table(cover_info_data, colWidths=[2.5*inch, 4*inch])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#111827')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    
    elements.append(cover_table)
    elements.append(PageBreak())
    
    elements.append(Paragraph("1. Dataset Overview", heading2_style))
    elements.append(Spacer(1, 0.15*inch))
    
    equipment_stats = dataset.equipment.aggregate(
        max_flowrate=models.Max('flowrate'),
        min_flowrate=models.Min('flowrate'),
        std_flowrate=models.StdDev('flowrate'),
        var_flowrate=models.Variance('flowrate'),
        max_pressure=models.Max('pressure'),
        min_pressure=models.Min('pressure'),
        std_pressure=models.StdDev('pressure'),
        var_pressure=models.Variance('pressure'),
        max_temperature=models.Max('temperature'),
        min_temperature=models.Min('temperature'),
        std_temperature=models.StdDev('temperature'),
        var_temperature=models.Variance('temperature'),
    )
    
    overview_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(dataset.total_equipment)],
        ['Average Parameter 1 (Flowrate)', f"{dataset.avg_flowrate:.2f} m³/h"],
        ['Average Parameter 2 (Pressure)', f"{dataset.avg_pressure:.2f} bar"],
        ['Average Parameter 3 (Temperature)', f"{dataset.avg_temperature:.2f} °C"],
        ['Parameter 1 Range', f"{equipment_stats['min_flowrate']:.2f} - {equipment_stats['max_flowrate']:.2f} m³/h"],
        ['Parameter 2 Range', f"{equipment_stats['min_pressure']:.2f} - {equipment_stats['max_pressure']:.2f} bar"],
        ['Parameter 3 Range', f"{equipment_stats['min_temperature']:.2f} - {equipment_stats['max_temperature']:.2f} °C"],
    ]
    
    overview_table = Table(overview_data, colWidths=[4*inch, 2.5*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    
    elements.append(overview_table)
    elements.append(Spacer(1, 0.25*inch))
    
    type_dist = dataset.equipment.values('equipment_type').annotate(count=models.Count('id'))
    type_distribution = {item['equipment_type']: item['count'] for item in type_dist}
    
    elements.append(Paragraph("Equipment Type Distribution", heading3_style))
    elements.append(Spacer(1, 0.1*inch))
    
    type_data = [['Equipment Type', 'Count', 'Percentage']]
    for eq_type, count in type_distribution.items():
        percentage = (count / dataset.total_equipment) * 100
        type_data.append([eq_type, str(count), f"{percentage:.1f}%"])
    
    type_table = Table(type_data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdf4')])
    ]))
    
    elements.append(type_table)
    elements.append(PageBreak())
    
    elements.append(Paragraph("2. Data Visualizations", heading2_style))
    elements.append(Spacer(1, 0.15*inch))
    
    chart_images = create_chart_images(dataset)
    
    elements.append(Paragraph("2.1 Equipment Distribution Chart", heading3_style))
    elements.append(Spacer(1, 0.1*inch))
    bar_img = Image(chart_images['bar_chart'], width=6.5*inch, height=4*inch)
    elements.append(bar_img)
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("2.2 Type Distribution Breakdown", heading3_style))
    elements.append(Spacer(1, 0.1*inch))
    pie_img = Image(chart_images['pie_chart'], width=4.5*inch, height=4.5*inch)
    elements.append(pie_img)
    elements.append(PageBreak())
    
    elements.append(Paragraph("2.3 Parameter Trend Analysis", heading3_style))
    elements.append(Spacer(1, 0.1*inch))
    line_img = Image(chart_images['line_chart'], width=6.5*inch, height=3.5*inch)
    elements.append(line_img)
    elements.append(Spacer(1, 0.25*inch))
    
    elements.append(Paragraph("2.4 Statistical Distribution Analysis", heading3_style))
    elements.append(Spacer(1, 0.1*inch))
    box_img = Image(chart_images['box_plot'], width=6.5*inch, height=3*inch)
    elements.append(box_img)
    elements.append(PageBreak())
    
    elements.append(Paragraph("3. Comprehensive Statistical Analysis", heading2_style))
    elements.append(Spacer(1, 0.15*inch))
    
    stats_data = [
        ['Parameter', 'Average', 'Min', 'Max', 'Std Dev', 'Variance'],
        [
            'Flowrate',
            f"{dataset.avg_flowrate:.2f}",
            f"{equipment_stats['min_flowrate']:.2f}",
            f"{equipment_stats['max_flowrate']:.2f}",
            f"{equipment_stats['std_flowrate']:.2f}" if equipment_stats['std_flowrate'] else 'N/A',
            f"{equipment_stats['var_flowrate']:.2f}" if equipment_stats['var_flowrate'] else 'N/A'
        ],
        [
            'Pressure',
            f"{dataset.avg_pressure:.2f}",
            f"{equipment_stats['min_pressure']:.2f}",
            f"{equipment_stats['max_pressure']:.2f}",
            f"{equipment_stats['std_pressure']:.2f}" if equipment_stats['std_pressure'] else 'N/A',
            f"{equipment_stats['var_pressure']:.2f}" if equipment_stats['var_pressure'] else 'N/A'
        ],
        [
            'Temperature',
            f"{dataset.avg_temperature:.2f}",
            f"{equipment_stats['min_temperature']:.2f}",
            f"{equipment_stats['max_temperature']:.2f}",
            f"{equipment_stats['std_temperature']:.2f}" if equipment_stats['std_temperature'] else 'N/A',
            f"{equipment_stats['var_temperature']:.2f}" if equipment_stats['var_temperature'] else 'N/A'
        ],
    ]
    
    stats_table = Table(stats_data, colWidths=[1.5*inch, 1.1*inch, 1.0*inch, 1.0*inch, 1.1*inch, 1.1*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fffbeb')])
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("4. Quartile Distribution Analysis", heading2_style))
    elements.append(Spacer(1, 0.15*inch))
    
    all_flowrates = [eq.flowrate for eq in dataset.equipment.all()]
    all_pressures = [eq.pressure for eq in dataset.equipment.all()]
    all_temperatures = [eq.temperature for eq in dataset.equipment.all()]
    
    flowrate_quartiles = calculate_quartiles(all_flowrates)
    pressure_quartiles = calculate_quartiles(all_pressures)
    temperature_quartiles = calculate_quartiles(all_temperatures)
    
    quartile_data = [
        ['Parameter', 'Q1 (25%)', 'Median (Q2)', 'Q3 (75%)', 'IQR'],
        [
            'Flowrate',
            f"{flowrate_quartiles['q1']:.2f}" if flowrate_quartiles else 'N/A',
            f"{flowrate_quartiles['median']:.2f}" if flowrate_quartiles else 'N/A',
            f"{flowrate_quartiles['q3']:.2f}" if flowrate_quartiles else 'N/A',
            f"{flowrate_quartiles['iqr']:.2f}" if flowrate_quartiles else 'N/A'
        ],
        [
            'Pressure',
            f"{pressure_quartiles['q1']:.2f}" if pressure_quartiles else 'N/A',
            f"{pressure_quartiles['median']:.2f}" if pressure_quartiles else 'N/A',
            f"{pressure_quartiles['q3']:.2f}" if pressure_quartiles else 'N/A',
            f"{pressure_quartiles['iqr']:.2f}" if pressure_quartiles else 'N/A'
        ],
        [
            'Temperature',
            f"{temperature_quartiles['q1']:.2f}" if temperature_quartiles else 'N/A',
            f"{temperature_quartiles['median']:.2f}" if temperature_quartiles else 'N/A',
            f"{temperature_quartiles['q3']:.2f}" if temperature_quartiles else 'N/A',
            f"{temperature_quartiles['iqr']:.2f}" if temperature_quartiles else 'N/A'
        ],
    ]
    
    quartile_table = Table(quartile_data, colWidths=[1.5*inch, 1.2*inch, 1.3*inch, 1.2*inch, 1.2*inch])
    quartile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#faf5ff')])
    ]))
    
    elements.append(quartile_table)
    elements.append(Spacer(1, 0.2*inch))
    
    quartile_explanation_style = ParagraphStyle(
        'QuartileExplanation',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        leading=18,
        leftIndent=20,
        bulletIndent=10
    )
    
    quartile_note = """
    <b>Quartile Distribution Explanation:</b><br/>
    <br/>
    • <b>Q1 (25th percentile):</b> Twenty-five percent of all data points fall below this value<br/>
    <br/>
    • <b>Median (Q2, 50th percentile):</b> The middle value that divides the dataset into two equal halves<br/>
    <br/>
    • <b>Q3 (75th percentile):</b> Seventy-five percent of all data points fall below this value<br/>
    <br/>
    • <b>IQR (Interquartile Range):</b> A measure of statistical dispersion calculated as (Q3 - Q1), representing the middle 50% of the data
    """
    elements.append(Paragraph(quartile_note, quartile_explanation_style))
    elements.append(PageBreak())
    
    elements.append(Paragraph("5. Complete Equipment Data", heading2_style))
    elements.append(Spacer(1, 0.15*inch))
    
    equipment_list = dataset.equipment.all()[:50]
    
    table_data = [['#', 'Equipment Name', 'Type', 'Param 1', 'Param 2', 'Param 3']]
    
    for idx, eq in enumerate(equipment_list, 1):
        table_data.append([
            str(idx),
            eq.equipment_name[:25],
            eq.equipment_type[:15],
            f"{eq.flowrate:.2f}",
            f"{eq.pressure:.2f}",
            f"{eq.temperature:.2f}"
        ])
    
    equipment_table = Table(table_data, colWidths=[0.4*inch, 2.2*inch, 1.5*inch, 0.9*inch, 0.9*inch, 0.9*inch])
    equipment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#06b6d4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecfeff')])
    ]))
    
    elements.append(equipment_table)
    
    if dataset.total_equipment > 50:
        elements.append(Spacer(1, 0.15*inch))
        note_style_small = ParagraphStyle('NoteSmall', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#6b7280'), fontName='Helvetica-Oblique')
        elements.append(Paragraph(f"<i>Note: Displaying first 50 of {dataset.total_equipment} total equipment items.</i>", note_style_small))
    
    elements.append(PageBreak())
    
    elements.append(Paragraph("6. Operational Intelligence Dashboard", heading2_style))
    elements.append(Spacer(1, 0.15*inch))
    
    all_equipment = dataset.equipment.all()
    
    metrics_data = [['Parameter', 'Data Points', 'Efficiency', 'Status']]
    
    for param_name, values in [
        ('Parameter 1 (Flowrate)', all_flowrates),
        ('Parameter 2 (Pressure)', all_pressures),
        ('Parameter 3 (Temperature)', all_temperatures)
    ]:
        if values:
            avg = np.mean(values)
            data_range = max(values) - min(values)
            relative_spread = data_range / abs(avg) if avg != 0 else 0
            
            if relative_spread < 0.5:
                efficiency = 'Excellent'
                status = '✓ Stable'
            elif relative_spread < 1.0:
                efficiency = 'Good'
                status = '✓ Good'
            elif relative_spread < 2.0:
                efficiency = 'Fair'
                status = '⚠ Moderate'
            else:
                efficiency = 'Poor'
                status = '⚠ Review'
            
            metrics_data.append([
                param_name,
                str(len(values)),
                efficiency,
                status
            ])
    
    metrics_table = Table(metrics_data, colWidths=[2.8*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#06b6d4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecfeff')])
    ]))
    
    elements.append(metrics_table)
    elements.append(Spacer(1, 0.35*inch))
    
    elements.append(Paragraph("7. Summary", heading2_style))
    elements.append(Spacer(1, 0.15*inch))
    
    summary_text = f"""
    <b>Key Findings:</b><br/><br/>
    • Total equipment analyzed: <b>{dataset.total_equipment}</b> units<br/><br/>
    • Equipment types identified: <b>{len(type_distribution)}</b> categories<br/><br/>
    • Average Parameter 1 (Flowrate): <b>{dataset.avg_flowrate:.2f} m³/h</b><br/><br/>
    • Average Parameter 2 (Pressure): <b>{dataset.avg_pressure:.2f} bar</b><br/><br/>
    • Average Parameter 3 (Temperature): <b>{dataset.avg_temperature:.2f} °C</b>
    """
    
    summary_para = Paragraph(summary_text, note_style)
    elements.append(summary_para)
    
    doc.build(elements, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    
    for chart_buf in chart_images.values():
        chart_buf.close()
    
    return buffer