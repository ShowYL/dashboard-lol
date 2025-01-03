
export async function load(){
    const PANTRY_API_KEY = import.meta.env.VITE_PANTRY_API_KEY;
    if (!PANTRY_API_KEY) {
        return json({ error: 'Missing API key' }, { status: 500 });
    }

    try {
        const response = await fetch(`https://getpantry.cloud/apiv1/pantry/${PANTRY_API_KEY}/basket/Changes`)
        const data = await response;
        return data.json();
    } catch (err) {
        return json({ error: 'Error fetching data' }, { status: 500 });
    }
}