import React from 'react'
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { setCredentials, logOut } from '../features/auth/authSlice'
import { RootState } from '../store'


const baseQuery = fetchBaseQuery({
    baseUrl: process.env.REACT_APP_BACKEND_ADRESS,
    credentials: 'include',
    prepareHeaders: (headers, { getState }) => {
        const token = (getState() as RootState).auth.token
        if (token) {
            headers.set("authorization", `Bearer ${token}`)
        }
        return headers;
    }
})


export const apiSlice = createApi({
    baseQuery: baseQuery,
    endpoints: (builder) => ({
    }),
  });