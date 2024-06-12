// import { createClient } from '@supabase/supabase-js'

// export const supabase = createClient('https://https://cflncektpegrccomneqc.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNmbG5jZWt0cGVncmNjb21uZXFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYzODg3MzQsImV4cCI6MjAzMTk2NDczNH0.YaNGZ3fjFKoGC48PXEpLCZZTjuH10OZqgxgxXKO8le8')

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://cflncektpegrccomneqc.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNmbG5jZWt0cGVncmNjb21uZXFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYzODg3MzQsImV4cCI6MjAzMTk2NDczNH0.YaNGZ3fjFKoGC48PXEpLCZZTjuH10OZqgxgxXKO8le8';

export const supabase = createClient(supabaseUrl, supabaseKey);
