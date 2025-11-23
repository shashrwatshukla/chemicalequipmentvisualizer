import React, { useState } from 'react';
import { FaSearch, FaSort, FaSortUp, FaSortDown } from 'react-icons/fa';

function DataTable({ equipment }) {
  const [sortField, setSortField] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  if (!equipment || equipment.length === 0) {
    return null;
  }

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  let filteredData = equipment.filter(item =>
    item.equipment_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.equipment_type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (sortField) {
    filteredData.sort((a, b) => {
      const aVal = a[sortField];
      const bVal = b[sortField];
      
      if (typeof aVal === 'string') {
        return sortDirection === 'asc' 
          ? aVal.localeCompare(bVal)
          : bVal.localeCompare(aVal);
      } else {
        return sortDirection === 'asc' 
          ? aVal - bVal
          : bVal - aVal;
      }
    });
  }

  const totalPages = Math.ceil(filteredData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedData = filteredData.slice(startIndex, startIndex + itemsPerPage);

  const getSortIcon = (field) => {
    if (sortField !== field) return <FaSort />;
    return sortDirection === 'asc' ? <FaSortUp /> : <FaSortDown />;
  };

  return (
    <div className="data-table-section">
      <h2>Equipment Data Table</h2>
      
      <div className="table-controls">
        <div style={{ position: 'relative', flex: 1, maxWidth: '400px' }}>
          <FaSearch style={{ 
            position: 'absolute', 
            left: '1rem', 
            top: '50%', 
            transform: 'translateY(-50%)',
            color: 'var(--gray)'
          }} />
          <input
            type="text"
            placeholder="Search equipment..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentPage(1);
            }}
            className="search-input"
            style={{ paddingLeft: '2.5rem' }}
          />
        </div>
        <span className="table-info">
          Showing {startIndex + 1} to {Math.min(startIndex + itemsPerPage, filteredData.length)} of {filteredData.length} entries
        </span>
      </div>

      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('equipment_name')}>
                Equipment Name {getSortIcon('equipment_name')}
              </th>
              <th onClick={() => handleSort('equipment_type')}>
                Type {getSortIcon('equipment_type')}
              </th>
              <th onClick={() => handleSort('flowrate')}>
                Flowrate {getSortIcon('flowrate')}
              </th>
              <th onClick={() => handleSort('pressure')}>
                Pressure {getSortIcon('pressure')}
              </th>
              <th onClick={() => handleSort('temperature')}>
                Temperature {getSortIcon('temperature')}
              </th>
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((item, index) => (
              <tr key={item.id || index}>
                <td>{item.equipment_name}</td>
                <td>
                  <span className="type-badge">{item.equipment_type}</span>
                </td>
                <td className="numeric">{item.flowrate.toFixed(2)}</td>
                <td className="numeric">{item.pressure.toFixed(2)}</td>
                <td className="numeric">{item.temperature.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
            className="pagination-btn"
          >
            ← Previous
          </button>
          
          <span className="page-info">
            Page {currentPage} of {totalPages}
          </span>
          
          <button
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            disabled={currentPage === totalPages}
            className="pagination-btn"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
}

export default DataTable;