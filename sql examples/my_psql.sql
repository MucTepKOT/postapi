CREATE USER muctepkot WITH PASSWORD 'muctepkot';
DROP DATABASE IF EXISTS postapi_security;
CREATE DATABASE postapi_security;
ALTER DATABASE postapi_security OWNER TO muctepkot;
GRANT ALL PRIVILEGES ON DATABASE postapi_security TO muctepkot;

CREATE TABLE IF NOT EXISTS users
(
  id SERIAL,
  user_name varchar(20) NOT NULL UNIQUE,
  password varchar(50) NOT NULL,
  token varchar(200) NOT NULL,
  disabled boolean NOT NULL DEFAULT false
 );

INSERT INTO users(id, user_name, password, token, disabled)
VALUES ('1','admin', 'admin_password', 'admin_token', FALSE);

GRANT ALL PRIVILEGES ON TABLE users TO muctepkot;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO muctepkot