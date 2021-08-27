from django.core.management import BaseCommand
from ...models import Movie


# Check if genres are valid
def check_valid_genres(genres: str) -> bool:
    if bool(genres and not genres.isspace()) and genres != 'na':
        return True
    else:
        return False

# Add a Jaccard similarity method here
def jaccard_similarity(l1, l2):
    s1 = set(l1)
    s2 = set(l2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))  

# Add a movie similarity method here
def similarity_between_movies(m1, m2):
    if check_valid_genres(m1.genres) and check_valid_genres(m2.genres):
        m1_genre = m1.genres.split()
        m2_genre = m2.genres.split()
        return jaccard_similarity(m1_genre, m2_genre)
    else:
        return 0        

class Command(BaseCommand):
    help = 'Recommend movies'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        # Figure the recommended field for each unwatched movie
        # Based on the similarity on movie genres
        THRESHOLD = 0.8
        watched_movies = Movie.objects.filter(
                watched=True)
        unwatched_movies = Movie.objects.filter(
                watched=False)
        for unwatched_movie in unwatched_movies:
            max_similarity = 0
            will_recommed = False
            for watched_movie in watched_movies:
                similarity = similarity_between_movies(unwatched_movie, watched_movie)
                if similarity >= max_similarity:
                    max_similarity = similarity
                if max_similarity >=THRESHOLD:
                    break
            if max_similarity > THRESHOLD:
                will_recommed = True
                print(f"Recommended Movie Found: {unwatched_movie.original_title}")
        unwatched_movie.recommended = will_recommed
        unwatched_movie.save()

# python manage.py make_recommendations