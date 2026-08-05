function AttentionWidget() {
  const attention = 92;

  return (
    <div className="bg-white rounded-xl shadow-md p-6">

      <h2 className="text-2xl font-bold mb-6">
        AI Attention Monitor
      </h2>

      <div className="flex justify-center">

        <div className="relative w-44 h-44">

          <svg className="w-44 h-44 rotate-[-90deg]">

            <circle
              cx="88"
              cy="88"
              r="70"
              stroke="#E5E7EB"
              strokeWidth="12"
              fill="none"
            />

            <circle
              cx="88"
              cy="88"
              r="70"
              stroke="#2563EB"
              strokeWidth="12"
              fill="none"
              strokeDasharray={440}
              strokeDashoffset={440 - (440 * attention) / 100}
              strokeLinecap="round"
            />

          </svg>

          <div className="absolute inset-0 flex flex-col justify-center items-center">

            <h1 className="text-4xl font-bold">
              {attention}%
            </h1>

            <p className="text-gray-500">
              Focus
            </p>

          </div>

        </div>

      </div>

      <p className="text-center text-gray-600 mt-6">
        Excellent concentration detected during learning.
      </p>

    </div>
  );
}

export default AttentionWidget;