import {
  getVideoLinks,
  createVideoLink,
  deleteVideoLink,
  updateVideoLink,
} from "@/services/videolinks";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export function useVideoLinks() {
  return useQuery({
    queryKey: ["video-links"],
    queryFn: getVideoLinks,
  });
}

export function useVideoLinkMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createVideoLink,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["video-links"] });
    },
  });
}

export function useDeleteVideoLinkMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteVideoLink,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["video-links"] });
    },
  });
}

export function useUpdateVideoLinkMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateVideoLink,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["video-links"] });
    },
  });
}
