using MoviesApp.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace MoviesApp.View
{
	[XamlCompilation(XamlCompilationOptions.Compile)]
	public partial class MovieInfoDetaliPage : ContentPage
	{
		public MovieInfoDetaliPage (MovieInfo movieInfo)
		{
			InitializeComponent ();
            if (movieInfo != null)
                BindingContext = movieInfo;
            else new ArgumentNullException("movie Info is null");
		}
	}
}