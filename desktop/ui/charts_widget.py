from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QScrollArea, QGridLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
import os
import sys
import tempfile
import subprocess


class ChartsWidget(QWidget):
    def __init__(self, api):
        super().__init__()
        self.api = api
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(25)
        
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f0f4f8, stop:0.5 #e8eef5, stop:1 #dde7f3);
            }
        """)
        
        header_container = QFrame()
        header_container.setMinimumHeight(140)
        header_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:0.3 #764ba2, stop:0.7 #f093fb, stop:1 #667eea);
                border-radius: 25px;
            }
        """)
        header_shadow = QGraphicsDropShadowEffect()
        header_shadow.setBlurRadius(40)
        header_shadow.setColor(QColor(102, 126, 234, 120))
        header_shadow.setOffset(0, 8)
        header_container.setGraphicsEffect(header_shadow)
        
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(40, 30, 40, 30)
        header_layout.setSpacing(8)
        
        title = QLabel("Data Visualization and Analytics Dashboard")
        title.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title.setWordWrap(True)
        title.setStyleSheet("""
            color: white;
            padding: 0px;
            letter-spacing: 1.5px;
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Comprehensive interactive charts and detailed statistical insights for chemical equipment parameter analysis")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 0.95);
            padding: 5px 0px;
            letter-spacing: 0.3px;
            line-height: 1.5;
        """)
        header_layout.addWidget(subtitle)
        
        decorative_line = QFrame()
        decorative_line.setFixedHeight(3)
        decorative_line.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255,255,255,0.2), 
                stop:0.5 rgba(255,255,255,0.7), 
                stop:1 rgba(255,255,255,0.2));
            border-radius: 1.5px;
            margin-top: 8px;
        """)
        header_layout.addWidget(decorative_line)
        
        layout.addWidget(header_container)
        
        self.empty = QLabel("No Data Available\n\nUpload a dataset to begin visualization and analysis")
        self.empty.setFont(QFont("Segoe UI", 16))
        self.empty.setAlignment(Qt.AlignCenter)
        self.empty.setStyleSheet("""
            QLabel {
                background: white;
                padding: 90px 60px;
                border-radius: 22px;
                color: #64748b;
                border: 3px dashed #cbd5e1;
                line-height: 2;
                font-weight: 500;
            }
        """)
        empty_shadow = QGraphicsDropShadowEffect()
        empty_shadow.setBlurRadius(30)
        empty_shadow.setColor(QColor(0, 0, 0, 35))
        empty_shadow.setOffset(0, 5)
        self.empty.setGraphicsEffect(empty_shadow)
        layout.addWidget(self.empty)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #e2e8f0;
                width: 14px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 7px;
                min-height: 40px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a3f8f);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                background: #e2e8f0;
                height: 14px;
                border-radius: 7px;
                margin: 2px;
            }
            QScrollBar::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 7px;
                min-width: 40px;
            }
            QScrollBar::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5568d3, stop:1 #6a3f8f);
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background: transparent;")
        scroll_widget.setMinimumWidth(2400)
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(30)
        scroll_layout.setContentsMargins(8, 8, 8, 8)
        
        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(30)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        self.chart1 = self.create_chart_box(
            "Equipment Distribution by Type",
            "#3b82f6",
            height=650
        )
        grid_layout.addWidget(self.chart1, 0, 0)
        
        self.chart2 = self.create_chart_box(
            "Proportional Distribution",
            "#ec4899",
            height=650
        )
        grid_layout.addWidget(self.chart2, 0, 1)
        
        self.chart3 = self.create_chart_box(
            "Equipment Composition",
            "#8b5cf6",
            height=650
        )
        grid_layout.addWidget(self.chart3, 1, 0)
        
        self.chart4 = self.create_chart_box(
            "Average Parameters Analysis",
            "#10b981",
            height=650
        )
        grid_layout.addWidget(self.chart4, 1, 1)
        
        scroll_layout.addWidget(grid_widget)
        
        self.chart5 = self.create_chart_box(
            "Parameter Trends Analysis - First 15 Equipment",
            "#f59e0b",
            height=750
        )
        scroll_layout.addWidget(self.chart5)
        
        scroll_layout.addStretch()
        
        self.scroll.setWidget(scroll_widget)
        layout.addWidget(self.scroll)
        self.scroll.hide()
        
        print("  Charts widget created with modern UI (5 premium charts)")
    
    def create_chart_box(self, title, accent_color, height=650):
        box = QGroupBox()
        
        box.setStyleSheet(f"""
            QGroupBox {{
                background: white;
                border-radius: 20px;
                padding: 28px;
                border: none;
                margin-top: 18px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 12px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {accent_color}, stop:1 {self.adjust_color(accent_color)});
                color: white;
                border-radius: 12px;
                font-weight: bold;
                font-size: 15px;
                margin-left: 12px;
                letter-spacing: 0.5px;
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 45))
        shadow.setOffset(0, 7)
        box.setGraphicsEffect(shadow)
        
        box.setTitle(title)
        
        layout = QVBoxLayout(box)
        layout.setContentsMargins(18, 40, 18, 18)
        layout.setSpacing(12)
        
        chart_label = QLabel("Loading visualization...")
        chart_label.setAlignment(Qt.AlignCenter)
        chart_label.setStyleSheet("""
            QLabel {
                background: #f8fafc;
                border-radius: 14px;
                padding: 25px;
                color: #94a3b8;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        
        chart_label.setMinimumHeight(height)
        
        layout.addWidget(chart_label)
        box.chart_label = chart_label
        
        return box
    
    def adjust_color(self, hex_color):
        color_map = {
            "#3b82f6": "#60a5fa",
            "#ec4899": "#f472b6",
            "#8b5cf6": "#a78bfa",
            "#10b981": "#34d399",
            "#f59e0b": "#fbbf24"
        }
        return color_map.get(hex_color, "#94a3b8")
    
    def load_dataset(self, dataset_id):
        print(f"  [Charts] Loading dataset {dataset_id}")
        
        try:
            success, summary = self.api.get_dataset_summary(dataset_id)
            if not success:
                print("  [Charts] Failed to get summary")
                return
            
            success2, detail = self.api.get_dataset_detail(dataset_id)
            if not success2:
                print("  [Charts] Failed to get detail")
                return
            
            self.empty.hide()
            self.scroll.show()
            
            temp_dir = tempfile.gettempdir()
            dist = summary.get('type_distribution', {})
            avg = summary.get('averages', {})
            ranges = summary.get('ranges', {})
            equipment = detail.get('equipment', [])
            
            if dist:
                self.generate_bar_chart(temp_dir, dist, summary.get('total_equipment', 1))
                self.generate_pie_chart(temp_dir, dist)
                self.generate_doughnut_chart(temp_dir, dist)
            
            if avg and ranges:
                self.generate_avg_params_chart(temp_dir, avg, ranges)
            
            if equipment:
                self.generate_line_chart(temp_dir, equipment)
            
            print("  [Charts] All charts generated successfully")
            
        except Exception as e:
            print(f"  [Charts] Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def generate_bar_chart(self, temp_dir, dist, total):
        img_path = os.path.join(temp_dir, 'chart1.png')
        types = list(dist.keys())
        counts = list(dist.values())
        percentages = [(count / total) * 100 for count in counts]
        
        script = """
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

types = {types}
counts = {counts}
percentages = {percentages}
total = {total}
colors = ['#3b82f6', '#ec4899', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']

fig, ax = plt.subplots(figsize=(12, 9), facecolor='white')
fig.patch.set_facecolor('white')

bars = ax.bar(types, counts, color=colors[:len(types)], alpha=0.88, 
              edgecolor='white', linewidth=4, width=0.65)

for i, (bar, count, pct) in enumerate(zip(bars, counts, percentages)):
    height = bar.get_height()
    label_text = '{{}}\\n({{:.1f}}%)'.format(int(count), pct)
    ax.text(bar.get_x() + bar.get_width()/2., height + max(counts) * 0.05, label_text,
           ha='center', va='bottom', fontweight='bold', fontsize=12, 
           color='#1e293b', bbox=dict(boxstyle='round,pad=0.6', 
           facecolor='white', edgecolor=colors[i], linewidth=2.5, alpha=0.95))

ax.set_title('Equipment Type Distribution Analysis\\nTotal Equipment: {{}}'.format(total), 
            fontsize=16, fontweight='bold', color='#1e293b', pad=25, loc='center')

ax.set_xlabel('Equipment Type', fontsize=15, fontweight='bold', color='#334155', labelpad=15)
ax.set_ylabel('Count', fontsize=15, fontweight='bold', color='#334155', labelpad=15)

ax.set_ylim(0, max(counts) * 1.25)

ax.grid(axis='y', alpha=0.25, linestyle='--', linewidth=1.8, zorder=1)
ax.set_axisbelow(True)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cbd5e1')
ax.spines['bottom'].set_color('#cbd5e1')
ax.spines['left'].set_linewidth(2.5)
ax.spines['bottom'].set_linewidth(2.5)

plt.xticks(fontsize=13, color='#475569', fontweight='600')
plt.yticks(fontsize=12, color='#475569')

textstr = 'Statistical Summary:\\n'
textstr += 'Total Types: {{}}\\n'.format(len(types))
textstr += 'Highest: {{}} ({{}} units)\\n'.format(types[counts.index(max(counts))], max(counts))
textstr += 'Lowest: {{}} ({{}} units)'.format(types[counts.index(min(counts))], min(counts))

props = dict(boxstyle='round,pad=1', facecolor='#f8fafc', edgecolor='#3b82f6', linewidth=2.5, alpha=0.95)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='left', bbox=props, color='#1e293b', fontweight='600')

plt.tight_layout(pad=2.5)
plt.savefig(r'{path}', dpi=140, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print("Bar chart saved successfully")
""".format(types=types, counts=counts, percentages=percentages, total=total, path=img_path.replace('\\', '/'))
        
        self.run_chart_script(script, img_path, self.chart1.chart_label, width=1150, height=620)
    
    def generate_pie_chart(self, temp_dir, dist):
        img_path = os.path.join(temp_dir, 'chart2.png')
        types = list(dist.keys())
        counts = list(dist.values())
        total = sum(counts)
        
        script = """
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

types = {types}
counts = {counts}
total = {total}
colors = ['#3b82f6', '#ec4899', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']

fig, ax = plt.subplots(figsize=(13, 9), facecolor='white')
fig.patch.set_facecolor('white')

wedges, texts, autotexts = ax.pie(counts, labels=types, autopct='%1.1f%%',
                                    colors=colors[:len(types)], startangle=90,
                                    textprops={{'fontsize': 13, 'fontweight': 'bold', 'color': '#1e293b'}},
                                    wedgeprops={{'edgecolor': 'white', 'linewidth': 4.5, 'antialiased': True}},
                                    pctdistance=0.78, labeldistance=1.18, explode=[0.08]*len(types))

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(14)
    autotext.set_fontweight('bold')
    autotext.set_bbox(dict(boxstyle='round,pad=0.5', facecolor='#1e293b', 
                           edgecolor='white', linewidth=2.5, alpha=0.88))

for text in texts:
    text.set_fontsize(13)
    text.set_fontweight('700')
    text.set_color('#1e293b')

ax.set_title('Proportional Distribution of Equipment Types\\nTotal Units: {{}}'.format(total), 
            fontsize=16, fontweight='bold', color='#1e293b', pad=25)

legend_labels = ['{{}} ({{}} units)'.format(t, c) for t, c in zip(types, counts)]
ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1.05, 0.5), 
         fontsize=12, framealpha=0.95, edgecolor='#cbd5e1', 
         fancybox=True, shadow=True, title='Equipment Details', 
         title_fontsize=13, borderpad=1.2)

plt.tight_layout(pad=2.5)
plt.savefig(r'{path}', dpi=140, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print("Pie chart saved successfully")
""".format(types=types, counts=counts, total=total, path=img_path.replace('\\', '/'))
        
        self.run_chart_script(script, img_path, self.chart2.chart_label, width=1250, height=620)
    
    def generate_doughnut_chart(self, temp_dir, dist):
        img_path = os.path.join(temp_dir, 'chart3.png')
        types = list(dist.keys())
        counts = list(dist.values())
        total = sum(counts)
        
        script = """
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

types = {types}
counts = {counts}
total = {total}
colors = ['#3b82f6', '#ec4899', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']

fig, ax = plt.subplots(figsize=(13, 9), facecolor='white')
fig.patch.set_facecolor('white')

wedges, texts, autotexts = ax.pie(counts, labels=types, autopct='%1.1f%%', 
       colors=colors[:len(types)], startangle=90,
       wedgeprops={{'edgecolor': 'white', 'linewidth': 4.5, 'width': 0.5, 'antialiased': True}},
       textprops={{'fontsize': 13, 'fontweight': 'bold', 'color': '#1e293b'}},
       pctdistance=0.68, labeldistance=1.18, explode=[0.08]*len(types))

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(14)
    autotext.set_fontweight('bold')
    autotext.set_bbox(dict(boxstyle='round,pad=0.5', facecolor='#1e293b',
                           edgecolor='white', linewidth=2.5, alpha=0.88))

for text in texts:
    text.set_fontsize(13)
    text.set_fontweight('700')
    text.set_color('#1e293b')

centre_circle = plt.Circle((0, 0), 0.50, fc='white', linewidth=0)
ax.add_artist(centre_circle)

ax.text(0, 0.12, 'Total', ha='center', va='center', fontsize=16, fontweight='bold', color='#64748b')
ax.text(0, -0.05, str(total), ha='center', va='center', fontsize=28, fontweight='bold', color='#1e293b')
ax.text(0, -0.25, 'Equipment', ha='center', va='center', fontsize=13, fontweight='600', color='#64748b')

ax.set_title('Equipment Composition Overview\\nDistribution Across {{}} Categories'.format(len(types)), 
            fontsize=16, fontweight='bold', color='#1e293b', pad=25)

legend_labels = ['{{}} ({{}} units - {{:.1f}}%)'.format(t, c, (c/total)*100) for t, c in zip(types, counts)]
ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1.05, 0.5), 
         fontsize=11, framealpha=0.95, edgecolor='#cbd5e1', 
         fancybox=True, shadow=True, title='Detailed Breakdown', 
         title_fontsize=12, borderpad=1.2)

plt.tight_layout(pad=2.5)
plt.savefig(r'{path}', dpi=140, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print("Doughnut chart saved successfully")
""".format(types=types, counts=counts, total=total, path=img_path.replace('\\', '/'))
        
        self.run_chart_script(script, img_path, self.chart3.chart_label, width=1250, height=620)
    
    def generate_avg_params_chart(self, temp_dir, avg, ranges):
        img_path = os.path.join(temp_dir, 'chart4.png')
        
        flow_avg = avg.get('flowrate', 0)
        press_avg = avg.get('pressure', 0)
        temp_avg = avg.get('temperature', 0)
        
        flow_range = ranges.get('flowrate', {})
        press_range = ranges.get('pressure', {})
        temp_range = ranges.get('temperature', {})
        
        script = """
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

params = ['Flowrate', 'Pressure', 'Temperature']
values = [{flow}, {press}, {temp}]
colors = ['#3b82f6', '#10b981', '#f59e0b']

flow_min = {flow_min}
flow_max = {flow_max}
press_min = {press_min}
press_max = {press_max}
temp_min = {temp_min}
temp_max = {temp_max}

fig, ax = plt.subplots(figsize=(12, 9), facecolor='white')
fig.patch.set_facecolor('white')

bars = ax.bar(params, values, color=colors, alpha=0.88, 
              edgecolor='white', linewidth=4, width=0.5)

ranges_text = [
    'Avg: {{:.2f}}\\nRange: {{:.2f}} - {{:.2f}}'.format(values[0], flow_min, flow_max),
    'Avg: {{:.2f}}\\nRange: {{:.2f}} - {{:.2f}}'.format(values[1], press_min, press_max),
    'Avg: {{:.2f}}\\nRange: {{:.2f}} - {{:.2f}}'.format(values[2], temp_min, temp_max)
]

for bar, color, range_text in zip(bars, colors, ranges_text):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + max(values) * 0.05,
           range_text, ha='center', va='bottom', 
           fontweight='bold', fontsize=12, color='#1e293b',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='white', 
           edgecolor=color, linewidth=2.5, alpha=0.95))

