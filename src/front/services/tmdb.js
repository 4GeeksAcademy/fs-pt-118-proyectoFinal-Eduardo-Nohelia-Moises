
//crear una funcion que traera peliculas desde una API externa tmdb 

export async function getPopularMovies() {

  //conectate al endpoint de peliculas populares y me traes la primera pagina
  const API_URL =
    "https://api.themoviedb.org/3/movie/popular?language=es-ES&page=1";

  const response = await fetch(API_URL, {            //hace la llamada http a la api
    headers: {
      Authorization: `Bearer ${import.meta.env.VITE_TMDB_TOKEN}`,
    },
  });

  const data = await response.json();    //convierte la respuesta de la api que viene en texto a objeto   
  return data.results;
}
