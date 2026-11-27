import { LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";
import SidebarLink from "./SidebarLink";
import { bottomNav, mainNav } from "./navItems";
import { clearToken, getSession, logout } from "../../features/auth/authApi";
import { useEffect, useState } from "react";
import { SessionResponse } from "../../features/auth/types";

export default function Sidebar() {
    const navigate = useNavigate();
    const [sessionInfo, setSessionInfo] = useState<SessionResponse | null>(null);

    function handleLogOut() {
        // TODO: call POST /api/v1/auth/logout and delete the saved token
        logout();
        alert("logging out")
        navigate('/signin')
    }

    // If not logged in, not allow access to dashboard
    useEffect(() => {
        getSession()
            .then(setSessionInfo)
            .catch(() => {
                clearToken();
                alert("you are not logged in")
                navigate("/signin");
            });
    }, [navigate]);

    return (
        <aside className="sticky top-0 flex h-screen w-58 shrink-0 flex-col bg-surface-dim px-4 pb-6">
            {/* Logo + brand name */}
            <div className="flex h-20 items-end gap-4 border-b border-outline-variant px-4 pb-3">
                {/* Placeholder logo */}
                <div className="size-10 bg-on-surface"></div> 

                <div className="flex flex-col ">
                    <span className="text-lg font-bold text-primary">KhoAI</span>
                    <span className="text-xs ">{sessionInfo?.email}</span>
                </div>

            </div>

            {/* Main Menu */}
            <nav className="mt-12 flex flex-col gap-6">
                {mainNav.map((item) => (
                    <SidebarLink key={item.to} {...item} />
                ))}
            </nav>

            {/* Bottom menu */}
            <div className="mt-auto border-t border-outline-variant gap-6">
                {bottomNav.map((item) => (
                    <SidebarLink key={item.to} {...item} />
                ))}

                <button
                type="button"
                onClick={handleLogOut}
                className="flex h-12 w-full cursor-pointer items-center gap-3 rounded-xl px-4 text-sm font-medium text-error transition-colors hover:bg-error-container"
                >
                    <LogOut size={24} />
                    Log Out
                </button>
            </div>
        </aside>
    )
}
