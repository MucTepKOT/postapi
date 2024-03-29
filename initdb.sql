CREATE USER muctepkot WITH PASSWORD 'muctepkot';
DROP DATABASE IF EXISTS postapi_security;
CREATE DATABASE postapi_security;
ALTER DATABASE postapi_security OWNER TO muctepkot;
GRANT ALL PRIVILEGES ON DATABASE postapi_security TO muctepkot;
GRANT ALL PRIVILEGES ON TABLE users TO muctepkot;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO muctepkot