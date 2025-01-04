import { VITE_PANTRY_API_KEY } from "$env/static/private";

export async function fetchData(){
    try{
        const response = await fetch(`https://getpantry.cloud/apiv1/pantry/${VITE_PANTRY_API_KEY}/basket/Changes`);
        if(!response.ok){
            throw new Error("Error fetching data");
        }
        return response.json();
    }catch(err){
        console.error(`There was a problem with the fetching`,err);
    }
}