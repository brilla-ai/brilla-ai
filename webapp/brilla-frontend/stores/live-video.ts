import { create, StateCreator } from "zustand";
import { persist } from "zustand/middleware";

type State = {
  liveVideo: string;
  videoLinks: Video[];
};

export type Video = {
  id: number;
  link: string;
  status: string;
  schedule_date: string;
  schedule_time: string;
  tags: string;
};

type Actions = {
  /** reset store to initial state */
  reset: () => void;
  setLiveVideo: (liveVideo: string) => void;
  setVideo: (video: Video) => void;
  removeVideo: (id: number) => void;
  changeVideoStatus: (id: number, status: string) => void;
  editVideo: (video: Video) => void;
};

const initialState: State = {
  liveVideo: "",
  videoLinks: [],
};

const videoStore: StateCreator<State & Actions> = (set, get) => ({
  ...initialState,
  reset: () => set(initialState),
  setLiveVideo: (liveVideo) => set({ liveVideo }),
  setVideo: (video) => set({ videoLinks: [...get().videoLinks, video] }),
  removeVideo: (id) => {
    const videoLinks = get().videoLinks.filter((video) => video.id !== id);
    set({ videoLinks });
  },
  changeVideoStatus: (id: number, status: string) => {
    const videoLinks = get().videoLinks.map((video) =>
      video.id === id ? { ...video, status } : video
    );
    set({ videoLinks });
  },
  editVideo: (video: Video) => {
    const videoLinks = get().videoLinks.map((v) => (v.id === video.id ? video : v));
    set({ videoLinks });
  },
});

const useVideosStore = create(
  persist(videoStore, { name: "brillaai-live-video-store" })
);

export { useVideosStore };
