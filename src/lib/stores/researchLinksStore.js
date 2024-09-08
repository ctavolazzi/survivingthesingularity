// researchLinksStore.js
import { writable } from 'svelte/store';
import { supabase } from '$lib/utils/supabaseClient';

function createResearchLinksStore() {
    const { subscribe, set, update } = writable({
        links: [],
        isLoading: false,
        error: null,
        searchTerm: ''
    });

    async function fetchLinks(search = '') {
        update(state => ({ ...state, isLoading: true, error: null }));
        try {
            let query = supabase
                .from('research_links')
                .select('*')
                .order('added_at', { ascending: false });

            if (search) {
                query = query.or(`title.ilike.%${search}%,description.ilike.%${search}%,url.ilike.%${search}%`);
            }

            const { data, error: supabaseError } = await query;
            if (supabaseError) throw supabaseError;
            
            update(state => ({ 
                ...state, 
                links: data, 
                isLoading: false 
            }));
        } catch (error) {
            console.error('Error fetching research links:', error);
            update(state => ({ ...state, error: error.message, isLoading: false }));
        }
    }

    function setSearchTerm(term) {
        update(state => ({ ...state, searchTerm: term }));
        fetchLinks(term);
    }

    return {
        subscribe,
        fetchLinks,
        setSearchTerm
    };
}

export const researchLinksStore = createResearchLinksStore();