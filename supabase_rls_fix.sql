-- PostgreSQL 15+ Fix: Grant schema permissions
-- This is required because PostgreSQL 15 revoked CREATE permission from public schema by default

-- Grant all privileges on the public schema to anon and authenticated roles
GRANT ALL ON SCHEMA public TO anon;
GRANT ALL ON SCHEMA public TO authenticated;
GRANT ALL ON SCHEMA public TO service_role;

-- Grant all privileges on all tables in public schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO anon;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO service_role;

-- Grant all privileges on all sequences (for auto-incrementing IDs)
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO authenticated;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO service_role;

-- Make sure future tables also get these permissions
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO service_role;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO service_role;

-- Now also handle RLS policies if needed
-- Option 1: Disable RLS for todos table (simplest for development)
ALTER TABLE todos DISABLE ROW LEVEL SECURITY;

-- Option 2: Or create permissive RLS policies (better for production)
-- Uncomment these if you want to keep RLS enabled:
/*
DROP POLICY IF EXISTS "Allow all todo operations" ON todos;
CREATE POLICY "Allow all todo operations" ON todos
FOR ALL
TO anon, authenticated, service_role
USING (true)
WITH CHECK (true);
*/
