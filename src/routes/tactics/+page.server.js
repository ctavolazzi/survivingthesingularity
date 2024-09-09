import { supabase } from '$lib/utils/supabaseClient';

export async function load() {
    const { data, error } = await supabase
        .from('tactics')
        .select('id, title, summary, category, tags, status')
        .eq('status', 'published')
        .order('created_at', { ascending: false })

    if (error) {
        console.error('Error fetching tactics:', error)
        return {
            tactics: []
        }
    }

    return { tactics: data }
}
