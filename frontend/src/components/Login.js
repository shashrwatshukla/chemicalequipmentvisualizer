import React, { useState } from 'react';
import { FaUser, FaLock, FaEnvelope, FaGoogle, FaArrowLeft, FaKey, FaEye, FaEyeSlash } from 'react-icons/fa';
import { useGoogleLogin } from '@react-oauth/google';
import api from '../services/api';

function Login({ onLogin }) {
  const [mode, setMode] = useState('login');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    newPassword: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [verificationCode, setVerificationCode] = useState('');
  const [registeredUsername, setRegisteredUsername] = useState('');
  const [resetEmail, setResetEmail] = useState('');
  
  const [showPassword, setShowPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const calculatePasswordStrength = (password) => {
    if (!password) return { strength: 0, label: '', color: '' };
    
    let strength = 0;
    if (password.length >= 8) strength += 25;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 25;
    if (/\d/.test(password)) strength += 25;
    if (/[^a-zA-Z0-9]/.test(password)) strength += 25;
    
    if (strength <= 25) return { strength, label: 'Weak', color: '#ef4444' };
    if (strength <= 50) return { strength, label: 'Fair', color: '#f59e0b' };
    if (strength <= 75) return { strength, label: 'Good', color: '#3b82f6' };
    return { strength, label: 'Strong', color: '#10b981' };
  };

  const passwordStrength = mode === 'register' ? calculatePasswordStrength(formData.password) : null;

  const handleGoogleLogin = useGoogleLogin({
    onSuccess: async (tokenResponse) => {
      setLoading(true);
      setError('');
      try {
        const response = await api.googleAuth(tokenResponse.access_token);
        setSuccess('Google authentication successful!');
        setTimeout(() => {
          onLogin(response.data.user);
        }, 500);
      } catch (err) {
        setError(err.response?.data?.error || 'Google authentication failed');
      } finally {
        setLoading(false);
      }
    },
    onError: () => {
      setError('Google authentication failed');
    },
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      if (mode === 'login') {
        const response = await api.login(formData.username, formData.password);
        setSuccess('Login successful!');
        setTimeout(() => {
          onLogin(response.data.user);
        }, 500);
      } else if (mode === 'register') {
        const response = await api.register(
          formData.username,
          formData.email,
          formData.password
        );
        
        if (response.data.verification_required) {
          setRegisteredUsername(formData.username);
          setMode('verify');
          setSuccess(response.data.message);
          
          if (response.data.dev_code) {
            setSuccess(`${response.data.message}\n\nDEV CODE: ${response.data.dev_code}`);
          }
        }
      }
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleVerification = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.verifyEmail(registeredUsername, verificationCode);
      setSuccess(response.data.message);
      
      setTimeout(() => {
        setMode('login');
        setFormData({ username: '', email: '', password: '', newPassword: '' });
        setVerificationCode('');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Verification failed');
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.forgotPassword(resetEmail);
      setSuccess(response.data.message);
      
      if (response.data.dev_code) {
        setSuccess(`${response.data.message}\n\nDEV CODE: ${response.data.dev_code}`);
      }
      
      setTimeout(() => {
        setMode('reset');
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send reset code');
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.resetPassword(
        resetEmail,
        verificationCode,
        formData.newPassword
      );
      setSuccess(response.data.message);
      
      setTimeout(() => {
        setMode('login');
        setFormData({ username: '', email: '', password: '', newPassword: '' });
        setVerificationCode('');
        setResetEmail('');
        setShowNewPassword(false);
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Password reset failed');
    } finally {
      setLoading(false);
    }
  };

  if (mode === 'verify') {
    return (
      <div className="login-container-white">
        <div className="login-box">
          <div className="login-icon">
            <FaEnvelope />
          </div>
          <h1>Verify Your Email</h1>
          <p>Enter the 6-digit code sent to your email</p>

          <form onSubmit={handleVerification}>
            {error && <div className="error-message"><FaEnvelope /><span>{error}</span></div>}
            {success && <div className="success-message"><FaEnvelope /><span style={{ whiteSpace: 'pre-line' }}>{success}</span></div>}

            <div className="form-group">
              <label><FaKey /> Verification Code</label>
              <input
                type="text"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)}
                placeholder="Enter 6-digit code"
                maxLength="6"
                required
              />
            </div>

            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? 'Verifying...' : 'Verify Email'}
            </button>

            <button type="button" className="back-btn" onClick={() => { setMode('login'); setVerificationCode(''); }}>
              <FaArrowLeft /> Back to Login
            </button>
          </form>
        </div>
      </div>
    );
  }

  if (mode === 'forgot') {
    return (
      <div className="login-container-white">
        <div className="login-box">
          <div className="login-icon">
            <FaKey />
          </div>
          <h1>Forgot Password</h1>
          <p>Enter your email to receive a reset code</p>

          <form onSubmit={handleForgotPassword}>
            {error && <div className="error-message"><FaEnvelope /><span>{error}</span></div>}
            {success && <div className="success-message"><FaEnvelope /><span style={{ whiteSpace: 'pre-line' }}>{success}</span></div>}

            <div className="form-group">
              <label><FaEnvelope /> Email Address</label>
              <input
                type="email"
                value={resetEmail}
                onChange={(e) => setResetEmail(e.target.value)}
                placeholder="Enter your email"
                required
              />
            </div>

            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? 'Sending...' : 'Send Reset Code'}
            </button>

            <button type="button" className="back-btn" onClick={() => { setMode('login'); setResetEmail(''); }}>
              <FaArrowLeft /> Back to Login
            </button>
          </form>
        </div>
      </div>
    );
  }

  if (mode === 'reset') {
    const resetPasswordStrength = calculatePasswordStrength(formData.newPassword);
    
    return (
      <div className="login-container-white">
        <div className="login-box">
          <div className="login-icon">
            <FaLock />
          </div>
          <h1>Reset Password</h1>
          <p>Enter the code and your new password</p>

          <form onSubmit={handleResetPassword}>
            {error && <div className="error-message"><FaLock /><span>{error}</span></div>}
            {success && <div className="success-message"><FaLock /><span>{success}</span></div>}

            <div className="form-group">
              <label><FaKey /> Reset Code</label>
              <input
                type="text"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)}
                placeholder="Enter 6-digit code"
                maxLength="6"
                required
              />
            </div>

            <div className="form-group">
              <label><FaLock /> New Password</label>
              <div className="password-input-wrapper">
                <input
                  type={showNewPassword ? 'text' : 'password'}
                  name="newPassword"
                  value={formData.newPassword}
                  onChange={handleChange}
                  placeholder="Enter new password"
                  required
                />
                <button
                  type="button"
                  className="password-toggle-btn"
                  onClick={() => setShowNewPassword(!showNewPassword)}
                  tabIndex="-1"
                >
                  {showNewPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              <small>Must be 8+ characters with uppercase, number, and special character</small>
              
              {formData.newPassword && (
                <div className="password-strength-indicator">
                  <div className="strength-bar-container">
                    <div 
                      className="strength-bar" 
                      style={{ 
                        width: `${resetPasswordStrength.strength}%`,
                        backgroundColor: resetPasswordStrength.color 
                      }}
                    ></div>
                  </div>
                  <span className="strength-label" style={{ color: resetPasswordStrength.color }}>
                    {resetPasswordStrength.label}
                  </span>
                </div>
              )}
            </div>

            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? 'Resetting...' : 'Reset Password'}
            </button>

            <button type="button" className="back-btn" onClick={() => { 
              setMode('login'); 
              setVerificationCode(''); 
              setFormData({ ...formData, newPassword: '' }); 
              setShowNewPassword(false);
            }}>
              <FaArrowLeft /> Back to Login
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="login-container-white">
      <div className="login-box">
        <div className="login-icon">
          <FaUser />
        </div>
        <h1>Chemical Equipment Visualizer</h1>
        <p>Professional data analysis and visualization</p>

        <div className="auth-tabs">
          <button className={`auth-tab ${mode === 'login' ? 'active' : ''}`} onClick={() => { 
            setMode('login'); 
            setError(''); 
            setSuccess(''); 
            setShowPassword(false);
          }}>
            Login
          </button>
          <button className={`auth-tab ${mode === 'register' ? 'active' : ''}`} onClick={() => { 
            setMode('register'); 
            setError(''); 
            setSuccess(''); 
            setShowPassword(false);
          }}>
            Register
          </button>
        </div>

        <button className="google-login-btn" onClick={() => handleGoogleLogin()} disabled={loading}>
          <FaGoogle />
          {mode === 'login' ? 'Sign in with Google' : 'Sign up with Google'}
        </button>

        <div className="divider">
          <span>OR</span>
        </div>

        <form onSubmit={handleSubmit}>
          {error && <div className="error-message"><FaUser /><span>{error}</span></div>}
          {success && <div className="success-message"><FaUser /><span style={{ whiteSpace: 'pre-line' }}>{success}</span></div>}

          <div className="form-group">
            <label>
              <FaUser /> {mode === 'login' ? 'Username or Email' : 'Username'}
            </label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder={mode === 'login' ? 'Enter username or email' : 'Enter username'}
              required
            />
          </div>

          {mode === 'register' && (
            <div className="form-group">
              <label><FaEnvelope /> Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter email"
                required
              />
            </div>
          )}

          <div className="form-group">
            <label><FaLock /> Password</label>
            <div className="password-input-wrapper">
              <input
                type={showPassword ? 'text' : 'password'}
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter password"
                required
              />
              <button
                type="button"
                className="password-toggle-btn"
                onClick={() => setShowPassword(!showPassword)}
                tabIndex="-1"
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
            {mode === 'register' && (
              <>
                <small>Must be 8+ characters with uppercase, number, and special character</small>
                {formData.password && passwordStrength && (
                  <div className="password-strength-indicator">
                    <div className="strength-bar-container">
                      <div 
                        className="strength-bar" 
                        style={{ 
                          width: `${passwordStrength.strength}%`,
                          backgroundColor: passwordStrength.color 
                        }}
                      ></div>
                    </div>
                    <span className="strength-label" style={{ color: passwordStrength.color }}>
                      {passwordStrength.label}
                    </span>
                  </div>
                )}
              </>
            )}
          </div>

          {mode === 'login' && (
            <div className="forgot-password-link">
              <button type="button" onClick={() => { setMode('forgot'); setError(''); }}>
                Forgot Password?
              </button>
            </div>
          )}

          <button type="submit" className="login-btn" disabled={loading}>
            {loading ? (mode === 'login' ? 'Logging in...' : 'Registering...') : (mode === 'login' ? 'Login' : 'Register')}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;