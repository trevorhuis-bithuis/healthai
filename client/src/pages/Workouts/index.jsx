import { useState } from 'react';
import Layout from '../../components/Layout';
import { useAuth } from '../../hooks/auth';
import api from '../../services/api';

const Workouts = () => {
  const { cookies } = useAuth();
  const token = cookies.token;

  const [isLoading, setIsLoading] = useState(false);
  const [duration, setDuration] = useState('');
  const [muscles, setMuscles] = useState('');
  const [workout, setWorkout] = useState(null);

  const handleGenerateWorkout = async () => {
    setIsLoading(true);
    const durationNum = parseInt(duration);
    const musclesList = muscles.split(',').map((allergy) => allergy.trim());

    const response = await api.post('/exercise/workouts/generate', { duration: durationNum, muscles: musclesList }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    setWorkout(response.data.workout);
    setIsLoading(false);
  }

  const handleSaveWorkout = async () => {
    await api.post('/exercise/workouts', { title: `${duration}-minute ${muscles} workout`, steps: workout.steps }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    alert('Recipe saved successfully!');
  }

  return (
    <Layout>
      <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-3xl space-y-8">
          <h1 className='text-4xl text-center'>Generate a new workout</h1>
          <div className='grid grid-cols-2 gap-4'>
            <div>
              <label htmlFor="ingredients" className="block text-sm font-medium leading-6 text-gray-900">
                {`Duration (minutes)`}
              </label>
              <div className="mt-2">
                <input
                  type="text"
                  name="ingredients"
                  id="ingredients"
                  className="block w-full rounded-md border-0 p-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  placeholder="20"
                  onChange={(e) => { setDuration(e.target.value) }}
                />
              </div>
            </div>
            <div>
              <label htmlFor="muscles" className="block text-sm font-medium leading-6 text-gray-900">
                Body Parts
              </label>
              <div className="mt-2">
                <input
                  type="text"
                  name="muscles"
                  id="muscles"
                  className="block w-full rounded-md border-0 p-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  placeholder="chest, shoulders, triceps"
                  onChange={(e) => { setMuscles(e.target.value) }}
                />
              </div>
            </div>
          </div>
          <button
            type="button"
            className="group relative flex w-full justify-center rounded-md bg-indigo-600 py-2 px-3 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            onClick={handleGenerateWorkout}
          >
            Generate
          </button>

          {isLoading && (
            <div className='text-center'>
              <p>
                Generating workout...
              </p>
            </div>
          )}

          {!isLoading && workout !== null && (
            <div className='bg-white border-1'>
              <p>
                {`Title: ${workout.title}`}
              </p>
              <br />
              <p>
                Steps:
              </p>
              <ul>
                {workout.steps.map((step) => (
                  <li>
                    {step}
                  </li>
                ))}
              </ul>

              <button
                type="button"
                className="group relative flex w-full justify-center rounded-md bg-indigo-600 py-2 px-3 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                onClick={handleSaveWorkout}
              >
                Save
              </button>
            </div>
          )}

        </div>
      </div>
    </Layout>
  );
};

export default Workouts;
