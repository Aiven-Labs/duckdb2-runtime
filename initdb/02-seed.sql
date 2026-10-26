CREATE TABLE IF NOT EXISTS users (
  id serial PRIMARY KEY,
  name text NOT NULL,
  email text UNIQUE NOT NULL,
  country text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS orders (
  id serial PRIMARY KEY,
  user_id int REFERENCES users(id),
  product text NOT NULL,
  quantity int NOT NULL,
  unit_price numeric(10,2) NOT NULL,
  ordered_at timestamptz NOT NULL
);

INSERT INTO users (name, email, country)
SELECT 'User ' || g, 'user' || g || '@example.com',
       (ARRAY['US','CA','DE','FI','JP','BR'])[1 + g % 6]
FROM generate_series(1, 50) g
ON CONFLICT DO NOTHING;

INSERT INTO orders (user_id, product, quantity, unit_price, ordered_at)
SELECT 1 + g % 50,
       (ARRAY['widget','gadget','gizmo','doohickey'])[1 + g % 4],
       1 + g % 5,
       round((5 + (g * 7) % 95)::numeric, 2),
       now() - (g || ' hours')::interval
FROM generate_series(1, 1000) g;