ax.set_ylim(0, max(values) * 1.35)

ax.set_title('Average Parameters Analysis\\nComparative View of Key Equipment Metrics', 
            fontsize=16, fontweight='bold', color='#1e293b', pad=25)

ax.set_xlabel('Parameter Type', fontsize=15, fontweight='bold', color='#334155', labelpad=15)
ax.set_ylabel('Average Value', fontsize=15, fontweight='bold', color='#334155', labelpad=15)

ax.grid(axis='y', alpha=0.25, linestyle='--', linewidth=1.8, zorder=1)
ax.set_axisbelow(True)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cbd5e1')
ax.spines['bottom'].set_color('#cbd5e1')
ax.spines['left'].set_linewidth(2.5)
ax.spines['bottom'].set_linewidth(2.5)

plt.xticks(fontsize=13, color='#475569', fontweight='600')
plt.yticks(fontsize=12, color='#475569')

textstr = 'Statistical Insights:\\n'
textstr += 'Highest Avg: {{}} ({{:.2f}})\\n'.format(params[values.index(max(values))], max(values))
textstr += 'Lowest Avg: {{}} ({{:.2f}})\\n'.format(params[values.index(min(values))], min(values))
textstr += 'Total Parameters: 3'

props = dict(boxstyle='round,pad=1', facecolor='#f8fafc', edgecolor='#10b981', linewidth=2.5, alpha=0.95)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='left', bbox=props, color='#1e293b', fontweight='600')

