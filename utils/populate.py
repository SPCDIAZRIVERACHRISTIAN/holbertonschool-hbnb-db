# populate.py
from src.persistence.repository import Repository
from src.models.country import Country
import pycountry



def populate_db(repo: Repository) -> None:
    """Populate the database with countries and cities."""

    try:
        countries = []

        for count in pycountry.countries:
            existing_countries = Country.get(count.alpha_2)
            if existing_countries is None:
                count = Country(count.name, count.alpha_2)
                countries.append(count)

        for country in countries:
            repo.save(country)
        print("Memory DB populated")
    except ImportError:
        print("No more countries to add")
