import { User } from "@/types";
import { create, StateCreator } from "zustand";
import { persist } from "zustand/middleware";

type State = {
  token?: string | null;
  user?: User | null;
};

type Actions = {
  /** reset auth store to initial state */
  reset: () => void;
  /**
   * authenticate user
   * @param {Object} details - object containing user object and token
   */
  authenticate: (details: { user: User; token: string }) => void;
  getToken: () => State["token"];
  setToken: (newToken: string) => void;
  setUser: (user: User) => void;
};

const initialState: State = {
  token: null,
  user: null,
};

const authStore: StateCreator<State & Actions> = (set, get) => ({
  ...initialState,
  reset: () => set({ ...initialState }),
  authenticate: ({ user, token }) => {
    set({
      user,
      token,
    });
  },
  setUser: (user) => set({ user }),
  getToken: () => get().token,
  setToken: (newToken: string) => set({ token: newToken }),
});

const useAuthStore = create(
  persist(authStore, { name: "brillaai-auth-store" })
);

export { useAuthStore };
