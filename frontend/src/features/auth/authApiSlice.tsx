import { apiSlice } from "../../api/apiSlice"

export const authApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        login: builder.mutation({
            query: credentials => {
                return {
                    url: '/login',
                    method: 'POST',
                    body: { ...credentials },
                    credentials: 'include'
                };
            }
        }),
    })
});

export const {
    useLoginMutation
} = authApiSlice