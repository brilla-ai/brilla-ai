"use client";
import { DotsVerticalIcon } from "@radix-ui/react-icons";
import { ActionDropdown } from "./ui/action-dropdown-menu";
import { Modal } from "./ui/modal";
import React from "react";
import { DialogClose } from "./ui/dialog";
import { Button } from "./ui/button";
import LiveVideoUrlForm from "./live-video-url-form";
import { useVideosStore, Video } from "@/stores";

const LiveVideoLinks = () => {
  const { videoLinks } = useVideosStore();

  const links = React.useMemo(() => videoLinks, [videoLinks]);

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
          {links.map((video) => {
            return (
              <div key={video.id} className="grid lg:grid-cols-2">
                <p>{video.tags}</p>
                <div className="flex justify-between">
                  <p>{video.status}</p>
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

  const { setLiveVideo, removeVideo } = useVideosStore();

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

  const handleStopLiveVideo = () => {
    setLiveVideo("");
    removeVideo(video.id);
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
            onClick={handleStopLiveVideo}
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
          <LiveVideoUrlForm isEditing video={videoToEdit!} />
        </div>
      </Modal>
    </>
  );
};
