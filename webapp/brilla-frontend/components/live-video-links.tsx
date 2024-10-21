"use client";
import { DotsVerticalIcon } from "@radix-ui/react-icons";
import { ActionDropdown } from "./ui/action-dropdown-menu";
import { Modal } from "./ui/modal";
import React from "react";
import { DialogClose } from "./ui/dialog";
import { Button } from "./ui/button";
import LiveVideoUrlForm from "./live-video-url-form";
import {
  useDeleteVideoLinkMutation,
  useVideoLinks,
} from "@/hooks/requests/use-video-links";
import {
  AIOperationsEventProps,
  LiveVideoLinksEventProps,
  Video,
} from "@/types";
import { formatDate } from "@/utils/helpers";
import { cn } from "@/lib/utils";
import { STATUS_CLASSES } from "@/utils/constants";

const LiveVideoLinks = ({ lastJsonMessage }: LiveVideoLinksEventProps) => {
  const [videos, setVideos] = React.useState<Video[]>([]);

  React.useEffect(() => {
    if (lastJsonMessage) {
      if (lastJsonMessage.videos) {
        console.log(
          "lastJsonMessage",
          lastJsonMessage.ai_operations.stage_round
        );
        setVideos(lastJsonMessage.videos);
      }

      if (lastJsonMessage.target === "update_video") {
        const newVideo = lastJsonMessage.arguments.data;
        const videoIndex = videos.findIndex(
          (video) => video.id === newVideo.id
        );
        console.log("videoIndex", videoIndex);
        if (videoIndex !== -1) {
          videos[videoIndex] = newVideo;
          setVideos([...videos]);
        }
      }
    }
  }, [lastJsonMessage]);

  return (
    <>
      <div className="border border-[#ADB5BD] rounded py-4 px-7 max-w-[604px] w-full h-max">
        <div className="grid lg:grid-cols-2">
          <p className="text-lg text-[#0F172A] font-semibold">
            Live Video Links
          </p>
          <p className="text-lg text-[#0F172A] font-semibold">Status</p>
        </div>
        <div className="grid gap-8 mt-8">
          {videos.map((video: Video) => {
            return (
              <div key={video.id} className="grid lg:grid-cols-2">
                <p>{video.tag}</p>
                <div className="flex justify-between">
                  <div className="flex flex-col gap-1">
                    <p
                      className={cn(
                        STATUS_CLASSES[
                          video.status as keyof typeof STATUS_CLASSES
                        ],
                        "capitalize border p-2 rounded-lg max-w-fit px-4"
                      )}
                    >
                      {video.status}
                    </p>
                    <p>
                      {formatDate(video.start_time, "MMM DD, YYYY | HH:mm A")}
                    </p>
                  </div>
                  {/* <p>{video.end_time ? formatDate(video.end_time) : ""}</p> */}
                  <ActionCell video={video} />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
};

export default LiveVideoLinks;

const ActionCell = ({ video }: { video: any }) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const [isStopLiveModalOpen, setIsStopLiveModalOpen] = React.useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = React.useState(false);
  const [videoToEdit, setVideoToEdit] = React.useState<
    Video | null | undefined
  >(null);

  // const { setLiveVideo, removeVideo } = useVideosStore();
  const { mutateAsync: deleteVideoLink } = useDeleteVideoLinkMutation();
  // const { sendMessage } = useWebSocket("ws://localhost:8000/links");

  const sharedAction = [
    {
      action: "Delete",
      onClickFn: () => setIsOpen(true),
    },
  ];
  const liveActions = [
    {
      action: "Stop",
      onClickFn: () => setIsStopLiveModalOpen(true),
    },
    ...sharedAction,
  ];

  const scheduledActions = [
    {
      action: "Edit",
      onClickFn: () => {
        setVideoToEdit(video);
        setIsEditModalOpen(true);
      },
    },
    ...sharedAction,
  ];

  const handleDeleteVideo = async () => {
    // sendMessage(`delete:${video.id}`);
    await deleteVideoLink(video.id);
    if (isOpen) setIsOpen(false);
  };

  const handleStopLiveVideo = () => {
    // setLiveVideo("");
    // removeVideo(video.id);
    if (isStopLiveModalOpen) setIsStopLiveModalOpen(false);
    if (isOpen) setIsOpen(false);
  };

  const actions = video.status === "Live" ? liveActions : scheduledActions;
  return (
    <>
      <ActionDropdown actions={actions}>
        <DotsVerticalIcon />
      </ActionDropdown>
      <Modal
        isOpen={isOpen}
        setIsOpen={setIsOpen}
        title="Delete Live Video Url"
        description="Are you sure you want to delete this live video url?"
      >
        <div className="bg-[#FAFAFA] p-4 flex gap-4 items-center justify-center rounded-b-lg">
          <DialogClose asChild>
            <Button className="max-w-[126px] self-end" variant={"outline"}>
              Cancel
            </Button>
          </DialogClose>
          <Button
            className="max-w-[126px] self-end bg-red-600"
            onClick={handleDeleteVideo}
          >
            Proceed
          </Button>
        </div>
      </Modal>
      <Modal
        isOpen={isStopLiveModalOpen}
        setIsOpen={setIsStopLiveModalOpen}
        title="Stop Live Video"
        description="Are you sure you want to stop this live video?"
      >
        <div className="bg-[#FAFAFA] p-4 flex gap-4 items-center justify-center rounded-b-lg">
          <DialogClose asChild>
            <Button className="max-w-[126px] self-end" variant={"outline"}>
              Cancel
            </Button>
          </DialogClose>
          <Button
            className="max-w-[126px] self-end"
            onClick={handleStopLiveVideo}
          >
            Proceed
          </Button>
        </div>
      </Modal>
      <Modal isOpen={isEditModalOpen} setIsOpen={setIsEditModalOpen}>
        <div className="bg-white p-4 flex gap-4 items-center justify-center rounded-b-lg">
          <LiveVideoUrlForm
            isEditing
            video={videoToEdit!}
            closeModal={() => setIsEditModalOpen(false)}
          />
        </div>
      </Modal>
    </>
  );
};
