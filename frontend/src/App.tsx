import { Navigate, Route, Routes } from "react-router-dom";
import AppLayout from "./components/layout/AppLayout";
import PlaceholderPage from "./components/PlaceholderPage";

export default function App() {
    return (
        <Routes>
            {/* Pages without the sidebar */}
            <Route element={<AppLayout />}>
                <Route path="/dashboard" element={<PlaceholderPage title="Dashboard" />}></Route>
                <Route path="/recommendation" element={<PlaceholderPage title="Recommendations" />}></Route>
                <Route path="/products" element={<PlaceholderPage title="Products" />}></Route>
                <Route path="/inventory" element={<PlaceholderPage title="Inventory" />}></Route>
                <Route path="/sales" element={<PlaceholderPage title="Sales" />}></Route>
                <Route path="/account" element={<PlaceholderPage title="Account" />}></Route>
                <Route path="/notifications" element={<PlaceholderPage title="Notifications" />}></Route>
            </Route>
            
            <Route path="/" element={<Navigate to="/dashboard" />}></Route>
        </Routes>
    )
}