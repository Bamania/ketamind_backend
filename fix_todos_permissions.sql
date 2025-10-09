-- Fix permissions specifically for the todos table

-- First, make sure the schema permissions are set
GRANT USAGE ON SCHEMA public TO anon;
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT USAGE ON SCHEMA public TO service_role;

-- Grant all permissions on the todos table specifically
GRANT ALL PRIVILEGES ON TABLE public.todos TO anon;
GRANT ALL PRIVILEGES ON TABLE public.todos TO authenticated;
GRANT ALL PRIVILEGES ON TABLE public.todos TO service_role;

-- If todos table has a sequence (for id), grant permissions on it
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- Disable Row Level Security for development/testing
ALTER TABLE public.todos DISABLE ROW LEVEL SECURITY;

-- Verify the permissions
SELECT 
    grantee, 
    privilege_type 
FROM information_schema.role_table_grants 
WHERE table_name='todos';
