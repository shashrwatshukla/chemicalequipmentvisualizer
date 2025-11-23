import React, { useState, useRef } from 'react';
import { 
  FaCloudUploadAlt, 
  FaFileCsv, 
  FaCheckCircle, 
  FaExclamationTriangle, 
  FaFileDownload, 
  FaTrash, 
  FaRedo,
  FaChartBar,
  FaTint,
  FaBolt,
  FaThermometerHalf,
  FaChartLine,
  FaCube,
  FaLayerGroup,
  FaTachometerAlt
} from 'react-icons/fa';
import api from '../services/api';
import Charts from './Charts';
import DataTable from './DataTable';

function Dashboard({ user }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [datasetData, setDatasetData] = useState(null);
  const [summaryData, setSummaryData] = useState(null);
  const [columnMapping, setColumnMapping] = useState(null);
  const [uploadResponse, setUploadResponse] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    processFile(file);
  };

  const processFile = (file) => {
    if (file && file.name.endsWith('.csv')) {
      setSelectedFile(file);
      setError('');
    } else {
      setError('Please select a valid CSV file');
      setSelectedFile(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    processFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  const clearFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const resetDashboard = () => {
    setDatasetData(null);
    setSummaryData(null);
    setColumnMapping(null);
    setUploadResponse(null);
    setSelectedFile(null);
    setError('');
    setSuccess('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const response = await api.uploadDataset(selectedFile);
      setDatasetData(response.data.dataset);
      setColumnMapping(response.data.column_mapping);
      setUploadResponse(response.data);
      
      const summaryResponse = await api.getDatasetSummary(response.data.dataset.id);
      setSummaryData(summaryResponse.data);
      
      setSuccess('File uploaded and analyzed successfully!');
      clearFile();
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!datasetData) return;

    try {
      const response = await api.downloadReport(datasetData.id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${datasetData.name}_report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to download report');
    }
  };

  const getParameterIcon = (index) => {
    const icons = [FaTint, FaBolt, FaThermometerHalf, FaChartLine, FaCube];
    return icons[index] || FaChartLine;
  };

  const getNumericColumns = () => {
    if (!datasetData?.equipment || datasetData.equipment.length === 0) return [];
    
    const firstEquipment = datasetData.equipment[0];
    const numericCols = [];
    
    Object.keys(firstEquipment).forEach(key => {
      const value = firstEquipment[key];
      if (typeof value === 'number' && !isNaN(value) && 
          key !== 'id' && key !== 'dataset_id' && 
          !key.includes('name') && !key.includes('type')) {
        numericCols.push(key);
      }
    });
    
    return numericCols;
  };

  const calculateAverages = () => {
    if (!datasetData?.equipment || datasetData.equipment.length === 0) return {};
    
    const numericColumns = getNumericColumns();
    const averages = {};
    
    numericColumns.forEach(col => {
      const values = datasetData.equipment
        .map(eq => eq[col])
        .filter(val => val !== null && val !== undefined && !isNaN(val));
      
      if (values.length > 0) {
        const sum = values.reduce((a, b) => a + b, 0);
        averages[col] = sum / values.length;
      }
    });
    
    return averages;
  };

  const calculateRanges = () => {
    if (!datasetData?.equipment || datasetData.equipment.length === 0) return {};
    
    const numericColumns = getNumericColumns();
    const ranges = {};
    
    numericColumns.forEach(col => {
      const values = datasetData.equipment
        .map(eq => eq[col])
        .filter(val => val !== null && val !== undefined && !isNaN(val));
      
      if (values.length > 0) {
        ranges[col] = {
          min: Math.min(...values),
          max: Math.max(...values)
        };
      }
    });
    
    return ranges;
  };

  const calculateParameterMetrics = () => {
    if (!datasetData?.equipment || datasetData.equipment.length === 0) return null;

    const metrics = [];
    const equipment = datasetData.equipment;
    const numericColumns = getNumericColumns();

    if (numericColumns.length === 0) return null;

    numericColumns.forEach(col => {
      const values = equipment
        .map(eq => {
          const val = eq[col];
          return (val !== null && val !== undefined && !isNaN(val)) ? Number(val) : null;
        })
        .filter(v => v !== null)
        .sort((a, b) => a - b);

      if (values.length === 0) return;

      const sum = values.reduce((a, b) => a + b, 0);
      const avg = sum / values.length;
      const min = Math.min(...values);
      const max = Math.max(...values);

      const variance = values.reduce((acc, val) => acc + Math.pow(val - avg, 2), 0) / values.length;
      const std = Math.sqrt(variance);

      const getQuartile = (arr, percentile) => {
        if (arr.length === 0) return 0;
        const index = (percentile / 100) * (arr.length - 1);
        const lower = Math.floor(index);
        const upper = Math.ceil(index);
        const weight = index % 1;
        
        if (lower === upper) return arr[lower];
        return arr[lower] * (1 - weight) + arr[upper] * weight;
      };

      const q1 = getQuartile(values, 25);
      const median = getQuartile(values, 50);
      const q3 = getQuartile(values, 75);
      const iqr = q3 - q1;

      const lowerBound = q1 - (1.5 * iqr);
      const upperBound = q3 + (1.5 * iqr);
      const outliers = values.filter(v => v < lowerBound || v > upperBound).length;

      const dataRange = max - min;
      const relativeSpread = avg !== 0 ? dataRange / Math.abs(avg) : 0;
      const efficiency = relativeSpread < 0.5 ? 'Excellent' : relativeSpread < 1.0 ? 'Good' : relativeSpread < 2.0 ? 'Fair' : 'Poor';

      metrics.push({
        parameter: col,
        average: avg.toFixed(2),
        min: min.toFixed(2),
        max: max.toFixed(2),
        std: std.toFixed(2),
        median: median.toFixed(2),
        q1: q1.toFixed(2),
        q3: q3.toFixed(2),
        iqr: iqr.toFixed(2),
        outliers: outliers,
        dataPoints: values.length,
        efficiency: efficiency,
        status: outliers === 0 ? 'stable' : outliers <= 2 ? 'moderate' : 'unstable'
      });
    });

    return metrics;
  };

  const parameterMetrics = calculateParameterMetrics();
  const numericColumns = getNumericColumns();
  const calculatedAverages = calculateAverages();
  const calculatedRanges = calculateRanges();

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        {datasetData && (
          <button className="action-btn primary" onClick={handleDownloadReport}>
            <FaFileDownload /> Download PDF Report
          </button>
        )}
      </div>
      <p className="dashboard-subtitle">Upload and analyze your chemical equipment data</p>

      {!datasetData ? (
        <div className="upload-section-pro">
          <div className="upload-header-minimal">
            <h2>Upload CSV Data</h2>
            <span className="file-badge"><FaFileCsv /> CSV Only</span>
          </div>
          
          {!selectedFile ? (
            <div
              className={`dropzone-pro ${dragOver ? 'dragover' : ''}`}
              onClick={() => fileInputRef.current?.click()}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
            >
              <FaCloudUploadAlt className="upload-icon-pro" />
              <h3>Drop your CSV file here</h3>
              <p>or click to browse</p>
              <button type="button" className="browse-file-btn">
                <FaFileCsv /> Select File
              </button>
              <div className="upload-hints">
                <span>✓ Auto-detects columns</span>
                <span>✓ Max 50MB</span>
                <span>✓ Instant analysis</span>
              </div>
            </div>
          ) : (
            <div className="file-ready-card">
              <div className="file-ready-content">
                <FaFileCsv className="file-ready-icon" />
                <div className="file-ready-info">
                  <h4>{selectedFile.name}</h4>
                  <p>{(selectedFile.size / 1024).toFixed(2)} KB • Ready to upload</p>
                </div>
                <button className="file-remove-btn" onClick={clearFile} title="Remove">
                  <FaTrash />
                </button>
              </div>
            </div>
          )}

          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />

          {error && (
            <div className="error-message">
              <FaExclamationTriangle />
              <span>{error}</span>
            </div>
          )}
          
          {success && (
            <div className="success-message">
              <FaCheckCircle />
              <span>{success}</span>
            </div>
          )}

          {selectedFile && (
            <button className="upload-action-btn-pro" onClick={handleUpload} disabled={uploading}>
              {uploading ? (
                <>
                  <div className="btn-spinner"></div>
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <FaCloudUploadAlt />
                  <span>Upload & Analyze</span>
                </>
              )}
            </button>
          )}
        </div>
      ) : (
        <div className="current-file-bar">
          <FaFileCsv className="current-file-icon" />
          <div className="current-file-info">
            <h3>{datasetData.name}</h3>
            <span>Uploaded successfully • {summaryData?.total_equipment || 0} items</span>
          </div>
          <button className="analyze-another-btn" onClick={resetDashboard}>
            <FaRedo /> Analyze Another File
          </button>
        </div>
      )}

      {datasetData && summaryData && columnMapping && (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">
                <FaChartBar />
              </div>
              <div className="stat-label">Total Equipment</div>
              <div className="stat-value">{summaryData.total_equipment}</div>
            </div>
            
            {numericColumns.length > 0 && 
              numericColumns.map((colName, index) => {
                const IconComponent = getParameterIcon(index);
                const avg = calculatedAverages[colName];
                const range = calculatedRanges[colName];
                
                return (
                  <div className="stat-card" key={colName}>
                    <div className="stat-icon">
                      <IconComponent />
                    </div>
                    <div className="stat-label">Avg {colName}</div>
                    <div className="stat-value">
                      {avg ? avg.toFixed(2) : 'N/A'}
                    </div>
                    {range && (
                      <div className="stat-range">
                        Range: {range.min.toFixed(2)} - {range.max.toFixed(2)}
                      </div>
                    )}
                  </div>
                );
              })
            }
          </div>

          <DataTable equipment={datasetData.equipment || []} />

          <Charts dataset={datasetData} summary={summaryData} />

          <div className="insights-section">
            <h2><FaChartLine /> Operational Intelligence Dashboard</h2>
            <div className="insights-grid-two">
              
              <div className="insight-card-scrollable">
                <h3><FaLayerGroup /> Dataset Overview</h3>
                
                <div className="scrollable-content">
                  <div className="card-section">
                    <h4 className="section-subtitle">Data Structure</h4>
                    <div className="structure-info">
                      <div className="structure-row">
                        <span className="structure-label">Total Equipment:</span>
                        <span className="structure-value">{summaryData.total_equipment}</span>
                      </div>
                      <div className="structure-row">
                        <span className="structure-label">Total Columns:</span>
                        <span className="structure-value">{Object.keys(datasetData.equipment[0] || {}).length}</span>
                      </div>
                      <div className="structure-row">
                        <span className="structure-label">Numeric Parameters:</span>
                        <span className="structure-value">{numericColumns.length}</span>
                      </div>
                      <div className="structure-row">
                        <span className="structure-label">Identifier:</span>
                        <span className="structure-value-highlight">
                          {datasetData.equipment[0]?.equipment_name ? 'equipment_name' : 'name'}
                        </span>
                      </div>
                      {datasetData.equipment[0]?.equipment_type && (
                        <div className="structure-row">
                          <span className="structure-label">Category:</span>
                          <span className="structure-value-highlight">equipment_type</span>
                        </div>
                      )}
                    </div>
                    
                    <div className="column-tags">
                      <p className="tags-title">Numeric Parameters:</p>
                      <div className="tags-wrapper">
                        {numericColumns.map((col, idx) => (
                          <span key={idx} className="param-tag">{col}</span>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="card-section">
                    <h4 className="section-subtitle">Equipment Distribution</h4>
                    <div className="distribution-content">
                      {summaryData.type_distribution && Object.entries(summaryData.type_distribution).map(([type, count]) => {
                        const percentage = ((count / summaryData.total_equipment) * 100).toFixed(1);
                        return (
                          <div key={type} className="distribution-item">
                            <div className="distribution-header">
                              <span className="distribution-type">{type}</span>
                              <span className="distribution-count">{count} units ({percentage}%)</span>
                            </div>
                            <div className="distribution-bar-container">
                              <div 
                                className="distribution-bar" 
                                style={{ width: `${percentage}%` }}
                              ></div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>

              {parameterMetrics && parameterMetrics.length > 0 && (
                <div className="insight-card-scrollable insight-card-wide">
                  <h3><FaTachometerAlt /> Parameter Statistical Metrics</h3>
                  <p className="card-description">Comprehensive statistical analysis of all {parameterMetrics.length} parameters</p>
                  
                  <div className="scrollable-content">
                    <div className="parameter-metrics-list">
                      {parameterMetrics.map((metric, idx) => (
                        <div key={idx} className="parameter-metric-item">
                          <div className="metric-header-row">
                            <span className="metric-param-name">{metric.parameter}</span>
                            <span className={`efficiency-badge ${metric.status}`}>
                              {metric.efficiency}
                            </span>
                          </div>
                          
                          <div className="metric-stats-grid-four">
                            <div className="metric-stat">
                              <span className="stat-label">Average</span>
                              <span className="stat-value">{metric.average}</span>
                            </div>
                            <div className="metric-stat">
                              <span className="stat-label">Median</span>
                              <span className="stat-value">{metric.median}</span>
                            </div>
                            <div className="metric-stat">
                              <span className="stat-label">Min</span>
                              <span className="stat-value">{metric.min}</span>
                            </div>
                            <div className="metric-stat">
                              <span className="stat-label">Max</span>
                              <span className="stat-value">{metric.max}</span>
                            </div>
                          </div>

                          <div className="quartile-section">
                            <h5 className="quartile-title">Quartile Distribution</h5>
                            <div className="quartile-grid-four">
                              <div className="quartile-item">
                                <span className="quartile-label">Q1 (25%)</span>
                                <span className="quartile-value">{metric.q1}</span>
                              </div>
                              <div className="quartile-item">
                                <span className="quartile-label">Q2 (50%)</span>
                                <span className="quartile-value">{metric.median}</span>
                              </div>
                              <div className="quartile-item">
                                <span className="quartile-label">Q3 (75%)</span>
                                <span className="quartile-value">{metric.q3}</span>
                              </div>
                              <div className="quartile-item">
                                <span className="quartile-label">IQR</span>
                                <span className="quartile-value">{metric.iqr}</span>
                              </div>
                            </div>
                          </div>

                          <div className="metric-footer">
                            <div className="metric-info-item">
                              <span className="info-label">Std Deviation:</span>
                              <span className="info-value">{metric.std}</span>
                            </div>
                            <div className="metric-info-item">
                              <span className="info-label">Data Points:</span>
                              <span className="info-value">{metric.dataPoints}</span>
                            </div>
                            {metric.outliers > 0 && (
                              <div className="metric-info-item warning">
                                <span className="info-label">⚠ Outliers:</span>
                                <span className="info-value">{metric.outliers}</span>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default Dashboard;