from serpapi import GoogleSearch


def googleScholorSearch(queries):
    q = ""
    for querie in queries:
        q += '"' + querie + '"'

    params = {
    "engine": "google_scholar",
    "q": q,
    "api_key": "6545549a738190735020bcca2e40cac4c8f007fb4c7eebe2a9408943353f9682"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
