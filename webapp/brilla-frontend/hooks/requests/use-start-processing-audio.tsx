import {
  getAiOperations,
  startProcessingAudio,
  updateAiOperations,
} from "@/services/ai-operations";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export function useStartProcessingAudioQuery() {
  return useQuery({
    queryKey: ["start-processing-audio"],
    queryFn: startProcessingAudio,
    enabled: false,
  });
}

export function useUpdateAiOperationsMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateAiOperations,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ai-operations"] });
    },
  });
}

export function useGetAiOperationsQuery() {
  const httpQuery = useQuery({
    queryKey: ["ai-operations"],
    queryFn: getAiOperations,
    select: (data) => data.data,
  });
  return {
    ...httpQuery,
    isProcessing: httpQuery.data?.start_audio_processing,
    stageRound: httpQuery.data?.stage_round,
  };
}
