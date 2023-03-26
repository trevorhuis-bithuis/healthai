import { useAuth } from '../hooks/auth';
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

const NavButton = ({ text, handleClick }) => {
  return (
    <button
      type="button"
      className="rounded bg-indigo-50 py-1 px-2 text-lg font-semibold text-indigo-600 shadow-sm hover:bg-indigo-100"
      onClick={handleClick}
    >
      {text}
    </button>
  );
};

const Navbar = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleRecipes = () => {
    navigate('/recipes');
  }

  const handleLogout = () => {
    logout();
  };

  const handleWorkouts = () => {
    navigate('/workouts');
  }

  return (
    <div className="flex bg-white shadow">
      <div className="flex-none m-4">
        <Link to="/home" className="text-3xl font-bold text-black-600">health.ai</Link>
      </div>
      <div className="flex-none m-4">
        <NavButton text={'Recipes'} handleClick={handleRecipes} />
      </div>
      <div className="flex-none m-4">
        <NavButton text={'Workouts'} handleClick={handleWorkouts} />
      </div>
      <div className="flex-grow"></div>
      <div className="flex-none m-4">
        <NavButton text={'Logout'} handleClick={handleLogout} />
      </div>
    </div>
  );
};

export default Navbar;
