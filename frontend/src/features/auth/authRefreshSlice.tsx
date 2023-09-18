import { apiSlice } from "../../api/apiSlice"

export const authApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        refresh: builder.mutation({
            query: credentials => {
                return {
                    url: '/refresh',
                    method: 'POST',
                    body: { ...credentials },
                    credentials: 'include'
                };
            }
        }),
    })
});

export const {
    useRefreshMutation
} = authApiSlice