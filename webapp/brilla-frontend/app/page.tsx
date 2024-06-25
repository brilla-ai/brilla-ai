import AnswerBox from "@/components/answer-box";
// import QuizFooter from "@/components/footer";
import Navbar from "@/components/navbar";
import QuizFooter from "@/components/quiz-footer";
import VideoPlayer from "@/components/videoplayer";

export default function Home() {
  const youtubeUrl =
    "https://www.youtube.com/watch?v=lKMm0FDxj9s&pp=ygUJbnNtcSAyMDIz";
  return (
    <main className="flex flex-col ">
     <Navbar gradientBg = {true} />
     <div className="flex flex-col md:flex-row justify-evenly md:items-start items-center md:align-top mt-6 md:mt-8 md:mx-16 md:gap-8 ">
     <div className="md:mt-[24px] flex-1 ">
        <VideoPlayer url={youtubeUrl} />
      </div>
      <div className="min-h-[580px]">
      <AnswerBox chatHistory={["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae aliquam quam. Nulla facilisi. Integer ac dapibus libero, eu efficitur purus. Nam consectetur venenatis libero, in rutrum ex. Vestibulum nec est tortor"
      ,"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae aliquam quam. Nulla facilisi. Integer ac dapibus libero, eu efficitur purus. Nam consectetur venenatis libero, in rutrum ex. Vestibulum nec est tortor"
    ,"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vitae aliquam quam. Nulla facilisi. Integer ac dapibus libero, eu efficitur purus. Nam consectetur venenatis libero, in rutrum ex. Vestibulum nec est tortor"] } />
      </div>
      </div>
      <QuizFooter/>
    </main>
  );
}
