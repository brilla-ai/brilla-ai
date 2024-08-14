import { create, StateCreator } from "zustand";
import { persist } from "zustand/middleware";

type State = {
  token?: string | null;
  user?: User | null;
  role: (Partial<Role> & { permissions: RemotePermissions }) | null;
  isAuthenticated: boolean;
  redirect?: string;
  authType: AuthType | null;
  country?: string;
  loginUrl: string;
  kycUpdates?: KycUpdates | null;
};

type Actions = {
  /** reset auth store to initial state */
  reset: () => void;
  /**
   * authenticate user
   * @param {Object} details - object containing user object and token
   */
  authenticate: (details: {
    user: User;
    token: string;
    authType: AuthType;
    loginUrl?: string;
  }) => void;
  setRedirect: (redirect: string) => void;
  getToken: () => State["token"];
  setToken: (newToken: string) => void;
  setCountry: (newCountry: string) => void;
  setKycUpdates: (kycUpdates: KycUpdates) => void;
  setUser: (user: User) => void;
  setRole: (role: Partial<Role> & { permissions: RemotePermissions }) => void;
};

const initialState: State = {
  token: null,
  isAuthenticated: false,
  authType: null,
  user: null,
  loginUrl: "/auth/login",
  role: null,
};

const authStore: StateCreator<State & Actions> = (set, get) => ({
  ...initialState,
  country: "NG",
  reset: () => set(initialState),
  authenticate: ({ user, token, authType, loginUrl = "/auth/login" }) => {
    set({
      user,
      token,
      isAuthenticated: true,
      authType,
      loginUrl,
    });
  },
  setUser: (user) => set({ user }),
  setRole: (role) => set({ role }),
  setRedirect: (redirect: string) => set({ redirect }),
  getToken: () => get().token,
  setToken: (newToken: string) => set({ token: newToken }),
  setCountry: (newCountry: string) => set({ country: newCountry }),
  setKycUpdates: (kycUpdates: KycUpdates) => set({ kycUpdates }),
});

const useAuthStore = create(
  persist(authStore, { name: "carduvy-web-auth-store" })
);

export { useAuthStore };
