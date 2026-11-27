import { useState, type FormEvent } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { register } from "./authApi";
import { validateRegister } from "./validation";

export default function SignUpPage() {
    const navigate = useNavigate();

    const [showPassword, setShowPassword] = useState(false);
    const [showCPassword, setShowCPassword] = useState(false);

    const [fullName, setFullName] = useState("");
    const [shopName, setShopName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const inputStyles = {
        backgroundColor: "var(--color-surface-container-highest)",
        width: "100%",
        padding: "1rem ",
        borderRadius: "1rem",
    }

    const buttonStyles = {
        backgroundColor: "var(--color-primary)",
        color: "var(--color-white-text)",
        padding: "1rem 2rem",
        fontSize: "1.25rem",
        borderRadius: "1.25rem",
        margin: "1rem 0rem",
        opacity: loading ? 0.6 : 1,
    }

    async function handleSubmit(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();
        setError(null);

        const payload = {
            full_name: fullName.trim(),
            shop_name: shopName.trim(),
            email: email.trim(),
            password,
            confirm_password: confirmPassword,
        };

        const validationError = validateRegister(payload);
        if (validationError) {
            setError(validationError);
            return;
        }

        setLoading(true);
        try {
            await register(payload);
            alert("Account created successfully")
            navigate("/signin");
        } catch (err) {
            setError((err as Error).message);
        } finally {
            setLoading(false);
        }
    }

    return(
        <>
        <div className="flex justify-between h-full">
            {/* Left */}
            <div className="flex flex-col w-full h-full p-5 items-center">
                {/* Top Left */}
                <div className="flex flex-col flex-1 justify-between items-center gap-2">
                    <div className="w-20 h-20 bg-gray-300"></div>
                    <h1 className="font-bold text-5xl">Sign Up</h1>
                    <div className="text-base">Welcome to KhoAI - Let's create account</div>
                </div>
                {/* Bottom Left */}
                <div className="flex flex-col flex-5 items-center px-16 min-w-150">
                    <form onSubmit={handleSubmit} className="flex flex-col h-full justify-around  w-full">
                        <div className="flex flex-col gap-1">
                            <label htmlFor="form-fullname" className="font-bold text-lg">Full Name</label>
                            <input
                                id="form-fullname"
                                type="text"
                                placeholder="Nguyen Van A"
                                value={fullName}
                                onChange={(e) => setFullName(e.target.value)}
                                required
                                minLength={4}
                                maxLength={100}
                                style={inputStyles}
                            />
                        </div>

                        <div className="flex flex-col gap-1">
                            <label htmlFor="form-shopname" className="font-bold text-lg">Shop Name</label>
                            <input
                                id="form-shopname"
                                type="text"
                                placeholder="My Shop"
                                value={shopName}
                                onChange={(e) => setShopName(e.target.value)}
                                required
                                maxLength={100}
                                style={inputStyles}
                            />
                        </div>

                        <div className="flex flex-col gap-1">
                            <label htmlFor="form-email" className="font-bold text-lg">Email</label>
                            <input
                                id="form-email"
                                type="email"
                                placeholder="you@example.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                style={inputStyles}
                            />
                        </div>

                        {/* Password */}
                        <div className="flex flex-col gap-1">
                            <label htmlFor="form-password" className="font-bold text-lg">Password</label>
                            <div className="relative">
                                <input
                                    id="form-password"
                                    type={showPassword ? "text" : "password"}
                                    placeholder="At least 8 characters"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    minLength={8}
                                    maxLength={100}
                                    style={{ ...inputStyles, paddingRight: "3.5rem" }}
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword((prev) => !prev)}
                                    aria-label={showPassword ? "Hide password" : "Show password"}
                                    className="absolute right-4 top-1/2 -translate-y-1/2"
                                >
                                    {showPassword ? <Eye size={20} /> : <EyeOff size={20} />}
                                </button>
                            </div>
                        </div>

                        <div className="flex flex-col gap-1">
                            <label htmlFor="form-confirm-password" className="font-bold text-lg">Confirm Password</label>
                            <div className="relative">
                                <input
                                    id="form-confirm-password"
                                    type={showCPassword ? "text" : "password"}
                                    placeholder="Repeat your password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    required
                                    minLength={8}
                                    maxLength={100}
                                    style={{ ...inputStyles, paddingRight: "3.5rem" }}
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowCPassword((prev) => !prev)}
                                    aria-label={showCPassword ? "Hide password" : "Show password"}
                                    className="absolute right-4 top-1/2 -translate-y-1/2"
                                >
                                    {showCPassword ? <Eye size={20} /> : <EyeOff size={20} />}
                                </button>
                            </div>
                        </div>

                        {error && (
                            <div role="alert" className="text-center text-red-600">{error}</div>
                        )}

                        <button type="submit" disabled={loading} style={buttonStyles} className="self-center">
                            {loading ? "Creating account..." : "Sign up"}
                        </button>
                        <div className="text-center">Already have an account? Sign in <Link to="/signin" style={{color: "var(--color-primary)"}}>here.</Link></div>
                    </form>
                </div>
            </div>

            {/* Right */}
            <div className="w-full p-5">
                <div className="bg-gray-300 h-full w-full rounded-2xl"></div>
            </div>
        </div>
        </>
    )
}