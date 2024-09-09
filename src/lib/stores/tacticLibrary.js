import { writable } from 'svelte/store';
import { supabase } from '$lib/utils/supabaseClient';

function createTacticLibrary() {
    const { subscribe, set, update } = writable([]);

    return {
        subscribe,
        fetchTactics: async () => {
            const { data, error } = await supabase
                .from('tactics')
                .select('*')
                .eq('status', 'published')
                .order('created_at', { ascending: false });

            if (error) {
                console.error('Error fetching tactics:', error);
                return;
            }

            set(data);
        },
        fetchTactic: async (id) => {
            const { data, error } = await supabase
                .from('tactics')
                .select('*')
                .eq('id', id);

            if (error) {
                console.error('Error fetching tactic:', error);
                return;
            }
            return data[0];
        }       
    };  
}

export const tacticLibrary = createTacticLibrary();