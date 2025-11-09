import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { useState } from 'react';
import './Header.css';

function Header() {
  const navigate = useNavigate();
  const { currentUser, logout } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);

  const handleLogout = async () => {
    await logout();
    setShowUserMenu(false);
    navigate('/');
  };

  return (
    <header className="app-header">
      <div className="app-header-content">
        {/* Classic Soren Logo */}
        <Link to="/" className="app-logo-section">
          <img 
            src="/soren-logo.png" 
            alt="Soren Logo" 
            className="app-logo-image"
          />
        </Link>

        {/* Auth Section */}
        <div className="app-auth-section">
          {currentUser ? (
            <div className="app-user-menu-wrapper">
              <button 
                className="app-user-menu-btn"
                onClick={() => setShowUserMenu(!showUserMenu)}
              >
                <div className="app-user-avatar">
                  {currentUser.name ? currentUser.name.charAt(0).toUpperCase() : 'U'}
                </div>
                <span className="app-user-name">{currentUser.name || currentUser.email}</span>
                <svg className="app-dropdown-icon" width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4.5L6 7.5L9 4.5"></path>
                </svg>
              </button>
              
              {showUserMenu && (
                <div className="app-user-dropdown">
                  <div className="app-user-info">
                    <div className="app-user-info-name">{currentUser.name}</div>
                    <div className="app-user-info-email">{currentUser.email}</div>
                  </div>
                  <button onClick={handleLogout} className="app-logout-btn">
                    <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                    </svg>
                    Log Out
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <Link to="/login" className="app-btn app-btn-secondary">
                Sign In
              </Link>
              <Link to="/signup" className="app-btn app-btn-primary">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;