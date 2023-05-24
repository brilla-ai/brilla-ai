import Link from "next/link";

type VideoCardProps = {
  id: number;
  image: string;
};

const VideoCard = ({ id, image }: VideoCardProps) => {
  return (
    <div
      className="max-w-sm bg-transparent  text-black"
      data-testid="video-card"
    >
      <img className="w-full" src={image} alt={`Video number ${id}`} />
      <div className="flex justify-center my-5">
        <Link
          href={`/demos/${id}`}
          className="inline-flex items-center px-5 py-2 text-md font-medium text-center text-white bg-blue-600 rounded-lg hover:bg-blue-800"
        >
          Try this out
        </Link>
      </div>
    </div>
  );
};

export default VideoCard;
