import { createContext, useContext, useState, useCallback } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useLocalStorage('rl_user', null);
    const [isLoading, setIsLoading] = useState(false);

    const login = useCallback(async (email, password) => {
        setIsLoading(true);
        // Mock login — simulate API delay
        await new Promise((resolve) => setTimeout(resolve, 800));
        const mockUser = {
            id: '1',
            name: email.split('@')[0],
            email,
            avatar: null,
        };
        setUser(mockUser);
        setIsLoading(false);
        return mockUser;
    }, [setUser]);

    const signup = useCallback(async (name, email, password) => {
        setIsLoading(true);
        await new Promise((resolve) => setTimeout(resolve, 800));
        const mockUser = {
            id: '1',
            name,
            email,
            avatar: null,
        };
        setUser(mockUser);
        setIsLoading(false);
        return mockUser;
    }, [setUser]);

    const logout = useCallback(() => {
        setUser(null);
    }, [setUser]);

    return (
        <AuthContext.Provider value={{ user, isLoading, login, signup, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
