# populate.py
from src.persistence.repository import Repository
from src.models.country import Country
import pycountry



def populate_db(repo: Repository) -> None:
    """Populate the database with countries and cities."""

    countries = []

    for count in pycountry.countries:
        count = Country(count.name, count.alpha_2)
        countries.append(count)

    for country in countries:
        repo.save(country)
    print("Memory DB populated")
