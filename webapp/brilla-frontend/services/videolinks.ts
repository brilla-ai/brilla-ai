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
