import { getContributors } from "@/apis/contributors";
import { Avatar, AvatarImage } from "./avatar";
const Contributors = async () => {
  const data = await getContributors();

  const contributors: Record<string, any>[] = data?.slice(0, 6);
  return (
    <div className="mt-4">
      <div className="flex">
        {contributors?.map((contributor, index: number) => (
          <Avatar
            className="z-10 -ml-3"
            title={contributor.login}
            key={contributor.login}
          >
            <AvatarImage src={contributor.avatar_url} alt="contributor" />
          </Avatar>
        ))}
        {contributors && (
          <a
            href="https://github.com/brilla-ai/brilla-ai/graphs/contributors"
            className="bg-white w-11 h-11 rounded-full text-black text-2xl grid place-items-center relative z-10 -ml-3"
            data-testid="contributors-link"
          >
            +
          </a>
        )}
      </div>
    </div>
  );
};

export default Contributors;
