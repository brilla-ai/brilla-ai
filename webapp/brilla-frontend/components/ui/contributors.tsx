"use client";
import { useState, useEffect } from "react";
import { getContributors } from "@/apis/contributors";
import { Avatar, AvatarImage } from "./avatar";
  const Contributors =  () => {
  // const data = await getContributors();
  const [contributors, setContributors] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchContributors = async () => {
      try {
        const data = await getContributors();
        setContributors(data?.slice(0,6));
      } catch (err: any) {
        setError(err.message);
      }
    };

    fetchContributors();
  }, []);

  if (error) {
    return  <a
    href="https://github.com/brilla-ai/brilla-ai/graphs/contributors"
    className="bg-white w-11 h-11 rounded-full text-black text-2xl  items-center  mt-2 grid place-items-center relative z-10 mx-auto"
    data-testid="contributors-link"
  >+ </a>;
  }

  return (

    <div className="mt-4">
      <div className="flex">
        {contributors?.map((contributor: any, index: number) => (
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
