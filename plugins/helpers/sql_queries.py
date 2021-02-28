class SqlQueries:
    songplay_table_insert = ("""
        SELECT
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id, 
                songs.artist_id, 
                events.sessionid, 
                events.location, 
                events.useragent
                FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
       WHERE events.start_time IS NOT NULL
       AND events.userid IS NOT NULL
    """)

    user_table_insert = ("""
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
        AND userid IS NOT NULL
        AND level IS NOT NULL
    """)

    song_table_insert = ("""
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
        WHERE song_id IS NOT NULL
        AND artist_id IS NOT NULL
    """)

    artist_table_insert = ("""
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
        WHERE artist_id IS NOT NULL
    """)

    time_table_insert = ("""
        SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
               extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
        FROM songplays
        WHERE start_time IS NOT NULL
    """)
    
    # CREATE TABLES 
    staging_events_table_create = ("CREATE TABLE IF NOT EXISTS staging_events (event_raw_id INT IDENTITY(0,1) PRIMARY KEY,\
                                    artist VARCHAR,\
                                    auth VARCHAR,\
                                    first_name VARCHAR,\
                                    gender VARCHAR,\
                                    item_in_session INT,\
                                    last_name VARCHAR,\
                                    length NUMERIC,\
                                    level VARCHAR,\
                                    location VARCHAR,\
                                    method VARCHAR,\
                                    page VARCHAR,\
                                    registration VARCHAR,\
                                    session_id INT,\
                                    song VARCHAR,\
                                    status INT,\
                                    ts DOUBLE PRECISION,\
                                    user_agent  VARCHAR,\
                                    user_id INT);")

    staging_songs_table_create = ("CREATE TABLE IF NOT EXISTS staging_songs (song_raw_id INT IDENTITY(0,1) PRIMARY KEY, \
                                    artist_id  VARCHAR,\
                                    artist_latitude VARCHAR,\
                                    artist_location VARCHAR,\
                                    artist_longitude VARCHAR,\
                                    artist_name VARCHAR,\
                                    duration NUMERIC,\
                                    num_songs INT,\
                                    song_id  VARCHAR,\
                                    title VARCHAR,\
                                    year INT);")

    songplay_table_create = ("CREATE TABLE IF NOT EXISTS songplays (songplay_id INT IDENTITY(0,1) PRIMARY KEY, \
                                                               start_time TIMESTAMP REFERENCES time(start_time),\
                                                               user_id INT REFERENCES users(user_id),\
                                                               level VARCHAR NOT NULL,\
                                                               song_id VARCHAR REFERENCES songs(song_id),\
                                                               artist_id VARCHAR REFERENCES artists(artist_id),\
                                                               session_id INT,\
                                                               location VARCHAR,\
                                                               user_agent VARCHAR);")

    user_table_create = ("CREATE TABLE IF NOT EXISTS users (user_id INT NOT NULL PRIMARY KEY,\
                                                            first_name VARCHAR,\
                                                            last_name VARCHAR,\
                                                            gender VARCHAR,\
                                                            level VARCHAR NOT NULL);")

    song_table_create = ("CREATE TABLE IF NOT EXISTS songs (song_id VARCHAR NOT NULL PRIMARY KEY,\
                                                            title VARCHAR,\
                                                            artist_id VARCHAR NOT NULL,\
                                                            year INT,\
                                                            duration NUMERIC);")

    artist_table_create = ("CREATE TABLE IF NOT EXISTS artists (artist_id VARCHAR NOT NULL PRIMARY KEY,\
                                                            name VARCHAR,\
                                                            location VARCHAR,\
                                                            latitude NUMERIC(9,5),\
                                                            longitude NUMERIC(9,5));")

    time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time TIMESTAMP NOT NULL PRIMARY KEY,\
                                                            hour INT,\
                                                            day INT,\
                                                            week INT,\
                                                            month INT,\
                                                            year INT,\
                                                            weekday INT);""")

