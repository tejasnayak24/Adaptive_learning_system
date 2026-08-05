import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import StudentLayout from "../layouts/StudentLayout";

function Quiz() {
  const navigate = useNavigate();
  const { id } = useParams();

  const quizQuestions = [
    {
      question: "Which keyword is used to define a function in Python?",
      options: ["function", "def", "func", "define"],
      answer: "def",
    },
    {
      question: "Which loop executes at least once?",
      options: ["for", "while", "do-while", "foreach"],
      answer: "do-while",
    },
    {
      question: "Which data type stores True or False?",
      options: ["int", "bool", "float", "string"],
      answer: "bool",
    },
    {
      question: "Which symbol is used for comments in Python?",
      options: ["//", "#", "<!--", "/*"],
      answer: "#",
    },
    {
      question: "Which function displays output?",
      options: ["input()", "print()", "display()", "show()"],
      answer: "print()",
    },
  ];

  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState("");
  const [score, setScore] = useState(0);

  const question = quizQuestions[currentQuestion];

  const handleNext = () => {
    if (!selectedAnswer) {
      alert("Please select an answer.");
      return;
    }

    let updatedScore = score;

    if (selectedAnswer === question.answer) {
      updatedScore += 1;
      setScore(updatedScore);
    }

    if (currentQuestion + 1 < quizQuestions.length) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer("");
    } else {
      navigate("/quiz-result", {
        state: {
          score: updatedScore,
          total: quizQuestions.length,
          lessonId: id,
        },
      });
    }
  };

  return (
    <StudentLayout>

      <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-md p-8">

        <h1 className="text-3xl font-bold mb-2">
          Quiz
        </h1>

        <p className="text-gray-500 mb-6">
          Question {currentQuestion + 1} of {quizQuestions.length}
        </p>

        <div className="w-full bg-gray-200 rounded-full h-3 mb-8">

          <div
            className="bg-blue-600 h-3 rounded-full"
            style={{
              width: `${((currentQuestion + 1) / quizQuestions.length) * 100}%`,
            }}
          ></div>

        </div>

        <h2 className="text-2xl font-semibold mb-8">
          {question.question}
        </h2>

        <div className="space-y-4">

          {question.options.map((option, index) => (

            <button
              key={index}
              onClick={() => setSelectedAnswer(option)}
              className={`w-full text-left p-4 rounded-lg border transition ${
                selectedAnswer === option
                  ? "bg-blue-600 text-white border-blue-600"
                  : "hover:bg-gray-100"
              }`}
            >
              {option}
            </button>

          ))}

        </div>

        <div className="flex justify-end mt-8">

          <button
            onClick={handleNext}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
          >
            {currentQuestion === quizQuestions.length - 1
              ? "Submit Quiz"
              : "Next Question"}
          </button>

        </div>

      </div>

    </StudentLayout>
  );
}

export default Quiz;
