import { createClient } from '@supabase/supabase-js';
import { SUPABASE_URL, SUPABASE_SERVICE_KEY } from '$env/static/private';

// This file is only imported server-side
export const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);