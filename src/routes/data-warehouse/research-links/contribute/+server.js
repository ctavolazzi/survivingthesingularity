import { json } from '@sveltejs/kit';
import { supabase } from '$lib/utils/supabaseClient';

export async function POST({ request }) {
    const { url, title, author, description, tags, notes, date_of_publication } = await request.json();

    try {
        const { data, error } = await supabase
            .from('research_links')
            .insert({ 
                url, 
                title, 
                author,  // New field
                description, 
                tags, 
                notes,
                date_of_publication
            });

        if (error) throw error;

        return json({ success: true });
    } catch (error) {
        console.error('Error adding link:', error);
        return json({ error: error.message }, { status: 500 });
    }
}