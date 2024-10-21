import { axiosClient } from "@/config/axios-client";

export async function getVideoLinks() {
  const response = await axiosClient.get("/video/all");
  return response;
}

export async function createVideoLink(data: {
  video_link: string;
  schedule: boolean;
  tag: string;
  start_time: string;
  end_time: string;
}) {
  const response = await axiosClient.post("/video/create", data);
  return response;
}

export async function deleteVideoLink(id: string) {
  const response = await axiosClient.delete(`/video/${id}`);
  return response;
}

export async function updateVideoLink({ id, data }: { id: string; data: any }) {
  const response = await axiosClient.put(`/video/${id}`, data);
  return response;
}

export async function getVideoLink(id: string) {
  const response = await axiosClient.get(`/video/${id}`);
  return response;
}
