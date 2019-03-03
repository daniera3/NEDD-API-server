using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using NEDDApp.Models;
using Newtonsoft.Json;

namespace NEDDApp.Services
{
    class TestPerDateService : ITestPerDateDataService
    {
        public Task<List<TestInfo>> GetTestPerDate(string query)
        {
            var moviesSearch=await GetTMDBMovieSearch(query);

            if (moviesSearch == new TMDBMovieSearch())
                return new List<MovieInfo>();
            List<MovieInfo> MoviesInfos = new List<MovieInfo>();
            foreach(var result in moviesSearch.results)
            {

                MovieInfo movieInfo = new MovieInfo
                {
                    Name = result.title,
                    Description = result.overview,
                    ImageSource = $"https://image.tmdb.org/t/p/w250_and_h141_face/{result.poster_path}",
                    ReleaseYear = !String.IsNullOrEmpty(result.release_date) ? result.release_date.Substring(0, 4) : ""

                };
                MoviesInfos.Add(movieInfo);
            }
            return MoviesInfos.OrderByDescending(o => o.ReleaseYear).ToList(); ;

        }

        
    

        private async Task<TMDBMovieSearch> GetTMDBMovieSearch(String query)
        {
            using (HttpClient client = new HttpClient())
            {
                string TMDB_KEY = "34a9ab80294cc1212b86a2635d31d308";
                String URL = $"https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&query={query}";

                HttpResponseMessage response= await client.GetAsync(new Uri(URL));

                string JsonString = await response.Content.ReadAsStringAsync();

                TMDBMovieSearch result =JsonConvert.DeserializeObject<TMDBMovieSearch>(JsonString);

                if (result == null)
                    return new TMDBMovieSearch();
                return result;

            }
        }
    }
}
