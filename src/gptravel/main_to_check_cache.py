from gptravel.core.services.geocoder import GeoCoder


def geocode(name: str) -> str:
    geo = GeoCoder()
    return geo.country_from_location_name(name)


def main():
    geocode("Milan")
    geocode("Roma")
    geocode("Milan")


if __name__ == "__main__":
    main()
