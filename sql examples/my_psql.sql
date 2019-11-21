CREATE USER muctepkot WITH PASSWORD 'muctepkot';
DROP DATABASE IF EXISTS postapi_security;
CREATE DATABASE postapi_security;
ALTER DATABASE postapi_security OWNER TO muctepkot;
GRANT ALL PRIVILEGES ON DATABASE postapi_security TO muctepkot;

CREATE TABLE IF NOT EXISTS users
(
  id SERIAL,
  user_name varchar(20) NOT NULL UNIQUE,
  password varchar(200) NOT NULL,
  token varchar(200) NOT NULL,
  time integer NOT NULL
 );

INSERT INTO users(id, user_name, password, token, time)
VALUES (1,'admin', 'admin_password', 'admin_token', 1234567);

GRANT ALL PRIVILEGES ON TABLE users TO muctepkot;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO muctepkot