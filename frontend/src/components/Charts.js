import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Bar, Pie, Line, Doughnut } from 'react-chartjs-2';
import { FaCalculator, FaTint, FaBolt, FaThermometerHalf } from 'react-icons/fa';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function Charts({ dataset, summary }) {
  const [typeDistribution, setTypeDistribution] = useState({});

  useEffect(() => {
    if (summary && summary.type_distribution) {
      setTypeDistribution(summary.type_distribution);
    }
  }, [summary]);

  const generateBlueShades = (count) => {
    const shades = [];
    const borderShades = [];
    
    for (let i = 0; i < count; i++) {
      const lightness = 35 + (i * 40 / count);
      const saturation = 75 - (i * 15 / count);
      
      shades.push(`hsla(210, ${saturation}%, ${lightness}%, 0.92)`);
      borderShades.push(`hsl(210, ${saturation + 5}%, ${lightness - 12}%)`);
    }
    
    return { fill: shades, border: borderShades };
  };

  const typeCount = Object.keys(typeDistribution).length;
  const colors = generateBlueShades(typeCount);

  const commonOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 14,
            weight: '600',
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto',
          },
          padding: 18,
          usePointStyle: true,
          color: '#111827',
          boxWidth: 12,
          boxHeight: 12,
        },
      },
      tooltip: {
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        padding: 16,
        titleFont: {
          size: 15,
          weight: 'bold',
        },
        bodyFont: {
          size: 14,
        },
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderWidth: 1,
        displayColors: true,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            const value = context.parsed.y !== null && context.parsed.y !== undefined 
              ? context.parsed.y 
              : (context.parsed !== null && context.parsed !== undefined ? context.parsed : 0);
            label += typeof value === 'number' ? value.toFixed(2) : value;
            return label;
          },
          afterLabel: function(context) {
            if (context.dataset.additionalInfo && context.dataset.additionalInfo[context.dataIndex]) {
              return context.dataset.additionalInfo[context.dataIndex];
            }
            return '';
          }
        }
      },
    },
  };

  const barChartData = {
    labels: Object.keys(typeDistribution),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(typeDistribution),
        backgroundColor: colors.fill,
        borderColor: colors.border,
        borderWidth: 2,
        borderRadius: 12,
        barThickness: 'flex',
        maxBarThickness: 90,
        additionalInfo: Object.entries(typeDistribution).map(([type, count]) => {
          const percentage = ((count / summary.total_equipment) * 100).toFixed(1);
          return `${percentage}% of total equipment`;
        })
      },
    ],
  };

  const barChartOptions = {
    ...commonOptions,
    plugins: {
      ...commonOptions.plugins,
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Equipment Distribution Analysis by Type',
        font: {
          size: 19,
          weight: 'bold',
        },
        padding: 24,
        color: '#111827',
      },
      tooltip: {
        ...commonOptions.plugins.tooltip,
        callbacks: {
          label: function(context) {
            const value = context.parsed.y || 0;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0.0';
            return [
              `Count: ${value} units`,
              `Percentage: ${percentage}%`,
              `Total Equipment: ${total}`
            ];
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
          font: {
            size: 13,
            weight: '600',
          },
          color: '#6b7280',
          callback: function(value) {
            return Number.isInteger(value) ? value : '';
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
          drawBorder: false,
        },
        title: {
          display: true,
          text: 'Number of Equipment Units',
          font: {
            size: 14,
            weight: 'bold',
          },
          color: '#374151',
          padding: 12,
        },
      },
      x: {
        ticks: {
          font: {
            size: 12,
            weight: '600',
          },
          color: '#6b7280',
        },
        grid: {
          display: false,
          drawBorder: false,
        },
        title: {
          display: true,
          text: 'Equipment Type Category',
          font: {
            size: 14,
            weight: 'bold',
          },
          color: '#374151',
          padding: 12,
        },
      },
    },
  };

  const pieChartData = {
    labels: Object.keys(typeDistribution),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(typeDistribution),
        backgroundColor: colors.fill,
        borderColor: 'white',
        borderWidth: 5,
        hoverOffset: 20,
        hoverBorderWidth: 6,
      },
    ],
  };

  const pieChartOptions = {
    ...commonOptions,
    plugins: {
      ...commonOptions.plugins,
      legend: {
        position: 'right',
        labels: {
          font: {
            size: 13,
            weight: '600',
          },
          padding: 16,
          usePointStyle: true,
          color: '#111827',
          generateLabels: function(chart) {
            const data = chart.data;
            if (!data.datasets || !data.datasets[0] || !data.datasets[0].data) {
              return [];
            }
            const total = data.datasets[0].data.reduce((a, b) => a + b, 0);
            return data.labels.map((label, i) => {
              const value = data.datasets[0].data[i] || 0;
              const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0.0';
              return {
                text: `${label}: ${value} (${percentage}%)`,
                fillStyle: data.datasets[0].backgroundColor[i],
                hidden: false,
                index: i,
              };
            });
          },
        },
      },
      title: {
        display: true,
        text: 'Proportional Type Distribution Overview',
        font: {
          size: 19,
          weight: 'bold',
        },
        padding: 24,
        color: '#111827',
      },
    },
  };

  const lineChartData = {
    labels: dataset.equipment?.slice(0, 15).map(eq => eq.equipment_name) || [],
    datasets: [
      {
        label: 'Flowrate',
        data: dataset.equipment?.slice(0, 15).map(eq => eq.flowrate || 0) || [],
        borderColor: 'hsl(210, 80%, 42%)',
        backgroundColor: 'hsla(210, 80%, 42%, 0.2)',
        tension: 0.4,
        fill: true,
        pointRadius: 6,
        pointHoverRadius: 9,
        pointBackgroundColor: 'hsl(210, 80%, 42%)',
        pointBorderColor: 'white',
        pointBorderWidth: 3,
        borderWidth: 3,
      },
      {
        label: 'Pressure',
        data: dataset.equipment?.slice(0, 15).map(eq => eq.pressure || 0) || [],
        borderColor: 'hsl(210, 75%, 52%)',
        backgroundColor: 'hsla(210, 75%, 52%, 0.2)',
        tension: 0.4,
        fill: true,
        pointRadius: 6,
        pointHoverRadius: 9,
        pointBackgroundColor: 'hsl(210, 75%, 52%)',
        pointBorderColor: 'white',
        pointBorderWidth: 3,
        borderWidth: 3,
      },
      {
        label: 'Temperature',
        data: dataset.equipment?.slice(0, 15).map(eq => eq.temperature || 0) || [],
        borderColor: 'hsl(210, 70%, 62%)',
        backgroundColor: 'hsla(210, 70%, 62%, 0.2)',
        tension: 0.4,
        fill: true,
        pointRadius: 6,
        pointHoverRadius: 9,
        pointBackgroundColor: 'hsl(210, 70%, 62%)',
        pointBorderColor: 'white',
        pointBorderWidth: 3,
        borderWidth: 3,
      },
    ],
  };

  const lineChartOptions = {
    ...commonOptions,
    layout: {
      padding: {
        top: 30,
        right: 30,
        bottom: 30,
        left: 30,
      },
    },
    plugins: {
      ...commonOptions.plugins,
      title: {
        display: true,
        text: 'Parameter Trends Analysis (First 15 Equipment)',
        font: {
          size: 18,
          weight: 'bold',
        },
        padding: 24,
        color: '#111827',
      },
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 14,
            weight: '600',
          },
          padding: 18,
          usePointStyle: true,
          color: '#111827',
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          font: {
            size: 13,
            weight: '600',
          },
          color: '#374151',
          padding: 12,
          callback: function(value) {
            return typeof value === 'number' ? value.toFixed(1) : value;
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.06)',
          drawBorder: false,
        },
        title: {
          display: true,
          text: 'Parameter Values',
          font: {
            size: 14,
            weight: 'bold',
          },
          color: '#374151',
        },
      },
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 45,
          font: {
            size: 11,
            weight: '500',
          },
          color: '#374151',
          padding: 10,
          autoSkip: true,
          maxTicksLimit: 15,
        },
        grid: {
          display: false,
          drawBorder: false,
        },
        offset: true,
        title: {
          display: true,
          text: 'Equipment Name',
          font: {
            size: 14,
            weight: 'bold',
          },
          color: '#374151',
        },
      },
    },
    interaction: {
      intersect: false,
      mode: 'index',
    },
  };

  const doughnutChartData = {
    labels: Object.keys(typeDistribution),
    datasets: [
      {
        label: 'Count',
        data: Object.values(typeDistribution),
        backgroundColor: colors.fill,
        borderColor: 'white',
        borderWidth: 5,
        hoverOffset: 18,
        hoverBorderWidth: 6,
      },
    ],
  };

  const doughnutChartOptions = {
    ...commonOptions,
    plugins: {
      ...commonOptions.plugins,
      legend: {
        position: 'bottom',
        labels: {
          font: {
            size: 13,
            weight: '600',
          },
          padding: 18,
          usePointStyle: true,
          color: '#111827',
        },
      },
      title: {
        display: true,
        text: 'Equipment Composition & Structure',
        font: {
          size: 19,
          weight: 'bold',
        },
        padding: 24,
        color: '#111827',
      },
      tooltip: {
        ...commonOptions.plugins.tooltip,
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.parsed || 0;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0.0';
            return [
              `${label}`,
              `Count: ${value} units`,
              `Share: ${percentage}%`
            ];
          }
        }
      }
    },
  };

  const avgParamsData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Value',
        data: [
          summary?.averages?.flowrate || 0,
          summary?.averages?.pressure || 0,
          summary?.averages?.temperature || 0,
        ],
        backgroundColor: [
          'hsla(210, 80%, 42%, 0.92)',
          'hsla(210, 75%, 52%, 0.92)',
          'hsla(210, 70%, 62%, 0.92)',
        ],
        borderColor: [
          'hsl(210, 85%, 37%)',
          'hsl(210, 80%, 47%)',
          'hsl(210, 75%, 57%)',
        ],
        borderWidth: 2,
        borderRadius: 12,
        additionalInfo: [
          `Range: ${summary?.ranges?.flowrate?.min?.toFixed(2) || 0} - ${summary?.ranges?.flowrate?.max?.toFixed(2) || 0}`,
          `Range: ${summary?.ranges?.pressure?.min?.toFixed(2) || 0} - ${summary?.ranges?.pressure?.max?.toFixed(2) || 0}`,
          `Range: ${summary?.ranges?.temperature?.min?.toFixed(2) || 0} - ${summary?.ranges?.temperature?.max?.toFixed(2) || 0}`,
        ]
      },
    ],
  };

  const avgParamsOptions = {
    ...commonOptions,
    plugins: {
      ...commonOptions.plugins,
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Average Operational Parameters Comparison',
        font: {
          size: 19,
          weight: 'bold',
        },
        padding: 24,
        color: '#111827',
      },
      tooltip: {
        ...commonOptions.plugins.tooltip,
        callbacks: {
          label: function(context) {
            const value = context.parsed.y || 0;
            const label = context.label || '';
            const range = context.dataset.additionalInfo?.[context.dataIndex] || '';
            return [
              `${label}: ${value.toFixed(2)}`,
              range,
              `Std Dev: ${summary?.ranges?.[label.toLowerCase()]?.std?.toFixed(2) || 0}`
            ];
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          font: {
            size: 13,
            weight: '600',
          },
          color: '#6b7280',
          callback: function(value) {
            return typeof value === 'number' ? value.toFixed(1) : value;
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
          drawBorder: false,
        },
        title: {
          display: true,
          text: 'Average Parameter Value',
          font: {
            size: 14,
            weight: 'bold',
          },
          color: '#374151',
          padding: 12,
        },
      },
      x: {
        ticks: {
          font: {
            size: 13,
            weight: '600',
          },
          color: '#6b7280',
        },
        grid: {
          display: false,
          drawBorder: false,
        },
        title: {
          display: true,
          text: 'Parameter Type',
          font: {
            size: 14,
            weight: 'bold',
          },
          color: '#374151',
          padding: 12,
        },
      },
    },
  };

  return (
    <div className="charts-section">
      <h2>Data Visualization & Comprehensive Analysis</h2>
      
      <div className="charts-grid">
        <div className="chart-container">
          <Bar data={barChartData} options={barChartOptions} />
        </div>

        <div className="chart-container">
          <Pie data={pieChartData} options={pieChartOptions} />
        </div>

        <div className="chart-container">
          <Doughnut data={doughnutChartData} options={doughnutChartOptions} />
        </div>

        <div className="chart-container">
          <Bar data={avgParamsData} options={avgParamsOptions} />
        </div>
      </div>

      <div className="chart-container-full-width">
        <Line data={lineChartData} options={lineChartOptions} />
      </div>

      {summary && summary.ranges && (
        <div className="stats-summary">
          <h3>
            <FaCalculator style={{ marginRight: '10px', color: '#2563eb' }} />
            Comprehensive Statistical Analysis
          </h3>
          <div className="stats-details-grid">
            
            <div className="stats-detail-card">
              <h4>
                <FaTint style={{ marginRight: '8px', color: '#2563eb' }} />
                Flowrate Analysis
              </h4>
              <div className="stats-detail-item">
                <span className="label">Average:</span>
                <span className="value">{(summary.averages?.flowrate || 0).toFixed(2)} m³/h</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Minimum:</span>
                <span className="value">{(summary.ranges?.flowrate?.min || 0).toFixed(2)} m³/h</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Maximum:</span>
                <span className="value">{(summary.ranges?.flowrate?.max || 0).toFixed(2)} m³/h</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Range:</span>
                <span className="value">
                  {((summary.ranges?.flowrate?.max || 0) - (summary.ranges?.flowrate?.min || 0)).toFixed(2)} m³/h
                </span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Std. Deviation:</span>
                <span className="value">{(summary.ranges?.flowrate?.std || 0).toFixed(2)}</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Variance:</span>
                <span className="value">{(summary.ranges?.flowrate?.var || 0).toFixed(2)}</span>
              </div>
              <div className="stats-detail-item highlight">
                <span className="label">Coef. of Variation:</span>
                <span className="value">{(summary.ranges?.flowrate?.cv || 0).toFixed(2)}%</span>
              </div>
            </div>

            <div className="stats-detail-card">
              <h4>
                <FaBolt style={{ marginRight: '8px', color: '#10b981' }} />
                Pressure Analysis
              </h4>
              <div className="stats-detail-item">
                <span className="label">Average:</span>
                <span className="value">{(summary.averages?.pressure || 0).toFixed(2)} bar</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Minimum:</span>
                <span className="value">{(summary.ranges?.pressure?.min || 0).toFixed(2)} bar</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Maximum:</span>
                <span className="value">{(summary.ranges?.pressure?.max || 0).toFixed(2)} bar</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Range:</span>
                <span className="value">
                  {((summary.ranges?.pressure?.max || 0) - (summary.ranges?.pressure?.min || 0)).toFixed(2)} bar
                </span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Std. Deviation:</span>
                <span className="value">{(summary.ranges?.pressure?.std || 0).toFixed(2)}</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Variance:</span>
                <span className="value">{(summary.ranges?.pressure?.var || 0).toFixed(2)}</span>
              </div>
              <div className="stats-detail-item highlight">
                <span className="label">Coef. of Variation:</span>
                <span className="value">{(summary.ranges?.pressure?.cv || 0).toFixed(2)}%</span>
              </div>
            </div>

            <div className="stats-detail-card">
              <h4>
                <FaThermometerHalf style={{ marginRight: '8px', color: '#f59e0b' }} />
                Temperature Analysis
              </h4>
              <div className="stats-detail-item">
                <span className="label">Average:</span>
                <span className="value">{(summary.averages?.temperature || 0).toFixed(2)} °C</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Minimum:</span>
                <span className="value">{(summary.ranges?.temperature?.min || 0).toFixed(2)} °C</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Maximum:</span>
                <span className="value">{(summary.ranges?.temperature?.max || 0).toFixed(2)} °C</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Range:</span>
                <span className="value">
                  {((summary.ranges?.temperature?.max || 0) - (summary.ranges?.temperature?.min || 0)).toFixed(2)} °C
                </span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Std. Deviation:</span>
                <span className="value">{(summary.ranges?.temperature?.std || 0).toFixed(2)}</span>
              </div>
              <div className="stats-detail-item">
                <span className="label">Variance:</span>
                <span className="value">{(summary.ranges?.temperature?.var || 0).toFixed(2)}</span>
              </div>
              <div className="stats-detail-item highlight">
                <span className="label">Coef. of Variation:</span>
                <span className="value">{(summary.ranges?.temperature?.cv || 0).toFixed(2)}%</span>
              </div>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}

export default Charts;