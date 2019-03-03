using NEDDApp.Models;
using NEDDApp.Services;
using NEDDApp.View;
using System;
using System.Collections.Generic;
using Xamarin.Forms;

namespace NEDDApp
{

    public partial class MainPage : ContentPage
    {
        private IMovieSearchDataService movieSearchDataService;
        private int i;
        public MainPage()
        {
            InitializeComponent();
            movieSearchDataService = new TMDBMoviesSearchService();

        }

        private async void Listview_ItemSelected(object sender, SelectedItemChangedEventArgs e)
        {
            var SelectedMovieInfo = e.SelectedItem as MovieInfo;
            if (SelectedMovieInfo != null)
            {
                await Navigation.PushAsync(new MovieInfoDetaliPage(SelectedMovieInfo));
                listview.SelectedItem = null;
            }
        }

        private async void SearchBar_TextChanged(object sender, TextChangedEventArgs e)
        {
            
            try
            {
                var query = e.NewTextValue as String;

                if (!String.IsNullOrEmpty(query))
                {
                    if (query.Length >= 1)
                    {
                        i = query.Length;
                        listview.ItemsSource = new List<MovieInfo>();
                        loader.IsRunning = true;
                        var movies = await movieSearchDataService.GetMoviesSearch(query);
                        if (i == query.Length)
                        {
                            loader.IsRunning = false;
                            if (movies.Count == 0)
                            {
                                searchBar.Text = "";
                                await DisplayAlert("Message", "Couldn't find movie.", "OK");
                                return;
                            }
                            
                            listview.ItemsSource = movies;
                        }
                    }
                }
            }
            catch (Exception)
            {
                loader.IsRunning = false;
                return;
            }
        }
    }
}
