create_movie_cypher = """
        MERGE (m:Movie {index: $index, title: $original_title})
        SET m.budget = $budget,
            m.original_language = $original_language,
            m.overview = $overview,
            m.revenue = $revenue,
            m.status = $status,
            m.title = $title,
            m.vote_average = $vote_average,
            m.vote_count = $vote_count
    
        WITH m
    
        FOREACH (genre IN $genresList |
            MERGE (g:Genre {name: trim(genre)})
            MERGE (m)-[:IN_GENRE]->(g))
    
        MERGE (d:Person {name: $director})
        MERGE (d)-[:DIRECTED]->(m)
    
        // Relationships with Budget, Revenue, Language, and Status
        MERGE (b:Budget {amount: $budget})
        MERGE (m)-[:COST]->(b)
    
        MERGE (r:Revenue {amount: $revenue})
        MERGE (m)-[:GROSSED {weight: 0.8}]->(r)
    
        MERGE (l:Language {name: $original_language})
        MERGE (m)-[:LANGUAGE_ACTED_IN {weight: 0.5}]->(l)
    
        MERGE (s:Status {name: $status})
        MERGE (m)-[:CURRENT_STATUS {weight: 1.0}]->(s)
    """
