export default function SignInPage() {
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
                    <h1 className="font-bold text-5xl">Sign In</h1>
                    <div className="text-base">Welcome to KhoAI!</div>
                </div>
                {/* Bottom Left */}
                <div className="flex flex-col flex-5 items-center px-16 min-w-150">
                    <form action="" className="flex flex-col h-full  w-full gap-6">
                        <div className="flex flex-col gap-1">
                            <label htmlFor="email" className="font-bold text-lg">Email</label>
                            <input 
                                id="form-email"
                                type="email"
                                placeholder="demo_email@gmail.com"
                                className=""
                                style={inputStyles}
                            />
                        </div>

                        {/* Password */}
                        <div className="flex flex-col gap-1">
                            <label htmlFor="password" className="font-bold text-lg">Password</label>
                            <input 
                                id="form-password"
                                type="password"
                                className=""
                                value="Sigma123@"
                                style={inputStyles}
                            />
                        </div>

                        <button style={buttonStyles} className="self-center">Sign up</button>
                        <div className="text-center">Already have an account? Sign in <span style={{color: "var(--color-primary)"}}>here.</span></div>
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