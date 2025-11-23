import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import History from './components/History';
import Navbar from './components/Navbar';
import api from './services/api';
import './App.css';

const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID || 'your-google-client-id.apps.googleusercontent.com';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await api.getCurrentUser();
      if (response.status === 200 && response.data) {
        setUser(response.data);
        console.log('✅ User authenticated:', response.data.username);
      } else {
        setUser(null);
        console.log('❌ No user data returned');
      }
    } catch (error) {
      console.log('❌ Auth check failed:', error.response?.status, error.message);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = async () => {
    try {
      await api.logout();
      setUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <Router>
        <div className="App">
          {user && <Navbar user={user} onLogout={handleLogout} />}
          <Routes>
            <Route
              path="/login"
              element={
                user ? (
                  <Navigate to="/dashboard" replace />
                ) : (
                  <Login onLogin={handleLogin} />
                )
              }
            />
            <Route
              path="/dashboard"
              element={
                user ? (
                  <Dashboard user={user} />
                ) : (
                  <Navigate to="/login" replace />
                )
              }
            />
            <Route
              path="/history"
              element={
                user ? (
                  <History user={user} />
                ) : (
                  <Navigate to="/login" replace />
                )
              }
            />
            <Route
              path="/"
              element={<Navigate to={user ? "/dashboard" : "/login"} replace />}
            />
          </Routes>
        </div>
      </Router>
    </GoogleOAuthProvider>
  );
}

export default App;