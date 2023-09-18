import { useLocation, Navigate, Outlet } from "react-router-dom"
import { useSelector } from "react-redux"
import { selectTokenExists } from "./authSlice"

const RequireAuth = () => {
    const tokenexist = useSelector(selectTokenExists)
    const location = useLocation()

    return (
        tokenexist
            ? <Outlet />
            : <Navigate to="/login" state={{ from: location }} replace />
    )
}
export default RequireAuth