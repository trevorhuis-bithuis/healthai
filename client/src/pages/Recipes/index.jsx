import { useState } from 'react';
import Layout from '../../components/Layout';
import { useAuth } from '../../hooks/auth';
import api from '../../services/api';

const Recipes = () => {
  const { cookies } = useAuth();
  const token = cookies.token;

  const [ingredients, setIngredients] = useState('');
  const [allergies, setAllergies] = useState('');
  const [recipe, setRecipe] = useState(null);

  const handleGenerateRecipe = async () => {
    const ingredientsList = ingredients.split(',').map((ingredient) => ingredient.trim());
    const allergiesList = allergies.split(',').map((allergy) => allergy.trim());

    const response = await api.post('/diet/recipes/generate', { ingredients: ingredientsList, allergies: allergiesList }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    setRecipe(response.data.recipe);
  }

  return (
    <Layout>
      <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-3xl space-y-8">
          <h1 className='text-4xl text-center'>Generate a new recipe</h1>
          <div className='grid grid-cols-2 gap-4'>
            <div>
              <label htmlFor="ingredients" className="block text-sm font-medium leading-6 text-gray-900">
                Ingredients
              </label>
              <div className="mt-2">
                <input
                  type="text"
                  name="ingredients"
                  id="ingredients"
                  className="block w-full rounded-md border-0 p-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  placeholder="eggs, milk, flour"
                  onChange={(e) => { setIngredients(e.target.value) }}
                />
              </div>
            </div>
            <div>
              <label htmlFor="allergies" className="block text-sm font-medium leading-6 text-gray-900">
                Allergies
              </label>
              <div className="mt-2">
                <input
                  type="text"
                  name="allergies"
                  id="allergies"
                  className="block w-full rounded-md border-0 p-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  placeholder="soy, gluten, dairy"
                  onChange={(e) => { setAllergies(e.target.value) }}
                />
              </div>
            </div>
          </div>
          <button
            type="button"
            className="group relative flex w-full justify-center rounded-md bg-indigo-600 py-2 px-3 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            onClick={handleGenerateRecipe}
          >
            Generate
          </button>

          {recipe !== null && (
            <div className='bg-white border-1'>
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
          )}
        </div>
      </div>
    </Layout>
  );
};

export default Recipes;
