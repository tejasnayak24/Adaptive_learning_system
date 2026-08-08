import { createContext, useContext, useEffect, useState } from "react";
import authService from "../services/authService";
import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
	const [user, setUser] = useState(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		// try to load profile if token exists
		const token = api.getAuthToken();
		if (!token) {
			setLoading(false);
			return;
		}

		let mounted = true;
		authService
			.getProfile()
			.then((res) => {
				const profile = res?.data ?? null;
				if (mounted) setUser(profile ? { ...profile, id: profile.id ?? Number(profile.sub || profile.sub) } : null);
			})
			.catch(() => {
				authService.logout();
			})
			.finally(() => mounted && setLoading(false));

		return () => (mounted = false);
	}, []);

	const login = async (email, password) => {
		const token = await authService.login(email, password);
		// refresh profile
		const profile = await authService.getProfile();
		const data = profile?.data ?? null;
		setUser(data ? { ...data, id: data.id ?? Number(data.sub || data.sub) } : null);
		return token;
	};

	const register = async (name, email, password) => {
		const resp = await authService.register(name, email, password);
		return resp;
	};

	const logout = () => {
		authService.logout();
		setUser(null);
	};

	return (
		<AuthContext.Provider value={{ user, loading, login, register, logout }}>
			{children}
		</AuthContext.Provider>
	);
}

export function useAuth() {
	return useContext(AuthContext);
}

export default AuthContext;
