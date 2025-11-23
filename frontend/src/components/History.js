import React, { useState, useEffect } from 'react';
import { FaHistory, FaFileDownload, FaTrash, FaInbox, FaCalendarAlt } from 'react-icons/fa';
import api from '../services/api';

function History() {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      const response = await api.getDatasets();
      setDatasets(response.data);
    } catch (err) {
      setError('Failed to load datasets');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (id, name) => {
    try {
      const response = await api.downloadReport(id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${name}_report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert('Failed to download report');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this dataset?')) {
      try {
        await api.deleteDataset(id);
        fetchDatasets();
      } catch (err) {
        alert('Failed to delete dataset');
      }
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="history-container">
        <div className="loading-screen" style={{ minHeight: '50vh', background: 'transparent' }}>
          <div className="spinner"></div>
          <p style={{ color: 'var(--gray)' }}>Loading history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <h1>Upload History</h1>
        <p>Your last 5 uploaded datasets</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {datasets.length === 0 ? (
        <div className="empty-state">
          <FaInbox className="empty-state-icon" />
          <h2>No datasets yet</h2>
          <p>Upload your first CSV file from the Dashboard</p>
        </div>
      ) : (
        <div className="datasets-list">
          {datasets.map((dataset) => (
            <div key={dataset.id} className="dataset-card">
              <div className="dataset-header">
                <div>
                  <div className="dataset-name">{dataset.name}</div>
                  <div className="dataset-date">
                    <FaCalendarAlt style={{ marginRight: '0.5rem' }} />
                    {formatDate(dataset.uploaded_at)}
                  </div>
                </div>
              </div>

              <div className="dataset-stats">
                <div className="dataset-stat">
                  <div className="dataset-stat-label">Total Equipment</div>
                  <div className="dataset-stat-value">{dataset.total_equipment}</div>
                </div>
                <div className="dataset-stat">
                  <div className="dataset-stat-label">Avg Flowrate</div>
                  <div className="dataset-stat-value">{dataset.avg_flowrate.toFixed(2)}</div>
                </div>
                <div className="dataset-stat">
                  <div className="dataset-stat-label">Avg Pressure</div>
                  <div className="dataset-stat-value">{dataset.avg_pressure.toFixed(2)}</div>
                </div>
                <div className="dataset-stat">
                  <div className="dataset-stat-label">Avg Temperature</div>
                  <div className="dataset-stat-value">{dataset.avg_temperature.toFixed(2)}</div>
                </div>
              </div>

              <div className="dataset-actions">
                <button 
                  className="btn-small btn-download"
                  onClick={() => handleDownload(dataset.id, dataset.name)}
                >
                  <FaFileDownload /> Download Report
                </button>
                <button 
                  className="btn-small btn-delete"
                  onClick={() => handleDelete(dataset.id)}
                >
                  <FaTrash /> Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default History;