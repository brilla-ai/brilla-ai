import axios from "axios";

export const getContributors = async () => {
  const { data } = await axios.get(
    "https://api.github.com/repos/brilla-ai/brilla-ai/contributors"
  );

  return data;
};
