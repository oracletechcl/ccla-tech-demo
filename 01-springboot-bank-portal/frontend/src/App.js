import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';

const SESSION_KEY = 'bankportal_user';
const SESSION_TIMESTAMP = 'bankportal_login_time';
const SESSION_DURATION = 15 * 60 * 1000; // 15 min in ms

export default function App() {
  const [user, setUser] = useState(null);

  // Restore session on load
  useEffect(() => {
    const storedUser = localStorage.getItem(SESSION_KEY);
    const storedTime = localStorage.getItem(SESSION_TIMESTAMP);
    if (storedUser && storedTime) {
      const age = Date.now() - parseInt(storedTime, 10);
      if (age < SESSION_DURATION) {
        setUser(JSON.parse(storedUser));
      } else {
        // Session expired
        localStorage.removeItem(SESSION_KEY);
        localStorage.removeItem(SESSION_TIMESTAMP);
      }
    }
  }, []);

  // When user logs in, save to localStorage with timestamp
  const handleLogin = (userObj) => {
    setUser(userObj);
    localStorage.setItem(SESSION_KEY, JSON.stringify(userObj));
    localStorage.setItem(SESSION_TIMESTAMP, Date.now().toString());
  };

  // On logout, clear everything
  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem(SESSION_KEY);
    localStorage.removeItem(SESSION_TIMESTAMP);
  };

  // Optional: auto-logout after 15 minutes (even if not navigating)
  useEffect(() => {
    if (!user) return;
    const storedTime = localStorage.getItem(SESSION_TIMESTAMP);
    if (!storedTime) return;

    const expiresIn = SESSION_DURATION - (Date.now() - parseInt(storedTime, 10));
    if (expiresIn <= 0) {
      handleLogout();
      return;
    }
    const timeout = setTimeout(handleLogout, expiresIn);
    return () => clearTimeout(timeout);
  }, [user]);

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={user ? <Navigate to="/" /> : <Login setUser={handleLogin} />}
        />
        <Route
          path="/"
          element={
            user
              ? <Home user={user} onLogout={handleLogout} />
              : <Navigate to="/login" />
          }
        />
      </Routes>
    </Router>
  );
}
