import { useLocation, Navigate, Outlet } from "react-router-dom"
import { useSelector } from "react-redux"
import { selectTokenExists } from "./authSlice"

const RequireNotAuth = () => {
    const tokenexist = useSelector(selectTokenExists)
    const location = useLocation()
    
    return (
        tokenexist
            ? <Navigate to="/homepage" state={{ from: location }} replace />
            : <Outlet />
    )
}
export default RequireNotAuth