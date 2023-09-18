import { createSlice } from "@reduxjs/toolkit"
import { RootState } from "../../store"

const authSlice = createSlice({
    name: 'auth',
    initialState: { userId: null, token: null },
    reducers: {
        setCredentials: (state, action) => {
            const { userId, accessToken } = action.payload
            state.userId = userId
            state.token = accessToken
        },
        logOut: (state, action) => {
            state.userId = null
            state.token = null
        }
    },
})

export const { setCredentials, logOut } = authSlice.actions

export default authSlice.reducer

export const selectCurrentUser = (state: RootState) => state.auth.userId
export const selectCurrentToken = (state: RootState) => state.auth.token
export const selectTokenExists = (state: RootState) => !!state.auth.token