import { NavLink } from "react-router-dom";
import type { NavItem } from "./navItems";

export default function SidebarLink({ label, to, icon: Icon }: NavItem) {
    return (
        <NavLink
        to={to}
        className={({ isActive }) =>
                [
                    'flex h-12 items-center gap-3 rounded-lg px-4 text-sm font-medium',
                    isActive
                    ? 'border-2 border-primary bg-surface-container text-primary'
                    : 'text-on-surface hover:bg-surface-container-highest',
                ].join(' ')
            }
        >
        {({ isActive }) => (
            <>
                <Icon
                    size={24}
                    className={isActive? 'text-primary' : 'text-on-surface-variant'}
                />
                {label}
            </>
        )}
        </NavLink>
    )
}