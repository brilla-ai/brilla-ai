import { getVideoLinks, createVideoLink } from "@/services/videolinks";

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