plt.tight_layout(pad=2.5)
plt.savefig(r'{path}', dpi=140, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print("Average params chart saved successfully")
""".format(
    flow=flow_avg, press=press_avg, temp=temp_avg,
    flow_min=flow_range.get('min', 0), flow_max=flow_range.get('max', 0),
    press_min=press_range.get('min', 0), press_max=press_range.get('max', 0),
    temp_min=temp_range.get('min', 0), temp_max=temp_range.get('max', 0),
    path=img_path.replace('\\', '/')
)
        
        self.run_chart_script(script, img_path, self.chart4.chart_label, width=1150, height=620)
    
    def generate_line_chart(self, temp_dir, equipment):
        img_path = os.path.join(temp_dir, 'chart5.png')
        
        eq_subset = equipment[:15]
        names = [eq['equipment_name'] for eq in eq_subset]
        flowrates = [eq['flowrate'] for eq in eq_subset]
        pressures = [eq['pressure'] for eq in eq_subset]
        temperatures = [eq['temperature'] for eq in eq_subset]
        
        script = """
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

names = {names}
flowrates = {flowrates}
pressures = {pressures}
temperatures = {temperatures}

fig, ax = plt.subplots(figsize=(18, 10), facecolor='white')
fig.patch.set_facecolor('white')

x = np.arange(len(names))

line1 = ax.plot(x, flowrates, marker='o', linewidth=4.5, markersize=12, 
       label='Flowrate (Avg: {{:.2f}})'.format(np.mean(flowrates)), 
       color='#3b82f6', markerfacecolor='#3b82f6', 
       markeredgecolor='white', markeredgewidth=3.5, alpha=0.95, zorder=3)

line2 = ax.plot(x, pressures, marker='s', linewidth=4.5, markersize=12,
       label='Pressure (Avg: {{:.2f}})'.format(np.mean(pressures)), 
       color='#10b981', markerfacecolor='#10b981',
       markeredgecolor='white', markeredgewidth=3.5, alpha=0.95, zorder=3)

line3 = ax.plot(x, temperatures, marker='^', linewidth=4.5, markersize=13,
       label='Temperature (Avg: {{:.2f}})'.format(np.mean(temperatures)), 
       color='#f59e0b', markerfacecolor='#f59e0b',
       markeredgecolor='white', markeredgewidth=3.5, alpha=0.95, zorder=3)

ax.set_title('Parameter Trends Analysis - Equipment Comparison\\nFirst 15 Equipment Units with Detailed Metrics', 
            fontsize=18, fontweight='bold', color='#1e293b', pad=30)

ax.set_xlabel('Equipment Name', fontsize=16, fontweight='bold', color='#334155', labelpad=18)
ax.set_ylabel('Parameter Values', fontsize=16, fontweight='bold', color='#334155', labelpad=18)

ax.legend(loc='upper left', fontsize=13, framealpha=0.95, 
         edgecolor='#cbd5e1', fancybox=True, shadow=True,
         frameon=True, facecolor='white', borderpad=1.5, 
         title='Parameters', title_fontsize=14)

ax.grid(True, alpha=0.25, linestyle='--', linewidth=1.8, zorder=1)
ax.set_axisbelow(True)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cbd5e1')
ax.spines['bottom'].set_color('#cbd5e1')
ax.spines['left'].set_linewidth(2.5)
ax.spines['bottom'].set_linewidth(2.5)

plt.xticks(x, names, rotation=45, ha='right', fontsize=12, color='#475569', fontweight='600')
plt.yticks(fontsize=13, color='#475569')

textstr = 'Trend Analysis:\\n'
textstr += 'Flow Range: {{:.2f}} - {{:.2f}}\\n'.format(min(flowrates), max(flowrates))
textstr += 'Press Range: {{:.2f}} - {{:.2f}}\\n'.format(min(pressures), max(pressures))
textstr += 'Temp Range: {{:.2f}} - {{:.2f}}\\n'.format(min(temperatures), max(temperatures))
textstr += 'Equipment Count: {{}}'.format(len(names))

props = dict(boxstyle='round,pad=1', facecolor='#f8fafc', edgecolor='#f59e0b', linewidth=2.5, alpha=0.95)
ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='bottom', horizontalalignment='right', bbox=props, color='#1e293b', fontweight='600')

