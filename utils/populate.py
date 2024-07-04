# populate.py
""" Populate the database with some data at the start of the application"""

from src.persistence.repository import Repository
import pycountry


def populate_db(repo: Repository) -> None:
	"""Populates the db with a dummy country"""
	from src.models.country import Country

	try:
		countries = []

		for c in pycountry.countries:
			c = Country(c.name, c.alpha_2)
			if c not in countries:
				countries.append(c)

			for country in countries:
				existing_country = repo.get_by_code(Country, country.code)
				if existing_country is None:
					repo.save(country)

		print("Memory DB populated")

	except ImportError:
		print("No more countries to add")

