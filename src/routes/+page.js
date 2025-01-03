import {load} from '$lib/api/pantry.js'

export async function _getBanner(){
    const data = await load()
    return data['banner']
}