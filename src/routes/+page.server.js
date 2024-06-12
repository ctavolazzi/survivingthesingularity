// /Users/ctavolazzi/Code/survivingthesingularity/my-app/src/routes/+page.server.js
import { supabase } from "$lib/supabaseClient";

export async function load() {
  const { data } = await supabase.from("countries").select();
  return {
    countries: data ?? [],
  };
}

