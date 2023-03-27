import { createContext, useContext, useMemo } from 'react';
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const navigate = useNavigate();
  const [cookies, setCookies, removeCookie] = useCookies();

  const login = async (email, password) => {
    const res = await api.post('/auth/login', {
      email,
      password,
      test: 'test'
    });

    setCookies('token', res.data.token);

    navigate('/home');
  };

  const register = async (email, password) => {
    const res = await api.post('/auth/register', {
      email,
      password
    });

    setCookies('token', res.data.token);

    navigate('/home');
  };

  const logout = () => {
    removeCookie('token');
    navigate('/login');
  };

  const value = useMemo(
    () => ({
      cookies,
      login,
      register,
      logout
    }),
    [cookies]
  );

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};

export const useAuth = () => {
  return useContext(UserContext);
};
