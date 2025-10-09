-- Fix todos table for VAPI integration
-- Remove the foreign key constraint that requires user_id to exist in auth.users
-- This allows us to use generated UUIDs from phone numbers

ALTER TABLE todos DROP CONSTRAINT IF EXISTS todos_user_id_fkey;

-- Now the table will accept any UUID as user_id
-- Same phone number will always map to the same UUID

-- Verify the change
SELECT 
    constraint_name, 
    constraint_type 
FROM information_schema.table_constraints 
WHERE table_name = 'todos';
