import { createClient } from '@supabase/supabase-js';

const PUBLIC_SUPABASE_URL = "https://cflncektpegrccomneqc.supabase.co";
const PUBLIC_SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNmbG5jZWt0cGVncmNjb21uZXFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYzODg3MzQsImV4cCI6MjAzMTk2NDczNH0.YaNGZ3fjFKoGC48PXEpLCZZTjuH10OZqgxgxXKO8le8";
const supabase = createClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY);

export { supabase as s };
//# sourceMappingURL=supabaseClient-DNeOHnRL.js.map
