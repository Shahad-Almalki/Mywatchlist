# My Watchlist 🎬

A Django-based web application to manage your personal movies & series watchlist.  
Built by **Shahad Almalki**.
---

#  Features
- Add, edit, delete movies & series to your personal watchlist  
- Filter by type (Movies or Series) directly from the navbar dropdown  
- Integrated local search to quickly find items in your own watchlist  
- Smart integration with TMDB API: 
      - If not found locally, automatically fetches results from TMDB
      - Lets you add movies/series from TMDB directly to your watchlist with one click  
- Handles both uploaded poster images and external poster URLs  
- Many-to-Many relationship to assign cast members to movies & series, with Select2 for elegant multiple selection  
- Pagination to handle long watchlists cleanly  
- Responsive dark-themed UI using Bootstrap, with stylish cards and fixed footer  
- Success messages on add/edit/delete actions  
- Secure with CSRF tokens and validation
