CREATE table if not EXISTS users (
    user_id      INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    gender       VARCHAR(255),
    name_title   VARCHAR(255),
    name_first   VARCHAR(255),
    name_last    VARCHAR(255),
    age 		 INT,
    nat          VARCHAR(255),
    created_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Создание таблицы contact_details
CREATE table if not EXISTS contact_details (
    user_id      INT NOT NULL,
    phone        VARCHAR(255),
    cell         VARCHAR(255),
    created_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Создание таблицы media_data
CREATE table if not EXISTS media_data (
    user_id         INT NOT NULL,
    picture         VARCHAR(255),
    created_dttm    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_dttm    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
CREATE table if not EXISTS registration_data (
    user_id             INT NOT NULL,
    email               VARCHAR(255),
    username            VARCHAR(255),
    password            VARCHAR(255),
    password_md5        VARCHAR(255),
    password_validation BOOLEAN,
    created_dttm        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_dttm        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- Создание таблицы cities
CREATE table if not EXISTS cities (
    city_id 	 INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    city 		 VARCHAR(255),
    state 		 VARCHAR(255),
    country 	 VARCHAR(255),
    created_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_city UNIQUE (city),
    CONSTRAINT unique_state UNIQUE (state),
    CONSTRAINT unique_country UNIQUE (country)
);


-- Создание таблицы locations
CREATE table if not EXISTS locations (
    user_id       INT NOT NULL,
    city_id       INT NOT NULL,
    street_name   VARCHAR(255),
    street_number INT,
    postcode      VARCHAR(255),
    latitude      INT,
    longitude     INT,
    created_dttm  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_dttm  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

