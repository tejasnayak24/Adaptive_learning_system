import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import StudentLayout from "../layouts/StudentLayout";
import quizService from "../services/quizService";
import attentionService from "../services/attentionService";
import recommendationService from "../services/recommendationService";
import lessonService from "../services/lessonService";
import progressService from "../services/progressService";
import { useAuth } from "../context/AuthContext";

function Quiz() {
  const navigate = useNavigate();
  const { id } = useParams(); // may be quiz_id or lesson_id depending on routing
  const { user } = useAuth();

  const [quiz, setQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    const load = async () => {
      try {
        // Try startQuiz (returns questions with answers) first
        let resp = null;
        try {
          resp = await quizService.startQuiz(Number(id));
        } catch (e) {
          // fallback to getQuiz
          resp = await quizService.getQuiz(Number(id));
        }

        const data = resp?.data ?? resp;
        const q = data?.quiz ?? data?.quiz;
        const qs = data?.questions ?? data?.questions ?? [];

        if (!q || !qs) throw new Error("Quiz not found or invalid response");

        if (mounted) {
          setQuiz(q);
          setQuestions(qs);
        }
      } catch (err) {
        if (mounted) setError(err.message || "Failed to load quiz");
      } finally {
        if (mounted) setLoading(false);
      }
    };
    load();
    return () => (mounted = false);
  }, [id]);

  const totalQuestions = questions.length;

  const handleSelect = (qId, choice) => {
    setAnswers((s) => ({ ...s, [qId]: choice }));
  };

  const handleNext = () => {
    if (!answers[questions[currentQuestion].id]) {
      alert("Please select an answer.");
      return;
    }
    if (currentQuestion + 1 < totalQuestions) {
      setCurrentQuestion((c) => c + 1);
    } else {
      submitQuiz();
    }
  };

  const submitQuiz = async () => {
    if (!user) {
      setError("User not authenticated");
      return;
    }

    setSubmitting(true);
    try {
      // Compute score: compare answers to question.correct_answer (if provided)
      let correct = 0;
      for (const q of questions) {
        const userChoice = answers[q.id];
        // backend correct_answer may be 'A'|'B' etc or text
        const correctAnswer = q.correct_answer ?? q.answer ?? null;
        if (!correctAnswer) continue;
        // normalize: if correctAnswer is letter, map user's selected option index to letter
        if (typeof correctAnswer === "string" && /^[A-D]$/i.test(correctAnswer)) {
          const opts = [q.option_a, q.option_b, q.option_c, q.option_d];
          const idx = opts.indexOf(userChoice);
          const letter = idx >= 0 ? String.fromCharCode(65 + idx) : userChoice;
          if (letter.toUpperCase() === correctAnswer.toUpperCase()) correct += 1;
        } else {
          if (userChoice === correctAnswer) correct += 1;
        }
      }

      const quiz_score = totalQuestions > 0 ? Math.round((correct / totalQuestions) * 100) : 0;

      // response_time: not tracked per-question here; use 0 for now or compute if needed
      const response_time = 0;

      // get attention
      let attention = 0.0;
      try {
        const attResp = await attentionService.getLatestAttention(user.id);
        let val = attResp?.attention_score ?? attResp?.score ?? attResp?.value ?? attResp;
        if (typeof val === "number") {
          if (val > 1.0) val = val / 100.0; // convert percentage to 0-1
          attention = Number(val);
        }
      } catch (e) {
        // ignore, use 0
      }

      const payload = {
        student_id: user.id,
        lesson_id: quiz.lesson_id,
        quiz_score,
        response_time,
        attention_score: attention,
        difficulty: quiz.difficulty,
      };

      const submitResp = await quizService.submitQuiz(payload);

      // get previous quiz score if available
      let previous_quiz_score = 0;
      try {
        const prev = await progressService.getLessonProgress(user.id, quiz.lesson_id);
        previous_quiz_score = prev?.data?.quiz_score ?? prev?.quiz_score ?? 0;
      } catch (e) {
        previous_quiz_score = 0;
      }

      // load lesson info to fill subject/topic/lesson
      let lesson = null;
      try {
        const lessonResp = await lessonService.getLessonById(quiz.lesson_id);
        lesson = lessonResp?.data ?? lessonResp;
      } catch (e) {
        lesson = { title: "", topic: "", id: quiz.lesson_id };
      }

      // count completed lessons
      let completed_lessons = 0;
      try {
        const allProgress = await progressService.getStudentProgress(user.id);
        const items = allProgress?.data ?? allProgress;
        if (Array.isArray(items)) completed_lessons = items.filter((p) => p.completed).length;
      } catch (e) {
        completed_lessons = 0;
      }

      const rlRequest = {
        subject: lesson.topic || lesson.title || "",
        topic: lesson.topic || "",
        lesson: lesson.title || "",
        previous_quiz_score: previous_quiz_score ?? 0,
        current_quiz_score: quiz_score,
        attention_score: attention,
        yawning: false,
        looking_away: false,
        difficulty: quiz.difficulty || "EASY",
        response_time,
        hints_used: 0,
        lesson_attempts: 0,
        completed_lessons: completed_lessons,
      };

      let rec = null;
      try {
        const recResp = await recommendationService.getRecommendation(rlRequest);
        rec = recResp?.data ?? recResp;
      } catch (e) {
        // ignore
      }

      navigate("/quiz-result", {
        state: {
          score: quiz_score,
          total: totalQuestions,
          lessonId: quiz.lesson_id,
          recommendation: rec,
        },
      });
    } catch (err) {
      setError(err.message || "Failed to submit quiz");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <StudentLayout>
        <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-md p-8 text-center">Loading quiz...</div>
      </StudentLayout>
    );
  }

  if (error) {
    return (
      <StudentLayout>
        <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-md p-8 text-center text-red-600">{error}</div>
      </StudentLayout>
    );
  }

  const question = questions[currentQuestion];
  const options = [question?.option_a, question?.option_b, question?.option_c, question?.option_d].filter(Boolean);

  return (
    <StudentLayout>
      <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-md p-8">
        <h1 className="text-3xl font-bold mb-2">Quiz</h1>
        <p className="text-gray-500 mb-6">Question {currentQuestion + 1} of {totalQuestions}</p>

        <div className="w-full bg-gray-200 rounded-full h-3 mb-8">
          <div className="bg-blue-600 h-3 rounded-full" style={{ width: `${((currentQuestion + 1) / Math.max(totalQuestions, 1)) * 100}%` }}></div>
        </div>

        <h2 className="text-2xl font-semibold mb-8">{question?.question}</h2>

        <div className="space-y-4">
          {options.map((option, index) => (
            <button key={index} onClick={() => handleSelect(question.id, option)} className={`w-full text-left p-4 rounded-lg border transition ${answers[question.id] === option ? "bg-blue-600 text-white border-blue-600" : "hover:bg-gray-100"}`}>
              {option}
            </button>
          ))}
        </div>

        <div className="flex justify-end mt-8">
          <button onClick={handleNext} disabled={submitting} className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">{currentQuestion === totalQuestions - 1 ? (submitting ? "Submitting..." : "Submit Quiz") : "Next Question"}</button>
        </div>
      </div>
    </StudentLayout>
  );
}

export default Quiz;
