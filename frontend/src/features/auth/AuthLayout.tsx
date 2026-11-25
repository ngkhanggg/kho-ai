import { Outlet } from "react-router-dom";
import "../../styles.css"

export default function AuthLayout() {
    const backGroundStyles = {
        backgroundColor: "var(--color-secondary-container)",
        minHeight: "100vh",
        padding: "5rem 2rem",
        display: "flex",
    }

    return(
        <>
            <main style={backGroundStyles}>
                <div className="flex-1 bg-white border rounded-xl">
                    <Outlet />
                </div>
            </main>
        </>
    )
}