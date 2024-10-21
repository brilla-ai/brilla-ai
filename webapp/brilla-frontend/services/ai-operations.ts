import { axiosClient } from "@/config/axios-client";

export function startProcessingAudio() {
  const response = axiosClient.get("/operations/start-audio-processing");
  return response;
}

export function updateAiOperations(data: {
  id: string;
  data: {
    stage_round: string;
    start_audio_processing: boolean;
  };
}) {
  return axiosClient.put(`/operations/operation/${data.id}`, data.data);
}

export function getAiOperations() {
  const response = axiosClient.get("/operations/operation");
  return response;
}
