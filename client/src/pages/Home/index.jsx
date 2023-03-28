import { useState, useEffect } from 'react';
import Layout from '../../components/Layout';
import api from '../../services/api';
import { useAuth } from '../../hooks/auth';

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}


const Home = () => {
  const { cookies } = useAuth();
  const token = cookies.token;

  const [isLoading, setIsLoading] = useState(true);
  const [recipes, setRecipes] = useState(null);
  const [workouts, setWorkouts] = useState(null);
  const [selectedTab, setSelectedTab] = useState('Recipes');

  const tabs = [
    { name: 'Recipes', current: selectedTab === 'Recipes' },
    { name: 'Workouts', current: selectedTab === 'Workouts' },
  ]

  const getUserData = async () => {
    const response = await api.get('/user', {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    setRecipes(response.data.recipes);
    setWorkouts(response.data.workouts);
    setIsLoading(false);
  }

  useEffect(() => {
    getUserData();
  }, []);

  return (
    <Layout>
      <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-3xl space-y-8">
          <h1 className='text-center text-3xl my-4'>Dashboard</h1>
          <div>
            <div className="sm:hidden">
              <label htmlFor="tabs" className="sr-only">
                Select a tab
              </label>
              <select
                id="tabs"
                name="tabs"
                className="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
                defaultValue={tabs.find((tab) => tab.current).name}
                onChange={(e) => {
                  setSelectedTab(e.target.value)
                }}
              >
                {tabs.map((tab) => (
                  <option key={tab.name} value={tab.name}>{tab.name}</option>
                ))}
              </select>
            </div>
            <div className="hidden sm:block">
              <nav className="isolate flex divide-x divide-gray-200 rounded-lg shadow" aria-label="Tabs">
                {tabs.map((tab, tabIdx) => (
                  <div
                    key={tab.name}
                    className={classNames(
                      tab.current ? 'text-gray-900' : 'text-gray-500 hover:text-gray-700',
                      tabIdx === 0 ? 'rounded-l-lg' : '',
                      tabIdx === tabs.length - 1 ? 'rounded-r-lg' : '',
                      'group relative min-w-0 flex-1 overflow-hidden bg-white py-4 px-4 text-center text-sm font-medium hover:bg-gray-50 focus:z-10'
                    )}
                    aria-current={tab.current ? 'page' : undefined}
                    onClick={() => setSelectedTab(tab.name)}
                  >
                    <span>{tab.name}</span>
                    <span
                      aria-hidden="true"
                      className={classNames(
                        tab.current ? 'bg-indigo-500' : 'bg-transparent',
                        'absolute inset-x-0 bottom-0 h-0.5'
                      )}
                    />
                  </div>
                ))}
              </nav>
            </div>
          </div>

          {isLoading && (
            <div className="text-center">
              Processing...
            </div>
          )}

          {!isLoading && (

            <div className='mt-4'>
              {selectedTab === 'Recipes' && recipes && (
                recipes.map((recipe) => {
                  return (
                    <div key={recipe.id} className='bg-white border-1 mt-4'>
                      <p>
                        {`Title: ${recipe.title}`}
                      </p>
                      <br />
                      <p>
                        Ingredients:
                      </p>
                      <ul>
                        {recipe.ingredients.map((ingredient) => (
                          <li>
                            {ingredient}
                          </li>
                        ))}
                      </ul>
                      <br />
                      <p>
                        Instructions:
                      </p>
                      <ul>
                        {recipe.instructions.map((instruction) => (
                          <li>
                            {instruction}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )
                })
              )}
              {selectedTab === 'Workouts' && workouts &&
                workouts.map((workout) => {
                  return (
                    <div key={workout.id} className='bg-white border-1 mt-4'>
                      <p>
                        {`Title: ${workout.title}`}
                      </p>
                      <br />
                      <p>
                        Steps:
                      </p>
                      <ul>
                        {workout.steps.map((step) => {
                          return (<li>
                            {step}
                          </li>)
                        })}
                      </ul>
                    </div>
                  )
                }
                )
              }

            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default Home;
