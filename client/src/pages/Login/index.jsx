import { useState } from 'react';
import AuthInput from '../../components/AuthInput';
import { useAuth } from '../../hooks/auth';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();

  const handleLogin = () => {
    login(email, password);
  };

  return (
    <div>
      <AuthInput
        email={email}
        setEmail={setEmail}
        password={password}
        setPassword={setPassword}
        headerText={'Sign up'}
        handleSubmit={handleLogin}
      />
    </div>
  );
};

export default Login;
