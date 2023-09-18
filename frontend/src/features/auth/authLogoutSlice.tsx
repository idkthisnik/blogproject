import { apiSlice } from "../../api/apiSlice"

export const authApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        logout: builder.mutation({
            query: credentials => {
                return {
                    url: '/logout',
                    method: 'POST',
                    body: { ...credentials },
                    credentials: 'include'
                };
            }
        }),
    })
});

export const {
    useLogoutMutation
} = authApiSlice