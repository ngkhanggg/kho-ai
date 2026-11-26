import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Link } from "react-router-dom";

export default function SignUnPage() {
    const [showPassword, setShowPassword] = useState(false);
    const [showCPassword, setShowCPassword] = useState(false);
    
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
        margin: "1rem 0rem"
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
                    <form action="" className="flex flex-col h-full justify-around  w-full">
                        <div className="flex flex-col gap-1">
                            <label htmlFor="username" className="font-bold text-lg">Username</label>
                            <input 
                                id="form-username"
                                type="text"
                                placeholder="demo_username"
                                style={inputStyles}
                            />
                        </div>
                        
                        <div className="flex flex-col gap-1">
                            <label htmlFor="shopname" className="font-bold text-lg">Shop Name</label>
                            <input 
                                id="form-shopname"
                                type="text"
                                placeholder="demo_shopename"
                                className=""
                                style={inputStyles}
                            />
                        </div>

                        <div className="flex flex-col gap-1">
                            <label htmlFor="email" className="font-bold text-lg">Email</label>
                            <input 
                                id="form-email"
                                type="email"
                                placeholder="demo_email"
                                className=""
                                style={inputStyles}
                            />
                        </div>

                        {/* Password */}
                        <div className="flex flex-col gap-1">
                                <label htmlFor="form-password" className="font-bold text-lg">Password</label>                                <div className="relative">
                                <input 
                                    id="form-password"
                                    type={showPassword ? "text" : "password"}
                                    className="cursor-pointer "
                                    defaultValue="Sigma123@"
                                    style={{ ...inputStyles, paddingRight: "3.5rem" }}
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword((prev) => !prev)}
                                    aria-label={showPassword ? "Hide password" : "Show password"}
                                    className="absolute right-4 top-1/2 -translate-y-1/2"
                                >
                                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                                </button>
                            </div>
                        </div>

                        <div className="flex flex-col gap-1">
                                <label htmlFor="form-password" className="font-bold text-lg">Password</label>                                <div className="relative">
                                <input 
                                    id="form-password"
                                    type={showCPassword ? "text" : "password"}
                                    className="cursor-pointer "
                                    placeholder="Password"
                                    style={{ ...inputStyles, paddingRight: "3.5rem" }}
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowCPassword((prev) => !prev)}
                                    aria-label={showCPassword ? "Hide password" : "Show password"}
                                    className="absolute right-4 top-1/2 -translate-y-1/2"
                                >
                                    {showCPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                                </button>
                            </div>
                        </div>

                        <button style={buttonStyles} className="self-center">Sign up</button>
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