plt.tight_layout(pad=2.5)
plt.savefig(r'{path}', dpi=140, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print("Line chart saved successfully")
""".format(names=names, flowrates=flowrates, pressures=pressures, 
          temperatures=temperatures, path=img_path.replace('\\', '/'))
        
        self.run_chart_script(script, img_path, self.chart5.chart_label, width=1750, height=720)
    
    def run_chart_script(self, script, img_path, label, width=1150, height=620):
        try:
            result = subprocess.run(
                [sys.executable, '-c', script], 
                capture_output=True, 
                timeout=20, 
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            if result.returncode == 0:
                if os.path.exists(img_path):
                    QTimer.singleShot(100, lambda: self.load_image(img_path, label, width, height))
                else:
                    label.setText("Chart file not found")
                    label.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 14px;")
                    print(f"  Chart file not created at: {img_path}")
            else:
                label.setText("Chart generation failed")
                label.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 14px;")
                print(f"  Chart generation error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            label.setText("Chart generation timeout")
            label.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 14px;")
            print("  Chart generation timed out")
            
        except Exception as e:
            label.setText(f"Error: {str(e)}")
            label.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 14px;")
            print(f"  Chart loading error: {str(e)}")
    
    def load_image(self, img_path, label, width, height):
        try:
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(
                        width, 
                        height, 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )
                    label.setPixmap(scaled_pixmap)
                    label.setStyleSheet("""
                        QLabel {
                            background: transparent;
                            border-radius: 14px;
                            padding: 10px;
                        }
                    """)
                    print(f"  Chart loaded successfully from: {img_path}")
                else:
                    label.setText("Failed to load chart image")
                    label.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 14px;")
                    print(f"  Invalid pixmap for: {img_path}")
            else:
                label.setText("Chart image not available")
                label.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 14px;")
                print(f"  Image file missing: {img_path}")
                
        except Exception as e:
            label.setText(f"Loading error: {str(e)}")
            label.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 14px;")
            print(f"  Image loading exception: {str(e)}")