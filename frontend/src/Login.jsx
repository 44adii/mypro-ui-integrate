import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Scale, Phone, Mail } from 'lucide-react';

export default function Login() {
    const [isPhoneLogin, setIsPhoneLogin] = useState(false);
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();
        // Allow login if EITHER (Email+Password) OR (Phone+Password) is provided
        if ((email || phone) && password) {
            // Mock Auth: Save token to localStorage
            localStorage.setItem('user_token', 'mock_token_123');
            navigate('/dashboard');
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-900 p-4 font-sans text-gray-100">
            <div className="w-full max-w-md rounded-xl bg-gray-800 p-8 shadow-2xl border border-gray-700">
                <div className="mb-8 text-center">
                    <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-indigo-600 shadow-lg shadow-indigo-500/30">
                        <Scale className="h-8 w-8 text-white" />
                    </div>
                    <h1 className="text-3xl font-bold tracking-tight text-white">NyayaGPT</h1>
                    <p className="mt-2 text-sm text-gray-400">Your AI Legal Companion</p>
                </div>

                <div className="flex justify-center mb-6">
                    <div className="bg-gray-700/50 p-1 rounded-lg flex space-x-2">
                        <button
                            onClick={() => setIsPhoneLogin(false)}
                            className={`px-4 py-2 rounded-md text-sm font-medium transition ${!isPhoneLogin ? 'bg-indigo-600 text-white shadow-md' : 'text-gray-400 hover:text-white'}`}
                        >
                            Email
                        </button>
                        <button
                            onClick={() => setIsPhoneLogin(true)}
                            className={`px-4 py-2 rounded-md text-sm font-medium transition ${isPhoneLogin ? 'bg-indigo-600 text-white shadow-md' : 'text-gray-400 hover:text-white'}`}
                        >
                            Phone
                        </button>
                    </div>
                </div>

                <form onSubmit={handleLogin} className="space-y-6">
                    {isPhoneLogin ? (
                        <div>
                            <label className="mb-2 block text-sm font-medium text-gray-300">Phone Number</label>
                            <div className="relative">
                                <input
                                    type="tel"
                                    value={phone}
                                    onChange={(e) => setPhone(e.target.value)}
                                    className="w-full rounded-lg border border-gray-600 bg-gray-700/50 p-3 pl-10 text-white placeholder-gray-500 transition focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                                    placeholder="+91 98765 43210"
                                    required={isPhoneLogin}
                                />
                                <Phone className="absolute left-3 top-3.5 h-5 w-5 text-gray-500" />
                            </div>
                        </div>
                    ) : (
                        <div>
                            <label className="mb-2 block text-sm font-medium text-gray-300">Email Address</label>
                            <div className="relative">
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full rounded-lg border border-gray-600 bg-gray-700/50 p-3 pl-10 text-white placeholder-gray-500 transition focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                                    placeholder="lawyer@example.com"
                                    required={!isPhoneLogin}
                                />
                                <Mail className="absolute left-3 top-3.5 h-5 w-5 text-gray-500" />
                            </div>
                        </div>
                    )}

                    <div>
                        <label className="mb-2 block text-sm font-medium text-gray-300">Password</label>
                        <div className="relative">
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full rounded-lg border border-gray-600 bg-gray-700/50 p-3 pl-10 text-white placeholder-gray-500 transition focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                                placeholder="••••••••"
                                required
                            />
                            <Lock className="absolute left-3 top-3.5 h-5 w-5 text-gray-500" />
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="w-full rounded-lg bg-indigo-600 py-3 font-semibold text-white shadow-lg transition hover:bg-indigo-500 hover:shadow-indigo-500/25 active:scale-[0.98]"
                    >
                        {isPhoneLogin ? 'Sign In with Phone' : 'Sign In with Email'}
                    </button>
                </form>

                <div className="mt-6 text-center text-xs text-gray-500">
                    By signing in, you agree to our <span className="cursor-pointer text-indigo-400 hover:underline">Terms</span> and <span className="cursor-pointer text-indigo-400 hover:underline">Privacy Policy</span>.
                </div>
            </div>
        </div>
    );
}
