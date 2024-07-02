NODES = {
    "Movie": {
        "properties": [
            "index", "overview", "title",
            "vote_average", "vote_count", "original_title"
        ]
    },
    "Person": {
        "properties": ["director"]
    },
    "Genre": {
        "properties": ["genre"]
    },
    "Budget": {
        "properties": ["budget"]
    },
    "Revenue": {
        "properties": ["revenue"]
    },
    "Status": {
        "properties": ["status"]
    },
    "Language": {
        "properties": ["original_language"]
    }
}

RELATIONSHIP = {
    "DIRECTED": {"from": "Person", "to": "Movie"},
    "IN_GENRE": {"from": "Movie", "to": "Genre"},
    "GROSSED": {"from": "Movie", "to": "Revenue", "weight": 0.8},
    "LANGUAGE_ACTED_IN": {"from": "Movie", "to": "Language", "weight": 0.5},
    "COST": {"from": "Movie", "to": "Budget"},  # Budget relationship
    "CURRENT_STATUS": {"from": "Movie", "to": "Status", "weight": 1.0}
}
