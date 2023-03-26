import { Route, Routes, Navigate } from 'react-router-dom';
import { ProtectRoutes } from './hooks/protectRoutes';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Recipes from './pages/Recipes';
import Workouts from './pages/Workouts';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="home" exact />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<ProtectRoutes />}>
        <Route path="/home" element={<Home />} />
        <Route path="/recipes" element={<Recipes />} />
        <Route path="/workouts" element={<Workouts />} />
      </Route>
    </Routes>
  );
}
