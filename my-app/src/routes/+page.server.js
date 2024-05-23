// /Users/ctavolazzi/Code/survivingthesingularity/my-app/src/routes/+page.server.js
import { supabase } from "$lib/supabaseClient";

export async function load() {
  const { data, error } = await supabase.from("countries").select();

  if (error) {
    console.error('Error fetching countries:', error);
    return {
      countries: [],
      error: error.message,
    };
  }
  console.log(data);

  return {
    countries: data ?? [],
  };
}
