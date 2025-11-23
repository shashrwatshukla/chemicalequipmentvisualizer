import React, { useState, useRef, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FaChartBar, FaHistory, FaSignOutAlt, FaUser, FaCog, FaKey, FaTrash } from 'react-icons/fa';
import api from '../services/api';

function Navbar({ user, onLogout }) {
  const location = useLocation();
  const [showSettings, setShowSettings] = useState(false);
  const [showChangePassword, setShowChangePassword] = useState(false);
  const [showDeleteAccount, setShowDeleteAccount] = useState(false);
  const [passwordData, setPasswordData] = useState({ current: '', new: '' });
  const [deletePassword, setDeletePassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const settingsRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (settingsRef.current && !settingsRef.current.contains(event.target)) {
        setShowSettings(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    try {
      const response = await api.changePassword(passwordData.current, passwordData.new);
      setMessage(response.data.message);
      setPasswordData({ current: '', new: '' });
      setTimeout(() => {
        setShowChangePassword(false);
        setMessage('');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Password change failed');
    }
  };

  const handleDeleteAccount = async (e) => {
  e.preventDefault();
  setError('');
  setMessage('');

  if (!window.confirm('Are you sure? This action cannot be undone!')) {
    return;
  }

  try {
    const response = await api.deleteAccount(deletePassword);
    alert('Account deleted successfully');
    window.location.href = '/login';
  } catch (err) {
    setError(err.response?.data?.error || 'Account deletion failed');
  }
};

  return (
    <>
      <nav className="navbar">
        <Link to="/dashboard" className="navbar-brand">
          <FaChartBar />
          Chemical Equipment Visualizer
        </Link>

        <div className="navbar-links">
          <Link to="/dashboard" className={location.pathname === '/dashboard' ? 'active' : ''}>
            <FaChartBar /> Dashboard
          </Link>
          <Link to="/history" className={location.pathname === '/history' ? 'active' : ''}>
            <FaHistory /> History
          </Link>
        </div>

        <div className="navbar-user">
          <span>
            <FaUser /> {user.username}
          </span>

          <div className="settings-dropdown" ref={settingsRef}>
            <button
              className="settings-btn"
              onClick={() => setShowSettings(!showSettings)}
              title="Settings"
            >
              <FaCog />
            </button>

            {showSettings && (
              <div className="settings-menu">
                <button onClick={() => { setShowChangePassword(true); setShowSettings(false); }}>
                  <FaKey /> Change Password
                </button>
                <button onClick={() => { setShowDeleteAccount(true); setShowSettings(false); }} className="danger">
                  <FaTrash /> Delete Account
                </button>
              </div>
            )}
          </div>

          <button onClick={onLogout} className="logout-btn">
            <FaSignOutAlt /> Logout
          </button>
        </div>
      </nav>

      {showChangePassword && (
        <div className="modal-overlay" onClick={() => setShowChangePassword(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2><FaKey /> Change Password</h2>
            
            {error && <div className="error-message">{error}</div>}
            {message && <div className="success-message">{message}</div>}

            <form onSubmit={handleChangePassword}>
              <div className="form-group">
                <label>Current Password</label>
                <input
                  type="password"
                  value={passwordData.current}
                  onChange={(e) => setPasswordData({ ...passwordData, current: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>New Password</label>
                <input
                  type="password"
                  value={passwordData.new}
                  onChange={(e) => setPasswordData({ ...passwordData, new: e.target.value })}
                  required
                />
                <small>Must be 8+ characters with uppercase, number, and special character</small>
              </div>

              <div className="modal-actions">
                <button type="submit" className="btn-primary">Change Password</button>
                <button type="button" onClick={() => setShowChangePassword(false)} className="btn-secondary">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showDeleteAccount && (
        <div className="modal-overlay" onClick={() => setShowDeleteAccount(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2><FaTrash /> Delete Account</h2>
            
            <div className="warning-box">
              <strong>⚠️ Warning:</strong> This action cannot be undone. All your data will be permanently deleted.
            </div>

            {error && <div className="error-message">{error}</div>}

            <form onSubmit={handleDeleteAccount}>
              <div className="form-group">
                <label>Enter your password to confirm</label>
                <input
                  type="password"
                  value={deletePassword}
                  onChange={(e) => setDeletePassword(e.target.value)}
                  required
                />
              </div>

              <div className="modal-actions">
                <button type="submit" className="btn-danger">Delete Account</button>
                <button type="button" onClick={() => setShowDeleteAccount(false)} className="btn-secondary">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}

export default Navbar;