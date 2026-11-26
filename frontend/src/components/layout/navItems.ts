import type { LucideIcon } from "lucide-react"
import {
    BellRing,
    Boxes,
    DollarSign,
    LayoutDashboard,
    Package,
    Star,
    User
} from "lucide-react"

export type NavItem = {
    label: string
    to: string
    icon: LucideIcon
}

// Main Menu of the sidebar
export const mainNav: NavItem[] = [
    { label: 'Dashboard', to: '/dashboard', icon: LayoutDashboard},
    { label: 'Recommendation', to: '/recommendation', icon: Star},
    { label: 'Products', to: '/products', icon: Package},
    { label: 'Inventory', to: '/inventory', icon: Boxes},
    { label: 'Sales', to: '/sales', icon: DollarSign}
]

// Bottom section of the sidebar
export const bottomNav: NavItem[] = [
    { label: 'Account', to: '/account', icon: User},
    { label: 'Notifications', to: '/notifications', icon: BellRing}
]