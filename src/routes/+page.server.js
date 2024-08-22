
import { supabase } from "$lib/supabaseClient";

export async function load() {
  const { data } = await supabase.from("test_data").select();
  return {
    items: data ?? [],
  };
}
