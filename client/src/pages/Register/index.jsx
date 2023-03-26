import { useState } from 'react';
import AuthInput from '../../components/AuthInput';
import { useAuth } from '../../hooks/auth';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { register } = useAuth();

  const handleRegister = () => {
    register(email, password);
  };

  return (
    <div>
      <AuthInput
        email={email}
        setEmail={setEmail}
        password={password}
        setPassword={setPassword}
        headerText={'Register'}
        handleSubmit={handleRegister}
      />
    </div>
  );
};

export default Register;
