import { apiSlice } from "../../api/apiSlice"

export const authApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        registration: builder.mutation({
            query: credentials => {
                return {
                    url: '/registration',
                    method: 'POST',
                    body: { ...credentials },
                    credentials: 'include'
                };
            }
        }),
    })
});

export const {
    useRegistrationMutation
} = authApiSlice