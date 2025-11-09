import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in from localStorage
    const storedUser = localStorage.getItem('currentUser');
    if (storedUser) {
      setCurrentUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  // Get all registered users from localStorage
  const getRegisteredUsers = () => {
    const users = localStorage.getItem('registeredUsers');
    return users ? JSON.parse(users) : [];
  };

  // Save registered users to localStorage
  const saveRegisteredUsers = (users) => {
    localStorage.setItem('registeredUsers', JSON.stringify(users));
  };

  const signup = (name, email, password) => {
    // Check if user already exists
    const registeredUsers = getRegisteredUsers();
    const existingUser = registeredUsers.find(u => u.email === email);
    
    if (existingUser) {
      return Promise.reject(new Error('An account with this email already exists.'));
    }

    // Create new user
    const user = {
      name,
      email,
      password, // In production, NEVER store plain passwords! Use backend hashing
      id: Date.now().toString(),
      createdAt: new Date().toISOString()
    };
    
    // Add to registered users
    registeredUsers.push(user);
    saveRegisteredUsers(registeredUsers);
    
    // Log them in immediately after signup
    const userToStore = { ...user };
    delete userToStore.password; // Don't store password in currentUser
    
    setCurrentUser(userToStore);
    localStorage.setItem('currentUser', JSON.stringify(userToStore));
    return Promise.resolve(userToStore);
  };

  const login = (email, password) => {
    // Get all registered users
    const registeredUsers = getRegisteredUsers();
    
    // Find user by email
    const user = registeredUsers.find(u => u.email === email);
    
    // Check if user exists
    if (!user) {
      return Promise.reject(new Error('No account found with this email. Please sign up first.'));
    }
    
    // Check if password matches
    if (user.password !== password) {
      return Promise.reject(new Error('Incorrect password. Please try again.'));
    }
    
    // Login successful - create user object without password
    const userToStore = {
      name: user.name,
      email: user.email,
      id: user.id,
      createdAt: user.createdAt
    };
    
    setCurrentUser(userToStore);
    localStorage.setItem('currentUser', JSON.stringify(userToStore));
    return Promise.resolve(userToStore);
  };

  const loginWithGoogle = async (credentialResponse) => {
    try {
      // The credential is a JWT token from Google
      const token = credentialResponse.credential;
      
      // Decode the JWT to get user info
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      
      const userData = JSON.parse(jsonPayload);
      
      // Create user object from Google data
      const user = {
        name: userData.name,
        email: userData.email,
        picture: userData.picture,
        id: userData.sub,
        provider: 'google',
        createdAt: new Date().toISOString()
      };
      
      // Check if this Google user is already registered
      const registeredUsers = getRegisteredUsers();
      const existingUser = registeredUsers.find(u => u.email === user.email && u.provider === 'google');
      
      if (!existingUser) {
        // Register the Google user
        registeredUsers.push(user);
        saveRegisteredUsers(registeredUsers);
      }
      
      setCurrentUser(user);
      localStorage.setItem('currentUser', JSON.stringify(user));
      return Promise.resolve(user);
    } catch (error) {
      console.error('Google login error:', error);
      throw error;
    }
  };

  const loginWithApple = async () => {
    // Placeholder for Apple Sign In
    try {
      const user = {
        name: 'Apple User',
        email: 'user@icloud.com',
        id: 'apple_' + Date.now(),
        provider: 'apple',
        createdAt: new Date().toISOString()
      };
      
      setCurrentUser(user);
      localStorage.setItem('currentUser', JSON.stringify(user));
      return Promise.resolve(user);
    } catch (error) {
      console.error('Apple login error:', error);
      throw error;
    }
  };

  const logout = () => {
    setCurrentUser(null);
    localStorage.removeItem('currentUser');
    return Promise.resolve();
  };

  const value = {
    currentUser,
    signup,
    login,
    loginWithGoogle,
    loginWithApple,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}